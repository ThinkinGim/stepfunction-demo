from aws_cdk import (
    core,
    aws_ec2,
    aws_iam as iam,
    aws_lambda as lambda_,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
)

class network(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.vpc = aws_ec2.Vpc(self, "demo-stepfunctions",
            cidr="10.100.0.0/16",
            max_azs=2,
            nat_gateways=0,
            subnet_configuration=[
                aws_ec2.SubnetConfiguration(
                    name='demo-stepfunctions',
                    subnet_type=aws_ec2.SubnetType.ISOLATED,
                    cidr_mask=24
                )
            ]
        )
        lambda_role = iam.Role(self, 'demo-lambda-role',
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )

        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaENIManagementAccess')
        )
        lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')
        )

        fn_submit = lambda_.Function(self, 'demo-sfn-submit',
            function_name='demo-sfn-submit',
            handler='handler.do',
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.asset('./craftaws/func_submit'),
            role=lambda_role,
            timeout=core.Duration.seconds(900),
            allow_public_subnet=False,
            vpc=self.vpc,
            vpc_subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.ISOLATED),
            environment={}
        )

        fn_job_1 = lambda_.Function(self, 'demo-sfn-job1',
            function_name='demo-sfn-job1',
            handler='handler.do',
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.asset('./craftaws/func_job_1'),
            role=lambda_role,
            timeout=core.Duration.seconds(900),
            allow_public_subnet=False,
            vpc=self.vpc,
            vpc_subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.ISOLATED),
            environment={}
        )

        fn_job_2 = lambda_.Function(self, 'demo-sfn-job2',
            function_name='demo-sfn-job2',
            handler='handler.do',
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.asset('./craftaws/func_job_2'),
            role=lambda_role,
            timeout=core.Duration.seconds(900),
            allow_public_subnet=False,
            vpc=self.vpc,
            vpc_subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.ISOLATED),
            environment={}
        )

        submit_job = tasks.LambdaInvoke(self, "Submit Job",
            lambda_function=fn_submit,
            # Lambda's result is in the attribute `Payload`
            output_path="$.Payload"
        )

        step_1_job = tasks.LambdaInvoke(self, "Job_1",
            lambda_function=fn_job_1,
            # Lambda's result is in the attribute `Payload`
            output_path="$.Payload"
        )

        wait_x = sfn.Wait(self, "Wait X Seconds",
            time=sfn.WaitTime.duration(core.Duration.seconds(60))
        )

        step_2_job = tasks.LambdaInvoke(self, "Job_2",
            lambda_function=fn_job_1,
            # Lambda's result is in the attribute `Payload`
            output_path="$.Payload"
        )

        
        job_succeed = sfn.Succeed(self, "Job Succeed",
            comment="AWS Batch Job Succeed"
        )

        definition = submit_job.next(step_1_job).next(wait_x).next(step_2_job).next(job_succeed)

        sfn.StateMachine(self, "StateMachine",
            definition=definition,
            timeout=core.Duration.minutes(5)
        )


