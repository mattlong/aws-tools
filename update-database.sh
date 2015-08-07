#!/bin/bash

hosts=(ec2-54-87-188-6.compute-1.amazonaws.com ec2-54-80-39-106.compute-1.amazonaws.com ec2-54-87-75-93.compute-1.amazonaws.com ec2-54-196-32-50.compute-1.amazonaws.com ec2-54-90-122-165.compute-1.amazonaws.com ec2-54-82-158-65.compute-1.amazonaws.com ec2-54-82-104-250.compute-1.amazonaws.com ec2-54-167-174-101.compute-1.amazonaws.com ec2-75-101-232-69.compute-1.amazonaws.com ec2-54-89-80-88.compute-1.amazonaws.com ec2-54-167-93-126.compute-1.amazonaws.com ec2-54-82-29-242.compute-1.amazonaws.com ec2-54-80-91-196.compute-1.amazonaws.com ec2-54-90-152-94.compute-1.amazonaws.com ec2-54-87-51-1.compute-1.amazonaws.com ec2-107-20-181-44.compute-1.amazonaws.com)

#old_host="v2-production.crhvoivh0856.us-east-1.rds.amazonaws.com"
#new_host="v2-production-56.crhvoivh0856.us-east-1.rds.amazonaws.com"

old_host="v2-production-56.crhvoivh0856.us-east-1.rds.amazonaws.com"
new_host="v2-production-mysql56.crhvoivh0856.us-east-1.rds.amazonaws.com"

command="sudo sed -e \"s/$old_host/$new_host/g\" -i".bak" /etc/default/crocodoc"

for host in ${hosts[@]}
do
    echo $host
    ssh ubuntu@$host "$command"
done
