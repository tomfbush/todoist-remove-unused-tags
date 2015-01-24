# -*- coding: utf-8 -*-

# Load prerequisites
import requests
import json
import os.path

# Set some timesaving constants

todoistURL = 'https://www.todoist.com/API'
usedLabelIDs = []
removeLabelIDs = []

# This function saves time printing JSON nicely
def pj(str):
   print(json.dumps(json.loads(str.content), indent=4))
   return

# Set login parameters (old, insecure) and obtain token
file = open('token.txt', 'r')
usertoken = file.read().strip()

##   loginParams = {'email': '', 'password': ''}
##   r = requests.post(todoistURL+"/login", params=loginParams).json()
##   usertoken = r['api_token']

token = {'token': usertoken}

# Get a list of projects and their details by API request and using token obtained above 
projectList = requests.post(todoistURL+"/getProjects", params=token).json()

# Put just the project IDs into projectIDs
projectIDs = [project['id'] for project in projectList]

# Get a list of all labels
labelList = requests.post(todoistURL+"/getLabels", params=token).json()

# Put just the label IDs into labelIDs
labelIDs = [labelList[label]['id'] for label in labelList]

# Get a list of incomplete tasks and the labels in use on them
for projectid in projectIDs:
    token.update({'project_id' : projectid})
    taskList = requests.post(todoistURL+"/getUncompletedItems", params=token).json()
    del token['project_id']

# Check if any content in each labels field and where there is, for each item append to a separate list
    for label in taskList:
        if label['labels']:
            newlabel = label['labels']
            for id in newlabel:
                usedLabelIDs.append(id)

# Remove the used labels from the overall list
removeLabelIDs = labelIDs

for label in usedLabelIDs:
    if label in removeLabelIDs:
        removeLabelIDs.remove(label)

### Print list of labels to remove as a check
##for x in labelList:
##	if labelList[x]['id'] in removeLabelIDs:
##		print labelList[x]['name']

# Remove the remainders from Todoist
for x in labelList:
   if labelList[x]['id'] in removeLabelIDs:
      token.update({'name' : labelList[x]['name']})
      requests.post(todoistURL+"/deleteLabel", params=token)

'''

TODO

[ ] Create new dicts for the tokens for each request instead of using del on lingering project_id

'''
