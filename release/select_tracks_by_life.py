# 3DE4.script.name: Select Tracks By Life
# 3DE4.script.version: v1.1
# 3DE4.script.comment: Created by Jaffords 2017
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Timeline Editor::Edit
# 3DE4.script.gui:	Object Browser::Context Menu Points::Select
# 3DE4.script.gui:	Object Browser::Context Menu Point::Select



from tde4 import *


pointLengthList = []
pgroup = ""


def updatePointLengthList():
	global pointLengthList
	global pgroup
	pointLengthList = []
	pgroup = ""
	pgroup = getCurrentPGroup()
	camera = getCurrentCamera()
	frames = getCameraPlaybackRange(camera)
	framerange = (frames[1]-frames[0])+1
	pointList = getPointList(pgroup, 0)
	for point in pointList:
		pointPosition2DBlock = getPointPosition2DBlock(pgroup, point, camera, frames[0], frames[1])
		trackLength = 0
		for frame in pointPosition2DBlock:
			if frame[0]!=-1.0 and frame[1]!=-1.0:
				trackLength += 1
		trackLength = int((100*trackLength)/framerange)
		pointLengthList.append([point, trackLength, getPointAutoTrackingFlag(pgroup, point)])


def startup(requester):
	updatePointLengthList()
	pointSelector(requester,"widget","action")


def pointSelector(requester,widget,action):
	global pointLengthList
	global pgroup
	life = getWidgetValue(requester, "life")
	auto_only = getWidgetValue(requester, "auto_only")
	invert = getWidgetValue(requester, "invert")
	flags = [0,1]
	for point in pointLengthList:
		if (invert == 1):
			flags = [1,0]
		if (life >= point[1] and auto_only == 0) or (life >= point[1] and auto_only == 1 and point[2] == 1):
			setPointSelectionFlag(pgroup, point[0], flags[1])
		else:
			setPointSelectionFlag(pgroup, point[0], flags[0])


def pointsAction(requester,widget,action):
	global pointLengthList
	global pgroup
	for point in pointLengthList:
		if getPointSelectionFlag(pgroup, point[0]):
			if widget == "delete":
				deletePoint(pgroup, point[0])
			elif widget == "active":
				setPointCalcMode(pgroup, point[0], "CALC_ACTIVE")
			elif widget == "passive":
				setPointCalcMode(pgroup, point[0], "CALC_PASSIVE")
			elif widget == "off":
				setPointCalcMode(pgroup, point[0], "CALC_OFF")
	updatePointLengthList()


def close(requester,widget,action):
	unpostCustomRequester(requester)


window = createCustomRequester()
addScaleWidget(window, "life", "Life %: ", "INT", 0, 100, 70)
setWidgetCallbackFunction(window, "life", "pointSelector")
addToggleWidget(window, "auto_only", "Only Autotracks", 0)
setWidgetCallbackFunction(window, "auto_only", "pointSelector")
addToggleWidget(window, "invert", "Invert Selection", 0)
setWidgetCallbackFunction(window, "invert", "pointSelector")
addButtonWidget(window, "active", "Active", 70, 137)
setWidgetCallbackFunction(window, "active", "pointsAction")
addButtonWidget(window, "passive", "Passive", 70, 10, "active")
setWidgetCallbackFunction(window, "passive", "pointsAction")
addButtonWidget(window, "off", "Off", 70, 10, "passive")
setWidgetCallbackFunction(window, "off", "pointsAction")
addButtonWidget(window, "delete", "Delete", 70, 10, "off")
setWidgetCallbackFunction(window, "delete", "pointsAction")
addSeparatorWidget(window, "separator")
addButtonWidget(window, "close", "Close", 70, 377)
setWidgetCallbackFunction(window, "close", "close")
postCustomRequesterAndContinue(window, "Select Tracks By Life v1", 457, 130, "startup")
updateGUI()