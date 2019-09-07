
# 3DE4.script.name: Save New Version
# 3DE4.script.version: v1
# 3DE4.script.comment: Created by Jaffords 2015
# 3DE4.script.gui:	Main Window::3DE4
# 3DE4.script.hide: false
# 3DE4.script.startup: false

import re
import os


currentProjectPath = str(tde4.getProjectPath())
if currentProjectPath != "None":
	currentProjectName = currentProjectPath.split("\\")[-1]
	currentProjectName = currentProjectName[0:-4]
	currentProjectVersion = re.findall("[vV]\d+$",currentProjectName)
	if currentProjectVersion:
		currentProjectNameWithOutVersion = currentProjectName[0:-len(str(re.findall("_*\s*-*[vV]\d+$",currentProjectName)[0]))]
		currentProjectVersion = int(str(currentProjectVersion[0])[1:])
		newProjectVersion = currentProjectVersion + 1
	else:
		currentProjectNameWithOutVersion = currentProjectName
		newProjectVersion = 2
	newProjectName = currentProjectNameWithOutVersion + "_v" + str(newProjectVersion)
	newProjectPath = currentProjectPath[0:-(len(currentProjectName)+4)] + newProjectName + ".3de"
	while os.path.isfile(newProjectPath) != False:
		newProjectVersion +=1
		newProjectName = currentProjectNameWithOutVersion + "_v" + str(newProjectVersion)
		newProjectPath = currentProjectPath[0:-(len(currentProjectName)+4)] + newProjectName + ".3de"
	if tde4.saveProject(newProjectPath):
		tde4.postQuestionRequester("Save New Version", "New version has successfully saved!", "Ok")
	else:
		tde4.postQuestionRequester("Save New Version", "Can't save new version. Permission denied!", "Ok")
else:
	tde4.postQuestionRequester("Save New Version", "Project not saved once!", "Ok")
