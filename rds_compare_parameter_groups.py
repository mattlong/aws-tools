import sys
from boto.rds2 import connect_to_region

import settings

if len(sys.argv) < 4:
    print 'usage: python %s <account> <group name 1> <group name 2>' % sys.argv[0]
    sys.exit(2)

account = sys.argv[1].lower()
first_group_name = sys.argv[2]
second_group_name = sys.argv[3]

account_info = settings.ACCOUNT_INFO[account]
region_name = account_info.get('region', 'us-east-1')

conn = connect_to_region(region_name, **account_info)

def get_group_params(group_name):
    params = {}
    marker = None
    while True:
        group = conn.describe_db_parameters(group_name, marker=marker)['DescribeDBParametersResponse']['DescribeDBParametersResult']
        marker, parameters = group['Marker'], group['Parameters']
        for p in parameters:
            params[p['ParameterName']] = p

        if not marker:
            break
    return params

first_params = get_group_params(first_group_name)
second_params = get_group_params(second_group_name)

def to_string(p):
    return '%s = %s' % (p['ParameterName'], p['ParameterValue'])

for key in set(first_params.keys()) - set(second_params.keys()):
    print '- %s' % to_string(first_params[key])

for key in set(second_params.keys()) - set(first_params.keys()):
    print '+ %s' % to_string(second_params[key])

for key in first_params.keys():
    if not key in second_params:
        continue

    if first_params[key]['ParameterValue'] != second_params[key]['ParameterValue']:
        print '- %s' % to_string(first_params[key])
        print '+ %s' % to_string(second_params[key])
    else:
        pass
        #print key, first_params[key]['ParameterValue'], second_params[key]['ParameterValue']
