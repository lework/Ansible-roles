#!/usr/bin/python
# -*- coding: utf-8 -*-

# @Time    : 2019-11-25
# @Author  : lework
# @Desc    : 针对supervisor的应用进行健康检查


import os
import sys
import time
import json
import yaml
import base64
import socket
import signal
import smtplib
import datetime
import platform
import threading
import subprocess
from email.header import Header
from email.mime.text import MIMEText
from collections import namedtuple
from supervisor.xmlrpc import SupervisorTransport

PY3 = sys.version_info[0] == 3

if PY3:
    import http.client as httplib
    from xmlrpc.client import Transport, ServerProxy, Fault


    def iterkeys(d, **kw):
        return iter(d.keys(**kw))


    def iteritems(d, **kw):
        return iter(d.items(**kw))
else:
    import httplib
    from xmlrpclib import Transport, ServerProxy, Fault


    def iterkeys(d, **kw):
        return d.iterkeys(**kw)


    def iteritems(d, **kw):
        return d.iteritems(**kw)


def shell(cmd):
    """
    执行系统命令
    :param cmd:
    :return: (exitcode, stdout, stderr)
    """
    # with os.popen(cmd) as f:
    #     return f.read()
    env_to_pass = dict(os.environ)
    proc = subprocess.Popen(cmd,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            env=env_to_pass)
    proc.wait()
    return (proc.returncode,) + proc.communicate()


def get_proc_cpu(pid):
    """
    获取进程CPU使用率
    :param pid:
    :return:
    """
    pscommand = 'ps -opcpu= -p %s'

    _, data, _ = shell(pscommand % pid)
    if not data:
        # 未获取到数据值，或者没有此pid信息
        return None
    try:
        cpu_utilization = data.strip()
        cpu_utilization = float(cpu_utilization)
    except ValueError:
        # 获取的结果不包含数据，或者无法识别cpu_utilization
        return None
    return cpu_utilization


def get_proc_rss(pid, cumulative=False):
    """
    获取进程内存使用
    :param pid:
    :param cumulative:
    :return:
    """
    pscommand = 'ps -orss= -p %s'
    pstreecommand = 'ps ax -o "pid= ppid= rss="'
    ProcInfo = namedtuple('ProcInfo', ['pid', 'ppid', 'rss'])

    def find_children(parent_pid, procs):
        # 找出进程的子进程信息
        children = []
        for proc in procs:
            pid, ppid, rss = proc
            if ppid == parent_pid:
                children.append(proc)
                children.extend(find_children(pid, procs))
        return children

    if cumulative:
        # 统计进程的子进程rss
        _, data, _ = shell(pstreecommand)
        data = data.strip()

        procs = []
        for line in data.splitlines():
            p_pid, p_ppid, p_rss = map(int, line.split())
            procs.append(ProcInfo(pid=p_pid, ppid=p_ppid, rss=p_rss))

        # 计算rss
        try:
            parent_proc = [p for p in procs if p.pid == pid][0]
            children = find_children(pid, procs)
            tree = [parent_proc] + children
            rss = sum(map(int, [p.rss for p in tree]))
        except (ValueError, IndexError):
            # 计算错误时，返回None
            return None

    else:
        _, data, _ = shell(pscommand % pid)
        if not data:
            # 未获取到数据值，或者没有此pid信息
            return None
        try:
            rss = data.strip()
            rss = int(rss)
        except ValueError:
            # 获取的结果不包含数据，或者无法识别rss
            return None

    rss = rss / 1024  # rss 的单位是 KB， 这里返回MB单位
    return rss


