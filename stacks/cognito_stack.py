from aws_cdk import (
    aws_cognito as cognito,
    aws_iam as iam,
    aws_ssm as ssm,
    core as cdk
)


class CognitoStack(cdk.Stack):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        user_pool = cognito.UserPool(
            self,
            'UserPool',
            auto_verify=cognito.AutoVerifiedAttrs(email=True),
            sign_in_aliases=cognito.SignInAliases(email=True, phone=True),
            user_pool_name=f'{prj_name}-user-pool',
            custom_attributes={
                'param1': cognito.StringAttribute(mutable=True)
            },
            password_policy=cognito.PasswordPolicy(
                min_length=10,
                require_lowercase=True,
                require_digits=True,
                require_symbols=False,
                require_uppercase=True
            )
        )

        user_pool_client = cognito.UserPoolClient(
            self,
            'PoolClient',
            user_pool=user_pool,
            user_pool_client_name=f'{env_name}-app-client'
        )

        identity_pool = cognito.CfnIdentityPool(
            self,
            'IdentityPool',
            allow_unauthenticated_identities=False,
            cognito_identity_providers=[
                cognito.CfnIdentityPool.CognitoIdentityProviderProperty(
                    client_id=user_pool_client.user_pool_client_id,
                    provider_name=user_pool.user_pool_provider_name
                )
            ],
            identity_pool_name=f'{prj_name}-identity-pool'
        )

        # SSM Params
        ssm.StringParameter(
            self,
            'app-id',
            parameter_name=f'/{env_name}/cognito-app-client-id',
            string_value=user_pool_client.user_pool_client_id
        )

        ssm.StringParameter(
            self,
            'user-pool-id',
            parameter_name=f'/{env_name}/cognito-user-pool-id',
            string_value=user_pool.user_pool_id
        )

        ssm.StringParameter(
            self,
            'identity-pool-id',
            parameter_name=f'/{env_name}/cognito-identity-pool-id',
            string_value=identity_pool.ref
        )
