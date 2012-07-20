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

conn = boto.connect_ec2()

TIER = 'production'
#TIER = 'staging'
#NAME = 'batch-processor'
ROLE = 'pdfworker'

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
        'tag:tier':TIER,
        #'tag:Name':NAME,
        #'tag:role':ROLE,
    })

print filters

#filters = {
#    'instance-state-name': 'running',
#
#    #v2
#    #'tag:tier':TIER,
#    #'tag:role':'pdfworker',
#    #'image-id': 'ami-baba68d3',
#    #'group-name': 'pdfworker',
#}

instances = [i for r in conn.get_all_instances(filters=filters) for i in r.instances]

name_counts = { '': 0 }
for i in instances:
    name = i.tags.get('Name', '<Empty>')
    name_counts[name] = name_counts.get(name, 0) + 1
    name_counts[''] += 1

def make_csshX(instances):
    cmd = 'csshX --login ubuntu '
    cmd += str.join(' ', [instance.public_dns_name for instance in instances])
    print cmd

for (name, count) in name_counts.items():
    print name, count
    make_csshX(filter(lambda i: i.tags.get('Name', '<Empty>').find(name) != -1, instances))
    print
