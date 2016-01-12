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


ec2 = boto.ec2.connect_to_region('eu-west-1')
reservations = ec2.get_all_instances(filters={"tag:SteveWalsh":"SteveWalsh", "instance-state-name" : "running"})

cw = boto.ec2.cloudwatch.connect_to_region('eu-west-1') #Setting cloudWatch

autoscale = boto.ec2.autoscale.connect_to_region('eu-west-1') #Setting Autoscale

group = autoscale.get_all_groups(names=['sw-ASG'])[0] #Setting group



def usage():
	group = autoscale.get_all_groups(names=['sw-ASG'])[0]
	reservations = ec2.get_all_instances(filters={"tag:SteveWalsh":"SteveWalsh", "instance-state-name" : "running"})
	numInstances = 1 # set to one to stop errors
	avgCPU = 0
	
	for x in range(numInstances):
		try:
			instance = reservations[x].instances[0]
			num = instance.id
			stats = cw.get_metric_statistics(300,datetime.datetime.now()-datetime.timedelta(seconds=600),datetime.datetime.now(),'CPUUtilization','AWS/EC2','Average',dimensions={'InstanceId':[instance.id]})
			print(instance.state)
			#print(stats)
			dict = stats[0]
			if instance.state == "running":
				numInstances += 1
				print(numInstances)
			avgCPU = avgCPU + dict['Average']
			#print ("Instance " + str(x) + " CPU usage is :" + str(dict['Average']) + " state : " +instance.state)
			pass
		except Exception as e:
			raise e
	#print(str(avgCPU) +" : " + str(numInstances-1))
	avgCPU = avgCPU / (numInstances-1)
	print("The average CPU usage across all instances is : " + str(avgCPU))

	if (avgCPU > 40):
		print("Average CPU usage is above 40")
		print("Want to add another Instance to ASG")
		correct = True
		while(correct):
			ans = input("Input (y or n) : ")
			if ans.lower() == 'y':
				increaseCap()
				correct = False
			if ans.lower() == 'n':
				correct = False

	



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
		print("You are already at Max capacity")

# Wget bash script to minic traffic on server (high load)
def wGet():
	cmd = 'gnome-terminal -e ./getpage2.sh'
	(status, output) = subprocess.getstatusoutput(cmd)

# wget bash script to minic traffic on server causing 404page for logs
def wGet404():
	cmd = 'gnome-terminal -e ./getpage.sh'
	(status, output) = subprocess.getstatusoutput(cmd)

# info showing current size and max and min size
def info():
	group = autoscale.get_all_groups(names=['sw-ASG'])[0]
	print("Currnt running instances are : " + str(group.desired_capacity))
	print("Max : " + str(group.max_size) + "   Min : " + str(group.min_size))




      


# Define a main() function.
def main():
    

	ans=True
	while ans:
		print("""
		1. CPU Usage on all Instances
		2. Info
		3. Add an instance to ASG
		4. Remove an Instance from ASG
		5. wGet bash script
		6. wGet 404 bash script
		0. Exit script

		""")
		ans=input("What would you like to do? ")
		if ans=="1": 
			usage()
			input("Press Enter to continue...")
			os.system("clear")
		elif ans=="2":
			info()
			input("Press Enter to continue...")
			os.system("clear")
		elif ans=="3":
			increaseCap()
			input("Press Enter to continue...")
			os.system("clear")
		elif ans=="4":
			decreaseCap()
			input("Press Enter to continue...")
			os.system("clear")
		elif ans=="4":
			wGet()
			input("Press Enter to continue...")
			os.system("clear")
		elif ans=='5':
			wGet404()
			input("Press Enter to continue...")
			os.system("clear")
		elif ans == "0" : 
			exit()
		else :
			print("Invalid selection plesae choose again")
			input("Press Enter to continue...")
			os.system("clear")


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()
