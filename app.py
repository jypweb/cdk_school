#!/usr/bin/env python3

# import os

from aws_cdk import core as cdk
from stacks.vpc_stack import VPCStack
from stacks.security_stack import SecurityStack
from stacks.bastion_stack import BastionStack
from stacks.kms_stack import KmsStack
from stacks.s3_stack import S3Stack
from stacks.rds_stack import RDSStack

app = cdk.App()
vpc_stack = VPCStack(app, "vpc")
security_stack = SecurityStack(app, "security", vpc=vpc_stack.vpc)
bastion_stack = BastionStack(app, "bastion",
                             vpc=vpc_stack.vpc, sg=security_stack.bastion_sg)
kms_stack = KmsStack(app, 'kms')
s3_stack = S3Stack(app, 's3-buckets')
rds_stack = RDSStack(app, 'rds',
                     vpc=vpc_stack.vpc,
                     lambdasg=security_stack.lambda_sg,
                     bastionsg=security_stack.bastion_sg,
                     kmskey=kms_stack.kms_rds,
                     )

app.synth()
