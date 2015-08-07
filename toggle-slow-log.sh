#!/bin/bash

profile="box"
parameter_group="boxview-production"
parameter_group="boxview-development"

#profile="core"
#parameter_group="crocodoc-56"
#parameter_group="crocodoc-m2-2xlarge-mysql56 "

#aws --profile $profile rds modify-db-parameter-group \
#    --db-parameter-group-name $parameter_group --parameters \
#    "ParameterName=max_connections,ParameterValue=1500,ApplyMethod=immediate " \

#aws --profile $profile rds reset-db-parameter-group \
#    --db-parameter-group-name $parameter_group --parameters \
#    "ParameterName=max_connections,ApplyMethod=immediate"

if true
then
    echo "not doing anything"
    exit
fi

if true
then

    aws --profile $profile rds reset-db-parameter-group \
        --db-parameter-group-name $parameter_group --parameters \
        "ParameterName=general_log,ApplyMethod=immediate " \
        "ParameterName=slow_query_log,ApplyMethod=immediate " \
        "ParameterName=log_output,ApplyMethod=immediate " \
        "ParameterName=log_queries_not_using_indexes,ApplyMethod=immediate " \
        "ParameterName=long_query_time,ApplyMethod=immediate "
else
    aws --profile $profile rds modify-db-parameter-group \
        --db-parameter-group-name $parameter_group --parameters \
        "ParameterName=slow_query_log,ParameterValue=1,ApplyMethod=immediate " \
        "ParameterName=log_output,ParameterValue=FILE,ApplyMethod=immediate " \
        "ParameterName=log_queries_not_using_indexes,ParameterValue=1,ApplyMethod=immediate " \
        "ParameterName=long_query_time,ParameterValue=0,ApplyMethod=immediate "
fi
