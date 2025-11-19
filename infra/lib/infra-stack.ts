import * as cdk from "aws-cdk-lib/core";
import { Construct } from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export class InfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const FirstLambdaFunction = new lambda.Function(
      this,
      "FirstLambdaFunction",
      {
        runtime: lambda.Runtime.PYTHON_3_13,
        handler: "index.handler",
        code: lambda.Code.fromInline("def handler(event, context):\n    return 'Hello, World!'"),
      }
    );

    const FirstLambdaFunctionUrl = FirstLambdaFunction.addFunctionUrl({
      authType: lambda.FunctionUrlAuthType.NONE,
    });

    new cdk.CfnOutput(this, "FirstLambdaFunctionUrlOutput", {
      value: FirstLambdaFunctionUrl.url,
    });

    // The code that defines your stack goes here

    // example resource
    // const queue = new sqs.Queue(this, 'InfraQueue', {
    //   visibilityTimeout: cdk.Duration.seconds(300)
    // });
  }
}
