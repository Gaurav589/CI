import boto3
import sys
import yaml
from time import sleep

boto3.setup_default_session(profile_name="crosaccount")
emr_client = boto3.client('emr')
tag_list=[]

# Function definition  to create cluster
def create_emr_cluster(tags,clustername='Default-Streaming-CLuster'):

    application_configuration = []
    cluster_infrastructure = []
    # Configuration List
    emr_configfile = file('/EMR Provisioner Script/hadoop_configs.yml', 'r')
    # Configuration file for EMR
    cluster_infra = file('/EMR Provisioner Script/infrastructure.yml', 'r')
    application_configuration = yaml.load(emr_configfile)[0]
    cluster_infrastructure = yaml.load(cluster_infra)
    response = emr_client.run_job_flow(
        Name=clustername,
        LogUri='s3://lookout-dw-dev/EMRlogs/',
        ReleaseLabel='emr-5.12.0',
        # The release label for the Amazon EMR release.
        Instances={
            'InstanceFleets': cluster_infrastructure[2],
            # Describes the EC2 instances and instance configurations for clusters that use the instance fleet configuration
            'Ec2KeyName': 'emrvishal',
            # The name of the EC2 key pair that can be used to ssh to the master node as the user called "hadoop."
            'KeepJobFlowAliveWhenNoSteps': True,
            # Specifies whether the cluster should remain available after completing all steps.
            'Ec2SubnetIds': cluster_infrastructure[1],
            # Applies to clusters that use the instance fleet configuration. When multiple EC2 subnet IDs are specified,
            # Amazon EMR evaluates them and launches instances in the optimal subnet.
            'EmrManagedMasterSecurityGroup': cluster_infrastructure[0][0],
            # the identifier of the Amazon EC2 security group for the master node.
            'EmrManagedSlaveSecurityGroup': cluster_infrastructure[0][1],
            # The identifier of the Amazon EC2 security group for the slave nodes.
        },
        Applications=[
            {
                'Name': 'Hive',
                # 'Version': 'string',
            },
            {
                'Name': 'Spark'
            }
        ],
        Configurations=application_configuration,
        VisibleToAllUsers=True,
        # CustomAmiId='ami-41190938',
        # Custom AMI id (Need to confirme from Sugi)
        JobFlowRole='EMR_EC2_DefaultRole',
        # Also called instance profile and EC2 role. An IAM role for an EMR cluster.
        # The EC2 instances of the cluster assume this role.
        ServiceRole='EMR_DefaultRole',
        # The IAM role that will be assumed by the Amazon EMR service to access AWS resources on your behalf.

        Tags=tags,

    )
    print response['JobFlowId']
    sleep(666)
    cluster_status = emr_client.describe_cluster(
        ClusterId=response['JobFlowId']
    )
    print cluster_status['Cluster']['Status']
    return response['JobFlowId']


# loading yaml file configurations into list
tag_configfile = file('/EMR Provisioner Script/cluster_tagging.yml', 'r')

tag_list=yaml.load(tag_configfile)
# print tag_list,tag_list[0]["Value"]

# Calling function to create cluster.
create_emr_cluster(tag_list,tag_list[0]["Value"])
