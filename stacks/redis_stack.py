from aws_cdk import (
    core as cdk,
    aws_elasticache as redis,
    aws_ec2 as ec2,
    aws_ssm as ssm
)


class RedisStack(cdk.Stack):

    def __init__(self,
                 scope: cdk.Construct,
                 construct_id: str,
                 vpc: ec2.Vpc,
                 redissg: ec2.SecurityGroup,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prj_name = self.node.try_get_context("project_name")
        env_name = self.node.try_get_context("env")

        subnets = [subnet.subnet_id for subnet in vpc.private_subnets]

        subnet_group = redis.CfnSubnetGroup(
            self,
            'RedisSubnetGroup',
            subnet_ids=subnets,
            description="Subnet group for Redis"
        )

        redis_cluster = redis.CfnCacheCluster(
            self,
            'RedisCacheCluster',
            cache_node_type='cache.t2.small',
            engine='redis',
            num_cache_nodes=1,
            cluster_name=f'{prj_name}-redis-{env_name}',
            cache_subnet_group_name=subnet_group.ref,
            vpc_security_group_ids=[redissg.security_group_id],
            auto_minor_version_upgrade=True
        )
        redis_cluster.add_depends_on(subnet_group)
