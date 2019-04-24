#!/usr/bin/env python3
import argparse

from autotags.base import AWSResourceTags
from autotags.ec2tags import EC2Tags
from autotags.ebstags import EBSTags
from autotags.s3tags import S3Tags
from autotags.rdstags import RDSTags

def update_tags():
    return 

def main():
    parser = argparse.ArgumentParser(prog='AWSResourceTagging', usage='%(prog)s [options]', description='Framework to auto tag AWS resources')
    parser.add_argument('--key', type=str, help='AWS Secret Key')
    parser.add_argument('--secret', type=str, help='AWS Secret')
    parser.add_argument('--region', type=str, help='AWS Region')
    args = parser.parse_args()

    if args.key is None:
        parser.error("AWS Key cannot be Null!")
    elif args.secret is None:
        parser.error("AWS Secret cannot be Null!")
    elif args.region is None:
        parser.error("AWS Region cannot be Null!")

    ec2 = EC2Tags(args.key, args.secret)
    instances = ec2.getAllInstances()

    for ins,reg in instances.items():
        user = ec2.getEC2userName(region=reg, resource_id=ins)
        status = ec2.setEC2Tags(resource_id=ins, region=reg, Owner="{}".format(user), OwnerEmail="{}@redhat.com".format(user), Project="CP-DevOps", CostCode="Test", Purpose="Test", Role="SSE", Environment="Development")
        print(status)
if __name__ == '__main__':
    main()
