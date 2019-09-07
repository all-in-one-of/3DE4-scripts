# 3DE4.script.name:	Export Nuke tracker...
# 3DE4.script.version:	v1
# 3DE4.script.comment: Created by Jaffords 2017
# 3DE4.script.gui:	Main Window::3DE4::File::Export
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.comment:	Writes selected 2D trackers to a Nuke tracker node.
# 3DE4.script.hide: false
# 3DE4.script.startup: false


trackerNode = ""


def createTrackerNode(c,pg,pl):
	global trackerNode
	n	= tde4.getCameraNoFrames(c)
	width	= tde4.getCameraImageWidth(c)
	height	= tde4.getCameraImageHeight(c)
	trackerNode = ("set cut_paste_input [stack 0]\n")
	trackerNode += ("version 10.5 v4\n")
	trackerNode += ("push $cut_paste_input\n")
	trackerNode += ("Tracker4 {\n")
	trackerNode += ("tracks { { 1 31 " + str(len(pl))+" }\n")  #count points
	trackerNode += ("""{ { 5 1 20 enable e 1 } { 3 1 75 name name 1 } { 2 1 58 track_x track_x 1 } 
		{ 2 1 58 track_y track_y 1 } { 2 1 63 offset_x offset_x 1 } { 2 1 63 offset_y offset_y 1 } 
		{ 4 1 27 T T 1 } { 4 1 27 R R 1 } { 4 1 27 S S 1 } { 2 0 45 error error 1 } 
		{ 1 1 0 error_min error_min 1 } { 1 1 0 error_max error_max 1 } 
		{ 1 1 0 pattern_x pattern_x 1 } { 1 1 0 pattern_y pattern_y 1 } 
		{ 1 1 0 pattern_r pattern_r 1 } { 1 1 0 pattern_t pattern_t 1 } 
		{ 1 1 0 search_x search_x 1 } { 1 1 0 search_y search_y 1 } 
		{ 1 1 0 search_r search_r 1 } { 1 1 0 search_t search_t 1 } 
		{ 2 1 0 key_track key_track 1 } { 2 1 0 key_search_x key_search_x 1 } 
		{ 2 1 0 key_search_y key_search_y 1 } { 2 1 0 key_search_r key_search_r 1 } 
		{ 2 1 0 key_search_t key_search_t 1 } { 2 1 0 key_track_x key_track_x 1 } 
		{ 2 1 0 key_track_y key_track_y 1 } { 2 1 0 key_track_r key_track_r 1 } 
		{ 2 1 0 key_track_t key_track_t 1 } { 2 1 0 key_centre_offset_x key_centre_offset_x 1 } 
		{ 2 1 0 key_centre_offset_y key_centre_offset_y 1 } }\n""")
	trackerNode += ("{\n")# start points block
	for point in pl:
		trackerNode += ("{ {1}\n")
		trackerNode += (str(tde4.getPointName(pg,point)) +" {curve\n")
		c2d	= tde4.getPointPosition2DBlock(pg,point,c,1,n)
		# write x
		frame	= 1
		for v in c2d:
			if tde4.isPointPos2DValid(pg,point,c,frame)==1:trackerNode += ("x%d %.6f\n"%( frame, v[0]*width ) )
			frame	+= 1
		trackerNode += ("}\n")
		trackerNode += ("{curve\n")
		# write y
		frame	= 1
		for v in c2d:
			if tde4.isPointPos2DValid(pg,point,c,frame)==1: trackerNode += ("x%d %.6f\n"%( frame, v[1]*height ) )
			frame	+= 1
		trackerNode += ("}\n")
		trackerNode += ("{0} {0} 0 0 0 {0} 1 0 -60 -60 60 60 -42 -42 42 42 {} {} {} {} {} {} {} {} {} {} {}\n")
		trackerNode += ("}\n")
	trackerNode += ("}}\n")
	trackerNode += ("name Trackers_3DE4_1\n")
	trackerNode += ("selected true\n")
	trackerNode += ("}\n")


def copyToClipboard(requester,widget,action):
	global trackerNode
	tde4.setClipboardString(trackerNode)


def saveNukeFile(requester,widget,action):
	global trackerNode
	path	= tde4.postFileRequester("Export Multiple Tracks To Nuke...","*.nk")
	if path!=None:
		if path[-3:] != ".nk":
			path = path+".nk"
		f	= open(path,"w")
	if not f.closed:
		f.write(trackerNode)
		f.close()
	else:
		tde4.postQuestionRequester("Export Multiple Tracks To Nuke...","Error, couldn't open file.","Ok")


c	= tde4.getCurrentCamera()
pg	= tde4.getCurrentPGroup()
if c!=None and pg!=None:
	pl	= tde4.getPointList(pg,1)
	if len(pl)>0:		
		createTrackerNode(c,pg,pl)
		window = tde4.createCustomRequester()
		tde4.addButtonWidget(window, "copyToClipboard", "Copy To Clipboard", 150, 10)
		tde4.setWidgetCallbackFunction(window, "copyToClipboard", "copyToClipboard")
		tde4.addButtonWidget(window, "saveNukeFile", "Save .nk", 80, 10, "copyToClipboard")
		tde4.setWidgetCallbackFunction(window, "saveNukeFile", "saveNukeFile")
		tde4.postCustomRequester(window, "Export Multiple Tracks To Nuke...", 280, 60, "Close")		
	else:
		tde4.postQuestionRequester("Export Multiple Tracks To Nuke...","Error, no points selected.","Ok")
else:
	tde4.postQuestionRequester("Export Multiple Tracks To Nuke...","There is no current Point Group or Camera.","Ok")