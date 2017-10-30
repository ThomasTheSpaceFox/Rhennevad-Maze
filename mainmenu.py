#!/usr/bin/env python
import os
import pygame
import time
from pygame.locals import *
import xml.etree.ElementTree as ET
#some notes


scrnx=400
scrny=400
#some variables used in the menu list.
menitm1='Launcher'
#menitm2='null'
#menitm3='null'
windowicon=pygame.image.load(os.path.join('TILE', 'icon32.png'))
pygame.display.set_icon(windowicon)
screensurfdex=pygame.display.set_mode((scrnx, scrny), RESIZABLE)
screensurf=screensurfdex.copy()

#set MENUFLG to 1. this will tell Text-maze-4.py to not try to play and start the music. 
#(as when Text-maze-4.py is run from here the music is already playing)
MENUFLG=0
#list of menu options.
mainlist=(menitm1, "about", "options", "quit")
#find out number of options in menu. (used by the menu selection wrap-around)
findcnt=0
for flx in mainlist:
	findcnt += 1

#load titlescreen image.

titlescreen=pygame.image.load(os.path.join('TILE', 'titlescreen.png'))
titlebg=pygame.image.load(os.path.join('TILE', 'game-bg.png'))

#init the mixer and start the music
pygame.mixer.init()
pygame.mixer.music.load(os.path.join('AUDIO', 'vg-mus-0_theme.ogg'))



print ('Rhennevad Maze main menu')
#init stuff
pygame.display.init()
pygame.font.init()

#prep subcode scripts
sclaunch=open('launcher.py', 'r')
exlaunch=compile(sclaunch.read(), 'launcher.py', 'exec')
scabt=open('about.py', 'r')
exabt=compile(scabt.read(), 'about.py', 'exec')
scopt=open('options.py', 'r')
exopt=compile(scopt.read(), 'options.py', 'exec')
#load conf.xml
mainconf = ET.parse("conf.xml")
mainconfroot = mainconf.getroot()
animtag=mainconfroot.find("anim")
gfxtag=mainconfroot.find("gfx")
sndtag=mainconfroot.find("sound")
musicflg=int(sndtag.attrib.get("music", "1"))
movescrlflg=int(animtag.attrib.get("smoothscrl", "1"))
rgbafilterflg=int(gfxtag.attrib.get("rgbafilter", "1"))
scrx=int(gfxtag.attrib.get("scrx", "400"))
scry=int(gfxtag.attrib.get("scry", "400"))
CONFLOADED=1
if musicflg==1:
	pygame.mixer.music.play(-1)
#set up display
screensurfdex=pygame.display.set_mode((scrnx, scrny), RESIZABLE)
screensurf=screensurfdex.copy()

screensurf.fill((100, 120, 100))
joytag=mainconfroot.find("joy")

joyid=int(joytag.attrib.get("joyid", "0"))
joyon=int(joytag.attrib.get("joyon", "0"))
if joyon==1:
	JOYSTICK=joyid
else:
	JOYSTICK=None

if JOYSTICK!=None:
	print "init joystick..."
	pygame.joystick.init()
	try:
		mainjoy=pygame.joystick.Joystick(JOYSTICK)
		mainjoy.init()
		if mainjoy.get_numaxes()<2:
			print "WARNING: Joystick does not have at least two axes!"
			JOYSTICK=None
		if mainjoy.get_numhats()>=1:
			print "hat found, enabling hat support."
			joyhat=1
		else:
			joyhat=0
		print pygame.joystick.get_count()
	except pygame.error:
		print "Invalid joystick id."
		JOYSTICK=None
jspolar=0
hatpolar=0



def resolvescreenscale():
	if scrnx<scrny:
		return(scrnx)
	elif scrny<scrnx:
		return(scrny)
	else:
		return(scrny)


#prep and display titlescreen image
titlescreenbox = titlescreen.get_rect()
titlescreenbox.centerx = screensurf.get_rect().centerx
titlescreenbox.centery = ((screensurf.get_rect().centery) - 90)
screensurf.blit(titlescreen, (0, 0))
screensurf.blit(titlebg, (0, 0))


scrnx=scrx
scrny=scry
screz=resolvescreenscale()
screensurfdex=pygame.display.set_mode((scrnx, scrny), RESIZABLE)
screensurfQ=pygame.transform.scale(screensurf, (screz, screz))
screensurfdex.blit(screensurfQ, (0, 0))
pygame.display.update()
def popuptextMENU(textto):
	text = simplefont.render(textto, True, (255, 255, 255), (0, 0, 0))
	textbox = text.get_rect()
	textbox.centerx=screensurf.get_rect().centerx
	textbox.centery=390
	screensurf.blit(text, textbox)


