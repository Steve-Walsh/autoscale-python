#!/usr/bin/python3

"""
Author  : Stephen Walsh
Course  : Applied Computing
Std Num : 20029981
Account : StudentA7
"""

import boto
import boto.ec2
import boto.ec2.cloudwatch
import boto.ec2.autoscale
import datetime
import subprocess
import os
import time


ec2 = boto.ec2.connect_to_region('eu-west-1')
reservations = ec2.get_all_instances(filters={"tag:SteveWalsh":"SteveWalsh", "instance-state-name" : "running"})

cw = boto.ec2.cloudwatch.connect_to_region('eu-west-1') #Setting cloudWatch

autoscale = boto.ec2.autoscale.connect_to_region('eu-west-1') #Setting Autoscale

group = autoscale.get_all_groups(names=['sw-ASG'])[0] #Setting group



def usage():
	roundNum =1 
	turn = 0
	while (True):
		print("This is round : " + str(roundNum))
		roundNum += 1
		group = autoscale.get_all_groups(names=['sw-ASG'])[0]
		reservations = ec2.get_all_instances(filters={"tag:SteveWalsh":"SteveWalsh", "instance-state-name" : "running"})
		numInstances = 1 # set to one to stop errors
		avgCPU = 1 # set to one to stop errors
		print("There is a total of " + str(len(reservations)) + " instance/s running")
	
		for x in range(numInstances):
			instance = reservations[x].instances[0]
			num = instance.id
			stats = cw.get_metric_statistics(300,datetime.datetime.now()-datetime.timedelta(seconds=600),datetime.datetime.now(),'CPUUtilization','AWS/EC2','Average',dimensions={'InstanceId':[instance.id]})
				
			if instance.state == "running":
				dict = stats[0]
				numInstances += 1
				avgCPU = avgCPU + dict['Average']
		avgCPU = avgCPU -1 / (numInstances-1)
		print("The average CPU usage across all instances is : " + str(avgCPU))

		if (avgCPU > 40):
			turn +=1
		if avgCPU < 15:
			turn -=1
		
		if turn > 2:
			increaseCap()
			turn=0

		if turn < -1:
			decreaseCap()
			turn = 0

		print("Sleep for 30 seconds")
		time.sleep(30)	



# Used to increase the desired AMI cap
def increaseCap():
	group = autoscale.get_all_groups(names=['sw-ASG'])[0]
	numInstances = group.desired_capacity
	maxInstances = group.max_size
	if maxInstances >= (numInstances + 1):
		autoscale.set_desired_capacity('sw-ASG', numInstances + 1)
		print("Size increased from "+ str(numInstances) + " to " + str(numInstances+1))
	else: 
		print("You are already at Max capacity")

# Used to lower the desired AMI cap
def decreaseCap():
	group = autoscale.get_all_groups(names=['sw-ASG'])[0]
	numInstances = group.desired_capacity
	minInstances = group.min_size
	if numInstances -1 >= minInstances:
		autoscale.set_desired_capacity('sw-ASG', numInstances -1)
		print("Size increased from "+ str(numInstances) + " to " + str(numInstances-1))
	else: 
		print("You are already at Min capacity")




      


# Define a main() function.
def main():
	usage()
    



# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
