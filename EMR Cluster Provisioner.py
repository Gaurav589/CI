# Below script creates 3 Node (1 master,2 Core)EMR cluster with Spark and Hive.

import boto3
import sys
boto3.setup_default_session(profile_name="crosaccount")
emr_client = boto3.client('emr')

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
        'InstanceFleets': [
        #Describes the EC2 instances and instance configurations for clusters that use the instance fleet configuration
            {
                'Name': 'Master',
                 #The friendly name of the instance fleet.
                'InstanceFleetType': 'MASTER',
                 #The node type that the instance fleet hosts. Valid values are MASTER,CORE,and TASK.
                'TargetOnDemandCapacity': 1,
                'TargetSpotCapacity': 0,
                'InstanceTypeConfigs': [
                        #An instance type configuration for each instance type in an instance fleet,
                         # which determines the EC2 instances Amazon EMR attempts to provision to fulfill On-Demand and Spot target capacities.
                        # There can be a maximum of 5 instance type configurations in a fleet.
                    {
                        'InstanceType': 'm1.large',
                        #[REQUIRED] An EC2 instance type, such as m3.xlarge .
                        'WeightedCapacity': 1,
                        #The number of units that a provisioned instance of this type provides toward fulfilling
                        # the target capacities defined in InstanceFleetConfig .
                        # This value is 1 for a master instance fleet, and must be 1 or greater for core and task instance fleets.
                        # Defaults to 1 if not specified.
                        #'BidPrice': 'string',
                        #'BidPriceAsPercentageOfOnDemandPrice': 123.0,
                        'EbsConfiguration': {
                            #The configuration of Amazon Elastic Block Storage (EBS) attached to each instance as defined by InstanceType .
                            'EbsBlockDeviceConfigs': [
                            #An array of Amazon EBS volume specifications attached to a cluster instance.

                                {
                                    'VolumeSpecification': {
                                        #[Required] EBS volume specifications such as
                                        #volume type, IOPS, and size (GiB) that will be requested for the EBS volume attached to an EC2 instance in the cluster.
                                        'VolumeType': 'gp2',
                                        #[Required] The volume type. Volume types supported are gp2, io1, standard.
                                        #'Iops': 123,
                                        #The number of I/O operations per second (IOPS) that the volume supports.
                                        'SizeInGB': 50
                                        #[Required] The volume size, in gibibytes (GiB). This can be a number from 1 - 1024.
                                        # If the volume type is EBS-optimized, the minimum value is 10.
                                    },
                                    'VolumesPerInstance': 1
                                    #Number of EBS volumes with a specific volume configuration that will be associated with every instance in the instance group
                                },
                            ],
                            'EbsOptimized': False
                            #Indicates whether an Amazon EBS volume is EBS-optimized.
                        },
                        #'Configurations': [
                        #    {
                        #        'Classification': 'string',
                        #        'Configurations': {'... recursive ...'},
                        #        'Properties': {
                        #            'string': 'string'
                        #        }
                        #    },
                        #]
                    },
                ]
            },
            {
                'Name': 'Core',
                 #The friendly name of the instance fleet.
                'InstanceFleetType': 'CORE',
                 #The node type that the instance fleet hosts. Valid values are MASTER,CORE,and TASK.
                'TargetOnDemandCapacity': 2,
                'TargetSpotCapacity': 0,
                'InstanceTypeConfigs': [
                        #An instance type configuration for each instance type in an instance fleet,
                         # which determines the EC2 instances Amazon EMR attempts to provision to fulfill On-Demand and Spot target capacities.
                        # There can be a maximum of 5 instance type configurations in a fleet.
                    {
                        'InstanceType': 'm1.medium',
                        #[REQUIRED] An EC2 instance type, such as m3.xlarge .
                        'WeightedCapacity': 1,
                        #The number of units that a provisioned instance of this type provides toward fulfilling
                        # the target capacities defined in InstanceFleetConfig .
                        # This value is 1 for a master instance fleet, and must be 1 or greater for core and task instance fleets.
                        # Defaults to 1 if not specified.
                        #'BidPrice': 'string',
                        #'BidPriceAsPercentageOfOnDemandPrice': 123.0,
                        'EbsConfiguration': {
                            #The configuration of Amazon Elastic Block Storage (EBS) attached to each instance as defined by InstanceType .
                            'EbsBlockDeviceConfigs': [
                            #An array of Amazon EBS volume specifications attached to a cluster instance.

                                {
                                    'VolumeSpecification': {
                                        #[Required] EBS volume specifications such as
                                        #volume type, IOPS, and size (GiB) that will be requested for the EBS volume attached to an EC2 instance in the cluster.
                                        'VolumeType': 'gp2',
                                        #[Required] The volume type. Volume types supported are gp2, io1, standard.
                                        #'Iops': 123,
                                        #The number of I/O operations per second (IOPS) that the volume supports.
                                        'SizeInGB': 50
                                        #[Required] The volume size, in gibibytes (GiB). This can be a number from 1 - 1024.
                                        # If the volume type is EBS-optimized, the minimum value is 10.
                                    },
                                    'VolumesPerInstance': 1
                                    #Number of EBS volumes with a specific volume configuration that will be associated with every instance in the instance group
                                },
                            ],
                            'EbsOptimized': False
                            #Indicates whether an Amazon EBS volume is EBS-optimized.
                        },
                        #'Configurations': [
                        #An optional configuration specification to be used when provisioning cluster instances, which can include configurations for applications and software bundled with Amazon EMR. A configuration consists of a classification, properties,
                        #and optional nested configurations. A classification refers to an application-specific configuration file. Properties are the settings you want to change in that file. For more informatio
                        #    {
                        #        'Classification': 'string',
                        #        'Configurations': {'... recursive ...'},
                        #        'Properties': {
                        #            'string': 'string'
                        #        }
                        #    },
                        #]

                    },
                ],
                #'LaunchSpecifications': {
                #    'SpotSpecification': {
                #        'TimeoutDurationMinutes': 123,
                #        'TimeoutAction': 'SWITCH_TO_ON_DEMAND'|'TERMINATE_CLUSTER',
                #        'BlockDurationMinutes': 123
                #    }
                #}
            },
        ],
        'Ec2KeyName': 'emrvishal',
        #The name of the EC2 key pair that can be used to ssh to the master node as the user called "hadoop."
        'KeepJobFlowAliveWhenNoSteps': True,
        #Specifies whether the cluster should remain available after completing all steps.
        #'EmrManagedMasterSecurityGroup': 'sg-Vishal_EMR_Master',
        #'EmrManagedSlaveSecurityGroup': 'sg-Vishal_EMR_Slave',
        #'ServiceAccessSecurityGroup': 'Vishal_EMR_Service',
    },
    Applications=[
    #    Adding Application to EMR cluster
       {
            'Name': 'Hive',
            #'Version': 'string',
        },
        {
            'Name': 'Spark'
        }
    ],
    Configurations=[
    # Sample Configurations for EMR CLuster
        {
            'Classification': 'hdfs-site',
            # 'Configurations': {'... recursive ...'},
            'Properties': {
                'dfs.block.size': '268435456'
            },
            'Properties': {
                'dfs.replication': '2'
            }
        },
        {
            'Classification': 'hive-site',
            'Properties': {
                'hive.execution.engine': 'mr'
            },

        },
        {
            'Classification': 'spark-defaults',
            'Properties': {
                'spark.executor.memory': '2G'
            },
        }

    ],
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

print response['JobFlowId']

from time import sleep
sleep(60)

cluster_status = emr_client.describe_cluster(
    ClusterId=response['JobFlowId']
)

print cluster_status['Cluster']['Status']