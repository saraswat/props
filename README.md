What is PropS?
------------
PropS offers an output representation designed to explicitly and uniformly express much of the proposition structure which is implied from syntax.

Semantic NLP applications often rely on dependency trees to recognize major elements of the proposition structure of sentences. 
Yet, while much semantic structure is indeed expressed by syntax, many phenomena are not easily read out of dependency trees, often leading to further ad-hoc heuristic post-processing or to information loss. 
For that end, PropS post-processes dependency trees to present a compelling representation for downstream tasks.

Find more details, examples, and an online demo at the [project page](http:/www.cs.biu.ac.il/~stanovg/props.html).


Installation
------------
Run `sudo -E python ./setup.py install` from the props root directory.
This will install several python packages and other resources which PropS uses and relies upon (see [requirements.txt](props/install/requirements.txt) and [install.sh](props/install/install.sh) for the complete list).

MacOS users might run into issues installing JPype. An instruction to manually install JPype on MacOS can be found on the [berkely parser python interface repository](https://github.com/emcnany/berkeleyinterface#installation-and-dependencies).

_vj: To install and run on my MacOs I had to do these things_
  1. First ensure you are working in a Python 2.7. For this, given that i am using `conda 3.6` I had to this:
```
conda create --name python27 python=2.7.13
source activate python27
```
  2. Comment out the line `sed -i s/six==1.5.2/six==1.10.0/ requirements.txt` in install/instal.sh (apparently MacOs does not support `-i` on sed?!). Instead execute what it says on `install/requirements.txt`. (The updated `requirements.txt` is committed.)
  3. Download `JPype` manually, (comment out its `wget` in `install/install.sh`) and edit its `setup.py` to add the following lines
```
        #I added this line below. The folder contains a jni.h
        "/System/Library/Frameworks/JavaVM.framework/Versions/A/Headers/"
```
at the end of `setupInclusion(self)` in its `setup.py`. Now rerun `sudo -E pythoon ./setup.py install` 

  4. I was also forced to install a legacy Java 1.6 when I attempted to run the unit test below.

Prerequisites
-------------

* python 2.7
* java 7 (make sure to set the JAVA_HOME enviroment variable (e.g., /usr/lib/[*your_java_folder*])

Testing 
-------

Run `python ./unit_tests/sanity_test.py`


