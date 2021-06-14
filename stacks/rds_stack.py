import json

from aws_cdk import (
    core as cdk,
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_ssm as ssm,
    aws_secretsmanager as sm,
)


class RDSStack(cdk.Stack):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 vpc: ec2.Vpc,
                 lambdasg: ec2.SecurityGroup,
                 bastionsg: ec2.SecurityGroup,
                 kmskey: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        default_database_name = \
            f'{prj_name.capitalize()}{env_name.capitalize()}'

        print(f"DEFAULT DB NAME {default_database_name}")

        db_mysql = rds.DatabaseCluster(
            self,
            'MySql',
            default_database_name=default_database_name,
            engine=rds.DatabaseClusterEngine.aurora_mysql(
                version=rds.AuroraMysqlEngineVersion.VER_5_7_12
            ),
            instance_props=rds.InstanceProps(
                vpc=vpc,
                vpc_subnets=ec2.SubnetSelection(
                    subnet_type=ec2.SubnetType.ISOLATED),
                instance_type=ec2.InstanceType(
                    instance_type_identifier="t3.small")
            ),
            instances=1,
            parameter_group=rds.ParameterGroup.from_parameter_group_name(  # noqa
                self,
                'PgDev',
                parameter_group_name='default.aurora-mysql5.7'
            ),
            credentials=rds.Credentials.from_generated_secret(
                username='admin'
            ),
            storage_encrypted=True,
            storage_encryption_key=kmskey,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        db_mysql.connections.allow_default_port_from(
            lambdasg, "Access from Lambda Functions")
        db_mysql.connections.allow_default_port_from(
            bastionsg, "Access from Bastion Host")

        ssm.StringParameter(
            self,
            'DbHost',
            parameter_name=f'/{env_name}/db-host',
            string_value=db_mysql.cluster_endpoint.hostname
        )
