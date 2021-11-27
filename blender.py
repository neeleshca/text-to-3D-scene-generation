#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 14:44:29 2017

@author: ninaad
"""
import random
import bpy
import sys  
import os
import math
#from nltk.corpus import wordnet
from operator import itemgetter
fp=open("check","w")
fp1=open("check1","w")
fp2=open("check2","w")
fp3=open("check3","w")
fp4=open("check4","w")
listofobjectsplaced=[]


def createzone(prepobj,pos1,pos2,dim1,dim2):
    
    listofloc=[]
    if(prepobj=='right'):
        y=pos1[1]+dim1[2]/2+dim2[2]/2+0.1
        while(y<=8):
            x=-8
            while(x<=8):
                listofloc.append([x,y])
                x+=0.1
            y+=0.1
            
    elif(prepobj=='left'):
        #fp4.write(str(pos1[1])+"  "+str(dim1[2])+"  "+str(dim2[2])+"  \n")
        y=pos1[1]-dim1[2]/2-dim2[2]/2-0.1
        #fp4.write("THe value of y "+str(y))
        #fp4.write("\n")
        while(y>=-8):
            x=-8
            while(x<=8):
                listofloc.append([x,y])
                x+=0.1
            y-=0.1
    if(prepobj=='front'):
        #fp4.write(str(pos1[0])+"  "+str(dim1[0])+"  "+str(dim2[0])+" \n")
        x=pos1[0]+dim1[0]/2+dim2[0]/2+0.1
        #fp4.write("THe value of x "+str(x))
        fp4.write("\n")
        while(x<=8):
            y=-8
            while(y<=8):
                listofloc.append([x,y])
                y+=0.1
            x+=0.1
            
    if(prepobj=='back'):
        x=pos1[0]-dim1[0]/2-dim2[0]/2-0.1
        while(x>=-8):
            y=-8
            while(y<=8):
                listofloc.append([x,y])
                y+=0.1
            x-=0.1
            
    if(prepobj in ['0','on','next','beside']):
        x=-8
        while(x<=8):
            y=-8
            while(y<=8):
                listofloc.append([x,y])
                y+=0.1
            x+=0.1
    
    
    return listofloc   

def distancematrix(pos1,listofloc):
    x=pos1[0]
    y=pos1[1]
    for i in range(len(listofloc)):
        listofloc[i].append(((x-listofloc[i][0])**2+(y-listofloc[i][1])**2)**0.5)
        
    listofloc=sorted(listofloc, key=itemgetter(2))    
    return listofloc
def distancematrixline(pos1,listofloc,wrtobj):
    if(wrtobj=="right_wall"):
        y=7.87
        for i in range(len(listofloc)):
            listofloc[i].append(abs(y-listofloc[i][1]))    
    if(wrtobj=="left_wall"):
        y=-7.87
        for i in range(len(listofloc)):
            listofloc[i].append(abs(y-listofloc[i][1]))   
    if(wrtobj=="front_wall"):
        x=-7.87
        for i in range(len(listofloc)):
            listofloc[i].append(abs(x-listofloc[i][0]))
    random.shuffle(listofloc)
    listofloc=sorted(listofloc, key=itemgetter(2))   
 
    return listofloc   
def checkcollission(objname,x,y,z,xpos,ypos,zpos):
    xaxis=0
    yaxis=0
    zaxis=0
    y,z=z,y
    for i4 in range(len(listofobjectsplaced)):
        tempx=x
        tempy=y
        tempz=z
        tempxpos=xpos
        tempypos=ypos
        tempzpos=zpos
        
        xaxis=0
        yaxis=0
        zaxis=0
        pos=listofobjectsplaced[i4][2]
        dim=listofobjectsplaced[i4][1]
        x1=pos[0]
        x2=dim[0]
        
        y1=pos[1]
        y2=dim[2]
        
        z1=pos[2]
        z2=dim[1]
        #print(type(x1),type(x2),type(xpos),type(x))
        if( (x1-x2/2)<tempxpos<(x1+x2/2) or (x1-x2/2)<(tempxpos+tempx/2)-0.00001<(x1+x2/2) or (x1-x2/2)<(tempxpos-tempx/2)+0.00001<(x1+x2/2)):
           xaxis=1
        if(((y1-y2/2)<tempypos<(y1+y2/2)) or ((y1-y2/2)<(tempypos+tempy/2)-0.00001<(y1+y2/2)) or ((y1-y2/2)<(tempypos-tempy/2)+0.00001<(y1+y2/2))):
            yaxis=1     
        if((z1-z2/2)<tempzpos<(z1+z2/2) or (z1-z2/2)<(tempzpos+tempz/2)-0.00001<(z1+z2/2) or (z1-z2/2)<(tempzpos-tempz/2)+0.00001<(z1+z2/2)):
            zaxis=1

        pos=listofobjectsplaced[i4][2]
        dim=listofobjectsplaced[i4][1]
        x1=pos[0]
        x2=dim[0]
        
        y1=pos[1]
        y2=dim[2]
        
        z1=pos[2]
        z2=dim[1]
        
        x1,tempxpos=tempxpos,x1
        x2,tempx=tempx,x2
        
        y1,tempypos=tempypos,y1
        y2,tempy=tempy,y2
        
        z1,tempzpos=tempzpos,z1
        z2,tempz=tempz,z2
        
        
        if( (x1-x2/2)<tempxpos<(x1+x2/2) or (x1-x2/2)<(tempxpos+tempx/2)-0.00001<(x1+x2/2) or (x1-x2/2)<(tempxpos-tempx/2)+0.00001<(x1+x2/2)):
            xaxis=1
        if(((y1-y2/2)<tempypos<(y1+y2/2)) or ((y1-y2/2)<(tempypos+tempy/2)-0.00001<(y1+y2/2)) or ((y1-y2/2)<(tempypos-tempy/2)+0.00001<(y1+y2/2))):
            yaxis=1
        if((z1-z2/2)<tempzpos<(z1+z2/2) or (z1-z2/2)<(tempzpos+tempz/2)-0.00001<(z1+z2/2) or (z1-z2/2)<(tempzpos-tempz/2)+0.00001<(z1+z2/2)):
            zaxis=1
        if(xaxis==1 and yaxis==1 and zaxis==1):
            '''
            fp1.write(str(x)+"  "+str(y)+"  "+str(z)+"  "+str(xpos)+"  "+str(ypos)+"  "+str(zpos)+"  ")
            fp1.write(objname)
            fp1.write(" ")
            fp1.write(str(sum(x.count(objname) for x in listofobjectsplaced)))
            fp1.write(" ")
            fp1.write(listofobjectsplaced[i4][0])
            fp1.write("\n")
            '''
            return 0
    return 1    
            
            
            
def checkbounds(objname,x,y,z,xpos,ypos,zpos):
    fw=0
    rw=0
    lw=0
    ow=0
    floor=0
    ceiling=0
    #fp2.write(str(y)+" "+str(z)+"\n")
    if(xpos-x/2<-7.87888+(0.207)/2):   
        fw=1
        #fp2.write(str(xpos)+"  "+str(x)+"  ")
        #fp2.write(objname)
        #fp2.write(" Front Wall \n")
        return 0
    if(xpos+x/2>+7.87888+(0.207)/2):
        ow=1
        #fp2.write(objname)
        #fp2.write(" Open Wall \n")
        return 0
    if(ypos+z/2>7.87):
        rw=1
        #fp2.write(str(ypos)+"  "+str(z)+"  ")
        #fp2.write(objname)
        #fp2.write(" Right Wall \n")
        return 0
    if(ypos-z/2<-7.87):
        lw=1
        #fp2.write(objname)
        #fp2.write(" Left Wall \n")
        return 0
    return 1                 
  
with open('testoutput') as f:
    content = f.readlines()
listoffullids=[]
impliedloc=[]
synid=[]
scalel=[]
dir='ShapeNetCore.v1/'
for i in content:
    
    aposflag=0
    syn=''
    full=''
    implied=''
    scale=''
    for j in i:
        if(j=="'"):
            aposflag+=1
        if(aposflag==3):
            implied+=j
        if(aposflag==5):
            syn+=j
        if(aposflag==7):
            full+=j
        if(aposflag==9):
            scale+=j
    fp3.write(str(scale))
    syn=syn[1:]
    syn='0'+syn
    synid.append(syn)
    #print("SYN IS ",syn)
    full=full[1:]
    listoffullids.append(full)
    implied=implied[1:]
    impliedloc.append(implied) 
    scale=scale[1:]
    fp4.write(str(scale))
    scalel.append(scale)
    #print("FULL IS ",full)       
    full_path=dir+'/'+syn+'/'+full+'/'+'model.obj'
    
    
    output_path='Output'
    bpy.ops.import_scene.obj(filepath=full_path)

    obj_objects = bpy.context.selected_objects[:]

    for obj in obj_objects:
	    #print("\n\n\n\nioqej\n\n\n",full_path_to_file1)
	    bpy.context.scene.objects.active = obj
	    bpy.ops.object.select_all(action='SELECT')
	    bpy.ops.object.join()
       
	    bpy.ops.export_scene.obj(
	                filepath=os.path.join(output_path, full + '.obj'),
	                use_selection=True)
		                
	    bpy.ops.object.delete()
	    break
 
 
 


scene = bpy.context.scene

# Create new lamp datablock
lamp_data = bpy.data.lamps.new(name="New Lamp", type='POINT')

# Create new object with our lamp datablock
lamp_object = bpy.data.objects.new(name="New Lamp", object_data=lamp_data)

# Link lamp object to the scene so it'll appear in this scene
scene.objects.link(lamp_object)

# Place lamp to a specified location
lamp_object.location = (0, 0, 8.0)

# And finally select it make active
lamp_object.select = True
scene.objects.active = lamp_object
with open('example1') as f:
    contentofsyn = f.readlines()
    
fp=open('testoutput1','w')   
flagsyn=0

for i in contentofsyn:
    s=''
    print("Value of i is",i)
    for j in i: 
        if(j!="\n"): 
            s+=j
    
    if(s[-1:]!=' '):
        s+=' '
    for j in synid[flagsyn]:
        if(j!="\n"): 
            s+=j    
    
    if(s[-1:]!=' '):
        s+=' '
    for j in listoffullids[flagsyn]:
        if(j!="\n"): 
            s+=j
    if(s[-1]!=' '):
        s+=' '
    for j in impliedloc[flagsyn]:
        if(j!="\n"):
            s+=j
    if(s[-1]!=' '):
        s+=' '
    for j in scalel[flagsyn]:
        if(j!="\n"):
            s+=j
    #print("Value of s is",s)
    fp.write(s)    
    fp.write("\n")
    fp4.write(s)
    fp4.write("\n")
    flagsyn+=1
    

fp.close()












full_path_to_file = "room.obj"
bpy.ops.import_scene.obj(filepath=full_path_to_file)

# make sure to get all imported objects
obj_objects = bpy.context.selected_objects[:]

# iterate through all objects
for obj in obj_objects:

    
    xroom=bpy.data.objects[obj.name].dimensions.x
    yroom=bpy.data.objects[obj.name].dimensions.y
    zroom=bpy.data.objects[obj.name].dimensions.z

    xfloor=16
    yfloor=0.207
    zfloor=16
    xswall=16
    yswall=8
    zswall=0.207
    xfwall=0.207   
    yfwall=8
    zfwall=16
    
	# set current object to the active one
    bpy.context.scene.objects.active = obj
     
    # move the object, if it's named "Cube"
    obj.location = (0,0,0)









with open('testoutput1') as f:
    content = f.readlines()

listofobjectsplaced.append(["floor",[xfloor,yfloor,zfloor],[0,0,0,]])
listofobjectsplaced.append(["right_wall",[xswall,yswall,zswall],[0,8.00078,4]])
listofobjectsplaced.append(["left_wall",[xswall,yswall,zswall],[0,-8.00078,4]])
listofobjectsplaced.append(["front_wall",[xfwall,yfwall,zfwall],[-7.87888,0,4]])

temp_dir="Output"
for i in content:
    
    print("Value of i is ",i)
    l=[]
    s=''
    
    i1=i[0:-1]
    i1+=' '
    for j in i1:
        
        if(j!=' '):
            s+=j
        else:
            
            l.append(s)
            s=''
    objname=l[0]
    temp=l[1]
    prepobj=l[2]
    wrtobj=l[3]
    synidobj=l[4]   
    idofobj=l[5]
    implicitloc=l[6]
    scale=l[7]
    fp4.write(str(s))
    objplacement=[]
    listofloc=[]
    pos1=[0,0,0]
    pos2=[0,0,0]
    dim1=[0,0,0]
    dim2=[0,0,0]
    #print(objname,temp,prepobj,wrtobj,synidobj,idofobj,implicitloc)
    #print("\n")
    #print("Hell World")
    
    
    
    full_dir=temp_dir+'/'+idofobj+'.obj'
    #print("Full_dir is ",full_dir)
    
    xpos=0
    ypos=0
    zpos=0
    
    #if(implicitloc=="right_wall"  
    
                
    bpy.ops.import_scene.obj(filepath=full_dir)

    # make sure to get all imported objects
    obj_objects = bpy.context.selected_objects[:]
    x1=1
    y1=1
    z1=1
    fp4.write("Type of scale is "+str(type(scale))+"\n")
    scale=int(scale)
    x1=scale
    y1=scale
    z1=scale
    fp4.write("\n"+str(x1)+" "+str(y1)+" "+str(z1)+" "+str(type(x1))+"\n")

    # iterate through all objects
    for obj in obj_objects:
        if(implicitloc=="ceiling"):
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        
            
        obj.scale=((x1,y1,z1))
        x=bpy.data.objects[obj.name].dimensions.x
        y=bpy.data.objects[obj.name].dimensions.y
        z=bpy.data.objects[obj.name].dimensions.z
        x=x*x1
        y=y*y1
        z=z*z1
        
        
        
        #fp.write("XYZ\n")
        #fp.write(str(x)+"  "+str(y)+"  "+str(z)+ "  "+prepobj+"\n")
         #  x,z=z,y
        if(implicitloc=="table" and prepobj=='0' and wrtobj=='0'):
            fp4.write("TABLE")
            prepobj='on'
            wrtobj='table'
         
        if(implicitloc=='right_wall' and "clock" not in objname):
            if(prepobj=='0'):
                prepobj='front'
                wrtobj='right_wall'
            if(wrtobj=='wall'):
                prepobj='front'
                wrtobj='right_wall'
            if(wrtobj=='0' or wrtobj=="right_wall"):
                obj.rotation_euler=(90*(math.pi/180),0,-90*(math.pi/180))
            if(wrtobj=="left_wall"):
                obj.rotation_euler=(90*(math.pi/180),0,90*(math.pi/180))
            
        if(prepobj=="front" and implicitloc=="right_wall"):
            if(wrtobj=="left_wall"):
                prepobj="right"
            if(wrtobj=="right_wall"):
                prepobj="left"
            if(wrtobj=="front_wall"):
                prepobj="front" 
            
         
        if(wrtobj in ["right_wall","left_wall"]):     
            x,z=z,x
            
            
        for i4 in range(len(listofobjectsplaced)):
            if(implicitloc in listofobjectsplaced[i4]):
                
                pos2=listofobjectsplaced[i4][2]
                dim2=listofobjectsplaced[i4][1]
                print("Implicit Object",pos2,dim2)
                if(implicitloc in ["right_wall","left_wall","front_wall"]):
                    pos2[2]=0
                    dim2[1]=0
        for i5 in range(len(listofobjectsplaced)):
            if(wrtobj in listofobjectsplaced[i5]):
                pos1=listofobjectsplaced[i5][2]
                dim1=listofobjectsplaced[i5][1]        
        if(wrtobj=="left_wall"):
            pos1=[0,-8.00078,0]

            
        if(wrtobj=="right_wall"):
            pos1=[0,8.00078,0]
            
        if(wrtobj=="front_wall"):
            pos1=[-7.87888,0,0]
        
       
        
                   
        #if(implicitloc=='floor' and prepobj=='0' and wrtobj=='0'):
         #   prepobj='floor'
        #    wrtobj='on'
       
        listofloc=createzone(prepobj,pos1,pos2,dim1,[x,y,z])
        #fp3.write("\nLISTOFLOC\n")
        #fp3.write(str(listofloc))
        #fp3.write("\n\n")
        #fp.write("\n\n\n\n")
        if(wrtobj in ["right_wall","left_wall","front_wall"]):
            objplacement=distancematrixline(pos1,listofloc,wrtobj)
        else:
            objplacement=distancematrix(pos1,listofloc)
        #fp.write(str(pos1))
        #fp.write("\n\n\n")
            
        
        if(objname=="clock"):
            if(wrtobj=='0' or wrtobj=="right_wall"):
                obj.rotation_euler=(90*(math.pi/180),0,-90*(math.pi/180))
                obj.location=(0,7.72,6)
                break
            if(wrtobj=="left_wall"):
                obj.rotation_euler=(90*(math.pi/180),0,90*(math.pi/180))
                obj.location=(0,-7.92,6)
                break
            if(wrtobj=="front_wall"):
                obj.location=(-7.74278,0,6)
                break    
        if(wrtobj in ["left_wall","right_wall","front_wall"]):
            #fp4.write("HGAPPY vARIABLE")
            prepobj='on'
            wrtobj='floor'   
		#elif(wrtobj in ["right_wall","left_wall","front_wall"]):
            #if(wrtobj=="right_wall"
        #fp1.write(prepobj+"\n\n\n\n\n\n")
        #fp1.write(wrtobj+"\n\n\n\n\n")         
        if((prepobj=='0' and wrtobj=='0') and implicitloc=='floor'):
            xpos=pos1[0]
            ypos=(dim1[2]+z)/2+pos1[1]
            zpos=(y+dim2[1])/2+pos1[2]
            #fp1.write(str(objplacement))
            if((checkcollission(objname,x,y,z,xpos,ypos,zpos)==1) and (checkbounds(objname,x,y,z,xpos,ypos,zpos)==1)):
                    obj.location=(xpos,ypos,zpos)
            else:
                for i in objplacement:
                    xpos=i[0]
                    ypos=i[1]
                    if((checkcollission(objname,x,y,z,xpos,ypos,zpos)==1) and (checkbounds(objname,x,y,z,xpos,ypos,zpos)==1)):
                        obj.location=(xpos,ypos,zpos)
                        break
           
           
            listofobjectsplaced.append([objname,[x,y,z],[xpos,ypos,zpos],sum(x.count(objname) for x in listofobjectsplaced)])   
                
        elif(implicitloc=="ceiling"):
            xpos=0
            ypos=0
            zpos=8-y+0.2
            
            if((checkcollission(objname,x,y,z,xpos,ypos,zpos)==1) and (checkbounds(objname,x,y,z,xpos,ypos,zpos)==1)):
                    obj.location=(xpos,ypos,zpos)
            else:
                for i in objplacement:
                    xpos=i[0]
                    ypos=i[1]
                    if((checkcollission(objname,x,y,z,xpos,ypos,zpos)==1) and (checkbounds(objname,x,y,z,xpos,ypos,zpos)==1)):
                        obj.location=(xpos,ypos,zpos)
                        break
           
           
            listofobjectsplaced.append([objname,[x,y,z],[xpos,ypos,zpos],sum(x.count(objname) for x in listofobjectsplaced)])
                  
        elif(prepobj in ['next','right','beside']):
            xpos=pos1[0]
            ypos=(dim1[2]+z)/2+pos1[1]
            zpos=(y+dim2[1])/2+pos2[2]
            
            if((checkcollission(objname,x,y,z,xpos,ypos,zpos)==1) and (checkbounds(objname,x,y,z,xpos,ypos,zpos)==1)):
                    obj.location=(xpos,ypos,zpos)
            else:
                for i in objplacement:
                    xpos=i[0]
                    ypos=i[1]
                    if((checkcollission(objname,x,y,z,xpos,ypos,zpos)==1) and (checkbounds(objname,x,y,z,xpos,ypos,zpos)==1)):
                        obj.location=(xpos,ypos,zpos)
                        break
           
            listofobjectsplaced.append([objname,[x,y,z],[xpos,ypos,zpos],sum(x.count(objname) for x in listofobjectsplaced)])
                 
        elif(prepobj == 'left'):
            
            xpos=pos1[0]
            ypos=-(dim1[2]+z)/2+pos1[1]
            zpos=(y+dim2[1])/2+pos2[2]
            #fp1.write("Inside left\n")
            #fp1.write(str(zpos))
            #fp.write(str(objplacement))
            if((checkcollission(objname,x,y,z,xpos,ypos,zpos)==1) and (checkbounds(objname,x,y,z,xpos,ypos,zpos)==1)):
                    obj.location=(xpos,ypos,zpos)
            else:
                for i in objplacement:
                    xpos=i[0]
                    ypos=i[1]
                    if((checkcollission(objname,x,y,z,xpos,ypos,zpos)==1) and (checkbounds(objname,x,y,z,xpos,ypos,zpos)==1)):
                        obj.location=(xpos,ypos,zpos)
                        break
            
            listofobjectsplaced.append([objname,[x,y,z],[xpos,ypos,zpos],sum(x.count(objname) for x in listofobjectsplaced)])
            break
                      
              
        elif(prepobj == 'front'):
           # fp.write("IN FRONT")
            xpos=(dim1[0]+x)/2+pos1[0]
            ypos=pos1[1]
            zpos=(y+dim2[1])/2+pos2[2]
            #fp.write("\n\n\nOBJPLACEMENT\n\n\n")
            #fp.write(str(objplacement))
            if((checkcollission(objname,x,y,z,xpos,ypos,zpos)==1) and (checkbounds(objname,x,y,z,xpos,ypos,zpos)==1)):
                    obj.location=(xpos,ypos,zpos)
            else:
                for i in objplacement:
                    xpos=i[0]
                    ypos=i[1]
                    if((checkcollission(objname,x,y,z,xpos,ypos,zpos)==1) and (checkbounds(objname,x,y,z,xpos,ypos,zpos)==1)):
                        obj.location=(xpos,ypos,zpos)
                        break
            
            listofobjectsplaced.append([objname,[x,y,z],[xpos,ypos,zpos],sum(x.count(objname) for x in listofobjectsplaced)])
            break
  
        elif(prepobj in ['back','behind']):
            
            xpos=-(dim1[0]+x)/2+pos1[0]
            ypos=pos1[1]
            zpos=(y+dim2[1])/2+pos2[2]
            if((checkcollission(objname,x,y,z,xpos,ypos,zpos)==1) and (checkbounds(objname,x,y,z,xpos,ypos,zpos)==1)):
                    obj.location=(xpos,ypos,zpos)
            else:
                for i in objplacement:
                    xpos=i[0]
                    ypos=i[1]
                    if((checkcollission(objname,x,y,z,xpos,ypos,zpos)==1) and (checkbounds(objname,x,y,z,xpos,ypos,zpos)==1)):
                        obj.location=(xpos,ypos,zpos)
                        break
            
            listofobjectsplaced.append([objname,[x,y,z],[xpos,ypos,zpos],sum(x.count(objname) for x in listofobjectsplaced)])
            break
        elif(prepobj in ['on']):
            #fp1.write("IN ON")
            xpos=pos1[0]
            ypos=pos1[1]
            zpos=(y+dim1[1])/2+pos1[2]
            #fp1.write("qwewqeasdasf eryrbytdryyn")
            if(implicitloc=="right_wall"):
                zpos=(y+yfloor)/2
            
            if((checkcollission(objname,x,y,z,xpos,ypos,zpos)==1) and (checkbounds(objname,x,y,z,xpos,ypos,zpos)==1)):
                    obj.location=(xpos,ypos,zpos)
            else:
                for i in objplacement:
                    xpos=i[0]
                    ypos=i[1]
                    if((checkcollission(objname,x,y,z,xpos,ypos,zpos)==1) and (checkbounds(objname,x,y,z,xpos,ypos,zpos)==1)):
                        obj.location=(xpos,ypos,zpos)
                        break
            
            listofobjectsplaced.append([objname,[x,y,z],[xpos,ypos,zpos],sum(x.count(objname) for x in listofobjectsplaced)])
            break
              
                
fp.close()
fp1.close()
fp2.close()
fp3.close()
fp4.close()
'''
    if(objname in ["table","chair","sofa","bag","cabinet","fan","bookshelf"]):
        x1=3
        y1=3
        z1=3
'''
'''
    if(synidobj in ['02773838', '02871439', '02933112', '03001627', '03320046', '04256520', '04379243']):
        x1=3
        y1=3
        z1=3
'''
