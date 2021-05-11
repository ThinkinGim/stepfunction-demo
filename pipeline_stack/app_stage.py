from aws_cdk import core

from app_stack.my_service_stack import MyServiceStack

class AppStage(core.Stage):
    def __init__(self, scope: core.Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        MyServiceStack(self, 'MyServiceStack')