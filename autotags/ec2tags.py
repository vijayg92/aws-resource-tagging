#!/usr/bin/env python3
import threading
import multiprocessing
import logging

from autotags.base import AWSResourceTags
from botocore.exceptions import ClientError

class EC2Tags(AWSResourceTags):
    
    manager = multiprocessing.Manager()
    instances = manager.dict()
    logformat = "[%(levelname)-s %(asctime)-s %(threadName)-s ] %(message)s"

    def __init__(self, key, secret):
        AWSResourceTags.__init__(self, key, secret)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename='ec2tags.logs', level=logging.INFO, format=self.logformat)

    def getInstances(self, region='us-east-1'):
        conn = self._getConnection(region=region)
        try:
            self.logger.info("Fetching AWS EC2 list for {} Region".format(region))
            reservations = conn.describe_instances()["Reservations"]
            ''' Dictionary comprehension doesn't work with Multithreading/Multiprocess hence commented it out.
                self.instances = {instance['InstanceId']: instance['PrivateIpAddress'] for reservation in reservations for instance in reservation["Instances"]}
            '''
            for reservation in reservations:
                for instance in reservation["Instances"]:
                    self.instances[instance['InstanceId']] = region
                    self.logger.info("Fetched {} EC2 instance of AWS {} Region".format(instance['InstanceId'], region))
        except ClientError as e:
            self.logger.error("Connection Error : {}".format(e))
        return self.instances

    def getAllInstances(self):
            processes = []
            regions = self.getRegions()
            
            for region in regions:
                process = multiprocessing.Process(target=self.getInstances, args=(region,))
                process.start()
                processes.append(process)

            for process in processes:
                process.join()
            
            return self.instances
    
    def getEC2userName(self, region, resource_id):
        user = self.getResourceOwner( 
            region=region, 
            trail_event='RunInstances', 
            resource_type="AWS::EC2::Instance", 
            resource_id=resource_id
        )
        return user 

    def setEC2Tags(self, region, resource_id, **tags):
        status = False
        conn = self._getConnection(region=region,connection_type='resource')
        response = conn.Instance(resource_id)
        self.logger.info("Starting tagging resource {} of {} Region".format(resource_id, region))
        if response.tags:
            if list(filter(lambda x: x['Key'] == "Owner", response.tags)):
                self.logger.info("Owner tag is already set for , hence, no changes were made!!".format(resource_id))
            else:
                for k, v in tags.items():
                    conn.create_tags(Resources=[resource_id], Tags=[{'Key': k, 'Value': v}])
                    self.logger.info("Successfully added tags for EC2 {} instance".format(resource_id))
                    status = True
        else:
            for k, v in tags.items():
                conn.create_tags(Resources=[resource_id], Tags=[{'Key': k, 'Value': v}])
                self.logger.info("Successfully added tags for EC2 {} instance".format(resource_id))
            self.logger.info("Successfully added tags for EC2 {} instance".format(resource_id))
        self.logger.info("Tagging is Completed for EC {} Instance!!".format(resource_id))
        return status