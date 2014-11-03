import sys
import csv

#See http://aws.amazon.com/s3/faqs/#How_will_I_be_charged_and_billed_for_my_use_of_Amazon_S3
csv_path = 'reports/report.csv'
if len(sys.argv) > 1:
    filter_by_buckets = True
    buckets = sys.argv[1:]
else:
    filter_by_buckets = False
    buckets = None

#TODO: right now we'll only using the first tier prices. will require some modifications to support tiered pricing
DATA_OUT_PER_GB = 0.12
TIER1_REQUESTS_PER_K = 0.005
TIER2_REQUESTS_PER_10K = 0.004
STORAGE_PER_GB_PER_MONTH = 0.030

B_PER_GB = 1073741824L

data_out_bytes = 0
tier1_requests = 0
tier2_requests = 0
storage_byte_hrs = 0

csvfile = open(csv_path, 'rU')
for entry in csv.DictReader(csvfile):
    entry = {k.strip():v.strip() for k,v in entry.iteritems()}

    #filter by bucket
    if filter_by_buckets and entry.get('Resource') not in buckets: continue

    #parse fields
    usage_type = entry.get('UsageType')
    if usage_type.find('-Tier') > -1:
        usage_type, tier = usage_type.split('-')[0:2]
    else:
        tier = None
    operation = entry.get('Operation')
    value = int(float(entry.get('UsageValue')))

    if usage_type in ('DataTransfer-In-Bytes', 'C3DataTransfer-Out-Bytes', 'C3DataTransfer-In-Bytes', 'Requests-NoCharge', 'StorageObjectCount',):
        continue

    elif usage_type == 'DataTransfer-Out-Bytes':
        data_out_bytes += value

    elif usage_type == 'Requests' and tier is not None:
        #print usage_type, tier, operation
        if tier == 'Tier1':
            tier1_requests += value
        elif tier == 'Tier2':
            tier2_requests += value

    elif usage_type == 'TimedStorage-ByteHrs':
        storage_byte_hrs += value

    else:
        print usage_type, tier, operation
        #print entry
        pass

if filter_by_buckets:
    print 'Cost for these buckets: %s' % ', '.join(buckets)
else:
    print 'Cost for all buckets'

#data out
data_out_gb = float(data_out_bytes) / B_PER_GB
data_out_gb -= 1 #first GB free
cost_data_out = data_out_gb * DATA_OUT_PER_GB if data_out_gb > 0 else 0

cost_tier1 = (float(tier1_requests) / 1000) * TIER1_REQUESTS_PER_K
cost_tier2 = (float(tier2_requests) / 10000) * TIER2_REQUESTS_PER_10K

storage_gb_hrs = float(storage_byte_hrs) / B_PER_GB
storage_gb_months = float(storage_byte_hrs) / B_PER_GB / 744
cost_storage = storage_gb_months * STORAGE_PER_GB_PER_MONTH

cost_total = cost_data_out + cost_tier1 + cost_tier2 + cost_storage

print '''
  $%.2f data out
  $%.2f tier1 requests
  $%.2f tier2 requests
  $%.2f storage

  $%.2f total
''' % (cost_data_out, cost_tier1, cost_tier2, cost_storage, cost_total,)
