#
#
# 3DE4.script.name:	Houdini...
#
# 3DE4.script.version:	v1.0
#
# 3DE4.script.gui:	Main Window::3DE4::Export Project
#
# 3DE4.script.comment:	Creates a Houdini python script file that contains all project data, which can be imported into Houdini.
#
#

#
# import sdv's python vector lib...

import math
#r1 Foundation compability
import sys
instpath	= tde4.get3DEInstallPath()
if not "%s/sys_data/py_vl_sdv"%instpath in sys.path:
	sys.path.append("%s/sys_data/py_vl_sdv"%instpath)

from vl_sdv import *

#
# functions...

def convertToAngles(r3d,yup):
	rot	= rot3d(mat3d(r3d)).angles(VL_APPLY_ZXY)
	rx	= rot[0]
	ry	= rot[1]
	rz	= rot[2]
	return(rx,ry,rz)
		
def convertCameraToAngles(r3d,yup):
	rot	= rot3d(mat3d(r3d)).angles(VL_APPLY_ZXY)
	rx	= rot[0]
	ry	= rot[1]
	rz	= rot[2]
	return(rx,ry,rz)

def convertZup(p3d,yup):
	return([p3d[0],p3d[1],p3d[2]])


def angleMod360(d0,d):
	dd	= d-d0
	if dd>3.141592654:
		d	= angleMod360(d0,d-3.141592654*2.0)
	else:
		if dd<-180.0:
			d	= angleMod360(d0,d+3.141592654*2.0)
	return d


def validName(name):
	name	= name.replace(" ","_")
	name	= name.replace("#","_")
	return name



#
# main script...
		

#
# search for camera point group...

campg	= None
pgl	= tde4.getPGroupList()
for pg in pgl:
	if tde4.getPGroupType(pg)=="CAMERA": campg = pg
if campg==None:
	tde4.postQuestionRequester("Export Houdini...","Error, there is no camera point group.","Ok")


#
# open requester...

req	= tde4.createCustomRequester()
tde4.addFileWidget(req,"file_browser","Exportfile...","*.py")
tde4.addTextFieldWidget(req, "startframe_field", "Startframe", "1")
#tde4.addOptionMenuWidget(req,"mode_menu","Orientation","Y-Up", "Z-Up")

cam	= tde4.getCurrentCamera()

#r1 Foundation compability
if "getCameraFrameOffset" in dir(tde4):
	offset	= tde4.getCameraFrameOffset(cam)
else:
	offset = 0
	
tde4.setWidgetValue(req,"startframe_field",str(offset))

ret	= tde4.postCustomRequester(req,"Export Houdini (Python-Script)...",540,130,"Ok","Cancel")
if ret==1:
	yup	= 0
	path	= tde4.getWidgetValue(req,"file_browser")
	frame0	= float(tde4.getWidgetValue(req,"startframe_field"))
	frame0	-= 2
	if path!=None:
		f	= open(path,"w")
		if not f.closed:
			
			#
			# write some comments...
			
			f.write("import hou\n")
			f.write("# \n")
			f.write("# Houdini export data written by %s\n"%tde4.get3DEVersion())
			f.write("#\n")
			f.write("# All lengths are in centimeter, all angles are in degree.\n")
			f.write("#\n\n")
			
			#
			# write scene group...
			
			
			f.write("# create scene group...\n")
			
 			f.write("EQ4Scene = hou.node('/obj').createNode('null','3DEScene')\n")
			#
			# write cameras...
			
			cl	= tde4.getCameraList()
			index	= 1
			for cam in cl:
				noframes	= tde4.getCameraNoFrames(cam)
				lens		= tde4.getCameraLens(cam)
				if lens!=None:
					name		= validName(tde4.getCameraName(cam))
					name		= "%s_%s_1"%(name,index)
					index		+= 1
					fback_w		= tde4.getLensFBackWidth(lens)*10.0
					fback_h		= tde4.getLensFBackHeight(lens)*10.0
					p_aspect	= tde4.getLensPixelAspect(lens)
					focal		= tde4.getCameraFocalLength(cam,1)
					imagew		= tde4.getCameraImageWidth(cam)
					imageh		= tde4.getCameraImageHeight(cam)
					fps = tde4.getCameraFPS(cam)
				
					# convert focal length to mm...
					focal		= focal*10.0
					
					# create scene...
					f.write("\n")
					f.write("# create scene ...\n")
					
					# create camera...
					f.write("\n")
					f.write("# create camera %s...\n"%name)
					f.write("cam = hou.node('/obj').createNode('cam','%s')\n"%name)
					f.write("paspect = cam.parm('aspect')\n")
					f.write("paspect.set(%.15f)\n"%p_aspect)
					f.write("fb_w = cam.parm('aperture')\n")
					f.write("fb_w.lock(False)\n")
					f.write("fb_w.set(%.15f)\n"%fback_w)
					f.write("fb_w.setAutoscope(False)\n")
					f.write("rot_order = cam.parm('rOrd')\n")
					f.write("rot_order.lock(False)\n")
					f.write("rot_order.set('zxy')\n")
					f.write("rot_order.setAutoscope(False)\n")
					
					f.write("image_res_tuple = cam.parmTuple('res')\n")
					f.write("image_res_tuple.lock((False, False))\n")
					f.write("image_res_tuple.set((%d, %d))\n"%(imagew,imageh))
					f.write("image_res_tuple.setAutoscope((False, False))\n")				
					
					f.write("lco = cam.parmTuple('win')\n")
					f.write("lco.set((%.15f,%.15f))\n"%(-tde4.getLensLensCenterX(lens)*10.0 / fback_w,-tde4.getLensLensCenterY(lens)*10.0/ fback_h))
