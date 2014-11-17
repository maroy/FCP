Forest Cover Prediction
=======================

Disclaimer
----------
Not much planning or forethought went into these scripts.
I created them to learn and explore. Until near the end of the
project I never thought I would use them again

I make no guarantees nor am I responsible for any harm that
may be caused by running these scripts

Pre-requisites
---------------

* python 2.7
* pyyaml
* Updated orange:<br />
	I found an issue with the Orange source code. The fix can be found in my fork:<br />
	https://github.com/maroy/orange

To run the classification:
--------------------------

1. Get train.csv and test.csv from Kaggle.
2. To generate the train.tab file:<br />
	`python 2tab.py True False train.csv`
3. To generate the test.tab file:<br />
	`python 2tab.py False False test.csv True`
4. To run the actual classification:<br />
	`python mp_runner.py`

* Not much feedback is given during training<br />
	*2 warnings were reported during the Neural Network training, I never looked into the cause*
* On subsequent runs the pickled classifier will be used and training will not run<br />
Delete the classifier.pickle file to re-run training


The results will be in a file named out.csv

To check the correct ratio of the output:
---------------------------
`python score_classifier.py`