#!/usr/bin/env python
import os
import time
import random
import multiprocessing  # the module we will be using for multiprocessing

def work(Run):
	#NEvents=1000000
	WORKING_DIRECTORY=os.getcwd()
	#randSeed=random.randint(0,32766)
	#resultsFile="AmberTarget_"+str(Run)
	#os.system("mkdir "+resultsFile)
	#os.system("cp "+WORKING_DIRECTORY+"/MultipleFibbers "+resultsFile)
	#os.system("cp "+WORKING_DIRECTORY+"/*.mac "+resultsFile)
	#os.system("cp "+WORKING_DIRECTORY+"/TRITIUMSpectrumNew.txt "+resultsFile)
	#os.chdir(WORKING_DIRECTORY+"/"+resultsFile)
	os.system("./AmberTarget "+str(Run)+" 0")
	#os.system("mv *.root "+WORKING_DIRECTORY+"/DATA/")
	#os.system("mv output*.txt "+WORKING_DIRECTORY+"/OUTPUTS/")
	#os.chdir(WORKING_DIRECTORY)
	#os.system("rm -rf "+resultsFile)
	print ("Unit of work number %d" % Run ) # simply print the worker's number

if __name__ == "__main__":  # Allows for the safe importing of the main module
	print("There are %d CPUs on this machine" % multiprocessing.cpu_count())
	#os.system("mkdir DATA")
	#os.system("mkdir OUTPUTS")
	number_processes = multiprocessing.cpu_count()-1
	pool = multiprocessing.Pool(number_processes)
	total_tasks = 100
	tasks = range(total_tasks)
	results = pool.map_async(work, tasks)
	pool.close()
	pool.join()

#adicionar aqui o hadd
	
