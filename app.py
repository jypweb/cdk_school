#!/usr/bin/env python3

# import os

from aws_cdk import core as cdk
from stacks.vpc_stack import VPCStack
from stacks.security_stack import SecurityStack


app = cdk.App()
vpc_stack = VPCStack(app, "vpc")
security_stack = SecurityStack(app, "security", vpc=vpc_stack.vpc)

app.synth()
