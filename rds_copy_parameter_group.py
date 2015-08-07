import sys
from boto.rds2 import connect_to_region
from boto.rds2.exceptions import DBParameterGroupNotFound

import settings

if len(sys.argv) < 4:
    print 'usage: python %s <account> <old group name> <new group name> [<new family> [<new description>]]' % sys.argv[0]
    sys.exit(2)

account = sys.argv[1].lower()
old_group_name = sys.argv[2]
new_group_name = sys.argv[3]
new_family = sys.argv[4] if len(sys.argv) >= 5 else None
description = sys.argv[5] if len(sys.argv) >= 6 else None

account_info = settings.ACCOUNT_INFO[account]
region_name = account_info.get('region', 'us-east-1')

conn = connect_to_region(region_name)

old_group = conn.describe_db_parameter_groups(old_group_name)['DescribeDBParameterGroupsResponse']['DescribeDBParameterGroupsResult']['DBParameterGroups'][0]
new_family = new_family or old_group['DBParameterGroupFamily']
description = description or old_group['Description']

try:
    conn.delete_db_parameter_group(new_group_name)
except DBParameterGroupNotFound:
    pass
new_group = conn.create_db_parameter_group(new_group_name, new_family, description)

params_to_update = []
marker = None
while True:
    group = conn.describe_db_parameters(old_group_name, marker=marker)['DescribeDBParametersResponse']['DescribeDBParametersResult']
    marker, parameters = group['Marker'], group['Parameters']
    for p in parameters:
        if p['Source'] == 'user':
            if False and p['DataType'] == 'boolean':
                p['ParameterValue'] = 'true' if p['ParameterValue'] == '1' else 'false'


            params_to_update.append((p['ParameterName'],p['ParameterValue'],'pending-reboot'))

    if not marker:
        break

def chunks(l, size):
    for i in range(0, len(l), size):
        yield l[i:i+size]

for chunk in chunks(params_to_update, 20):
    for p in chunk:
        print '%s = %s' % (p[0], p[1])
    conn.modify_db_parameter_group(new_group_name, chunk)
