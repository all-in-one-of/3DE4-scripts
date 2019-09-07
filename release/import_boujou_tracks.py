# 3DE4.script.name:	Import Boujou Tracks...
# 3DE4.script.version:	v1
# 3DE4.script.gui:	Main Window::3DE4::File::Import
# 3DE4.script.gui:	Object Browser::Context Menu Point
# 3DE4.script.gui:	Object Browser::Context Menu Points
# 3DE4.script.gui:	Object Browser::Context Menu PGroup

		
c	= tde4.getCurrentCamera()
pg	= tde4.getCurrentPGroup()
print("begin")
if c!=None and pg!=None:
	frames	= tde4.getCameraNoFrames(c)
	width	= tde4.getCameraImageWidth(c)
	height	= tde4.getCameraImageHeight(c)	
	req	= tde4.createCustomRequester()
	tde4.addFileWidget(req,"file_browser","Filename...","*.txt")
	tde4.addTextFieldWidget(req, "offset", "Frame Offset", "0")
	tde4.addTextFieldWidget(req, "width", "Tracked Width", str(width))
	tde4.addTextFieldWidget(req, "height", "Tracked Height", str(height))
	ret	= tde4.postCustomRequester(req,"Import Boujou Tracks...",500,170,"Ok","Cancel")
	if ret==1:
		path	= tde4.getWidgetValue(req,"file_browser")
		offset = int(tde4.getWidgetValue(req,"offset"))
		width = int(tde4.getWidgetValue(req,"width"))
		height = int(tde4.getWidgetValue(req,"height"))
		if path!=None:
			print("start")
			with open(path,"r") as f:
				rows = f.readlines()
				point_name = None
				point = None
				t_curve = []
				for row in rows:
					print(row)
					if not "#" in row:
						row = row[:-1].split("  ")
						#print(row)
						if point_name != row[0] or point_name == None:
							if point_name != None:
								print("c",point_name, t_curve)
								tde4.setPointPosition2DBlock(pg, point, c, 1, t_curve)
							point_name = row[0]
							point = tde4.createPoint(pg)
							tde4.setPointName(pg, point, point_name)
							print("Create point:",point_name)
							t_curve = []
							for i in range(frames): t_curve.append([-1.0,-1.0])
						place = int(row[1])-1+offset
						if place >= 0 and place < frames:
							t_curve[place] = [float(row[2])/width, (height-float(row[3]))/height]		
				print("e",point_name, t_curve)
				tde4.setPointPosition2DBlock(pg, point, c, 1, t_curve)

		else:
			print("wrong path")
	else:
		print("canceled")
else:
	tde4.postQuestionRequester("Import 2D Tracks...","There is no current Point Group or Camera.","Ok")