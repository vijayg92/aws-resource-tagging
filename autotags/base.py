#!/usr/bin/env python3
import boto3
import logging

from botocore.exceptions import ClientError


class AWSResourceTags:  
    """
        Tagging AWS Resources using CloudTrail event
    """
    logformat = "[%(levelname)-s %(asctime)-s %(threadName)-s ] %(message)s"

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='base.logs', level=logging.INFO, format=self.logformat)

    def _getConnection(self, region='us-east-1', resource='ec2', connection_type='client'):
        connections = ['client', 'resource']
        if connection_type not in connections:
            raise ValueError("Invalid Parameter: connection_type must be client or resource")
        try:
            if connection_type == 'client':
                conn = boto3.client(resource, aws_access_key_id=self.key, aws_secret_access_key=self.secret, region_name=region)
                self.logger.info("Client Connection")
            else:
                conn = boto3.resource(resource, aws_access_key_id=self.key, aws_secret_access_key=self.secret, region_name=region)
                self.logger.info("Resource Connection")
        except ClientError.error as e:
            self.logger.error("Connection Error : {}".format(e))
        except Exception as err:
            self.logger.error("Other Error : {}".format(err))          
        return conn

    def getRegions(self):
        conn = self._getConnection()
        try:
            self.logger.info("Fetching AWS Regions.")
            regions = (region['RegionName'] for region in conn.describe_regions()['Regions'])
        except ClientError as e:
            self.logger.error("Connection Error : {}".format(e))
        return regions

    def getResourceOwner(self, region, resource_type, resource_id, trail_event):
        user = None
        conn = self._getConnection(resource='cloudtrail', region=region)
        try:
            self.logger.info("Looking up events for {} EC2 instance in AWS {} Region".format(resource_id, region))
            response = conn.lookup_events(LookupAttributes=[{'AttributeKey': 'ResourceName', 'AttributeValue': resource_id}])
            if response['Events']:
                for a in range(0, len(response['Events'])):
                    for b in range(0, (len(response['Events'][a]['Resources']))):
                        if response['Events'][a]['EventName'] == trail_event and response['Events'][a]['Resources'][b]['ResourceType'] == resource_type:
                            owner = response['Events'][a]['Username']
            else:
                self.logger.info("Empty responsefor {} EC2 instance in AWS {} Region".format(resource_id, region))
        except KeyError as e:
            self.logger.error("Unable to lookup for {} event_type & {} resource_type : {}".format(trail_event, resource_type, e))
        except Exception as err:
            self.logger.error("Other Error Occurred: {}".format(err))
        return user
