# PythonUtils
Some Python code, that I write to solve work tasks

## PMatrix.py
Script, working like console application. Made for creating access matrix for set of users in linux-like operation systems. 

### Dependencies:
- [Temcolor](https://pypi.python.org/pypi/termcolor). To install it use command 'sudo pip install termcolor' 



### Use example:

This example creates html table with users from users.txt file and their permissions to directories from dirs.txt file

**sudo python PMatrix.py**

**check permissions users.txt dirs.txt -matrixHTML**


### Screenshots:


## augmentDatasets.py
This script creating randomly augmented/distorted images for machine learning tasks.

### Dependencies:

- [Augmentor](https://github.com/mdbloice/Augmentor). To install it use command 'sudo pip install Augmentor' 

### Use example:

This example creates 1000 augmented images, based on source images from directories in datasets.txt file

**python augmentDatasets.py 1000 datasets.txt**
