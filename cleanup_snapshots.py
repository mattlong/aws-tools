import sys, re

import boto
from boto.ec2.connection import EC2Connection

try:
    import settings
except ImportError:
    pass

if len(sys.argv) == 1:
    print 'usage: python cleanup_snapshot.py <cluster> [<for_real>]'
    exit(0)

cluster = sys.argv[1].lower()
FOR_REAL = (sys.argv[2] if len(sys.argv) > 2 else 'false').lower() == 'true'

keys = settings.ACCOUNT_KEYS[account]
conn = EC2Connection(keys[0], keys[1])

amis = {}
for ami in conn.get_all_images(owners='self'):
    amis[ami.id] = ami
print '''AMIs
  count: %d
''' % (len(amis),)

skip_count, delete_count, save_count = 0, 0, 0
snaps = conn.get_all_snapshots(owner='self')
desc_regex = re.compile(r'Created by CreateImage\((i-\w{8})\) for (ami-\w{8}) from (vol-\w{8})')
for snap in snaps:
    m = desc_regex.match(snap.description)
    if not m:
        skip_count += 1
        continue

    img_id, ami_id, vol_id = m.groups()
    if ami_id not in amis:
        delete_count += 1
        conn.delete_snapshot(snap.id) if FOR_REAL else None
    else:
        save_count += 1
print '''snapshots
  skipped: %d
  deleted: %d
    saved: %d
''' % (skip_count, delete_count, save_count,)
