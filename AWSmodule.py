#!/usr/bin/env python
import os
import datetime
import boto
from boto.ec2.connection import EC2Connection

access_key = os.environ.get('AWS_ACCESS_KEY')
secret_key = os.environ.get('AWS_SECRET_KEY')

def roundTime(dt=None, roundTo=60):
   if dt == None : dt = datetime.datetime.now()
   seconds = (dt - dt.min).seconds
   rounding = (seconds+roundTo / 2) / roundTo * roundTo
   return dt + datetime.timedelta(0,rounding-seconds,-dt.microsecond)

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
		self.filters = {}
		
		for reservation in self.conn.get_all_instances(filters=filters):
			for instance in reservation.instances:
				instances.append(instance)

		return instances


	def start_instances(self, time):
		self.filters = {'tag:StartTime' : time}
	
		for i in self._get_instances():
			#i.add_tag('StartTime', i.tags['Default_StarTime'])
			#i.start()
			# Print i.name or whatever for testing
			print i

	def stop_instances(self, time):
		self.filters = {'tag:StopTime' : time}
	
		for i in self._get_instances():
			#i.add_tag('StopTime', i.tags['Default_StopTime'])
			#i.stop()
			# Print i.name or whatever for testing
			print i


	def get_instance_by_id(self, id):
		self.filters = {'instance-id' : id}
		return self._get_instances()[0]
	

	def all_instances(self):
		return self._get_instances()


if __name__ == "__main__":
	sa_inst = AWSInst('sa-east-1')
	nv_inst = AWSInst('us-east-1')
	requestminutes = 60

	now = roundTime(datetime.datetime.now(), roundTo=requestminutes*15)
	strtime = now.strftime('%H%M')

	noon = now.replace(hour=12)
	if now > noon:
		sa_inst.stop_instances(strtime)
		nv_inst.stop_instances(strtime)

	#else:
	#   sa_inst.stop_instances(strtime)
	#   nv_inst.stop_instances(strtime)
