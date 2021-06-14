from aws_cdk import (
    core as cdk,
    aws_apigateway as apigw,
    aws_ssm as ssm
)


class ApiGatewayStack(cdk.Stack):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prj_name = self.node.try_get_context('project_name')
        env_name = self.node.try_get_context('env')

        api_gateway = apigw.RestApi(
            self,
            'RestApi',
            endpoint_types=[apigw.EndpointType.REGIONAL],
            rest_api_name=f'{prj_name}-service'
        )
        api_gateway.root.add_method('ANY')

        # SSM Params
        ssm.StringParameter(
            self,
            'ApiGateway',
            parameter_name=f'/{env_name}/api-gateway-url',
            string_value=f'https://{api_gateway.rest_api_id}.execute-api.{self.region}.amazonaws.com'  # noqa
        )
        ssm.StringParameter(
            self,
            'ApiGatewayId',
            parameter_name=f'/{env_name}/api-gateway-id',
            string_value=api_gateway.rest_api_id
        )
