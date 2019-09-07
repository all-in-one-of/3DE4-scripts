# 3DE4.script.name:	Batch Reference Frame Creator
# 3DE4.script.version:	v1.0
# 3DE4.script.comment: Create reference frames from selected sequence camera.
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Object Browser::Context Menu Camera

from tde4 import *


def getSelectedSeqCams():		
	return([x for x in getCameraList(1) if getCameraType(x) == "SEQUENCE"])	

def createRefFrames(cam,each):
	cam_attr = getCameraSequenceAttr(cam)	#[<start>,<end>,<step>]	
	for f in range(cam_attr[0],cam_attr[1],cam_attr[2]*each):
		ref	= tde4.createCamera("REF_FRAME")
		lens	= tde4.getCameraLens(cam)
		tde4.setCameraLens(ref,lens)
		path2	= tde4.getCameraFrameFilepath(cam,f)
		tde4.setCameraPath(ref,path2)
		w	= tde4.getCameraImageWidth(cam)
		tde4.setCameraImageWidth(ref,w)
		h	= tde4.getCameraImageHeight(cam)
		tde4.setCameraImageHeight(ref,h)		
		pgl	= tde4.getPGroupList(0)
		for pg in pgl:
			pl	= tde4.getPointList(pg,0)
			for p in pl:
				if tde4.isPointPos2DValid(pg,p,cam,f):
					v2d	= tde4.getPointPosition2D(pg,p,cam,f)
					tde4.setPointPosition2D(pg,p,ref,1,v2d)

cams = getSelectedSeqCams()
if cams:
	req	= createCustomRequester()
	addLabelWidget(req, "cams_amount", "Selected cameras: "+str(len(cams)), "ALIGN_LABEL_LEFT")
	addTextFieldWidget(req, "each_widget","Create each frame:", "10")
	act	= postCustomRequester(req,"Batch Reference Frame Creator Settings",550,0,"Ok","Cancel")
	if act == 1:
		each = int(getWidgetValue(req, "each_widget"))
		if each and each > 0:
			for cam in cams:			
				createRefFrames(cam, each)
else:
	postQuestionRequester("Error", "No sequence cameras selected.","Ok")

	