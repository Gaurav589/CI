# Below script creates 3 Node (1 master,2 Core)EMR cluster on AWS.

import boto3
import sys
import yaml
boto3.setup_default_session(profile_name="crosaccount")
emr_client = boto3.client('emr')
Configuration_List=[]
InstanceFleet_List=[]
# Configuration List
emr_configfile = file('EMR_Apps_config.yml', 'r')
#Configuration file for EMR
cluster_configfile = file('Instance_types_config.yml', 'r')


Configuration_List=yaml.load(emr_configfile)[0]
InstanceFleet_List=yaml.load(cluster_configfile )

response = emr_client.run_job_flow(
    Name='DATA-PLATFORM-STREAMING-Vishal',
    ReleaseLabel='emr-5.11.1',
    # The release label for the Amazon EMR release.
    Instances={
        #[REQUIRED] A specification of the number and type of Amazon EC2 instances.
        #'MasterInstanceType': 't2.large',
         #The EC2 instance type of the master node.
        #'SlaveInstanceType': 't2.medium',
        #The EC2 instance type of the slave nodes.
        #'InstanceCount': 3,
        #
        'InstanceFleets': InstanceFleet_List,
        #Describes the EC2 instances and instance configurations for clusters that use the instance fleet configuration
        'Ec2KeyName': 'emrvishal',
        #The name of the EC2 key pair that can be used to ssh to the master node as the user called "hadoop."
        'KeepJobFlowAliveWhenNoSteps': True,
        #Specifies whether the cluster should remain available after completing all steps.
        #'EmrManagedMasterSecurityGroup': 'sg-Vishal_EMR_Master',
        #'EmrManagedSlaveSecurityGroup': 'sg-Vishal_EMR_Slave',
        #'ServiceAccessSecurityGroup': 'Vishal_EMR_Service',
    },
    Applications=[
       {
            'Name': 'Hive',
            #'Version': 'string',
        },
        {
            'Name': 'Spark'
        }
    ],
    Configurations=Configuration_List
    ,
    VisibleToAllUsers=True,
    JobFlowRole='EMR_EC2_DefaultRole',
    # Also called instance profile and EC2 role. An IAM role for an EMR cluster.
    # The EC2 instances of the cluster assume this role.
    ServiceRole='EMR_DefaultRole',
    # The IAM role that will be assumed by the Amazon EMR service to access AWS resources on your behalf.
    Tags=[
        {
            'Key': 'app_name',
            'Value': 'DATA-PLATFORM-STREAMING'
        },
        {
            'Key': 'env',
            'Value': 'DATA-PLATFORM-STREAMING'
        },
        {
            'Key': 'group_name',
            'Value': 'DATA-PLATFORM-STREAMING'
        },
        {
            'Key': 'product',
            'Value': 'DATA-PLATFORM-STREAMING'
        },
        {
            'Key': 'purpose',
            'Value': 'POC'
        },
        {
            'Key': 'service',
            'Value': 'EMR'
        },
        {
            'Key': 'ttl',
            'Value': '-1'
        },
        {
            'Key': 'user',
            'Value': 'vishal.dhavale'
        },
    ],


)

#print Configuration_List[0]
#print InstanceFleet_List
print response['JobFlowId']

from time import sleep
sleep(60)

cluster_status = emr_client.describe_cluster(
    ClusterId=response['JobFlowId']
)

print cluster_status['Cluster']['Status']

