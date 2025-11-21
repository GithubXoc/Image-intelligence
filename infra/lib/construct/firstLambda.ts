import * as lambda from "aws-cdk-lib/aws-lambda";
import * as cdk from "aws-cdk-lib/core";
import { Construct } from "constructs";

export class FirstLambda extends Construct {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    const FirstLambdaFunction = new lambda.Function(
      this,
      "FirstLambdaFunction",
      {
        runtime: lambda.Runtime.PYTHON_3_13,
        handler: "index.handler",
        code: lambda.Code.fromInline(
          "def handler(event, context):\n    return 'Hello, World!'"
        ),
      }
    );

    const FirstLambdaFunctionUrl = FirstLambdaFunction.addFunctionUrl({
      authType: lambda.FunctionUrlAuthType.NONE,
    });

    new cdk.CfnOutput(this, "FirstLambdaFunctionUrlOutput", {
      value: FirstLambdaFunctionUrl.url,
    });
  }
}
