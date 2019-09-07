#
#
# 3DE4.script.name:	Align Point Based On Ref Frame Pattern
#
# 3DE4.script.version:	v1
#
# 3DE4.script.gui:	Manual Tracking Controls::Tracking
cam	= tde4.getCurrentCamera()
pg	= tde4.getCurrentPGroup()

if cam!=None and pg!=None:
	target_camera = getCurrentCamera()
	pattern_camera = getCameraList(1)[0]
	print("target_camera",getCameraName(target_camera))
	print("pattern_camera",getCameraName(pattern_camera))

	frame = getCurrentFrame(target_camera)
	print("frame",frame)
	point = getPointList(pg,1)[0]
	print("point",getPointName(pg,point))
	box = getPointTrackingBoxes2D(pg,point,pattern_camera,1)
	search_2d = getPointPosition2D(pg,point,pattern_camera,1)
	setGPUTrackEngineRefPattern(pattern_camera,1,search_2d,box[1],box[2],box[3])
	setGPUTrackEngineSearchArea(target_camera,frame,[0,0],[1,0],[1,1],[0,1])
	new_position = runGPUTrackEngineProcedure()
	print("Status",getGPUTrackEngineProcedureStatus())
	if new_position[0]!=-1.0:
		setPointPosition2D(pg,point,target_camera,frame,new_position)