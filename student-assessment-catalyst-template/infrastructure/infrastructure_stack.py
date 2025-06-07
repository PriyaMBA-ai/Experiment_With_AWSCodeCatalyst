from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigw,
    aws_dynamodb as ddb,
    aws_iam as iam,
)
from constructs import Construct

class InfrastructureStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        table = ddb.Table(
            self, "StudentScores",
            partition_key={"name": "student_id", "type": ddb.AttributeType.STRING},
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST
        )

        fn = lambda_.Function(
            self, "BackendFunction",
            runtime=lambda_.Runtime.PYTHON_3_11,
            handler="lambda_function.lambda_handler",
            code=lambda_.Code.from_asset("../backend"),
            environment={"TABLE_NAME": table.table_name}
        )

        table.grant_read_write_data(fn)

        fn.add_to_role_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeModel"],
            resources=["*"]
        ))

        apigw.LambdaRestApi(self, "StudentAPI", handler=fn)