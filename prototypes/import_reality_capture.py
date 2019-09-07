# 3DE4.script.name:	Import Reality Capture Scene...
#
# 3DE4.script.version:	v1.0
#
# 3DE4.script.gui:	Main Window::3DE4::File::Import
#
# 3DE4.script.comment:	Reads in .csv files with Internal/External registration data.

from tde4 import *
from vl_sdv import *
import os


req	= createCustomRequester()
addFileWidget(req,"cameras_browser","Internal/External data...","*.csv")
addFileWidget(req,"images_browser","Image list...","*.imagelist")
addFileWidget(req,"points_browser","XYZ(RGB) pointcloud...","*.xyz")
ret	= postCustomRequester(req,"Import Reality Capture Scene...",700,0,"Ok","Cancel")

pg	= tde4.getCurrentPGroup()
if pg!=None:
	if ret==1:
		cameras_browser = getWidgetValue(req,"cameras_browser")
		images_browser = getWidgetValue(req,"images_browser")
		points_browser = getWidgetValue(req,"points_browser")
		if cameras_browser != None and images_browser != None:
			with open(cameras_browser,"r") as cams, open(images_browser,"r") as imgs:
				#sort camers 1,2,3....
				cams = cams.readlines()[1:]
				imgs = [x for y,x in sorted(zip(cams,imgs.readlines()))]
				cams = sorted(cams)
				#create cameras
				for cam, img in zip(cams, imgs):
					cam = cam[0:-2].split(",")
					img = img[0:-2]
					current_cam_id = createCamera("REF_FRAME")
					setCameraName(current_cam_id, str(cam[0]))
					setCameraPath(current_cam_id, "/BAS"+str(img)[2:].replace("\\","/"))
					setPGroupPosition3D(pg,current_cam_id,1,[float(cam[1])*(-1), float(cam[3]), float(cam[2])])
					x = float(cam[4])+90.0
					y = float(cam[5])*(-1)
					z = float(cam[6])-180.0
					rx = math.radians(x)
					ry = math.radians(y)
					rz = math.radians(z)
					rotmat = rot3d(rx, ry, rz, VL_APPLY_ZXY).mat().list()
					setPGroupRotation3D(pg,current_cam_id,1,rotmat)
					copyPGroupEditCurvesToFilteredCurves(pg,current_cam_id)	
		else:
			print("no path for cameras and(or) images")
		if points_browser != None:
			point_cloud = []
			with open(points_browser, "r") as points:
				for point in points.readlines():
					point_cloud.append(point[:-2].split(" "))
			model = create3DModel(pg,len(point_cloud))
			set3DModelSurveyFlag(pg,model,1)
			set3DModelName(pg,model,os.path.basename(points_browser))
			set3DModelRenderingFlags(pg,model,1,0,0)
			set3DModelHiddenLinesFlag(pg,model,0)
			set3DModelPerVertexColorsFlag(pg,model,1)
			for point in point_cloud:
				current_point = add3DModelVertex(pg,model,[float(point[0])*(-1),float(point[2]),float(point[1])])
				if len(point)>=6:
					set3DModelVertexColor(pg,model,current_point,float(point[3])/255.99,float(point[4])/255.99,float(point[5])/255.99,0.5)
	else:
		print("cancel pressed")
else:
	print("no PGroup")