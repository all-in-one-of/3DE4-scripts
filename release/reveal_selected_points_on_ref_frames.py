# 3DE4.script.name:	Reveal Selected Points On Ref Frames
# 3DE4.script.version:	v1.0
# 3DE4.script.comment: Revil selected points on all reference frames. Created by Jaffords 2017
# 3DE4.script.gui:	Object Browser::Edit
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Manual Tracking Controls::Edit

from tde4 import *

def sortCameras(camera_list):
	seq_cams, ref_cams = [],[]
	for cam_id in camera_list:
		if getCameraType(cam_id) == "SEQUENCE":
			seq_cams.append(cam_id)
		else:
			ref_cams.append(cam_id)
	return(seq_cams,ref_cams)


def getMatch(ref_cam, seq_cams):
	path_for_match = getCameraFrameFilepath(ref_cam,1)
	match = None
	for seq_cam in seq_cams:
		cam_attr = getCameraSequenceAttr(seq_cam)	#[<start>,<end>,<step>]	
		for frame in range(cam_attr[0],cam_attr[1],cam_attr[2]):
			if getCameraFrameFilepath(seq_cam,frame) == path_for_match:
				match = [seq_cam,frame]
				
	return(match)



def revealPointIfValid(point_group, point, ref_cam, match):
	if isPointPos2DValid(point_group, point, match[0], match[1]):
		position = getPointPosition2D(point_group, point, match[0], match[1])
		setPointPosition2D(point_group, point, ref_cam, 1, position)


point_group	= getCurrentPGroup()										#get current point group
if point_group!= None:
	point_list	= getPointList(point_group,1) 							#get selected points
	camera_list = getCameraList(0)										#get all cameras
	seq_cams, ref_cams = sortCameras(camera_list)						#sort cameras by type
	for ref_cam in ref_cams:
		match = getMatch(ref_cam, seq_cams)								#try to find refefence frame in sequence cameras
		if match != None:
			for point in point_list:
				revealPointIfValid(point_group, point, ref_cam, match)	#try to reveal point in referance frame

else:
	postQuestionRequester("Error", "There is no current Point Group.","Ok")