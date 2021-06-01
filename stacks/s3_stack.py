from aws_cdk import (
    core as cdk,
    aws_s3 as s3,
    aws_ssm as ssm
)


class S3Stack(cdk.Stack):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        env_name = self.node.try_get_context('env')
        account = self.account

        if not env_name:
            env_name = 'dev'

        lambda_bucket = s3.Bucket(
            self,
            'LambdaBucket',
            access_control=s3.BucketAccessControl.BUCKET_OWNER_FULL_CONTROL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            bucket_name=f'{account}-{env_name}-lambda-deploy-packages',
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=True,
                ignore_public_acls=True,
                restrict_public_buckets=True
            ),
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        ssm.StringParameter(
            self,
            'LambdaBucketSsm',
            parameter_name=f'/{env_name}/lambda-s3-bucket',
            string_value=lambda_bucket.bucket_name
        )
