#!/usr/bin/env python
#
#
#
import os
import boto
from boto.ec2.connection import EC2Connection

access_key = os.environ.get('AWS_ACCESS_KEY')
secret_key = os.environ.get('AWS_SECRET_KEY')

class AWSInst:

	def __init__(self, region):
		if not access_key or not secret_key:
			#raise KeyError (' ;)~ ')
			raise ValueError ('Missing access and or secret keys')

		self.filters = {}

		self.conn = boto.ec2.connect_to_region(region,
				aws_access_key_id=access_key,
				aws_secret_access_key=secret_key)

		if not self.conn:
			raise ValueError ('Failed to connect')

	
	def _get_instances(self):
		instances = []
		filters = {'tag:Managed': 'True'}
		filters.update(self.filters)
		
		for reservation in self.conn.get_all_instances(filters=filters):
			for instance in reservation.instances:
				instances.append(instance)

		return instances


	def start_servers(self, time):
		self.filters = {'tag:StartTime' : time}
	
		for i in self._get_instances():
			#i.add_tag('StartTime', i.tags['Default_StarTime'])
			#i.start()
			# Print i.name or whatever for testing
			print i

	def stop_servers(self, time):
		self.filters = {'tag:StopTime' : time}
	
		for i in self._get_instances():
			#i.add_tag('StopTime', i.tags['Default_StopTime'])
			#i.stop()
			# Print i.name or whatever for testing
			print i


x = AWSInst('sa-east-1')
x.start_servers('0900')
