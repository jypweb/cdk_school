from aws_cdk import (
    core as cdk,
    aws_ec2 as ec2,
    aws_ssm as ssm,
)


class VPCStack(cdk.Stack):

    def __init__(self,
                 scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        if not env_name:
            env_name = 'dev'

        self.vpc = ec2.Vpc(
            self,
            'devVPC',
            cidr='172.32.0.0/16',
            max_azs=2,
            enable_dns_hostnames=True,
            enable_dns_support=True,
            subnet_configuration=[
                # Allow public access to/from internet
                ec2.SubnetConfiguration(
                    name='Public',
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                ),
                # Private Subnet
                ec2.SubnetConfiguration(
                    name='Private',
                    subnet_type=ec2.SubnetType.PRIVATE,
                    cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name='Isolated',
                    subnet_type=ec2.SubnetType.ISOLATED,
                    cidr_mask=24
                ),
            ],
            nat_gateways=1
        )

        priv_subnets = [subnet.subnet_id
                        for subnet in self.vpc.private_subnets]

        count = 1
        for ps in priv_subnets:
            ssm.StringParameter(
                self,
                f'PrivateSubnet{count}',
                string_value=ps,
                parameter_name=f'/{env_name}/private-subnet-{count}'
            )
            count += 1
