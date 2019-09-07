#
#
# 3DE4.script.name:	Import xyz pointcloud...
#
# 3DE4.script.version:	v1.3
#
# 3DE4.script.gui:	Main Window::3DE4::File::Import
# 3DE4.script.gui:	Orientation Controls::3D Models::Create
# 3DE4.script.gui:	Object Browser::Context Menu PGroup::Add New
# 3DE4.script.gui:	Object Browser::Context Menu 3D Models::Add New
# 3DE4.script.gui:	Object Browser::Context Menu 3D Model::Add New
#
# 3DE4.script.comment:	Reads in .xyz and .pts files.
#
# Version 1.2: Bugfix for files with more than 6 channels.

import os.path

#
# main script...

pg	= tde4.getCurrentPGroup()
scale_factor=10
if pg!=None:

	req	= tde4.createCustomRequester()
	tde4.addFileWidget(req,"file_browser","Filename...","*")
	tde4.addScaleWidget(req,"alpha_scale","Alpha Channel","DOUBLE",0.0,1.0,0.5)
	tde4.addOptionMenuWidget(req,"cframe","Coordinate Frame","Y Up","Z Up")
	tde4.setWidgetValue(req,"cframe","2")
	tde4.addOptionMenuWidget(req,"import","Import","All Points","Every 2nd Point","Every 10th Point")
		
	ret	= tde4.postCustomRequester(req,"Import Raw LIDAR Scan...",700,0,"Ok","Cancel")
	if ret==1:
		path	= tde4.getWidgetValue(req,"file_browser")
		if path!=None:
			size	= os.path.getsize(path)
			alpha	= tde4.getWidgetValue(req,"alpha_scale")
			imp	= tde4.getWidgetValue(req,"import")
			if imp==3: imp = 10
			zup	= tde4.getWidgetValue(req,"cframe")-1
			
			f	= open(path,"r")
			sline = []
			if not f.closed:
				vertices = []

				tde4.postProgressRequesterAndContinue("Import Raw LIDAR Scan...","Loading Data...",size/1000,"Cancel")
				count	= 0
				i	= 0
				ret	= -1
				
				for line in f:
					count	= count+len(line)
					i	= i+1
					if i==5000:
						ret	= tde4.updateProgressRequester(count/1000,"Loading Data...")
						if ret!=-1: break
						i	= 0
					
					if i%imp==0:
						sline2 = line.lstrip(", \t").split()
						if len(sline2) > 0 and sline2[-1] == '\\':
							sline += sline2[0:-1]
						else:
							sline += sline2
							l	= len(sline)
							if l == 3:
								if zup==1: 	vertices.append([float(sline[0])*scale_factor,float(sline[2])*scale_factor,-float(sline[1])*scale_factor,0.2,0.2,1.0])
								else:		vertices.append([float(sline[0])*scale_factor,float(sline[1])*scale_factor,float(sline[2])*scale_factor,0.2,0.2,1.0])
							if l >= 6:
								if zup==1: 	vertices.append([float(sline[0])*scale_factor,float(sline[2])*scale_factor,-float(sline[1])*scale_factor,float(sline[3+(l-6)])/255.99,float(sline[4+(l-6)])/255.99,float(sline[5+(l-6)])/255.99])
								else:		vertices.append([float(sline[0])*scale_factor,float(sline[1])*scale_factor,float(sline[2])*scale_factor,float(sline[3+(l-6)])/255.99,float(sline[4+(l-6)])/255.99,float(sline[5+(l-6)])/255.99])
							sline = []
				f.close()
				
				if ret==-1 and len(vertices)>0:
					tde4.postProgressRequesterAndContinue("Import Raw LIDAR Scan...","Processing Data...",len(vertices),"Cancel")				
					model = tde4.create3DModel(pg,len(vertices))
					tde4.set3DModelSurveyFlag(pg,model,1)
					tde4.set3DModelName(pg,model,os.path.basename(path))
					tde4.set3DModelRenderingFlags(pg,model,1,0,0)
					tde4.set3DModelHiddenLinesFlag(pg,model,0)
					v	= vertices[0]
					if v[3]!=0.2 or v[4]!=0.2 or v[5]!=1.0: tde4.set3DModelPerVertexColorsFlag(pg,model,1)
					
					for v in vertices:
						i	= tde4.add3DModelVertex(pg,model,[v[0],v[1],v[2]])
						tde4.set3DModelVertexColor(pg,model,i,v[3],v[4],v[5],alpha)
						if i%5000==0:
							ret	= tde4.updateProgressRequester(i,"Processing Data...")
							if ret!=-1: break
					
				tde4.unpostProgressRequester()
				del vertices
			else:
				tde4.postQuestionRequester("Import Raw LIDAR Scan...","Error, couldn't open file.","Ok")
	
	tde4.deleteCustomRequester(req)
else:
	tde4.postQuestionRequester("Import Raw LIDAR Scan...","There is no current Point Group.","Ok")


