import json

from aws_cdk import (
    core as cdk,
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_kms as kms,
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

        json_template = {
            'username': 'admin'
        }

        db_creds = sm.Secret(
            self,
            'DbSecret',
            secret_name=f'{env_name}-rds-secret',
            generate_secret_string=sm.SecretStringGenerator(
                include_space=False,
                password_length=12,
                generate_string_key='rds-password',
                exclude_punctuation=True,
                secret_string_template=json.dumps(json_template)
            )
        )

        db_mysql = rds.DatabaseCluster(
            self,
            'MySql',
            default_database_name=f'{prj_name}-{env_name}',
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
            parameter_group=rds.CfnDBClusterParameterGroup.from_parameter_group_name(
                self,
                'PgDev',
                parameter_group_name='default.aurora-mysql5.7'
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY,
            credentials=rds.Credentials.from_secret(secret=db_creds),
            storage_encrypted=True,
            storage_encryption_key=kmskey
        )

        db_mysql.connections.allow_default_port_from(
            lambdasg, "Access from Lambda Functions")
        db_mysql.connections.allow_default_port_from(
            bastionsg, "Access from Bastion Host")
