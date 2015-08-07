#!/usr/bin/env python
import sys
from boto import ec2

import settings

if len(sys.argv) == 1:
    print 'usage: python generate_csshx.py <account> [<tier>]'
    exit(0)

account = sys.argv[1].lower()
tier = sys.argv[2] if len(sys.argv) > 2 else 'production'
grouping_tag = 'role'

filters = {
    'instance-state-name': 'running',
}

account_info = settings.ACCOUNT_INFO[account]
region_name = account_info.get('region', 'us-east-1')
username = account_info.get('username', 'ubuntu')

region = ec2.get_region(region_name)

conn = ec2.EC2Connection(
        account_info['aws_access_key_id'],
        account_info['aws_secret_access_key'],
        region=region)

if account == 'fat':
    filters.update({
        'image-id': 'ami-7f985216',
    })
elif account == 'box':
    if False:
        grouping_tag = 'Name'
    else:
        filters.update({
            'tag:environment': tier,
        })
else:
    filters.update({
        'tag:tier':tier,
    })

instances = [i for r in conn.get_all_instances(filters=filters) for i in r.instances]

group_counts = { '': 0 }
for i in instances:
    group = i.tags.get(grouping_tag, '<Empty>')
    group_counts[group] = group_counts.get(group, 0) + 1
    group_counts[''] += 1

def make_csshX(instances):
    cmd = 'csshX --login %s ' % (username,)
    cmd += ' '.join([instance.public_dns_name for instance in instances])
    print cmd
    print '\n'.join(['%s - %s' % (i.private_ip_address,i.public_dns_name)  for i in instances])

for (group, count) in group_counts.items():
    print group, count
    make_csshX(filter(lambda i: i.tags.get(grouping_tag, '<Empty>') == group, instances))
    print
