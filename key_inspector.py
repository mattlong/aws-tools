import sys

import boto
from boto.ec2.connection import EC2Connection
from boto.s3.connection import S3Connection
from boto.s3.key import Key

try:
    import settings
except ImportError:
    pass

if len(sys.argv) == 1:
    print 'usage: %s <account> <bucket> <key>' % (sys.argv[0],)
    exit(0)

account = sys.argv[1].lower()
bucket_name = sys.argv[2]
key_name = sys.argv[3]

keys = settings.ACCOUNT_KEYS[account]
conn = S3Connection(keys[0], keys[1])

bucket = conn.get_bucket(bucket_name)

key = bucket.get_key(key_name)

print dir(key)
print
print key.get_acl()
#print key.get_xml_acl()
print key.content_type
print key.content_encoding
print key.content_disposition
print key.encrypted
print key.owner
print key.last_modified
print key.size
print key.etag
