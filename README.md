# COMP90024 Group 75

## Overview
The general question we aim to answer is: what is the relationship between Australians’ moods, unemployment levels, and the stock market? We chose these three disparate yet related metrics in the hope that we could uncover some interesting patterns and relationships.

Our question can be more precisely reframed as three distinct questions:
1. What is (if any) the statistical relationship between the evaluated sentiments of Australian tweets and the daily ASX 200 from mid-2021 to mid-2022?
2. What is (if any) the statistical relationship between the evaluated sentiments of Australian tweets and the unemployment levels across various states during mid-2021?
3. What is (if any) the statistical relationship between the overall unemployment level across Australia and the ASX 200 from 2012 to 2021?

## Requirements
- Python 3.x
  - pandas
  - requests
  - matplotlib
  - statsmodels
  - elasticsearch
- Jupyter Notebook
- OpenStack CLI
- jq
- kubectul


## Directory structure
```
.
├── backend
│   ├── addAsx.py
│   ├── addUnemployment.py
│   ├── fission
│   │   ├── functions
│   │   │   ├── affords
│   │   │   │   ├── __init__.py
│   │   │   │   ├── addAffords.py
│   │   │   │   ├── build.sh
│   │   │   │   └── requirements.txt
│   │   │   ├── airmonitor
│   │   │   │   ├── addAir.py
│   │   │   │   └── airmonitor.py
│   │   │   ├── asx
│   │   │   │   ├── getDailyAsx.py
│   │   │   │   ├── getQuarterlyASX.py
│   │   │   │   └── indexAsx.py
│   │   │   ├── tweet
│   │   │   │   ├── getDailyTweets.py
│   │   │   │   ├── getTweets.py
│   │   │   │   └── getTweetsByState.py
│   │   │   └── unemployment
│   │   │       ├── IndexUnemployment.py
│   │   │       ├── getMidYearUnemp.py
│   │   │       ├── getQuarterlyUnemployment.py
│   │   │       └── getUnemployment.py
│   │   └── specs
│   │       ├── README
│   │       ├── airconst.yaml
│   │       ├── env-nodejs.yaml
│   │       ├── env-python.yaml
│   │       ├── env-python39x.yaml
│   │       ├── fission-deployment-config.yaml
│   │       ├── function-addafford.yaml
│   │       ├── function-addair.yaml
│   │       ├── function-addasx.yaml
│   │       ├── function-addunemployment.yaml
│   │       ├── function-getdailyasx.yaml
│   │       ├── function-getdailytweets.yaml
│   │       ├── function-getmidyearunemp.yaml
│   │       ├── function-getquarterlyasx.yaml
│   │       ├── function-getquarterlyunemp.yaml
│   │       ├── function-gettweets.yaml
│   │       ├── function-gettweetsbystate.yaml
│   │       ├── function-getunemployment.yaml
│   │       ├── function-harvestair.yaml
│   │       ├── route-addafford.yaml
│   │       ├── route-addair.yaml
│   │       ├── route-addasx.yaml
│   │       ├── route-addunemployment.yaml
│   │       ├── route-getdailyasx.yaml
│   │       ├── route-getdailytweets.yaml
│   │       ├── route-getmidyearunemp.yaml
│   │       ├── route-getquarterlyasx.yaml
│   │       ├── route-getquarterlyunemp.yaml
│   │       ├── route-gettweets.yaml
│   │       ├── route-gettweetsbystate.yaml
│   │       ├── route-getunemployment.yaml
│   │       ├── route-harvestair.yaml
│   │       └── timetrigger-everyminute.yaml
│   ├── get.py
│   ├── readdataset.py
│   └── res
│       ├── asx.csv
│       ├── salm.csv
│       └── sgs.csv
├── backendAPI
├── es
│   ├── mapping
│   │   ├── air
│   │   ├── asx
│   │   ├── tweets
│   │   └── unemployment
│   └── queries
├── frontend
│   └── Answers.ipynb
├── packagebuild
└── ted
```

## Instruction
# Setting up environment
1. Setting up the OpenStack Environment
run `source unimelb-comp90024-2024-grp-75-openrc.sh` and type password to sets up environment variables for OpenStack authentication and configuration

2. Setting up the SSH Tunnel
run `ssh -i mykeypair.pem -L 6443:$(openstack coe cluster show elastic -f json | jq -r '.master_addresses[]'):6443 ubuntu@$(openstack server show bastion -c addresses -f json | jq -r '.addresses["qh2-uom-internal"][]')
` to obtain the internal address of the bastion server and establish an SSH connection.

3. Checking Kubernetes Nodes
When the connection to bastion is confirmed, open a new terminal and repeat steps 1 and 2. Then use `kubectl get nodes` to list all nodes in the current Kubernetes cluster and check the nodes

4. Port Forwarding a Kubernetes Service
run `kubectl port-forward service/router -n fission 9090:80` to forward the port of a specific Kubernetes service locally so that the service can be accessed from the local environment.

# Run analysis
1. Install Jupyter Notebook
run `pip install notebook` to install Jupyter Notebook used for analysis

2. Navigate to the Directory
run `cd frontend` to navigate to the directory where Answers.ipynb is located

3. Start Jupyter Notebook
run `jupyter notebook` to start jupyter notebook

4. Open the Notebook (Answers.ipynb) and run each cell 
if Port Forwarding is successful in the Setting up environment, the data set is accessible and each cell is ready to run.
