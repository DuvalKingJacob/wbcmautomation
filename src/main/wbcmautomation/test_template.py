"""Test Module for Base IAM Cloudformation Template"""
import os
import unittest
import boto3
import botocore
from .template import create_cft

project_name = "wbcm"
bucket_name = "frgcloud.lab.internal"
file_template = "ci-cloudformation/%s/%s-%s-%s/tcsgtemplates.json"
file_name = file_template % (
    project_name,
    project_name,
    os.getenv("CIRCLE_BRANCH", "test"),
    os.getenv("CIRCLE_BUILD_NUM", "SNAPSHOT")
)
cft_url = "https://s3.amazonaws.com/%s/%s" % (bucket_name, file_name)


class TestCloudFormation(unittest.TestCase):
    """Test class"""
    @staticmethod
    def test_tcsgs_cft():
        """Test function"""
        tmpl = create_cft().to_json()
        cft = boto3.client('cloudformation')
        s3resource = boto3.resource('s3')
        try:
            # idempotent operation
            bucket = s3resource.create_bucket(Bucket=bucket_name)
            bucket.put_object(Key=file_name, Body=tmpl)
            return cft.validate_template(TemplateURL=cft_url)
        except botocore.exceptions.ClientError as exc:
            raise Exception(exc.response['Error']['Message'])

if __name__ == '__main__':
    unittest.main()
