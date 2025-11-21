import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import { S3bucket } from "./construct/S3bucket";
import { FirstLambda } from "./construct/firstLambda";

export class InfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    new FirstLambda(this, "FirstLambdaConstruct");

    const s3bucket = new S3bucket(this, "S3bucketConstruct");
  }
}