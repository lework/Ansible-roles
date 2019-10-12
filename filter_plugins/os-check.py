#
# author: lework
# date: 2019-10-11

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.module_utils.six import iteritems
import json
import datetime


def get_check_data(data):
    """
    Get the json data of check_result from hostvars and analyze it.
    :param data: hostvars
    :return: dict
    """
    item = {
        'time': '',
        'summary': {
            'ok': 0,
            'bad': 0,
            'critical': 0,
            'total': 0,
            'error': 0
        },
        'ok_item': {},
        'bad_item': {},
        'critical_item': {},
        'error_item': {}
    }

    for host, value in iteritems(data):
        result = value.get('check_result')
        if result:
            if 'msg' in result:
                item['error_item'][host] = {'msg': result['msg']}
                continue
            stdout = result.get('stdout')
            try:
                info = json.loads(stdout)
            except Exception as e:
                item['error_item'][host] = {'msg': stdout}
                continue

            if len(info['critical']) > 0:
                item['critical_item'][host] = info
            elif len(info['bad']) > 0:
                item['bad_item'][host] = info
            else:
                item['ok_item'][host] = info

    # import pydevd_pycharm
    # pydevd_pycharm.settrace('192.168.77.1', port=8888, stdoutToServer=True, stderrToServer=True)

    # summary
    item['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    item['summary']['ok'] = len(item['ok_item'])
    item['summary']['bad'] = len(item['bad_item'])
    item['summary']['critical'] = len(item['critical_item'])
    item['summary']['error'] = len(item['error_item'])
    item['summary']['total'] = len(data)

    # sorted
    item['ok_item'] = sorted(iteritems(item['ok_item']))
    item['bad_item'] = sorted(iteritems(item['bad_item']))
    item['critical_item'] = sorted(iteritems(item['critical_item']))
    item['error_item'] = sorted(iteritems(item['error_item']))

    return item


class FilterModule(object):
    """Filters for working with output from hostvars check_result"""

    def filters(self):
        return {
            'get_check_data': get_check_data
        }
