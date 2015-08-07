#!/usr/bin/env python
import sys
import subprocess

if len(sys.argv) < 3:
    print 'usage: python %s <account> <parameter group>' % sys.argv[0]
    sys.exit(2)

profile = sys.argv[1]

parameter_group=sys.argv[2]

default_apply = 'immediate'

params = [
    ('character_set_server', 'utf8'),
    ('character_set_database', 'utf8'),
    ('query_cache_type', '0', 'pending-reboot'),
    ('innodb_flush_log_at_trx_commit', '2'),
    ('innodb_io_capacity', '800'),
    ('innodb_use_native_aio', '1', 'pending-reboot'),
    ('innodb_purge_threads', '1', 'pending-reboot'),
    ('collation_server', 'utf8_general_ci'),
    ('innodb_file_format', 'Barracuda'),
    ('skip_name_resolve', '1', 'pending-reboot'),
]

cmds = ['aws', '--profile', profile, 'rds', 'modify-db-parameter-group',
        '--db-parameter-group-name', parameter_group, '--parameters']

template = 'ParameterName=%s,ParameterValue=%s,ApplyMethod=%s'
for param in params:
    if len(param) == 2:
        param += (default_apply,)
    cmds.append(template % param)

print ' '.join(cmds)

p = subprocess.Popen(cmds, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = p.communicate()

print stderr
print stdout
