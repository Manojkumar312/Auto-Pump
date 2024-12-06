from tkinter import *
import tkinter
import tkinter.font as tkFont
import RPi.GPIO as GPIO
import time
import subprocess
from returntemp import *

GPIO.setwarnings(False)


def tempupdate():
    global realtemp,reqtemp,relaystatus,motortemp,mode
    
    try:
        realtemp=int(qwerty())
        realview.config(text ="        "+str(realtemp))
        if mode==1:
            if(realtemp<reqtemp): 
                GPIO.output(8,GPIO.LOW)
            else:
                GPIO.output(8,GPIO.HIGH)
            
            if (realtemp<motortemp):
                print("off")
                GPIO.output(12,GPIO.HIGH)
            elif(realtemp>motortemp):
                print("on")
                GPIO.output(12,GPIO.LOW)
    except ValueError:
        realview.config(text ="        ERROR")
    
    if GPIO.input(8):
        relayview.config(text ="   HEATER : OFF")
    else:
        relayview.config(text ="   HEATER : ON")
    if GPIO.input(12):
        motorview.config(text ="OIL PUMP: OFF   ")
    else:
        motorview.config(text ="OIL PUMP: ON    ")

    win.after(1000,tempupdate)

def increase():
	global reqtemp
	
	file=open("reqtemp.txt","r+")
	temp=(file.read())
	file.close
	
	temp=int(temp)

	if temp<700:
		temp=temp+10

		reqtemp=temp
		
		file = open("reqtemp.txt", "w+")
		file.write(str(temp))
		file.close

		reqview.config(text =str(reqtemp))
	
def decrease():
	global reqtemp
	
	file=open("reqtemp.txt","r+")
	temp=(file.read())
	file.close
	
	temp=int(temp)

	if temp>10:
		temp=temp-10

		reqtemp=temp
		
		file = open("reqtemp.txt", "w+")
		file.write(str(temp))
		file.close

		reqview.config(text =str(reqtemp))


def relay():
    global mode
    if mode==0:
        if GPIO.input(8):
            GPIO.output(8,GPIO.LOW)
            reButton["text"] = "HEATER : ON "
            reButton["bg"]="yellow"
        else:
            GPIO.output(8,GPIO.HIGH)
            reButton["text"] = "HEATER : OFF"
            reButton["bg"]="red"

def motor():
    global mode
    if mode==0:
        if GPIO.input(12):
            GPIO.output(12,GPIO.LOW)
            mButton["text"] = "OIL PUMP: ON "
            mButton["bg"]="yellow"
        else:
            GPIO.output(12,GPIO.HIGH)
            mButton["text"] = "OIL PUMP: OFF"
            mButton["bg"]="red"


def mincrease():
	global motortemp
	
	file=open("mtemp.txt","r+")
	temp=(file.read())
	file.close
	
	temp=int(temp)

	if temp<700:
		temp=temp+10

		motortemp=temp
		
		file = open("mtemp.txt", "w+")
		file.write(str(temp))
		file.close

		mview.config(text =str(motortemp))
	
def mdecrease():
	global motortemp
	
	file=open("mtemp.txt","r+")
	temp=(file.read())
	file.close
	
	temp=int(temp)

	if temp>10:
		temp=temp-10

		motortemp=temp
		
		file = open("mtemp.txt", "w+")
		file.write(str(temp))
		file.close

		mview.config(text =str(motortemp))

def exitProgram():
	GPIO.cleanup()
	win.quit()
	command = "/usr/bin/sudo /sbin/shutdown -h now"
	process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
	output = process.communicate()[0]

"""
Relay Pin List
				          GPIO
Temperature Control    ->	8

PRE HEATER			   ->	7

Water Pump			   ->   21

Cooling Fan            ->   20
Main Power 1           ->   16
OIL PUMP          	   ->   12
Diesel Pump            ->   1
"""

	
def oilpump():
	if GPIO.input(7) :
		GPIO.output(7,GPIO.LOW)
		opButton["text"] = "PRE HEATER : ON"
		opButton["bg"]="yellow"
	else:
		GPIO.output(7,GPIO.HIGH)
		opButton["text"] = "PRE HEATER : OFF"
		opButton["bg"]="red"

def waterpump():
	if GPIO.input(21) :
		GPIO.output(21,GPIO.LOW)
		wpButton["text"] = "WATER PUMP : ON"
		wpButton["bg"]="yellow"
	else:
		GPIO.output(21,GPIO.HIGH)
		wpButton["text"] = "WATER PUMP : OFF"
		wpButton["bg"]="red"

def coolingfan():
	if GPIO.input(20) :
		GPIO.output(20,GPIO.LOW)
		coolButton["text"] = "COOLING FAN : ON"
		coolButton["bg"]="yellow"
	else:
		GPIO.output(20,GPIO.HIGH)
		coolButton["text"] = "COOLING FAN : OFF"
		coolButton["bg"]="red"

def mainpower1():
	if GPIO.input(16) :
		GPIO.output(16,GPIO.LOW)
		mp1Button["text"] = "MAIN POWER: ON "
		mp1Button["bg"]="yellow"
	else:
		GPIO.output(16,GPIO.HIGH)
		mp1Button["text"] = "MAIN POWER: OFF"
		mp1Button["bg"]="red"

def dieselpump():
	if GPIO.input(1) :
		GPIO.output(1,GPIO.LOW)
		dpButton["text"] = "DIESEL PUMP : ON"
		dpButton["bg"]="yellow"
	else:
		GPIO.output(1,GPIO.HIGH)
		dpButton["text"] = "DIESEL PUMP : OFF"
		dpButton["bg"]="red"

