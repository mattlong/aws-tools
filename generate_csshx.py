import sys

import boto
from boto.ec2.connection import EC2Connection

try:
    import settings
except ImportError:
    pass

if len(sys.argv) == 1:
    print 'usage: python generate_csshx.py <account> [<tier>]'
    exit(0)

account = sys.argv[1].lower()
tier = sys.argv[2] if len(sys.argv) > 2 else 'production'
grouping_tag = 'role'

filters = {
    'instance-state-name': 'running',
}

keys = settings.ACCOUNT_KEYS[account]
conn = EC2Connection(keys[0], keys[1])

if account.lower() == 'fat':
    filters.update({
        'image-id': 'ami-7f985216',
    })
else:
    filters.update({
        'tag:tier':tier,
        #'tag:Name':NAME,
        #'tag:role':ROLE,
    })

print filters

instances = [i for r in conn.get_all_instances(filters=filters) for i in r.instances]

group_counts = { '': 0 }
for i in instances:
    group = i.tags.get(grouping_tag, '<Empty>')
    group_counts[group] = group_counts.get(group, 0) + 1
    group_counts[''] += 1

def make_csshX(instances):
    cmd = 'csshX --login ubuntu '
    cmd += str.join(' ', [instance.public_dns_name for instance in instances])
    print cmd

for (group, count) in group_counts.items():
    print group, count
    make_csshX(filter(lambda i: i.tags.get(grouping_tag, '<Empty>') == group, instances))
    print
