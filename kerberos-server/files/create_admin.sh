#!/bin/bash
echo -e "$1\n$1" | kadmin.local  -q "addprinc $2/admin"