pygame.display.set_caption("Rhennevad Maze menu", "Rhennevad Maze")
menuhighnum=1  #integer used to track the highlighted menu item. 
menusel="null"
simplefontB = pygame.font.SysFont(None, 22)
simplefont = pygame.font.SysFont(None, 16) #define a simple font from the system fonts
ixplaymus=0
popuptextMENU("Rhennevad Maze 6.0.0  Copyright (c) 2015-2017 Thomas Leathers")
ixreturn=0
while menusel!="quit":
	#does things that need done upon returning to the menu from an option.
	if ixreturn==1:
		print ("Maze execution complete, returning to menu.")
		pygame.display.set_caption("Rhennevad Maze menu", "Rhennevad Maze menu")
		screensurf.fill((100, 120, 100))
		screensurf.blit(titlescreen, (0, 0))
		screensurf.blit(titlebg, (0, 0))
		#screensurf.blit(titlescreen, titlescreenbox)
		
		popuptextMENU("Rhennevad Maze 6.0.0  Copyright (c) 2015-2017 Thomas Leathers")
		ixreturn=0
		pygame.key.set_repeat()
		if musicflg==1 and ixplaymus==1:
			pygame.mixer.music.load(os.path.join('AUDIO', 'vg-mus-0_theme.ogg'))
			pygame.mixer.music.play(-1)
			ixplaymus=0
	menucnt=1
	evhappenflg=0
	#wraps around menu, i.e. when your at the top and you press up you will be at the bottom of the list.
	if menuhighnum<=0:
		menuhighnum=findcnt
	elif menuhighnum>findcnt:
		menuhighnum=1
	#starting point for menu
	texhigcnt=4
	#separation between each line of text's origin
	texhigjump=14
	#menu line count variable. should be set to 1 here.
	indlcnt=1
	#draws the menu. inverting the colors of the selected menu item.
	for indx in mainlist:
		if indlcnt==menuhighnum:
			textit=simplefontB.render(indx, True, (0, 0, 0), (255, 255, 255))
		else:
			textit=simplefontB.render(indx, True, (0, 0, 0), (234, 229, 210))
		screensurf.blit(textit, (texhigcnt, 32))
		texhigcnt +=(textit.get_width())
		texhigcnt += texhigjump
		indlcnt += 1
	screensurfQ=pygame.transform.scale(screensurf, (screz, screz))
	screensurfdex.blit(screensurfQ, (0, 0))
	pygame.display.update()
	pygame.event.pump()
	pygame.event.clear()
	#reads keyboard controlls, moves cursers when instructed by up/down arrow keys.
	#sets ixreturn to 1 when return is pressed.
	while evhappenflg==0:
		time.sleep(.1)
		if JOYSTICK!=None:
			#time.sleep(.1)
			lraxis=mainjoy.get_axis(0)
			#print lraxis
			if lraxis>0.5:
				menuhighnum += 1
				evhappenflg=1
			if lraxis<-0.5:
				menuhighnum -= 1
				evhappenflg=1
			udaxis=mainjoy.get_axis(1)
			#print lraxis
			if udaxis<-0.5:
				menuhighnum -= 1
				evhappenflg=1
			if udaxis>0.5:
				menuhighnum += 1
				evhappenflg=1
			###hat support (only enabled when at least 1 hat is present.)
			if joyhat==1:
				bothaxis=mainjoy.get_hat(0)
				lraxis=bothaxis[0]
				#print lraxis
				if lraxis>0.4:
					menuhighnum += 1
					evhappenflg=1
				if lraxis<-0.4:
					menuhighnum -= 1
					evhappenflg=1
				udaxis=bothaxis[1]
				#print lraxis
				if udaxis>0.4:
					menuhighnum -= 1
					evhappenflg=1
				if udaxis<-0.4:
					menuhighnum += 1
					evhappenflg=1
		for event in pygame.event.get():
			if event.type == JOYBUTTONDOWN:
				if event.button==0:
					ixreturn=1
					evhappenflg=1
					break
			if event.type == KEYDOWN and event.key == K_UP:
				menuhighnum -= 1
				evhappenflg=1
			if event.type == KEYDOWN and event.key == K_RIGHT:
				menuhighnum += 1
				evhappenflg=1
			if event.type == KEYDOWN and event.key == K_DOWN:
				menuhighnum += 1
				evhappenflg=1
			if event.type == KEYDOWN and event.key == K_LEFT:
				menuhighnum -= 1
				evhappenflg=1
			if event.type == KEYDOWN and event.key == K_RETURN:
				ixreturn=1
				evhappenflg=1
				break
			
					
			if event.type == QUIT:
				menusel="quit"
				evhappenflg=1
				break
			if event.type == VIDEORESIZE:
				sxh=event.h
				if sxh<400:
					sxh=400
				#sxratio=(sxh-400)
				sxw=event.w
				if sxw<400:
					sxw=400
				screensurfdex=pygame.display.set_mode((sxw, sxh), RESIZABLE)
				scrnx=sxw
				scrny=sxh
				screz=resolvescreenscale()
				screensurfQ=pygame.transform.scale(screensurf, (screz, screz))
				screensurfdex.blit(screensurfQ, (0, 0))
				pygame.display.update()
	#second menu line count variable. should be set to 1 here.
	indlcnt2=1
	#executes option in menu when ixreturn is 1, (this means player has pressed return.)
	if ixreturn==1 and menusel!="quit":
		#print "blk1"
		for indxB in mainlist:
			#print indxB
			if indlcnt2==menuhighnum:
				if indxB==menitm1:
					#MAZEIS='sample.xml'
					#mazefilepath=(os.path.join('MAZE', MAZEIS)) #global variable used by Text-maze-4.py
					
					exec(exlaunch)
					
				#if indxB==menitm2:
					#MAZEIS='sample.MAZE'
					#mazefilepath=(os.path.join('MAZE', MAZEIS))
					#execfile('Text-maze-4.py')
				#if indxB==menitm3:
					#MAZEIS='switchback1.MAZE'
					#mazefilepath=(os.path.join('MAZE', MAZEIS))
					#execfile('Text-maze-4.py')
				if indxB=='quit':
					menusel="quit"
				if indxB=='about':
					exec(exabt)
				if indxB=='options':
					exec(exopt)
			indlcnt2 += 1
	pygame.display.update()
print "saving conf.xml"
gfxtag.set("scrx", str(scrnx))
gfxtag.set("scry", str(scrny))
mainconf.write("conf.xml")
