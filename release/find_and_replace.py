# 3DE4.script.name: Find & Replace
# 3DE4.script.version: v1.0
# 3DE4.script.comment: Created by Jaffords 2019
# 3DE4.script.gui:	Object Browser::Path
# 3DE4.script.gui:	Object Browser::Context Menu Camera
# 3DE4.script.gui:	Object Browser::Context Menu Reference Camera


from tde4 import *
import os
import json
import platform


#Find = "/media/cake/Jaffords"
#Replace = "G:"
# user_data


class Presets():
	

	# variables
	DB_NAME = "FindAndReplacePresets.json"
	default = {"Defailt":{"find":"","replace":""}}
	db_path = os.path.join(get3DEInstallPath(),"user_data", DB_NAME)
	
	
	# methods
	def __init__(self):
		self.preset = {}
		self.loadBD() if os.path.exists(self.db_path) else self.updateDB()
	
	def updateDB(self):
		try:
			with open(self.db_path,"w") as file:
				if not self.preset: self.preset = self.default 
				json.dump(self.preset, file)
		except Exception as e:
			print("Create or Write presets database error! File:", self.db_path)
			raise e
	
	
	def loadBD(self):
		try:
			with open(self.db_path,"r") as file:
				tmp = json.load(file)
			self.preset = tmp if tmp else self.updateDB()
		except Exception as e:
			print("Open presets database error! File:", self.db_path)
			raise e


P = Presets()
cameras = getCameraList()

def getData(requester, data):
	data = getWidgetValue(requester, data)
	if not data: data = ""
	return data


def getSelected(requester):
	for item in range(0,getListWidgetNoItems(requester, "presets")):
		if getListWidgetItemSelectionFlag(requester, "presets",item):
			return getListWidgetItemLabel(requester, "presets",item)

def savePreset(requester,widget,action):
	find, replace = getData(requester,"find"), getData(requester,"replace")
	name = getSelected(requester)
	P.preset[name]["find"] = find
	P.preset[name]["replace"] = replace


def deletePreset(requester,widget,action):
	name = getSelected(requester)
	question = postQuestionRequester("Delete", "Do you want to remove '%s' preset?" %name,"Ok","Cancel")
	if question == 1:
		del P.preset[name]
		if not P.preset:
			P.preset = P.default
		printAll(requester)
		setListWidgetItemSelectionFlag(requester, "presets", 0, 1)
		select(requester, "presets", "select")

def renamePreset(requester,widget,action,default_name = "New Name"):
	window = createCustomRequester()
	addTextFieldWidget(window, "name", "Name", default_name)
	action = postCustomRequester(window, "Rename Preset", 400, 50, "Rename", "Cancel")
	if action == 1:
		old_name = getSelected(requester)
		name = getWidgetValue(window, "name")
		if name and name not in P.preset:
			P.preset[name] = P.preset[old_name]
			del P.preset[old_name]
			printAll(requester)
		else:
			question = postQuestionRequester("Error", "Name '%s' empty or already exists! Put anothe name?" %name,"Ok","Cancel")
			if question == 1:
				renamePreset(requester,widget,action,name)

def printAll(requester):
	removeAllListWidgetItems(requester, "presets")
	for key in sorted(P.preset):
		insertListWidgetItem(requester, "presets", key)



def select(requester,widget,action):
	p_name = getSelected(requester)
	find = P.preset[p_name]["find"]
	replace = P.preset[p_name]["replace"]
	setWidgetValue(requester, "find", find)
	setWidgetValue(requester, "replace", replace)



def path_replacer(cameras,find,replace,import_BCF):	
	postProgressRequesterAndContinue("Find & Replace", "", len(cameras), "Cancel")	
	iteration = 0
	for camera in cameras:
		cancel = updateProgressRequester(iteration, getCameraName(camera))
		if cancel == 0:
			break
		path = getCameraPath(camera)
		path = path.replace(find, replace)
		if platform.system() == "Windows":
			path = path.replace("/", "\\")
		else:			
			path = path.replace("\\", "/")
		setCameraPath(camera, path)
		iteration += 1
	unpostProgressRequester()
	if import_BCF:
		cameras = [i for i in cameras if getCameraType(i) == "SEQUENCE"]
		postProgressRequesterAndContinue("Import Buffer Compression Files", "", len(cameras), "Cancel")
		iteration = 0
		for camera in cameras:
			cancel = updateProgressRequester(iteration, getCameraName(camera))
			if cancel == 0:
				break
			importBufferCompressionFile(camera)
			iteration += 1
		unpostProgressRequester()

def switch(requester,widget,action):
	find, replace = getData(requester,"find"), getData(requester,"replace")
	setWidgetValue(requester, "find", replace)
	setWidgetValue(requester, "replace", find)


def addNew(requester,widget,action,default_name = "New Preset Name"):
	find, replace = getData(requester,"find"), getData(requester,"replace")
	window = createCustomRequester()
	addTextFieldWidget(window, "name", "Name", default_name)
	action = postCustomRequester(window, "Add New Preset", 400, 50, "Add", "Cancel")
	if action == 1:
		name = getWidgetValue(window, "name")
		if name and name not in P.preset:
			P.preset[name] = {"find" : find, "replace" : replace}
			printAll(requester)
		else:
			question = postQuestionRequester("Error", "Name '%s' empty or already exists! Put anothe name?" %name,"Ok","Cancel")
			if question == 1:
				addNew(requester,widget,action,name)
if cameras:
	requester = createCustomRequester()
	addListWidget(requester, "presets", "Presets", 0, 100)
	printAll(requester)
	addButtonWidget(requester, "add", "Add New *", 70)
	setWidgetCallbackFunction(requester, "add", "addNew")
	addButtonWidget(requester, "save", "Save", 70, 10,"add")
	setWidgetCallbackFunction(requester, "save", "savePreset")
	addButtonWidget(requester, "delete", "Delete", 70, 10,"save")
	setWidgetCallbackFunction(requester, "delete", "deletePreset")
	addButtonWidget(requester, "rename", "Rename", 70, 10,"delete")
	setWidgetCallbackFunction(requester, "rename", "renamePreset")
	addTextFieldWidget(requester, "find", "Find")
	addTextFieldWidget(requester, "replace", "Replace")
	addButtonWidget(requester, "switch", "Switch", 70,-70,"find")
	setWidgetCallbackFunction(requester, "switch", "switch")	
	setListWidgetItemSelectionFlag(requester, "presets", 0, 1)	
	select(requester, "presets", "select")
	setWidgetCallbackFunction(requester, "presets", "select")
	addToggleWidget(requester, "import_BCF", "Import Buffer Compression File", 0)
	addOptionMenuWidget(requester, "cams", "Cameras", "All","All Sequences","All Reference", "Selected", "Current")
	action = postCustomRequester(requester, "Find & Replace Camera Path", 740, 300,"Replace", "Cancel")	
	if action == 1:
		find, replace = getData(requester,"find"), getData(requester,"replace")
		import_BCF = bool(getWidgetValue(requester, "import_BCF"))
		cams = getWidgetValue(requester, "cams")
		if cams == 2:
			cameras = [i for i in cameras if getCameraType(i) == "SEQUENCE"]
		if cams == 3:
			cameras = [i for i in cameras if getCameraType(i) == "REF_FRAME"]
		if cams == 4:
			cameras = getCameraList(1)
		if cams == 5:
			cameras = [getCurrentCamera()]
		if find != replace:
			path_replacer(cameras,find,replace,import_BCF)
	P.updateDB() # save presets

