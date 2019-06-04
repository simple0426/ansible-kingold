#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import yaml
import os, sys, json

front_list = [ 'cloud', 'cloud-h5', 'ifa', 'kingold-web', 'mgt_user', 'mgt_cop_user',
               'kop', 'web-kingold', 'wechat', 'fop', 'haproxy', '59nginx', '60nginx']
f = open('site-prod.yml', 'r')
std = yaml.load(f.read())
f.close()
service = {}
for item in std:
    hosts_str = item['hosts']
    roles_dic = item['roles']
    hosts_list = hosts_str.split(',')
    for role in roles_dic:
        if role['tags'][0] not in front_list:
            service[role['tags'][0]] = hosts_list

def status(host, service):
    os.system('ansible -i environments/prod/hosts %s -m shell -b -a "supervisorctl status %s"' %
              (host, service))

def usage_info():
    role_list = []
    for role in service.keys():
        role_list.append(role)
    print('Usage: [python3] %s service' % sys.argv[0])
    print('Available service:', json.dumps(role_list, indent=4))

help_list = ['?', 'help', 'h', '-h', '--help']
if len(sys.argv) != 2:
    usage_info()
elif sys.argv[1] in help_list:
    usage_info()
else:
    service_list = sys.argv[1].split(',')
    while '' in service_list:
        service_list.remove('')
    for srv in service_list:
        if srv in service.keys():
            for host in service[srv]:
                status(host, srv)
