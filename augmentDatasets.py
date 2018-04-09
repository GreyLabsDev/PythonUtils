import os
import sys
import random
import Augmentor

def showHelp():
	print("\nTo generate augmentation use command 'augmentDatasets <paths_to_dataset_directories.txt>'")
	print("   Example:")
	print("           augmentDatasets datasetPaths.txt\n")

def getPipesFromFile(inputFile):
	file = open(inputFile, "r")
	samplePaths = file.readlines()
	file.close()

	pipesToProcess = []
	paths = []

	for i in range(0, len(samplePaths)):
		
		if (samplePaths[i].rstrip("\n") != ""):
			print("Found dataset directory:")
			path = samplePaths[i].rstrip("\n")

			print(path)
			tmpPipe = Augmentor.Pipeline(path)
			pipesToProcess.append(tmpPipe)

	return pipesToProcess

def setupPipes(pipesToProcess):
	print("Setting up the pipes operations")
	for i in range(0, len(pipesToProcess)):
		pipesToProcess[i].set_save_format("auto")
		pipesToProcess[i].skew_tilt(random.uniform(0,1), random.uniform(0.2, 0.9))
		pipesToProcess[i].skew(random.uniform(0,1), random.uniform(0.1,0.9))
		pipesToProcess[i].skew_left_right(random.uniform(0,1), random.uniform(0.2, 0.9))
		pipesToProcess[i].skew_top_bottom(random.uniform(0,1), random.uniform(0.2, 0.9))
		pipesToProcess[i].skew(random.uniform(0,1), random.uniform(0.2, 0.9))
		pipesToProcess[i].random_distortion(random.uniform(0,1), random.randint(2, 9),random.randint(2, 9), random.randint(1, 9))
		pipesToProcess[i].random_erasing(random.uniform(0,1), random.uniform(0.1, 0.2))
		pipesToProcess[i].rotate_random_90(random.uniform(0,1))
		pipesToProcess[i].shear(random.uniform(0,1), random.randint(5,15), random.randint(5,15))
		pipesToProcess[i].flip_left_right(random.uniform(0,1))
		pipesToProcess[i].flip_top_bottom(random.uniform(0,1))
		pipesToProcess[i].flip_random(random.uniform(0,1))

def processPipelines(pipesToProcess, samplesCount):
	for i in range(0, len(pipesToProcess)):
		pipesToProcess[i].sample(samplesCount)

def testAugmentor(pathToDataset):
	testPipe = Augmentor.Pipeline(pathToDataset)
	testPipe.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
	testPipe.zoom(probability=0.3, min_factor=1.1, max_factor=1.6)
	testPipe.sample(50)

# MAIN #
samplesN = sys.argv[1]
pipesListFile = sys.argv[2]

pipes = getPipesFromFile(pipesListFile)
setupPipes(pipes)

processPipelines(pipes, int(samplesN))