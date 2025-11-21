import * as cdk from "aws-cdk-lib";
import * as s3 from "aws-cdk-lib/aws-s3";
import { Construct } from "constructs";

export class S3bucket extends Construct {
  public readonly bucketName: string;

  constructor(scope: Construct, id: string) {
    super(scope, id);

    const bucket = new s3.Bucket(this, "ImageIntelligence", {
      versioned: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });

    this.bucketName = bucket.bucketName;

    const frontendBucket = new s3.Bucket(this, "FrontendBucket", {
      websiteIndexDocument: "index.html",
    });

    new cdk.CfnOutput(this, "FrontendBucketURL", {
      value: frontendBucket.bucketWebsiteUrl,
    });

    new cdk.CfnOutput(this, "ImageIntelligenceBucketName", {
      value: bucket.bucketName,
    });
  }
}