def automan():
    global mode
    if mode==0:
        mode=1
        amButton["text"] ="AUTO"
        amButton["bg"]="magenta"
        
        mButton["text"] = "OIL PUMP: AUTO"
        mButton["bg"]="magenta"
        
        reButton["text"] = "HEATER : AUTO"
        reButton["bg"]="magenta"
    else:
        mode=0
        amButton["text"]="MANUAL"
        amButton["bg"]="cyan"
        
        GPIO.output(12,GPIO.HIGH)
        mButton["text"] = "OIL PUMP: OFF"
        mButton["bg"]="red"
        
        GPIO.output(8,GPIO.HIGH)
        reButton["text"] = "HEATER : OFF"
        reButton["bg"]="red"
        
        
        


GPIO.setmode(GPIO.BCM)

relaylist=[8,7,1,12,16,20,21]
for i in relaylist:
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, GPIO.HIGH)

reqtemp=0
realtemp=0
motortemp=0

mode=0
# 0--> Manual
# 1--> Automatic

win = Tk()

myFont = tkFont.Font(family = 'Helvetica', size = 18, weight = 'bold')
viewfont= tkFont.Font(family = 'Helvetica', size = 15, weight = 'bold')
labelfont=tkFont.Font(family = 'Helvetica', size = 30, weight = 'bold')

win.title("PUMP CONTROL PANEL")
win.geometry('1024x600')


					###########################  LABEL LIST    ###########################

#Required Temperature

dummy = tkinter.Label(win,font = viewfont,text ="REQUIRED TEMPERATURE ℃: ")
dummy.grid(row = 0, column = 0,sticky=W,pady=10)

reqview = tkinter.Label(win,font = labelfont,text = "")
reqview.grid(row = 1, column = 0,sticky=W)

#Realtime Temperature

dummy1= tkinter.Label(win,font = viewfont,text ="REALTIME TEMPERATURE:")
dummy1.grid(row = 0, column = 1,sticky=W,pady=10)

realview = tkinter.Label(win,font = labelfont, text ="")
realview.grid(row = 1, column = 1,sticky=W)

#OIL PUMP Temperature

dummy2 = tkinter.Label(win,font = viewfont,text ="OIL PUMP TEMPERATURE ℃: ")
dummy2.grid(row = 3, column = 0,sticky=W,pady=10)

mview = tkinter.Label(win,font = labelfont,text = "")
mview.grid(row = 4, column = 0,sticky=W)



#Relay 
motorview = tkinter.Label(win,font = viewfont,text ="", height = 2)
motorview.grid(row = 5, column = 0,sticky=E,pady=10)

relayview = tkinter.Label(win,font = viewfont,text ="", height = 2)
relayview.grid(row = 5, column = 1,sticky=W,pady=10)





					###########################   BUTTON LIST   ############################
upButton=Button(win,text="+10",bg="yellow",font=labelfont,command=increase)
upButton.grid(row=1,column=0)

downButton=Button(win,text="-10",bg="red",font=labelfont,command=decrease)
downButton.grid(row=1,column=0,sticky=E)




mupButton=Button(win,text="+10",bg="yellow",font=labelfont,command=mincrease)
mupButton.grid(row=4,column=0)

mdownButton=Button(win,text="-10",bg="red",font=labelfont,command=mdecrease)
mdownButton.grid(row=4,column=0,sticky=E)




exitButton  = Button(win, text = "SHUT DOWN", bg="blue",font=viewfont, command = exitProgram, height=2 , width = 15) 
exitButton.grid(row = 4, column = 1,sticky=E,padx=150)




mp1Button = Button(win, text = "MAIN POWER : OFF",bg="red", font = myFont, command = mainpower1,height=2,width=40)
mp1Button.grid(row = 6, column = 0,sticky=W)

wpButton = Button(win, text = "WATER PUMP : OFF",bg="red", font = myFont, command = waterpump,height=2,width=40)
wpButton.grid(row = 7, column = 0,sticky=W)

coolButton = Button(win, text = "COOLING FAN : OFF",bg="red", font = myFont, command = coolingfan,height=2,width=40)
coolButton.grid(row = 8, column = 0,sticky=W)




mButton = Button(win, text = "OIL PUMP: OFF",bg="red", font = myFont, command = motor,height=2,width=40)
mButton.grid(row = 9, column = 0,sticky=W)




opButton = Button(win, text = "PRE HEATER : OFF",bg="red", font = myFont, command = oilpump,height=2,width=40)
opButton.grid(row = 6, column = 1,sticky=E)

dpButton = Button(win, text = "DIESEL PUMP : OFF",bg="red" ,font = myFont, command = dieselpump,height=2,width=40)
dpButton.grid(row = 7, column = 1,sticky=E)



amButton=Button(win, text = "MANUAL",bg="cyan", font = myFont, command =automan,height=2,width=40)
amButton.grid(row = 8, column = 1,sticky=E)




reButton= Button(win, text = "HEATER : OFF",bg="red", font = myFont, command = relay,height=2,width=40)
reButton.grid(row = 9, column = 1,sticky=E)





					######################################################################


f=open("reqtemp.txt", "r")
temp=(f.read())
reqtemp=int(temp)
f.close()
reqview.config(text =str(reqtemp))

f=open("mtemp.txt", "r")
temp=(f.read())
motortemp=int(temp)
f.close()
mview.config(text =str(motortemp))

win.after(1000,tempupdate)

mainloop()