class HealthCheck(object):
    def __init__(self, config):
        """
        初始化配置
        :param config:
        """

        self.mail_config = None
        self.wechat_config = None
        self.supervisord_url = 'unix:///var/run/supervisor.sock'

        if 'config' in config:
            self.mail_config = config['config'].get('mail')
            self.wechat_config = config['config'].get('wechat')
            self.supervisord_url = config['config'].get('supervisordUrl', self.supervisord_url)
            self.supervisord_user = config['config'].get('supervisordUser', None)
            self.supervisord_pass = config['config'].get('supervisordPass', None)
            config.pop('config')

        self.program_config = config

        self.periodSeconds = 5
        self.failureThreshold = 3
        self.successThreshold = 1
        self.initialDelaySeconds = 1
        self.sendResolved = False

        self.max_rss = 1024
        self.cumulative = False
        self.max_cpu = 90

    def get_supervisord_conn(self):
        """
        获取supervisor的连接
        :return:
        """
        transport = SupervisorTransport(self.supervisord_user, self.supervisord_pass, self.supervisord_url)
        s = ServerProxy('http://127.0.0.1', transport=transport)

        return s

    def get_pid(self, program, kind, pid_file):
        """
        获取进程pid
        :param program:
        :param kind:
        :param pid_file:
        :return:
        """
        pid = 0
        err = ''

        if kind == 'supervisor':
            try:
                s = self.get_supervisord_conn()
                info = s.supervisor.getProcessInfo(program)
                pid = info.get('pid')
                err = info.get('description')
            except Exception as e:
                self.log(program, "PID: Can't get pid from supervisor %s ", e)
        elif kind == 'name':
            pscommand = "ps -A -o pid,cmd |grep '[%s]%s' | awk '{print $1}' | head -1"
            exitcode, stdout, stderr = shell(pscommand % (program[0], program[1:]))
            if exitcode == 0:
                pid = stdout.strip()
            else:
                self.log(program, "PID: Can't get pid from name %s ", stderr)
                pid = 0
                err = stderr

        elif kind == 'file':
            if pid_file:
                try:
                    with open(pid_file) as f:
                        pid = f.read().strip()
                except Exception as e:
                    self.log(program, "PID: Can't get pid from file %s ", e)
                    err = "Can't get pid from file"
            else:
                err = "PID: pid file not set"
                self.log(program, err)
        if not pid:
            pid = 0

        return pid, err

    def log(self, program, msg, *args):
        """
        写信息到 STDERR.
        :param program:
        :param msg:
        :param args:
        :return:
        """

        curr_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        sys.stderr.write(
            '%s [%s] %s\n' % (curr_dt, program, msg % args,))

        sys.stderr.flush()

    def check(self, config):
        """
        检查主函数
        :param config:
        :return:
        """
        check_state = {}
        program = config.get('program')
        periodSeconds = config.get('periodSeconds', self.periodSeconds)
        failureThreshold = config.get('failureThreshold', self.failureThreshold)
        successThreshold = config.get('successThreshold', self.successThreshold)
        initialDelaySeconds = config.get('initialDelaySeconds', self.initialDelaySeconds)
        sendResolved = config.get('sendResolved', self.sendResolved)
        action_type = config.get('action', 'restart')

        check_type = config.get('type', 'HTTP').lower()
        check_method = self.http_check

        if check_type == 'tcp':
            check_method = self.tcp_check
        elif check_type == 'mem':
            check_method = self.mem_check
        elif check_type == 'cpu':
            check_method = self.cpu_check

        while 1:
            if program not in check_state:
                check_state[program] = {
                    'periodSeconds': 1,
                    'failure': 0,
                    'success': 0,
                    'action': False
                }
                self.log(program, 'CONFIG: %s', config)
                time.sleep(initialDelaySeconds)

            # self.log(program, '%s check state: %s', check_type, json.dumps(check_state[program]))
            if check_state[program]['periodSeconds'] % periodSeconds == 0:
                check_result = check_method(config)
                check_status = check_result.get('status', None)
                check_info = check_result.get('info', '')
                self.log(program, '%s check: info(%s) state(%s)', check_type.upper(), check_info, check_status)

                if check_status == 'failure':
                    check_state[program]['failure'] += 1
                elif check_status == 'success':
                    check_state[program]['success'] += 1

                # 先判断成功次数
                if check_state[program]['success'] >= successThreshold:
                    # 只有开启恢复通知和检测失败并且执行操作后,才可以发送恢复通知
                    if sendResolved and check_state[program]['action']:
                        # 只保留通知action
                        notice_action = ['email', 'wechat']
                        send_action = ','.join(list(set(action_type.split(',')) & set(notice_action)))
                        self.log(program, 'Use %s send resolved.', send_action)
                        action_param = {
                            'check_status': check_status,
                            'action_type': send_action,
                            'msg': check_result.get('msg', '')
                        }
                        self.action(program, **action_param)

                    # 成功后,将项目状态初始化
                    check_state[program]['failure'] = 0
                    check_state[program]['success'] = 0
                    check_state[program]['action'] = False

                # 再判断失败次数
                if check_state[program]['failure'] >= failureThreshold:
                    # 失败后, 只触发一次action, 或者检测错误数可以整除2倍periodSeconds与initialDelaySeconds时触发(避免重启失败导致服务一直不可用)
                    if not check_state[program]['action'] or (
                            check_state[program]['failure'] != 0 and check_state[program]['failure'] % (
                            (periodSeconds + initialDelaySeconds) * 2) == 0):
                        action_param = {
						    'config': config,
                            'action_type': action_type,
                            'check_status': check_status,
                            'msg': check_result.get('msg', '')
                        }
                        self.action(program, **action_param)
                        check_state[program]['action'] = True

                # 间隔时间清0
                check_state[program]['periodSeconds'] = 0

            time.sleep(1)
            check_state[program]['periodSeconds'] += 1

    def http_check(self, config):
        """
        用于检查http连接
        :param config:
        :return: dict
        """
        program = config.get('program')
        config_host = config.get('host', 'localhost')
        config_path = config.get('path', '/')
        config_port = config.get('port', '80')

        config_method = config.get('method', 'GET')
        config_timeoutSeconds = config.get('timeoutSeconds', 3)
        config_body = config.get('body', '')
        config_json = config.get('json', '')
        config_hearders = config.get('hearders', '')

        config_username = config.get('username', '')
        config_password = config.get('password', '')

        HEADERS = {'User-Agent': 'leops http_check'}

        headers = HEADERS.copy()
        if config_hearders:
            try:
                headers.update(json.loads(config_hearders))
            except Exception as e:
                self.log(program, 'HTTP: config_headers not loads: %s , %s', config_hearders, e)
            if config_json:
                headers['Content-Type'] = 'application/json'

        if config_username and config_password:
            auth_str = '%s:%s' % (config_username, config_password)
            headers['Authorization'] = 'Basic %s' % base64.b64encode(auth_str.encode()).decode()

        if config_json:
            try:
                config_body = json.dumps(config_json)
            except Exception as e:
                self.log(program, 'HTTP: config_json not loads: %s , %s', json, e)

        check_info = '%s %s %s %s %s %s' % (config_host, config_port, config_path, config_method,
                                            config_body, headers)

        try:
            httpClient = httplib.HTTPConnection(config_host, config_port, timeout=config_timeoutSeconds)
            httpClient.request(config_method, config_path, config_body, headers=headers)
            res = httpClient.getresponse()
        except Exception as e:
            self.log(program, 'HTTP: conn error, %s', e)
            return {'status': 'failure', 'msg': '[http_check] %s' % e, 'info': check_info}
        finally:
            if httpClient:
                httpClient.close()

        if res.status != httplib.OK:
            return {'status': 'failure', 'msg': '[http_check] return code %s' % res.status, 'info': check_info}

        return {'status': 'success', 'msg': '[http_check] return code %s' % res.status, 'info': check_info}

    def tcp_check(self, config):
        """
        用于检查TCP连接
        :param config:
        :return: dict
        """
        program = config.get('program')
        host = config.get('host', 'localhost')
        port = config.get('port', 80)
        timeoutSeconds = config.get('timeoutSeconds', 3)
        check_info = '%s %s' % (host, port)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeoutSeconds)
            sock.connect((host, port))
            sock.close()
        except Exception as e:
            self.log(program, 'TCP: conn error, %s', e)
            return {'status': 'failure', 'msg': '[tcp_check] %s' % e, 'info': check_info}
        return {'status': 'success', 'msg': '[tcp_check] connection succeeded', 'info': check_info}

    def mem_check(self, config):
        """
        用于检查进程内存
        :param config:
        :return: dict
        """
        program = config.get('program')
        max_rss = config.get('maxRss', self.max_rss)
        cumulative = config.get('cumulative', self.cumulative)
        pid_get = config.get('pidGet', 'supervisor')
        pid_file = config.get('pidFile', )
        check_info = 'max_rss:%sMB cumulative:%s' % (max_rss, cumulative)

        pid, err = self.get_pid(program, pid_get, pid_file)
        if pid == 0:
            self.log(program, 'MEM: check error, program not starting')
            return {'status': 'failure',
                    'msg': '[mem_check] program not starting, message: %s' % err,
                    'info': check_info}
        now_rss = get_proc_rss(pid, cumulative)
        check_info = '%s now_rss:%sMB pid:%s' % (check_info, now_rss, pid)
        if now_rss >= int(max_rss):
            return {'status': 'failure', 'msg': '[mem_check] max_rss(%sMB) now_rss(%sMB)' % (max_rss, now_rss),
                    'info': check_info}

        return {'status': 'success', 'msg': '[mem_check] max_rss(%sMB) now_rss(%sMB)' % (max_rss, now_rss),
                'info': check_info}

    def cpu_check(self, config):
        """
        用于检查进程CPU
        :param config:
        :return: dict
        """
        program = config.get('program')
        max_cpu = config.get('maxCpu', self.max_cpu)
        pid_get = config.get('pidGet', 'supervisor')
        pid_file = config.get('pidFile', )
        check_info = 'max_cpu:{cpu}%'.format(cpu=max_cpu)

        pid, err = self.get_pid(program, pid_get, pid_file)
        if pid == 0:
            self.log(program, 'CPU: check error, program not starting')
            return {'status': 'failure',
                    'msg': '[cpu_check] program not starting, message: %s' % err,
                    'info': check_info}
        now_cpu = get_proc_cpu(pid)
        check_info = '{info} now_cpu:{now}% pid:{pid}'.format(info=check_info, now=now_cpu, pid=pid)
        if now_cpu >= int(max_cpu):
            return {'status': 'failure',
                    'msg': '[cpu_check] max_cpu({max_cpu}%) now_cpu({now}%)'.format(max_cpu=max_cpu, now=now_cpu),
                    'info': check_info}

        return {'status': 'success',
                'msg': '[cpu_check] max_cpu({max_cpu}%) now_cpu({now}%)'.format(max_cpu=max_cpu, now=now_cpu),
                'info': check_info}

    def action(self, program, **args):
        """
        执行动作
        :param program:
        :param args:
        :return: None
        """
        action_type = args.get('action_type')
        msg = args.get('msg')
        check_status = args.get('check_status')
        config = args.get('config')
		
        self.log(program, 'Action: %s', action_type)
        action_list = action_type.split(',')

        if 'restart' in action_list:
            restart_result = self.action_supervisor_restart(program)
            msg += '\r\n Restart：%s' % restart_result
        elif 'exec' in action_list:
            action_exec_cmd = config.get('action_exec_cmd')
            exec_result = self.action_exec(program, action_exec_cmd)
            msg += '\r\n Exec：%s' % exec_result
        elif 'kill' in action_list:
            pid_get = config.get('pidGet', 'supervisor')
            pid_file = config.get('pidFile', )
            pid, err = self.get_pid(program, pid_get, pid_file)
            kill_result = self.action_kill(program, pid)
            msg += '\r\n Kill：%s' % kill_result

        if 'email' in action_list and self.mail_config:
            self.action_email(program, action_type, msg, check_status)
        if 'wechat' in action_list and self.wechat_config:
            self.action_wechat(program, action_type, msg, check_status)

    def action_supervisor_restart(self, program):
        """
        通过supervisor的rpc接口重启进程
        :param program:
        :return:
        """
        self.log(program, 'Action: restart')
        result = 'success'
        try:
            s = self.get_supervisord_conn()
            info = s.supervisor.getProcessInfo(program)
        except Exception as e:
            result = 'Get %s ProcessInfo Error: %s' % (program, e)
            self.log(program, 'Action: restart %s' % result)
            return result

        if info['state'] == 20:
            self.log(program, 'Action: restart stop process')
            try:
                stop_result = s.supervisor.stopProcess(program)
                self.log(program, 'Action: restart stop result %s', stop_result)
            except Fault as e:
                result = 'Failed to stop process %s, exiting: %s' % (program, e)
                self.log(program, 'Action: restart stop error %s', result)
                return result

            time.sleep(1)
            info = s.supervisor.getProcessInfo(program)

        if info['state'] != 20:
            self.log(program, 'Action: restart start process')
            try:
                start_result = s.supervisor.startProcess(program)
            except Fault as e:
                result = 'Failed to start process %s, exiting: %s' % (program, e)
                self.log(program, 'Action: restart start error %s', result)
                return result
            self.log(program, 'Action: restart start result %s', start_result)

        return result

    def action_exec(self, program, cmd):
        """
        执行系统命令
        :param program:
        :param cmd:
        :return:
        """
        self.log(program, 'Action: exec')
        result = 'success'

        exitcode, stdout, stderr = shell(cmd)

        if exitcode == 0:
            self.log(program, "Action: exec result success")
        else:
            result = 'Failed to exec %s, exiting: %s' % (program, exitcode)
            self.log(program, "Action: exec result %s", result)

        return result
		
    def action_kill(self, program, pid):
        """
        杀死进程
        :param program:
        :param pid:
        :return:
        """ 
        self.log(program, 'Action: kill')
        result = 'success'
		
        if int(pid) < 3:
            return 'Failed to kill %s, pid: %s '% (program, pid)
		  
        cmd = "kill -9 %s" % pid
        exitcode, stdout, stderr = shell(cmd)

        if exitcode == 0:
            self.log(program, "Action: kill result success")
        else:
            result = 'Failed to kill %s, pid: %s exiting: %s' % (program, pid, exitcode)
            self.log(program, "Action: kill result %s", result)

        return result

    def action_email(self, program, action_type, msg, check_status):
        """
        发送email
        :param program:
        :param action_type:
        :param msg:
        :param check_status:
        :return:
        """
        self.log(program, 'Action: email')

        ip = ""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception as e:
            self.log(program, 'Action: email get ip error %s' % e)
        finally:
            s.close()

        hostname = platform.node().split('.')[0]
        system_platform = platform.platform()

        if check_status == 'success':
            subject = "[Supervisor] %s Health check successful" % program
        else:
            subject = "[Supervisor] %s Health check failed" % program
        curr_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        content = """
        DateTime: {curr_dt}
        Program: {program}
        IP: {ip}
        Hostname: {hostname}
        Platfrom: {system_platform}
        Action: {action}
        Msg: {msg}
        """.format(curr_dt=curr_dt, program=program, ip=ip, hostname=hostname, system_platform=system_platform,
                   action=action_type, msg=msg)
        mail_port = self.mail_config.get('port', '')
        mail_host = self.mail_config.get('host', '')
        mail_user = self.mail_config.get('user', '')
        mail_pass = self.mail_config.get('pass', '')
        to_list = self.mail_config.get('to_list', [])

        msg = MIMEText(content, _subtype='plain', _charset='utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = mail_user
        msg['to'] = ",".join(to_list)
        try:
            s = smtplib.SMTP_SSL(mail_host, mail_port)
            s.login(mail_user, mail_pass)
            s.sendmail(mail_user, to_list, msg.as_string())
            s.quit()
        except Exception as e:
            self.log(program, 'Action: email send error %s' % e)
            return False

        self.log(program, 'Action: email send success.')
        return True

    def action_wechat(self, program, action_type, msg, check_status):
        """
        微信通知
        :param program:
        :param action_type:
        :param msg:
        :param check_status:
        :return:
        """
        self.log(program, 'Action: wechat')

        host = "qyapi.weixin.qq.com"

        corpid = self.wechat_config.get('corpid')
        secret = self.wechat_config.get('secret')
        agentid = self.wechat_config.get('agentid')
        touser = self.wechat_config.get('touser')
        toparty = self.wechat_config.get('toparty')
        totag = self.wechat_config.get('totag')

        headers = {
            'Content-Type': 'application/json'
        }

        access_token_url = '/cgi-bin/gettoken?corpid={id}&corpsecret={crt}'.format(id=corpid, crt=secret)
        try:
            httpClient = httplib.HTTPSConnection(host, timeout=10)
            httpClient.request("GET", access_token_url, headers=headers)
            response = httpClient.getresponse()
            token = json.loads(response.read())['access_token']
        except Exception as e:
            self.log(program, 'Action: wechat get token error %s' % e)
            return False
        finally:
            if httpClient:
                httpClient.close()

        send_url = '/cgi-bin/message/send?access_token={token}'.format(token=token)

        ip = ""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        except Exception as e:
            self.log(program, 'Action: wechat get ip error %s' % e)
        finally:
            s.close()

        hostname = platform.node().split('.')[0]
        system_platform = platform.platform()

        curr_dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if check_status == 'success':
            title = "<font color=\"info\">[Supervisor] %s Health check successful</font>" % program
        else:
            title = "<font color=\"warning\">[Supervisor] %s Health check failed</font>" % program

        content = "{title}\n \
        > **详情信息**\n \
        > DataTime: {curr_dt}\n \
        > Program: <font color=\"warning\">{program}</font>\n \
        > IP: {ip}\n \
        > Hostname: {hostname}\n \
        > Platfrom: {platfrom}\n \
        > Action: {action}\n \
        > Msg: {msg}".format(title=title, curr_dt=curr_dt, program=program, ip=ip, hostname=hostname,
                             platfrom=system_platform, action=action_type, msg=msg)

        data = {
            "msgtype": 'markdown',
            "agentid": agentid,
            "markdown": {'content': content},
            "safe": 0
        }

        if touser:
            data['touser'] = touser
        if toparty:
            data['toparty'] = toparty
        if toparty:
            data['totag'] = totag

        try:
            httpClient = httplib.HTTPSConnection(host, timeout=10)
            httpClient.request("POST", send_url, json.dumps(data), headers=headers)
            response = httpClient.getresponse()
            result = json.loads(response.read())
            if result['errcode'] != 0:
                self.log(program, 'Action: wechat send faild %s' % result)
                return False
        except Exception as e:
            self.log(program, 'Action: wechat send error %s' % e)
            return False
        finally:
            if httpClient:
                httpClient.close()

        self.log(program, 'Action: wechat send success')
        return True

    def start(self):
        """
        启动检测
        :return:
        """
        self.log('healthCheck:', 'start')
        threads = []

        for key, value in iteritems(self.program_config):
            item = value
            item['program'] = key
            t = threading.Thread(target=self.check, args=(item,))
            threads.append(t)
        for t in threads:
            try:
                t.setDaemon(True)
                t.start()
            except Exception, e:
                print('Exception in ' + t.getName() + ' (catch by main)')
                print(t.exc_traceback)
                t.setDaemon(True)
                t.start()
                
        while 1:
            time.sleep(0.1)


if __name__ == '__main__':

    # 信号处理
    def sig_handler(signum, frame):
        print("Exit check!")
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGQUIT, sig_handler)

    # 获取当前目录下的配置文件,没有的话就生成个模板
    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.yaml')
    if not os.path.exists(config_file):
        example_config = """
config:                                          # 脚本配置名称,请勿更改
#  supervisordUrl: http://localhost:9001/RPC2    # supervisor的接口地址, 默认使用本地socket文件unix:///var/run/supervisor.sock
#  supervisordUser: user                         # supervisor中设置的username, 没有设置可不填
#  supervisordPass: pass                         # supervisor中设置的password, 没有设置可不填
#  mail:                                         # stmp配置
#    host: 'smtp.test.com'
#    port': '465'
#    user': 'ops@test.com'
#    pass': '123456'
#    to_list: ['test@test.com']
#  wechat:                                       # 企业微信通知配置
#    corpid: 
#    secret: 
#    agentid: 
#    touser: 
#    toparty: 
#    totag: 

# 内存方式监控
cat1:                     # supervisor中配置的program名称
  type: mem               # 检查类型: http,tcp,mem,cpu  默认: http
  maxRss: 1024            # 内存阈值, 超过则为检测失败. 单位MB, 默认: 1024
  cumulative: True        # 是否统计子进程的内存, 默认: False
  pidGet: supervisor      # 获取pid的方式: supervisor,name,file, 选择name时,按program名称搜索pid,选择file时,需指定pidFile 默认: supervisor
  pidFile: /var/run/t.pid # 指定pid文件的路径, 只在pidGet为file的时候有用
  periodSeconds: 10       # 检查的频率(以秒为单位), 默认: 5
  initialDelaySeconds: 10 # 首次检查等待的时间(以秒为单位), 默认: 1
  failureThreshold: 3     # 检查成功后，最少连续检查失败多少次才被认定为失败, 默认: 3
  successThreshold: 2     # 失败后检查成功的最小连续成功次数, 默认：1
  action: restart,email   # 触发的动作: restart,exec,email,wechat (restart和exec互斥,同时设置时restart生效) 默认: restart
  execCmd: command        # action exec 的执行命令
  sendResolved: True      # 是否发送恢复通知,仅用作于email,wechat. 默认: False

# cpu方式监控
cat2:                     # supervisor中配置的program名称
  type: cpu               # 检查类型: http,tcp,mem,cpu 默认: http
  maxCpu: 80              # CPU阈值, 超过则为检测失败. 单位% 默认: 90%
  pidGet: supervisor      # 获取pid的方式: supervisor,name,file, 选择name时,按program名称搜索pid,选择file时,需指定pidFile 默认: supervisor
  pidFile: /var/run/t.pid # 指定pid文件的路径, 只在pidGet为file的时候有用
  periodSeconds: 10       # 检查的频率(以秒为单位), 默认: 5
  initialDelaySeconds: 10 # 首次检查等待的时间(以秒为单位), 默认: 1
  failureThreshold: 3     # 检查成功后，最少连续检查失败多少次才被认定为失败, 默认: 3
  successThreshold: 2     # 失败后检查成功的最小连续成功次数, 默认：1
  action: restart,email   # 触发的动作: restart,exec,email,wechat (restart和exec互斥,同时设置时restart生效) 默认: restart
  execCmd: command        # action exec 的执行命令
  sendResolved: True      # 是否发送恢复通知,仅用作于email,wechat. 默认: False

# HTTP方式监控
cat3:
  type: HTTP
  mode: POST              # http动作：POST,GET 默认: GET
  host: 127.0.0.1         # 主机地址, 默认: localhost
  path: /                 # URI地址，默认: /
  port: 8080              # 检测端口，默认: 80
  json: '{"a":"b"}'       # POST的json数据
  hearders: '{"c":1}'     # http的hearder头部数据
  username: test          # 用于http的basic认证
  password: pass          # 用于http的basic认证
  periodSeconds: 10       # 检查的频率(以秒为单位), 默认: 5
  initialDelaySeconds: 10 # 首次检查等待的时间(以秒为单位), 默认: 1
  timeoutSeconds: 5       # 检查超时的秒数, 默认: 3
  failureThreshold: 3     # 检查成功后，最少连续检查失败多少次才被认定为失败, 默认: 3
  successThreshold: 2     # 失败后检查成功的最小连续成功次数, 默认：1
  action: restart,email   # 触发的动作: restart,exec,email,wechat (restart和exec互斥,同时设置时restart生效) 默认: restart
  execCmd: command        # action exec 的执行命令
  sendResolved: True      # 是否发送恢复通知,仅用作于email,wechat. 默认: False

# TCP方式监控
cat4:
  type: TCP
  host: 127.0.0.1         # 主机地址, 默认: localhost
  port: 8082              # 检测端口，默认: 80
  periodSeconds: 10       # 检查的频率(以秒为单位), 默认: 5
  initialDelaySeconds: 10 # 首次检查等待的时间(以秒为单位), 默认: 1
  timeoutSeconds: 5       # 检查超时的秒数, 默认: 3
  failureThreshold: 3     # 检查成功后，最少连续检查失败多少次才被认定为失败, 默认: 3
  successThreshold: 2     # 失败后检查成功的最小连续成功次数, 默认：1
  action: restart,email   # 触发的动作: restart,exec,email,wechat (restart和exec互斥,同时设置时restart生效) 默认: restart
  execCmd: command        # action exec 的执行命令
  sendResolved: True      # 是否发送恢复通知,仅用作于email,wechat. 默认: False
"""
        with open(config_file, 'w') as f:
            f.write(example_config)

        print("\r\n\r\nThe configuration file has been initialized, please modify the file to start.")
        print("Config File: %s\r\n\r\n" % config_file)
        sys.exit(0)

    with open(config_file) as f:
        config = yaml.safe_load(f)

    check = HealthCheck(config)
    check.start()
