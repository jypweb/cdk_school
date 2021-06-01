from aws_cdk import (
    core as cdk,
    aws_ssm as ssm,
    aws_kms as kms
)


class KmsStack(cdk.Stack):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        self.kms_rds = kms.Key(
            self,
            'RdsKey',
            description=f'{prj_name}-key-rds',
            enable_key_rotation=True
        )

        self.kms_rds.add_alias(
            alias_name=f'alias/{prj_name}-key-rds'
        )

        ssm.StringParameter(
            self,
            'RdsKeyParam',
            string_value=self.kms_rds.key_id,
            parameter_name=f'/{env_name}/rds-kms-key'
        )
