from aws_cdk import (
    core,
)

class MyServiceStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        core.CfnOutput(self, 'MyService', value='completed bootstrapping')