#					f.write("cam.shift_x = %.15f\n"%(-tde4.getLensLensCenterX(lens)*10.0 / fback_w))
#					f.write("cam.shift_y = %.15f\n"%(-tde4.getLensLensCenterY(lens)*10.0 / fback_h * float(imageh)/float(imagew)))
					
					p3d	= tde4.getPGroupPosition3D(campg,cam,1)
					p3d	= convertZup(p3d,yup)
					r3d	= tde4.getPGroupRotation3D(campg,cam,1)
					rot	= convertCameraToAngles(r3d,yup)
					
					f.write("cam.setFirstInput(EQ4Scene)\n")
					# animate camera...
					
					f.write("rot_tuple = cam.parmTuple('r')\n")
					f.write("rot_tuple.lock((False, False, False))\n")
					f.write("rot_tuple.set((0, 0, 0))\n")
					f.write("rot_tuple.setAutoscope((True, True, True))\n")
					f.write("trans_tuple = cam.parmTuple('t')\n")
					f.write("trans_tuple.lock((False, False, False))\n")
					f.write("trans_tuple.set((0, 0, 0))\n")
					f.write("trans_tuple.setAutoscope((True, True, True))\n")
					f.write("focal = cam.parm('focal')\n")


					
					frame	= 1
					while frame<=(noframes):
						# rot/pos...
						p3d	= tde4.getPGroupPosition3D(campg,cam,frame)
						p3d	= convertZup(p3d,yup)
						r3d	= tde4.getPGroupRotation3D(campg,cam,frame)
						rot	= convertCameraToAngles(r3d,yup)

						if frame>1:
							rot	= [ angleMod360(rot0[0],rot[0]), angleMod360(rot0[1],rot[1]), angleMod360(rot0[2],rot[2]) ]
						rot0	= rot
												
						for i in range(0,3):
							f.write("hou_keyframe = hou.Keyframe()\n")
							f.write("hou_keyframe.setTime(%.15f)\n"%((frame+frame0)/fps))
							f.write("hou_keyframe.setValue(%.15f)\n"%p3d[i])
							f.write("hou_keyframe.setSlope(0)\n")
							f.write("hou_keyframe.setAccel(0.013888888888888888)\n")
							f.write("hou_keyframe.setInAccel(0.33333333333333331)\n")
							f.write("hou_keyframe.setExpression('bezier()', hou.exprLanguage.Hscript)\n")
							f.write("trans_tuple[%d].setKeyframe(hou_keyframe)\n"%i)
						
							f.write("hou_keyframe = hou.Keyframe()\n")
							f.write("hou_keyframe.setTime(%.15f)\n"%((frame+frame0)/fps))
							f.write("hou_keyframe.setValue(%.15f)\n"%(rot[i]*180.0/math.pi))
							f.write("hou_keyframe.setSlope(0)\n")
							f.write("hou_keyframe.setAccel(0.013888888888888888)\n")
							f.write("hou_keyframe.setInAccel(0.33333333333333331)\n")
							f.write("hou_keyframe.setExpression('bezier()', hou.exprLanguage.Hscript)\n")
							f.write("rot_tuple[%d].setKeyframe(hou_keyframe)\n"%i)
														
		
							# focal length...
						focal	= tde4.getCameraFocalLength(cam,frame)
						focal	= focal*10.0
	
						f.write("hou_keyframe = hou.Keyframe()\n")
						f.write("hou_keyframe.setTime(%.15f)\n"%((frame+frame0)/fps))
						f.write("hou_keyframe.setValue(%.15f)\n"%(focal))
						f.write("hou_keyframe.setSlope(0)\n")
						f.write("hou_keyframe.setAccel(0.013888888888888888)\n")
						f.write("hou_keyframe.setInAccel(0.33333333333333331)\n")
						f.write("hou_keyframe.setExpression('bezier()', hou.exprLanguage.Hscript)\n")
						f.write("focal.setKeyframe(hou_keyframe)\n")
						
										
						frame	+= 1
					
			#
			# write camera point group...
 			
 			f.write("\n")
 			f.write("# create camera point group...\n")
 			name	= "cameraPGroup_%s_1"%validName(tde4.getPGroupName(campg))
			f.write("pgHelper = hou.node('/obj').createNode('null','%s')\n"%name)
			f.write("pgHelper.setFirstInput(EQ4Scene)\n")
 			
 			# write points...
 			l	= tde4.getPointList(campg)
 			for p in l:
 				if tde4.isPointCalculated3D(campg,p):
 					name	= tde4.getPointName(campg,p)
 					name	= "p%s"%validName(name)
 					p3d	= tde4.getPointCalcPosition3D(campg,p)
 					p3d	= convertZup(p3d,yup)
 					f.write("point = hou.node('/obj').createNode('null','%s')\n"%name)
 					f.write("point.setFirstInput(pgHelper)\n")
					f.write("point_pos_tuple = point.parmTuple('t')\n")
					f.write("point_pos_tuple.set((%.15f, %.15f, %.15f))\n"%(p3d[0],p3d[1],p3d[2]))
			
 
 			
 			#
 			# write object point groups...
 			
 			camera		= tde4.getCurrentCamera()
 			noframes	= tde4.getCameraNoFrames(camera)
 			pgl		= tde4.getPGroupList()
 			index		= 1
 			for pg in pgl:
 				if tde4.getPGroupType(pg)=="OBJECT" and camera!=None:
 					f.write("\n")
 					f.write("# create object point group...\n")
 					pgname	= "objectPGroup_%s_%d_1"%(validName(tde4.getPGroupName(pg)),index)
 					index	+= 1
 					f.write("pgHelper_%s = hou.node('/obj').createNode('null','%s')\n"%(pgname,pgname))
 					
 					f.write("pgHelper_%s.setFirstInput(EQ4Scene)\n"%(pgname)) 
 					
 					# write points...
 					l	= tde4.getPointList(pg)
 					for p in l:
 						if tde4.isPointCalculated3D(pg,p):
 							name	= tde4.getPointName(pg,p)
 							name	= "p%s"%validName(name)
 							p3d	= tde4.getPointCalcPosition3D(pg,p)
 							p3d	= convertZup(p3d,yup)

 							f.write("point = hou.node('/obj').createNode('null','%s')\n"%(name))
 							f.write("point.setFirstInput(pgHelper_%s)\n"%(pgname)) 
 							#f.write("point.location = (%.15f,%.15f,%.15f) \n"%(p3d[0],p3d[1],p3d[2]))

							f.write("point_pos_tuple = point.parmTuple('t')\n")
							f.write("point_pos_tuple.set((%.15f, %.15f, %.15f))\n"%(p3d[0],p3d[1],p3d[2]))
 					
					f.write("\n")
 					scale	= tde4.getPGroupScale3D(pg)
 					f.write("pgHelper_scale = pgHelper_%s.parmTuple('s')\n"%(pgname))
 					f.write("pgHelper_scale.set((%.15f,%.15f,%.15f))\n"%(scale,scale,scale))
 
 					# animate object point group...
 					f.write("\n")
 					
 					f.write("rot_order = pgHelper_%s.parm('rOrd')\n"%pgname)
					f.write("rot_order.lock(False)\n")
					f.write("rot_order.set('zxy')\n")
					f.write("rot_order.setAutoscope(False)\n")
					f.write("pos_tuple = pgHelper_%s.parmTuple('t')\n"%pgname)
					f.write("rot_tuple = pgHelper_%s.parmTuple('r')\n"%pgname)
					
					frame	= 1
 					while frame<=noframes:
 						# rot/pos...
 						p3d	= tde4.getPGroupPosition3D(pg,camera,frame)
 						p3d	= convertZup(p3d,yup)
 						r3d	= tde4.getPGroupRotation3D(pg,camera,frame)
 						rot	= convertToAngles(r3d,yup)
 						if frame>1:
 							rot	= [ angleMod360(rot0[0],rot[0]), angleMod360(rot0[1],rot[1]), angleMod360(rot0[2],rot[2]) ]
 						rot0	= rot
 						
 						for i in range(0,3):
							f.write("hou_keyframe = hou.Keyframe()\n")
							f.write("hou_keyframe.setTime(%.15f)\n"%((frame+frame0)/fps))
							f.write("hou_keyframe.setValue(%.15f)\n"%p3d[i])
							f.write("hou_keyframe.setSlope(0)\n")
							f.write("hou_keyframe.setAccel(0.013888888888888888)\n")
							f.write("hou_keyframe.setInAccel(0.33333333333333331)\n")
							f.write("hou_keyframe.setExpression('bezier()', hou.exprLanguage.Hscript)\n")
							f.write("pos_tuple[%d].setKeyframe(hou_keyframe)\n"%i)
							
							f.write("hou_keyframe = hou.Keyframe()\n")
							f.write("hou_keyframe.setTime(%.15f)\n"%((frame+frame0)/fps))
							f.write("hou_keyframe.setValue(%.15f)\n"%(rot[i]*180.0/math.pi))
							f.write("hou_keyframe.setSlope(0)\n")
							f.write("hou_keyframe.setAccel(0.013888888888888888)\n")
							f.write("hou_keyframe.setInAccel(0.33333333333333331)\n")
							f.write("hou_keyframe.setExpression('bezier()', hou.exprLanguage.Hscript)\n")
							f.write("rot_tuple[%d].setKeyframe(hou_keyframe)\n"%i)
													 						
 						frame	+= 1
 			
 			
 			#
 			# global (scene node) transformation...
 			
 			p3d	= tde4.getScenePosition3D()
 			p3d	= convertZup(p3d,yup)
 			r3d	= tde4.getSceneRotation3D()
 			rot	= convertToAngles(r3d,yup)
 			s	= tde4.getSceneScale3D()
 			
 			f.write("scene_scale = EQ4Scene.parmTuple('s')\n")
 			f.write("scene_scale.set((%.15f,%.15f,%.15f))\n"%(s,s,s))
 			 
 			f.write("scene_pos = EQ4Scene.parmTuple('t')\n")
 			f.write("scene_pos.set((%.15f,%.15f,%.15f))\n"%(p3d[0],p3d[1],p3d[2]))
 			
 			f.write("rot_order = EQ4Scene.parm('rOrd')\n")
			f.write("rot_order.lock(False)\n")
			f.write("rot_order.set('zxy')\n")
			f.write("rot_order.setAutoscope(False)\n")
			f.write("scene_rot = EQ4Scene.parmTuple('r')\n")
 			f.write("scene_rot.set((%.15f,%.15f,%.15f))\n"%(rot[0]*180.0/math.pi,rot[1]*180.0/math.pi,rot[2]*180.0/math.pi))

			f.write("\n")
			f.close()
			tde4.postQuestionRequester("Export Houdini...","Project successfully exported.","Ok")
		else:
			tde4.postQuestionRequester("Export Houdini...","Error, couldn't open file.","Ok")


tde4.deleteCustomRequester(req)


