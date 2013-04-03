import os

if os.platform == 'darwin':

import keychain

access_key = ""
secret_key = ""
#...

class AWSInst:
	filters = {}


	def __init__(self, region):
		self.conn = boto.ec2.connect_to_region(region,
				aws_access_key_id=access_key,
				aws_secret_access_key=secret_key)

	
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
	
		for i in self.__get_instances():
			i.add_tag('StopTime', i.tags['Default_StopTime'])
			i.start()


	def stop_servers(self, time):
		self.filters = {'tag:StopTime' : time}
	
		for i in self.__get_instances():
			i.add_tag('StopTime', i.tags['Default_StopTime'])
			i.stop()



x = AWSInst('sa-east')
x.start_servers('0900')
