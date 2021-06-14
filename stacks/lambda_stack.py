from aws_cdk import (
    core as cdk,
    aws_lambda as _lambda,
    aws_apigateway as apigw
)


class LambdaStack(cdk.Stack):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_fn = _lambda.Function(
            self,
            'HelloWorldFunction',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('lambda_fn'),
            handler='hello.handler'
        )

        apigw.LambdaRestApi(
            self,
            'HelloWorld',
            handler=lambda_fn,
            rest_api_name='mylambdaapi'
        )
