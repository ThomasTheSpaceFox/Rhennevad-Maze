#!/usr/bin/env python

# Rhennevad Maze
#mazemodpath = (os.path.join('MAZE', 'sample.MOD.txt'))




##############
#wordbindings:
##############
#FORWARD
FORWARDWORDBIND=('w')
#BACKWARD
BACKWARDWORDBIND=('s')
#left
LEFTWORDBIND=('a')
#right
RIGHTWODBIND=('d')
#quit
QUITWORDBIND=('q')
##############
#import LIBTIMG
#import libtextmaze
import pygame.event
import pygame.key
import pygame.display
import pygame.image
import pygame.mixer
#import pygame.mixer.music
import pygame
import time
import os
from pygame.locals import *
import xml.etree.ElementTree as ET




#check for global variables
if 'mazefilepath' in globals():
	print ("Global variable: 'mazefilepath' detected, using as maze refrence.")
else:
	print ("Global variable: 'mazefilepath' not detected, using default maze.")
	mazefilepath = (os.path.join('MAZE', 'sample.xml'))
if 'MENUFLG' in globals():
	print ("Global variable: 'MENUFLG' present. following its setting.")
else:
	print ("Global variable: 'MENUFLG' not present. using default.")
	MENUFLG=0
if 'DEBUG' in globals():
	print ("Global variable: 'DEBUG' present. following its setting.")
else:
	print ("Global variable: 'DEBUG' not present. using default.")
	DEBUG=0
if 'scrnx' in globals():
	print ("Global variable: 'scrnx' present. following its setting.")
else:
	print ("Global variable: 'scrnx' not present. using default.")
	scrnx=400
if 'scrny' in globals():
	print ("Global variable: 'scrny' present. following its setting.")
else:
	print ("Global variable: 'scrny' not present. using default.")
	scrny=400

#load conf.xml
mainconf = ET.parse("conf.xml")
mainconfroot = mainconf.getroot()
animtag=mainconfroot.find("anim")
gfxtag=mainconfroot.find("gfx")
sndtag=mainconfroot.find("sound")
musicflg=int(sndtag.attrib.get("music", "1"))
movescrlflg=int(animtag.attrib.get("smoothscrl", "1"))
rgbafilterflg=int(gfxtag.attrib.get("rgbafilter", "1"))
scfast=int(animtag.attrib.get("fastscrl", "0"))
useHW=int(gfxtag.attrib.get("hwaccel", "1"))

#load main.grid file

def debugmsg(msg, printplaypos=0):
	if DEBUG==1:
		
		if printplaypos==1:
			print (msg + " x(" + str(playx) + "),y(" + str(playy) + ")")
		else:
			print msg


#load window icon, make window, set caption, start music, init things. etc.
debugmsg("Initalizing graphics and sound...")
pygame.mixer.init()

stepfx=pygame.mixer.Sound(os.path.join('AUDIO', 'step.ogg'))
mipfx=pygame.mixer.Sound(os.path.join('AUDIO', 'mip.ogg'))
gemfx=pygame.mixer.Sound(os.path.join('AUDIO', 'gemfx.ogg'))
supergemfx=pygame.mixer.Sound(os.path.join('AUDIO', 'supergemfx.ogg'))

levelwinfx=pygame.mixer.Sound(os.path.join('AUDIO', 'levelwin.ogg'))
switchonfx=pygame.mixer.Sound(os.path.join('AUDIO', 'switchon.ogg'))
switchofffx=pygame.mixer.Sound(os.path.join('AUDIO', 'switchoff.ogg'))

pygame.display.init()
pygame.font.init()
pygame.key.set_repeat(180, 50)


windowicon=pygame.image.load(os.path.join('TILE', 'icon32.png'))
pygame.display.set_icon(windowicon)
#screensurfdex=pygame.display.set_mode((scrnx, scrny), RESIZABLE)
#if useHW is 1, make screensurf HW surface and screensurfdex doublebuffered.
if useHW==1:
	screensurfdex=pygame.display.set_mode((scrnx, scrny), RESIZABLE|DOUBLEBUF)
	screensurf=pygame.Surface((400, 400), SRCALPHA|HWSURFACE).convert_alpha()
	#screensurfscroll=pygame.Surface((560, 480), SRCALPHA|HWSURFACE).convert_alpha()
else:
	screensurfdex=pygame.display.set_mode((scrnx, scrny), RESIZABLE)
	screensurf=pygame.Surface((400, 400), SRCALPHA).convert_alpha()
	screensurfscroll=pygame.Surface((560, 480), SRCALPHA).convert_alpha()
pygame.display.set_icon(windowicon)
pygame.display.set_caption("Rhennevad Maze", "Rhennevad Maze")
debugmsg("Loading Graphical data.")
#load tiles
gamebg=pygame.image.load(os.path.join('TILE', 'game-bg.png')).convert_alpha(screensurf)

#player overlay
tileplayer=pygame.image.load(os.path.join('TILE', 'player.png')).convert_alpha(screensurf)
tileplayerB=pygame.image.load(os.path.join('TILE', 'playerB.png')).convert_alpha(screensurf)
tileplayerL=pygame.image.load(os.path.join('TILE', 'playerL.png')).convert_alpha(screensurf)
tileplayerR=pygame.image.load(os.path.join('TILE', 'playerR.png')).convert_alpha(screensurf)
#shadowwall variants:
shadtileplayer=pygame.image.load(os.path.join('TILE', 'shadplayer.png')).convert_alpha(screensurf)
shadtileplayerB=pygame.image.load(os.path.join('TILE', 'shadplayerB.png')).convert_alpha(screensurf)
shadtileplayerL=pygame.image.load(os.path.join('TILE', 'shadplayerL.png')).convert_alpha(screensurf)
shadtileplayerR=pygame.image.load(os.path.join('TILE', 'shadplayerR.png')).convert_alpha(screensurf)
#walking variants
#player overlay
tileplayerstep=pygame.image.load(os.path.join('TILE', 'playerstep.png')).convert_alpha(screensurf)
tileplayerBstep=pygame.image.load(os.path.join('TILE', 'playerBstep.png')).convert_alpha(screensurf)
tileplayerLstep=pygame.image.load(os.path.join('TILE', 'playerLstep.png')).convert_alpha(screensurf)
tileplayerRstep=pygame.image.load(os.path.join('TILE', 'playerRstep.png')).convert_alpha(screensurf)
#shadowwall variants:
shadtileplayerstep=pygame.image.load(os.path.join('TILE', 'shadplayerstep.png')).convert_alpha(screensurf)
shadtileplayerBstep=pygame.image.load(os.path.join('TILE', 'shadplayerBstep.png')).convert_alpha(screensurf)
shadtileplayerLstep=pygame.image.load(os.path.join('TILE', 'shadplayerLstep.png')).convert_alpha(screensurf)
shadtileplayerRstep=pygame.image.load(os.path.join('TILE', 'shadplayerRstep.png')).convert_alpha(screensurf)

#Points and collectibles
pointcnt=0


#gems
objgem=pygame.image.load(os.path.join('TILE', 'genwhite.png')).convert_alpha(screensurf)
objgemred=pygame.image.load(os.path.join('TILE', 'gemred.png')).convert_alpha(screensurf)
objgemblue=pygame.image.load(os.path.join('TILE', 'gemblue.png')).convert_alpha(screensurf)
objgemgreen=pygame.image.load(os.path.join('TILE', 'gemgreen.png')).convert_alpha(screensurf)
objgemrain=pygame.image.load(os.path.join('TILE', 'gemrain.png')).convert_alpha(screensurf)




tilewall=pygame.image.load(os.path.join('TILE', 'wall.png')).convert(screensurf)

tilefloor=pygame.image.load(os.path.join('TILE', 'floor.png')).convert(screensurf)

tileexit=pygame.image.load(os.path.join('TILE', 'exit.png')).convert(screensurf)
tilewater=pygame.image.load(os.path.join('TILE', 'water.png')).convert(screensurf)
tilegrass=pygame.image.load(os.path.join('TILE', 'grass.png')).convert(screensurf)
tiledock=pygame.image.load(os.path.join('TILE', 'dock.png')).convert(screensurf)
tilebridge=pygame.image.load(os.path.join('TILE', 'bridge.png')).convert(screensurf)
tileroof1=pygame.image.load(os.path.join('TILE', 'roof1.png')).convert(screensurf)
tileinsidewall=pygame.image.load(os.path.join('TILE', 'insidewall.png')).convert(screensurf)
tilecarpet=pygame.image.load(os.path.join('TILE', 'carpet.png')).convert(screensurf)
tileredcarpet=pygame.image.load(os.path.join('TILE', 'redcarpet.png')).convert(screensurf)
tiletiledfloor=pygame.image.load(os.path.join('TILE', 'tilefloor.png')).convert(screensurf)
tileoutside=pygame.image.load(os.path.join('TILE', 'outsidein.png')).convert(screensurf)
tilebrickpath=pygame.image.load(os.path.join('TILE', 'brickpath.png')).convert(screensurf)
tilesand=pygame.image.load(os.path.join('TILE', 'sand.png')).convert(screensurf)
#(added batch-o-tiles 1)
tilecobblewall=pygame.image.load(os.path.join('TILE', 'cobblewall.png')).convert(screensurf)
tiledirt=pygame.image.load(os.path.join('TILE', 'dirt.png')).convert(screensurf)
tilestone=pygame.image.load(os.path.join('TILE', 'stone.png')).convert(screensurf)
tiledarkstone=pygame.image.load(os.path.join('TILE', 'darkstone.png')).convert(screensurf)
tilelava=pygame.image.load(os.path.join('TILE', 'lava.png')).convert(screensurf)
tilegreengoo=pygame.image.load(os.path.join('TILE', 'greengoo.png')).convert(screensurf)
#second interior set
tilehardwood=pygame.image.load(os.path.join('TILE', 'hardwoodfloor.png')).convert(screensurf)
tileconcretefloor=pygame.image.load(os.path.join('TILE', 'concretefloor.png')).convert(screensurf)
tilesteelfloor=pygame.image.load(os.path.join('TILE', 'steelfloor.png')).convert(screensurf)
tilegirderwall=pygame.image.load(os.path.join('TILE', 'girderwall.png')).convert(screensurf)
tilegrate=pygame.image.load(os.path.join('TILE', 'grate.png')).convert_alpha(screensurf)
SPECIALtilegrate=pygame.image.load(os.path.join('TILE', 'gratecliff.png')).convert_alpha(screensurf)

#skytiles
#sky1
tilesky1=pygame.image.load(os.path.join('TILE', 'sky1.png')).convert_alpha(screensurf)
#texture used for water reflections
tilesky1aqua=pygame.image.load(os.path.join('TILE', 'sky1.png'))
tilesky1aqua=tilesky1aqua.convert()
tilesky1aqua.set_alpha(40)

tilesky1x=pygame.image.load(os.path.join('TILE', 'sky1x.png')).convert_alpha(screensurf)
tilesky1y=pygame.image.load(os.path.join('TILE', 'sky1y.png')).convert_alpha(screensurf)
tilesky1b=pygame.image.load(os.path.join('TILE', 'sky1b.png')).convert_alpha(screensurf)
#overlay graphics
ovflowers=pygame.image.load(os.path.join('TILE', 'ovflowers.png')).convert_alpha(screensurf)
ovcrate=pygame.image.load(os.path.join('TILE', 'ovcrate.png')).convert_alpha(screensurf)
ovbuntowel=pygame.image.load(os.path.join('TILE', 'ovbuntowel.png')).convert_alpha(screensurf)
ovbunraft=pygame.image.load(os.path.join('TILE', 'ovbunraft.png')).convert_alpha(screensurf)
ovbunstand=pygame.image.load(os.path.join('TILE', 'ovbunstand.png')).convert_alpha(screensurf)
ovsink=pygame.image.load(os.path.join('TILE', 'ovsink.png')).convert_alpha(screensurf)
ovsinkr1=pygame.image.load(os.path.join('TILE', 'ovsinkr1.png')).convert_alpha(screensurf)
ovsinkr2=pygame.image.load(os.path.join('TILE', 'ovsinkr2.png')).convert_alpha(screensurf)
ovsinkr3=pygame.image.load(os.path.join('TILE', 'ovsinkr3.png')).convert_alpha(screensurf)

ovcounter=pygame.image.load(os.path.join('TILE', 'ovcounter.png')).convert_alpha(screensurf)
ovcounterr1=pygame.image.load(os.path.join('TILE', 'ovcounterr1.png')).convert_alpha(screensurf)
ovcounterr2=pygame.image.load(os.path.join('TILE', 'ovcounterr2.png')).convert_alpha(screensurf)
ovcounterr3=pygame.image.load(os.path.join('TILE', 'ovcounterr3.png')).convert_alpha(screensurf)

ovarrow=pygame.image.load(os.path.join('TILE', 'ovarrow.png')).convert_alpha(screensurf)

ovtoilet=pygame.image.load(os.path.join('TILE', 'ovtoilet.png')).convert_alpha(screensurf)
ovtoiletr1=pygame.image.load(os.path.join('TILE', 'ovtoiletr1.png')).convert_alpha(screensurf)
ovtoiletr2=pygame.image.load(os.path.join('TILE', 'ovtoiletr2.png')).convert_alpha(screensurf)
ovtoiletr3=pygame.image.load(os.path.join('TILE', 'ovtoiletr3.png')).convert_alpha(screensurf)

ovcat1=pygame.image.load(os.path.join('TILE', 'cat1.png')).convert_alpha(screensurf)
ovcat2=pygame.image.load(os.path.join('TILE', 'cat2.png')).convert_alpha(screensurf)
ovcat3=pygame.image.load(os.path.join('TILE', 'cat3.png')).convert_alpha(screensurf)

ovmouse1=pygame.image.load(os.path.join('TILE', 'mouse1.png')).convert_alpha(screensurf)
ovbulletin=pygame.image.load(os.path.join('TILE', 'ovbulletin.png')).convert_alpha(screensurf)
ovbulletinr1=pygame.image.load(os.path.join('TILE', 'ovbulletinr1.png')).convert_alpha(screensurf)
ovbulletinr2=pygame.image.load(os.path.join('TILE', 'ovbulletinr2.png')).convert_alpha(screensurf)
ovbulletinr3=pygame.image.load(os.path.join('TILE', 'ovbulletinr3.png')).convert_alpha(screensurf)

NPCballoon=pygame.image.load(os.path.join('TILE', 'NPCballoon.png')).convert_alpha(screensurf)
#overlay signs
signwater=pygame.image.load(os.path.join('TILE', 'signwater.png')).convert_alpha(screensurf)
signlava=pygame.image.load(os.path.join('TILE', 'signlava.png')).convert_alpha(screensurf)
signacid=pygame.image.load(os.path.join('TILE', 'signacid.png')).convert_alpha(screensurf)
signpool=pygame.image.load(os.path.join('TILE', 'signpool.png')).convert_alpha(screensurf)
signriver=pygame.image.load(os.path.join('TILE', 'signriver.png')).convert_alpha(screensurf)
signtree=pygame.image.load(os.path.join('TILE', 'signtree.png')).convert_alpha(screensurf)
signdiner=pygame.image.load(os.path.join('TILE', 'signdiner.png')).convert_alpha(screensurf)
signbeach=pygame.image.load(os.path.join('TILE', 'signbeach.png')).convert_alpha(screensurf)
signbun=pygame.image.load(os.path.join('TILE', 'signbun.png')).convert_alpha(screensurf)
signinfo=pygame.image.load(os.path.join('TILE', 'signinfo.png')).convert_alpha(screensurf)
signtask=pygame.image.load(os.path.join('TILE', 'signtask.png')).convert_alpha(screensurf)
#special shadows
wallshadow=pygame.image.load(os.path.join('TILE', 'wallshadow.png')).convert_alpha(screensurf)
landshadow=pygame.image.load(os.path.join('TILE', 'landshadow.png')).convert_alpha(screensurf)
wallliquidshadow=pygame.image.load(os.path.join('TILE', 'wallliquidshadow.png')).convert_alpha(screensurf)
#wall "side" hints
hinthedge=pygame.image.load(os.path.join('TILE', 'hinthedge.png')).convert_alpha(screensurf)
hintcobble=pygame.image.load(os.path.join('TILE', 'hintcobble.png')).convert_alpha(screensurf)
hintbuild=pygame.image.load(os.path.join('TILE', 'hintbuild.png')).convert_alpha(screensurf)
hintbuildgreen=pygame.image.load(os.path.join('TILE', 'hintbuildgreen.png')).convert_alpha(screensurf)

hintbuildout=pygame.image.load(os.path.join('TILE', 'hintbuildout.png')).convert_alpha(screensurf)
hintdoor=pygame.image.load(os.path.join('TILE', 'hintdoor.png')).convert_alpha(screensurf)
hintonsky=pygame.image.load(os.path.join('TILE', 'skycliff.png')).convert_alpha(screensurf)
playerfuzzshad=pygame.image.load(os.path.join('TILE', 'playerfuzzshad.png')).convert_alpha(screensurf)
playerfuzzshadSC=playerfuzzshad
#playerfuzzshadSC=pygame.image.load(os.path.join('TILE', 'playerfuzzshadB.png')).convert_alpha(screensurf)
#gates
gateopen=pygame.image.load(os.path.join('TILE', 'gateopen.png')).convert_alpha(screensurf)
gateclosed=pygame.image.load(os.path.join('TILE', 'gateclosed.png')).convert_alpha(screensurf)
#switches
switchon=pygame.image.load(os.path.join('TILE', 'switchon.png')).convert_alpha(screensurf)
switchoff=pygame.image.load(os.path.join('TILE', 'switchoff.png')).convert_alpha(screensurf)

#hudfaces
hudfacehappy=pygame.image.load(os.path.join('TILE', 'hudfacehappy.png')).convert_alpha(screensurf)
hudfacesad=pygame.image.load(os.path.join('TILE', 'hudfacesad.png')).convert_alpha(screensurf)
hudfaceshock=pygame.image.load(os.path.join('TILE', 'hudfaceshock.png')).convert_alpha(screensurf)
hudfaceangry=pygame.image.load(os.path.join('TILE', 'hudfaceanger.png')).convert_alpha(screensurf)
hudfacecasual=pygame.image.load(os.path.join('TILE', 'hudfacecasual.png')).convert_alpha(screensurf)
hudfacebored=pygame.image.load(os.path.join('TILE', 'hudfacebored.png')).convert_alpha(screensurf)

#hudicons
huggem=pygame.image.load(os.path.join('TILE', 'gemhud.png')).convert_alpha(screensurf)
winscreen=pygame.image.load(os.path.join('TILE', 'winscreen.png')).convert_alpha(screensurf)
#scroll masks (no longer used)
#hscrollmask=pygame.image.load(os.path.join('TILE', 'hscrollmask.png'))
#vscrollmask=pygame.image.load(os.path.join('TILE', 'vscrollmask.png'))


# *.MAZE file data loader
print ("loading data from:" + mazefilepath)
tree = ET.parse(mazefilepath)
root = tree.getroot()
setuptag=root.find('setup')
playx=int((setuptag.find('startposx')).text)
playy=int((setuptag.find('startposy')).text)
viewfilterflg=setuptag.attrib.get('filter', "0")
backdropf=setuptag.attrib.get('backdrop', "0")
if backdropf=="0":
	bdrop=pygame.image.load(os.path.join('TILE', 'backdrop0.png'))
elif backdropf=="1":
	bdrop=pygame.image.load(os.path.join('TILE', 'backdrop1.png'))
elif backdropf=="2":
	bdrop=pygame.image.load(os.path.join('TILE', 'backdrop2.png'))
else:
	bdrop=pygame.image.load(os.path.join('TILE', 'backdrop0.png'))
bdrop=bdrop.convert()
if viewfilterflg=="1":
	filterA=setuptag.attrib.get('a')
	filterR=setuptag.attrib.get('r')
	filterB=setuptag.attrib.get('b')
	filterG=setuptag.attrib.get('g')
	viewfilter=pygame.Surface((80, 80))
	viewfiltertall=pygame.Surface((80, 88))
	viewfiltershort=pygame.Surface((80, 72))
	viewfilter.fill((int(filterR), int(filterG), int(filterB)))
	viewfilter.set_alpha(int(filterA))
	viewfiltertall.fill((int(filterR), int(filterG), int(filterB)))
	viewfiltertall.set_alpha(int(filterA))
	viewfiltershort.fill((int(filterR), int(filterG), int(filterB)))
	viewfiltershort.set_alpha(int(filterA))
else:
	viewfilter=pygame.Surface((80, 80))
	viewfiltertall=pygame.Surface((80, 88))
	viewfiltertall.set_alpha(0)
	viewfilter.set_alpha(0)

bgmtrack=int(setuptag.attrib.get('bgmtrack', "1"))

mazemodpath=os.path.join("MAZE", ((root.find('maingrid')).text))
nodetag=root.find('nodes')
forktag=root.find('forks')
mazetitle=(setuptag.find('mazename')).text
print ("data loaded. \n")
debugset = ('1')
gameend = ('0')
CANTMOVE = ("Can't move in that direction.")
WINGAME = ("You win!")
lastmove="F"
inside=0
#music track definitions:

if bgmtrack==0:
	bgmname='vg-mus-0_theme.ogg'
if bgmtrack==1:
	bgmname='vg-mus-1_main_menu.ogg'
if bgmtrack==2:
	bgmname='vg-mus-2_spooky-hall.ogg'
if bgmtrack==3:
	bgmname='vg-mus-3-darkfeilds.ogg'

if musicflg==1:
	pygame.mixer.music.load(os.path.join('AUDIO', bgmname))
	#pygame.mixer.music.load(os.path.join('AUDIO', 'vgtrack1.mid'))
	if musicflg==1:
		pygame.mixer.music.play(-1)

#define a simple font from the system font
simplefont = pygame.font.SysFont(None, 16)
simplefontB = pygame.font.SysFont(None, 24)

def keyprint():
	if DEBUG==1:
		print keylist
#load main.grid here.
m = open(mazemodpath)
screenscrollbx=pygame.Surface((400, 400), SRCALPHA)
#draws tiles. used by tilegriddraw internally.
bgtext = simplefont.render(mazetitle, True, (0, 0, 0))
gamebg.blit(bgtext, (0, 0))
hudface="1"
def tileblit(xval, yval, tilestring, xfoo, yfoo, drawfox=0):
	tilepost=pygame.Surface((400, 400), SRCALPHA)
	if tilestring=="1":
		screensurf.blit(tilewall, (xval, (yval-8)))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="C":
		screensurf.blit(tilecobblewall, (xval, (yval-8)))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="0":
		screensurf.blit(tilefloor, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="e":
		screensurf.blit(tiledirt, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="S":
		screensurf.blit(tilestone, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="X":
		screensurf.blit(tilegreengoo, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="l":
		screensurf.blit(tilelava, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="G":
		screensurf.blit(tilegrate, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
	if tilestring=="z":
		#if playx%2!=0 and playy%2!=0:
			#screensurf.blit(tilesky1b, (xval, yval))
		#elif playx%2!=0:
			#screensurf.blit(tilesky1x, (xval, yval))
		#elif playy%2!=0:
			#screensurf.blit(tilesky1y, (xval, yval))
		#else:
			#screensurf.blit(tilesky1, (xval, yval))
		#screensurf.blit(tilesky1, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="D":
		screensurf.blit(tiledarkstone, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="3":
		screensurf.blit(tileexit, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="w":
		screensurf.blit(tilewater, (xval, yval))
		#doesn't look good yet.
		#screensurf.blit(tilesky1aqua, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="g":
		screensurf.blit(tilegrass, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		#print "ping"
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
			#print "pong"
	if tilestring=="s":
		screensurf.blit(tilesand, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		#print "ping"
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
			#print "pong"
	if tilestring=="d":
		screensurf.blit(tiledock, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="B":
		screensurf.blit(tilebrickpath, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	if tilestring=="b":
		screensurf.blit(tilebridge, (xval, yval))
		Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox)
		
		if inside==1:
			tilepost.blit(tileoutside, (xval, yval))
	#"inside" tiles below.
	if tilestring=="R":
		
		if inside==1:
			screensurf.blit(tileinsidewall, (xval, (yval-8)))
			Qinside=1
		else:
			screensurf.blit(tileroof1, (xval, (yval-8)))
			Qinside=0
		overlayscanB(xfoo, yfoo, xval, yval, drawfox, Qinside)
	if tilestring=="c":
		
		if inside==1:
			Qinside=1
			screensurf.blit(tilecarpet, (xval, yval))
		else:
			Qinside=0
			screensurf.blit(tileroof1, (xval, (yval-8)))
		overlayscanB(xfoo, yfoo, xval, yval, drawfox, Qinside)
	if tilestring=="Q":
		
		if inside==1:
			Qinside=1
			screensurf.blit(tilegirderwall, (xval, (yval-8)))
		else:
			Qinside=0
			screensurf.blit(tileroof1, (xval, (yval-8)))
		overlayscanB(xfoo, yfoo, xval, yval, drawfox, Qinside)
	if tilestring=="P":
		
		if inside==1:
			screensurf.blit(tilesteelfloor, (xval, yval))
			Qinside=1
		else:
			Qinside=0
			screensurf.blit(tileroof1, (xval, (yval-8)))
		overlayscanB(xfoo, yfoo, xval, yval, drawfox, Qinside)
	if tilestring=="Z":
		
		if inside==1:
			screensurf.blit(tileconcretefloor, (xval, yval))
			Qinside=1
		else:
			Qinside=0
			screensurf.blit(tileroof1, (xval, (yval-8)))
		overlayscanB(xfoo, yfoo, xval, yval, drawfox, Qinside)
	if tilestring=="H":
		
		if inside==1:
			screensurf.blit(tilehardwood, (xval, yval))
			Qinside=1
		else:
			Qinside=0
			screensurf.blit(tileroof1, (xval, (yval-8)))
		overlayscanB(xfoo, yfoo, xval, yval, drawfox, Qinside)
	
	if tilestring=="r":
		
		if inside==1:
			screensurf.blit(tileredcarpet, (xval, yval))
			Qinside=1
		else:
			Qinside=0
			screensurf.blit(tileroof1, (xval, (yval-8)))
		overlayscanB(xfoo, yfoo, xval, yval, drawfox, Qinside)
	if tilestring=="t":
		
		if inside==1:
			screensurf.blit(tiletiledfloor, (xval, yval))
			Qinside=1
		else:
			Qinside=0
			screensurf.blit(tileroof1, (xval, (yval-8)))
		overlayscanB(xfoo, yfoo, xval, yval, drawfox, Qinside)
	#screensurf.blit(tilepost, (0, 0))
#new function to draw tile grid


def tilegriddraw3(xoff=0, yoff=0):
	yhig=20
	xwid=0
	for fy in [2, 1, 0, -1, -2]:
		grdy=playy + fy
		xwid=0
		for fx in [2, 1, 0, -1, -2]:
			grdx=playx + fx
			grdblk=lookpoint(grdx, grdy)
			tileblit(xwid + xoff, yhig + yoff, grdblk, grdx, grdy)
			xwid += 80
		yhig += 80
	labelscan(xoff, yoff)

def ovrot(Qrot, Qgfx):
	if Qrot=="1":
		Qgfx=pygame.transform.rotate(Qgfx, 90)
	if Qrot=="2":
		Qgfx=pygame.transform.rotate(Qgfx, 180)
	if Qrot=="3":
		Qgfx=pygame.transform.rotate(Qgfx, 270)
	return Qgfx

def overlayblit(overlaytype, Qrotate="0"):
	if overlaytype=="flowers":
		return(ovrot(Qrotate, ovflowers), 0)
	if overlaytype=="2":
		return(ovrot(Qrotate, ovbuntowel), 0)
	if overlaytype=="3":
		return(ovrot(Qrotate, ovbunraft), 0)
	if overlaytype=="4":
		return(ovrot(Qrotate, ovbunstand), 0)
	if overlaytype=="sink":
		if Qrotate=="1":
			return(ovsinkr1, 1)
		if Qrotate=="2":
			return(ovsinkr2, 1)
		if Qrotate=="3":
			return(ovsinkr3, 1)
		else:
			return(ovsink, 1) #TWEAKS DONE
	if overlaytype=="counter":
		if Qrotate=="1":
			return(ovcounterr1, 1)
		if Qrotate=="2":
			return(ovcounterr2, 1)
		if Qrotate=="3":
			return(ovcounterr3, 1)
		else:
			return(ovcounter, 1) #TWEAKS DONE
	if overlaytype=="toilet":
		if Qrotate=="1":
			return(ovtoiletr1, 1)
		if Qrotate=="2":
			return(ovtoiletr2, 1)
		if Qrotate=="3":
			return(ovtoiletr3, 1)
		else:
			return(ovtoilet, 1) #TWEAKS DONE
	if overlaytype=="crate":
		return(ovrot(Qrotate, ovcrate), 1)# TWEAKING DONE
	if overlaytype=="cat1":
		return(ovrot(Qrotate, ovcat1), 0)
	if overlaytype=="cat2":
		return(ovrot(Qrotate, ovcat2), 0)
	if overlaytype=="cat3":
		return(ovrot(Qrotate, ovcat3), 0)
	if overlaytype=="mouse1":
		return(ovrot(Qrotate, ovmouse1), 0)
	if overlaytype=="arrow":
		return(ovrot(Qrotate, ovarrow), 0)
	if overlaytype=="signwater":
		return(ovrot(Qrotate, signwater), 0)
	if overlaytype=="signlava":
		return(ovrot(Qrotate, signlava), 0)
	if overlaytype=="signacid":
		return(ovrot(Qrotate, signacid), 0)
	if overlaytype=="signbeach":
		return(ovrot(Qrotate, signbeach), 0)
	if overlaytype=="signdiner":
		return(ovrot(Qrotate, signdiner), 0)
	if overlaytype=="signpool":
		return(ovrot(Qrotate, signpool), 0)
	if overlaytype=="signriver":
		return(ovrot(Qrotate, signriver), 0)
	if overlaytype=="signtree":
		return(ovrot(Qrotate, signtree), 0)
	if overlaytype=="signbun":
		return(ovrot(Qrotate, signbun), 0)
	if overlaytype=="signinfo":
		return(ovrot(Qrotate, signinfo), 0)
	if overlaytype=="signtask":
		return(ovrot(Qrotate, signtask), 0)
	if overlaytype=="NPCballoon":
		return(ovrot(Qrotate, NPCballoon), 0)
	if overlaytype=="bulletin":
		return(ovrot(Qrotate, ovbulletin), 1) #needs separate rotate views and 8 pix offset
	

def overlayscan():
	for node in nodetag.findall("overlay"):
		QX=int(node.attrib.get('x'))
		QY=int(node.attrib.get('y'))
		Qtype=node.attrib.get('type')
		Qvis=node.attrib.get('area')
		if Qvis=="i" and inside==1:
			ovvis=1
		elif Qvis=="o" and inside==0:
			ovvis=1
		elif Qvis=="b":
			ovvis=1
		else:
			ovvis=0
		labtext=overlayblit(Qtype)
		if ovvis==1:
			if QX==LEFTWARD3x and QY==LEFTWARD3y:
				screensurf.blit(labtext, (80, 20))
			if QX==RIGHTWARD3x and QY==RIGHTWARD3y:
				screensurf.blit(labtext, (240, 20))
			if QX==FARLEFT3x and QY==FARLEFT3y:
				screensurf.blit(labtext, (0, 20))
			if QX==FARRIGHT3x and QY==FARRIGHT3y:
				screensurf.blit(labtext, (320, 20))
			if QX==FORWARD2x and QY==FORWARD2y:
				screensurf.blit(labtext, (160, 20))
			if QX==LEFTWARD2x and QY==LEFTWARD2y:
				screensurf.blit(labtext, (80, 100))
			if QX==RIGHTWARD2x and QY==RIGHTWARD2y:
				screensurf.blit(labtext, (240, 100))
			if QX==FARLEFT2x and QY==FARLEFT2y:
				screensurf.blit(labtext, (0, 100))
			if QX==FARRIGHT2x and QY==FARRIGHT2y:
				screensurf.blit(labtext, (320, 100))
			if QX==FORWARDx and QY==FORWARDy:
				screensurf.blit(labtext, (160, 100))
			if QX==LEFTWARDx and QY==LEFTWARDy:
				screensurf.blit(labtext, (80, 180))
			if QX==CENTERx and QY==CENTERy:
				screensurf.blit(labtext, (160, 180))
			if QX==RIGHTWARDx and QY==RIGHTWARDy:
				screensurf.blit(labtext, (240, 180))
			if QX==FARLEFTx and QY==FARLEFTy:
				screensurf.blit(labtext, (0, 180))
			if QX==FARRIGHTx and QY==FARRIGHTy:
				screensurf.blit(labtext, (320, 180))
			if QX==LEFTWARD0x and QY==LEFTWARD0y:
				screensurf.blit(labtext, (80, 260))
			if QX==RIGHTWARD0x and QY==RIGHTWARD0y:
				screensurf.blit(labtext, (240, 260))
			if QX==FARLEFT0x and QY==FARLEFT0y:
				screensurf.blit(labtext, (0, 260))
			if QX==FARRIGHT0x and QY==FARRIGHT0y:
				screensurf.blit(labtext, (320, 260))
			if QX==BACKWARDx and QY==BACKWARDy:
				screensurf.blit(labtext, (160, 260))
	
def overlayscanB(xval, yval, xco, yco, drawfox=0, Qinside=0):
	
	
	for node in nodetag.findall("switch"):
		if int(node.attrib.get('x'))==xval and int(node.attrib.get('y'))==yval:
			keyid=node.attrib.get('keyid', "0")
			Qvis=node.attrib.get('area', "b")
			if Qvis=="i" and inside==1:
				ovvis=1
			elif Qvis=="o" and inside==0:
				ovvis=1
			elif Qvis=="b":
				ovvis=1
			else:
				ovvis=0
			
			if keyid!="0" and ovvis==1:
				if not keyid in keylist:
					screensurf.blit(switchoff, (xco, yco))
				elif keyid in keylist:
					screensurf.blit(switchon, (xco, yco))
	
	yshad=(yval + 1)
	shadblk=lookpoint(xval, yshad)
	curblk=lookpoint(xval, yval)
	nextblock=lookpoint(xval, (yval - 1))
	#depth hint engine:
	if shadblk!="z" and shadblk!="G":
		if curblk=="z":
			screensurf.blit(hintonsky, (xco, (yco)))
		if curblk=="G":
			screensurf.blit(SPECIALtilegrate, (xco, (yco)))
	if shadblk=="1" or shadblk=="R" or shadblk=="r"  or shadblk=="c"   or shadblk=="t" or shadblk=="C" or shadblk=="Q" or shadblk=="P" or shadblk=="Z" or shadblk=="H":
		if curblk!="1" and curblk!="R" and curblk!="C" and curblk!="c" and curblk!="t" and curblk!="r" and curblk!="Q" and curblk!="P" and curblk!="Z" and curblk!="H":
			if shadblk=="R" or shadblk=="Q":
				screensurf.blit(hintbuildout, (xco, (yco-8)))
			if shadblk=="1":
				screensurf.blit(hinthedge, (xco, (yco-8)))
			if shadblk=="C":
				screensurf.blit(hintcobble, (xco, (yco-8)))
			if shadblk=="r" or shadblk=="c" or shadblk=="t" or shadblk=="P" or shadblk=="Z" or shadblk=="H":
				if inside==0:
					screensurf.blit(hintdoor, (xco, (yco-8)))
	if inside==1:
		if shadblk=="R" or shadblk=="Q":
			if curblk=="t":
				screensurf.blit(hintbuild, (xco, (yco-8)))
			if curblk=="c":
				screensurf.blit(hintbuild, (xco, (yco-8)))
			if curblk=="r":
				screensurf.blit(hintbuild, (xco, (yco-8)))
			if curblk=="P":
				screensurf.blit(hintbuild, (xco, (yco-8)))
			if curblk=="Z":
				screensurf.blit(hintbuild, (xco, (yco-8)))
			if curblk=="H":
				screensurf.blit(hintbuildgreen, (xco, (yco-8)))
	for node in nodetag.findall("gate"):
		if int(node.attrib.get('x'))==xval and int(node.attrib.get('y'))==yval:
			keyid=node.attrib.get('keyid', "0")
			Qvis=node.attrib.get('area', "b")
			if Qvis=="i" and inside==1:
				ovvis=1
			elif Qvis=="o" and inside==0:
				ovvis=1
			elif Qvis=="b":
				ovvis=1
			else:
				ovvis=0
			if ovvis==1:
				if keyid!="0":
					if keyid in keylist:
						screensurf.blit(gateopen, (xco, (yco-8)))
					else:
						screensurf.blit(gateclosed, (xco, (yco-8)))
	for node in nodetag.findall("overlay"):
		xval=int(xval)
		yval=int(yval)
		QX=int(node.attrib.get('x'))
		QY=int(node.attrib.get('y'))
		Qtype=node.attrib.get('type')
		Qvis=node.attrib.get('area')
		Qrotate=node.attrib.get('rotate', "0")
		
		#keyid=node.attrib.get('keyid', "0")
		onkey=node.attrib.get('onkey', "0")
		offkey=node.attrib.get('offkey', "0")
		if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
			#if not keyid in keylist:
			#	keylist.extend([keyid])
			if Qvis=="i" and inside==1:
				ovvis=1
			elif Qvis=="o" and inside==0:
				ovvis=1
			elif Qvis=="b":
				ovvis=1
			else:
				ovvis=0
		else:
			ovvis=0
		labtextQ=overlayblit(Qtype, Qrotate)
		labtext=labtextQ[0]
		offsetflg=labtextQ[1]
		if ovvis==1:
			if QX==xval and QY==yval:
				#if Qrotate=="1":
				#	labtext=pygame.transform.rotate(labtext, 90)
				#if Qrotate=="2":
				#	labtext=pygame.transform.rotate(labtext, 180)
				#if Qrotate=="3":
				#	labtext=pygame.transform.rotate(labtext, 270)
				if offsetflg==0:
					screensurf.blit(labtext, (xco, yco))
				else:
					#print "foobar114"
					screensurf.blit(labtext, (xco, (yco-8)))
	#shadow engine
	if 0==0:
		if shadblk=="1" or shadblk=="R" or shadblk=="r"  or shadblk=="c"   or shadblk=="t" or shadblk=="C" or shadblk=="Q" or shadblk=="P" or shadblk=="Z" or shadblk=="H":
			if curblk!="1" and curblk!="R" and curblk!="C" and curblk!="c" and curblk!="t" and curblk!="r" and curblk!="Q" and curblk!="P" and curblk!="Z" and curblk!="H" and curblk!="z" and curblk!="G":
				if curblk=="w" or curblk=="l" or curblk=="X":
					screensurf.blit(wallliquidshadow, (xco, yco))
				else:
					screensurf.blit(wallshadow, (xco, yco))
		elif shadblk!="w" and shadblk!="l" and shadblk!="X" and shadblk!="x" and shadblk!="z":
			if curblk=="w" or curblk=="l" or curblk=="X":
				screensurf.blit(landshadow, (xco, yco))
	
	
	if drawfox==1:
		screensurf.blit(playerfuzzshad, (160, 180))
		if inside==1:
			if lastmove=="F":
				screensurf.blit(tileplayer, (160, 180))
			if lastmove=="B":
				screensurf.blit(tileplayerB, (160, 180))
			if lastmove=="L":
				screensurf.blit(tileplayerL, (160, 180))
			if lastmove=="R":
				screensurf.blit(tileplayerR, (160, 180))
		if inside==0:
			yshad=(playy + 1)
			shadblk=lookpoint(playx, yshad)
			curblk=lookpoint(playx, playy)
			if shadblk=="1" or shadblk=="R"  or shadblk=="r"  or shadblk=="c"   or shadblk=="t" or shadblk=="Q" or shadblk=="P" or shadblk=="Z" or shadblk=="H" or shadblk=="C":
				if curblk!="1" and curblk!="R" and curblk!="c" and curblk!="t" and curblk!="r" and curblk!="Q" and curblk!="P" and curblk!="H" and curblk!="Z" and curblk!="C":
					if lastmove=="F":
						screensurf.blit(shadtileplayer, (160, 180))
					if lastmove=="B":
						screensurf.blit(shadtileplayerB, (160, 180))
					if lastmove=="L":
						screensurf.blit(shadtileplayerL, (160, 180))
					if lastmove=="R":
						screensurf.blit(shadtileplayerR, (160, 180))
				else:
					if lastmove=="F":
						screensurf.blit(tileplayer, (160, 180))
					if lastmove=="B":
						screensurf.blit(tileplayerB, (160, 180))
					if lastmove=="L":
						screensurf.blit(tileplayerL, (160, 180))
					if lastmove=="R":
						screensurf.blit(tileplayerR, (160, 180))
			else:
				if lastmove=="F":
					screensurf.blit(tileplayer, (160, 180))
				if lastmove=="B":
					screensurf.blit(tileplayerB, (160, 180))
				if lastmove=="L":
					screensurf.blit(tileplayerL, (160, 180))
				if lastmove=="R":
					screensurf.blit(tileplayerR, (160, 180))
	if Qinside==0 and rgbafilterflg==1 and curblk!="z" and curblk!="G":
		if nextblock=="c" or nextblock=="t" or nextblock=="r" or nextblock=="P" or nextblock=="Z" or nextblock=="H":
				screensurf.blit(viewfiltertall, (xco, (yco-8)))
			#if inside==1:
			#	screensurf.blit(tileoutside, (xco, (yco-8)))
		else:
			if shadblk!="z" and shadblk!="G":
				screensurf.blit(viewfilter, (xco, (yco-8)))
			else:
				if nextblock=="z":
					screensurf.blit(viewfilter, (xco, (yco)))
				else:
					screensurf.blit(viewfiltershort, (xco, (yco)))
			#if inside==1:
			#	screensurf.blit(tileoutside, (xco, (yco-8)))
	for node in nodetag.findall("gem"):
		if int(node.attrib.get('x'))==xval and int(node.attrib.get('y'))==yval:
			onkey=node.attrib.get('onkey', "0")
			offkey=node.attrib.get('offkey', "0")
			if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
				gemtype=node.attrib.get('type', "gem")
				Qvis=node.attrib.get('area', "b")
				if Qvis=="i" and inside==1:
					ovvis=1
				elif Qvis=="o" and inside==0:
					ovvis=1
				elif Qvis=="b":
					ovvis=1
				else:
					ovvis=0
				
				if ovvis==1:
					if gemtype=="gem":
						screensurf.blit(objgem, (xco, yco))
					if gemtype=="redgem":
						screensurf.blit(objgemred, (xco, yco))
					if gemtype=="bluegem":
						screensurf.blit(objgemblue, (xco, yco))
					if gemtype=="greengem":
						screensurf.blit(objgemgreen, (xco, yco))
					if gemtype=="raingem":
						screensurf.blit(objgemrain, (xco, yco))
	
	
	
def labelscan(xoff=0, yoff=0):
	for node in nodetag.findall("label"):
		QX=int(node.attrib.get('x'))
		QY=int(node.attrib.get('y'))
		Qvis=node.attrib.get('area')
		if Qvis=="i" and inside==1:
			labvis=1
		elif Qvis=="o" and inside==0:
			labvis=1
		elif Qvis=="b":
			labvis=1
		else:
			labvis=0
		
		if labvis==1:
			if QX==LEFTWARD3x and QY==LEFTWARD3y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (80 + xoff, 20 + yoff))
			if QX==RIGHTWARD3x and QY==RIGHTWARD3y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (240 + xoff, 20 + yoff))
			if QX==FARLEFT3x and QY==FARLEFT3y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (0 + xoff, 20 + yoff))
			if QX==FARRIGHT3x and QY==FARRIGHT3y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (320 + xoff, 20 + yoff))
			if QX==FORWARD2x and QY==FORWARD2y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (160 + xoff, 20 + yoff))
			if QX==LEFTWARD2x and QY==LEFTWARD2y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (80 + xoff, 100 + yoff))
			if QX==RIGHTWARD2x and QY==RIGHTWARD2y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (240 + xoff, 100 + yoff))
			if QX==FARLEFT2x and QY==FARLEFT2y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (0 + xoff, 100 + yoff))
			if QX==FARRIGHT2x and QY==FARRIGHT2y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (320 + xoff, 100 + yoff))
			if QX==FORWARDx and QY==FORWARDy:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (160 + xoff, 100 + yoff))
			if QX==LEFTWARDx and QY==LEFTWARDy:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (80 + xoff, 180 + yoff))
			if QX==CENTERx and QY==CENTERy:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (160 + xoff, 180 + yoff))
			if QX==RIGHTWARDx and QY==RIGHTWARDy:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (240 + xoff, 180 + yoff))
			if QX==FARLEFTx and QY==FARLEFTy:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (0 + xoff, 180 + yoff))
			if QX==FARRIGHTx and QY==FARRIGHTy:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (320 + xoff, 180 + yoff))
			if QX==LEFTWARD0x and QY==LEFTWARD0y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (80 + xoff, 260 + yoff))
			if QX==RIGHTWARD0x and QY==RIGHTWARD0y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (240 + xoff, 260 + yoff))
			if QX==FARLEFT0x and QY==FARLEFT0y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (0 + xoff, 260 + yoff))
			if QX==FARRIGHT0x and QY==FARRIGHT0y:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (320 + xoff, 260 + yoff))
			if QX==BACKWARDx and QY==BACKWARDy:
				labtext = simplefont.render((node.attrib.get('text')), True, (255, 255, 255), (0, 0, 0))
				screensurf.blit(labtext, (160 + xoff, 260 + yoff))
	
#old function to draw tile grid

#function used to wait for a keystroke at the win screen
def winscreenwait():
	while True:
		time.sleep(.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				return()

def resolvescreenscale():
	if scrnx<scrny:
		return(scrnx)
	elif scrny<scrnx:
		return(scrny)
	else:
		return(scrny)

def convscreenwait(XQscrez, sxw, sxh, nillx):
	QLsteps=0
	while True:
		time.sleep(.1)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key != K_UP and event.key != K_DOWN and event.key != K_LEFT and event.key != K_RIGHT and event.key != K_w and event.key != K_a and event.key != K_s and  event.key != K_d:
				return([0, 0, 0, 0])
			if event.type == KEYDOWN and nillx==1:
				return([0, 0, 0, 0])
			if event.type == VIDEORESIZE:
				sxh=event.h
				if sxh<400:
					sxh=400
				#sxratio=(sxh-400)
				#sxw=int(sxratio + 400)
				sxw=event.w
				if sxw<400:
					sxw=400
				if sxw<sxh:
					XQscrez=sxw
				elif sxh<sxw:
					XQscrez=sxh
				else:
					XQscrez=sxh
				screensurfdex=pygame.display.set_mode((sxw, sxh), RESIZABLE)
				#print "vod"
				return([1, sxw, sxh, XQscrez])
				
		QLsteps +=1
		#print QLsteps
		if QLsteps == 10 and nillx==0:
			return([2, sxw, sxh, XQscrez])
		if QLsteps == 20 and nillx==1:
			return([2, sxw, sxh, XQscrez])
			


#datapoint lookup function. used to read data points from the main .grid file.
#when the point i out-of-range. 1 is returned.
def lookpoint(lookptx, lookpty):
	lineycnt=1
	linexcnt=1
	
	lookupdef=setuptag.attrib.get("defaulttile", "1")
	lookuppointis=lookupdef
	m.seek(0)
	for lineylst in m:
		if lineycnt==lookpty:
			for linexlst in lineylst:
				if linexcnt==lookptx:
					lookuppointis = linexlst
				linexcnt += 1
		lineycnt += 1
	if lookuppointis=="\n":
		lookuppointis=lookupdef
	return (lookuppointis)

#used by wall detection logic. modified to simplify wall detection.
#wether a tile is walkable is determined HERE
def lookpointB(lookptx, lookpty):
	lineycnt=1
	linexcnt=1
	lookuppointis='1'
	m.seek(0)
	for lineylst in m:
		if lineycnt==lookpty:
			for linexlst in lineylst:
				if linexcnt==lookptx:
					lookuppointis = linexlst
				linexcnt += 1
		lineycnt += 1
	if lookuppointis=="w":
		lookuppointis='1'
	if lookuppointis=="l":
		lookuppointis='1'
	if lookuppointis=="z":
		lookuppointis='1'
	if lookuppointis=="X":
		lookuppointis='1'
	if lookuppointis=="C":
		lookuppointis='1'
	if lookuppointis=="Q":
		lookuppointis='1'
	if lookuppointis=="\n":
		lookuppointis='1'
	if lookuppointis=="g":
		lookuppointis='0'
	if lookuppointis=="s":
		lookuppointis='0'
	if lookuppointis=="e":
		lookuppointis='0'
	if lookuppointis=="S":
		lookuppointis='0'
	if lookuppointis=="D":
		lookuppointis='0'
	if lookuppointis=="G":
		lookuppointis='0'
	if lookuppointis=="d":
		lookuppointis='0'
	if lookuppointis=="B":
		lookuppointis='0'
	if lookuppointis=="b":
		lookuppointis='0'
	if lookuppointis=="R":
		lookuppointis='1'
	if lookuppointis=="c":
		lookuppointis='0'
	if lookuppointis=="r":
		lookuppointis='0'
	if lookuppointis=="t":
		lookuppointis='0'
	if lookuppointis=="P":
		lookuppointis='0'
	if lookuppointis=="Z":
		lookuppointis='0'
	if lookuppointis=="H":
		lookuppointis='0'
	for node in nodetag.findall("gate"):
		if int(node.attrib.get('x'))==lookptx and int(node.attrib.get('y'))==lookpty:
			keyid=node.attrib.get('keyid', "0")
			if keyid!="0":
				if keyid in keylist:
					lookuppointis="0"
				else:
					lookuppointis="1"
			
			break
	for node in nodetag.findall("walkable"):
		if int(node.attrib.get('x'))==lookptx and int(node.attrib.get('y'))==lookpty:
			onkey=node.attrib.get('onkey', "0")
			offkey=node.attrib.get('offkey', "0")
			if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
				showlooktext=1
				lookuppointis=node.attrib.get('force')
				break
	return (lookuppointis)

def debugcon():
	print "Rhennevad Maze DEBUG CONSOLE ACTIVE"
	print "type return to return to gameplay."
	USRCMD="null"
	global pointcnt
	global keylist
	while USRCMD!=("return"):
		USRENTRYLINE = raw_input(':')
		USRLST=USRENTRYLINE.split(" ", 1)
		try:
			USRCMD=(USRLST[0])
		except IndexError:
			USRCMD=""
		try:
			USRTEXT=(USRLST[1])
		except IndexError:
			USRTEXT=""
		if (USRCMD==("keys")):
			print "current keylist:"
			print keylist
		if (USRCMD==("info")):
			print "playx:" + str(playx)
			print "playy:" + str(playy)
			print "score:" + str(pointcnt)
			print "mazexml:" + mazefilepath
			print "mazegrid:" + mazemodpath
			print "mazename:" + mazetitle
			print "defaulttile: " + setuptag.attrib.get("defaulttile", "1")
			print "startx: " + (setuptag.find('startposx')).text
			print "starty: " + (setuptag.find('startposy')).text
		if (USRCMD==("give") and USRTEXT!=""):
			if not USRTEXT in keylist:
				keylist.extend([USRTEXT])
		if (USRCMD==("setpoints") and USRTEXT!=""):
			pointcnt=int(USRTEXT)
		if (USRCMD==("addpoints") and USRTEXT!=""):
			pointcnt += int(USRTEXT)
		if (USRCMD==("take") and USRTEXT!=""):
			if USRTEXT in keylist:
				keylist.remove(USRTEXT)
		if (USRCMD==("about")):
			print '''about:
Rhennevad Maze
v6.0.0
(c) 2015-2017 Thomas Leathers


Rhennevad Maze is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Rhennevad Maze is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Rhennevad Maze.  If not, see <http://www.gnu.org/licenses/>.
'''
		
		if (USRCMD==("help")):
			print '''Help:
Rhennevad Maze Debug console commands:

keys: print current keylist
give [keyid]: grant a keyid
take [keyid]: take a keyid
setpoints [points]: manually set point total
addpoints [points]: manually add to point total.
info: engine status info.)
return: return to gameplay.
help: this text.
(be sure to double check any manual changes!)
'''
#function that draws text at the bottom of the display
def drawfoottext(textto, linemode):
	text = simplefont.render(textto, True, (255, 255, 255), (0, 0, 0))
	if linemode==0:
		screensurf.blit(text, (0, 340))
	if linemode==1:
		screensurf.blit(text, (0, 353))
#function that draws text at the top of the display
def drawheadertext(textto, linemode):
	text = simplefont.render(textto, True, (255, 255, 255), (0, 0, 0))
	if linemode==0:
		screensurf.blit(text, (0, 0))
	if linemode==1:
		screensurf.blit(text, (0, 12))
#main input reading function
showlooktext=0
def keyread():
	keyscantime=0
	foob=0
	while True:
		time.sleep(.05)
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == K_w:
				return(FORWARDWORDBIND)
			if event.type == KEYDOWN and event.key == K_a:
				return(LEFTWORDBIND)
			if event.type == KEYDOWN and event.key == K_s:
				return(BACKWARDWORDBIND)
			if event.type == KEYDOWN and event.key == K_d:
				return(RIGHTWODBIND)
			if event.type == KEYDOWN and event.key == K_ESCAPE:
				return(QUITWORDBIND)
			if event.type == QUIT:
				return(QUITWORDBIND)
			if event.type == KEYDOWN and event.key == K_UP and (pygame.key.get_mods() & KMOD_SHIFT or pygame.key.get_mods() & KMOD_CAPS) and DEBUG==1:
				return("debugF")
			if event.type == KEYDOWN and event.key == K_LEFT and (pygame.key.get_mods() & KMOD_SHIFT or pygame.key.get_mods() & KMOD_CAPS) and DEBUG==1:
				return("debugL")
			if event.type == KEYDOWN and event.key == K_DOWN and (pygame.key.get_mods() & KMOD_SHIFT or pygame.key.get_mods() & KMOD_CAPS) and DEBUG==1:
				return("debugB")
			if event.type == KEYDOWN and event.key == K_RIGHT and (pygame.key.get_mods() & KMOD_SHIFT or pygame.key.get_mods() & KMOD_CAPS) and DEBUG==1:
				return("debugR")
			if event.type == KEYDOWN and event.key == K_z and pygame.key.get_mods() & KMOD_SHIFT and DEBUG==1:
				return("debugcon")
			if event.type == KEYDOWN and event.key == K_x and pygame.key.get_mods() & KMOD_SHIFT and DEBUG==1:
				return("debugrefresh")
			if event.type == KEYDOWN and event.key == K_UP:
				return(FORWARDWORDBIND)
			if event.type == KEYDOWN and event.key == K_LEFT:
				return(LEFTWORDBIND)
			if event.type == KEYDOWN and event.key == K_DOWN:
				return(BACKWARDWORDBIND)
			if event.type == KEYDOWN and event.key == K_RIGHT:
				return(RIGHTWODBIND)
			if event.type == KEYDOWN and event.key == K_1:
				return("resize1")
			if event.type == KEYDOWN and event.key == K_2:
				return("resize2")
			if event.type == KEYDOWN and event.key == K_3:
				return("resize3")
			if event.type == KEYDOWN and event.key == K_4:
				return("resize4")
			if event.type == KEYDOWN and event.key == K_5:
				return("resize5")
			if event.type == KEYDOWN and event.key == K_6:
				return("resize6")
			if event.type == VIDEORESIZE:
				sxh=event.h
				if sxh<400:
					sxh=400
				#sxratio=(sxh-400)
				sxw=event.w
				#sxw=int(sxratio + 400)
				if sxw<400:
					sxw=400
				#if sxw<sxh:
				#	sxw=sxh
				screensurfdex=pygame.display.set_mode((sxw, sxh), RESIZABLE)
				return("evresize")
			#if event.type == KEYDOWN and event.key == K_l:
			#	return("l")
			#if event.type == KEYDOWN and event.key == K_t:
			#	return("t")
			if event.type == KEYDOWN and event.key == K_SPACE:
				return("space")
			if event.type == KEYDOWN and event.key == K_e:
				return("space")
			if keyscantime==20:
				return("redraw")
			if event.type == KEYDOWN:
				keyscantime +=1
				foob=1
		if keyscantime==20:
			return("redraw")
		if foob==0:
			keyscantime +=1

def popuptext(textto):
	text = simplefontB.render(textto, True, (255, 255, 255), (0, 0, 0))
	textbox = text.get_rect()
	textbox.centerx=screensurf.get_rect().centerx
	textbox.centery=380
	screensurf.blit(text, textbox)
	
def playchar(ismoving=0):
	if ismoving==0:
		PL=tileplayer
		PLB=tileplayerB
		PLL=tileplayerL
		PLR=tileplayerR
		SPL=shadtileplayer
		SPLB=shadtileplayerB
		SPLL=shadtileplayerL
		SPLR=shadtileplayerR
	else:
		PL=tileplayerstep
		PLB=tileplayerBstep
		PLL=tileplayerLstep
		PLR=tileplayerRstep
		SPL=shadtileplayerstep
		SPLB=shadtileplayerBstep
		SPLL=shadtileplayerLstep
		SPLR=shadtileplayerRstep
	screensurf.blit(playerfuzzshad, (160, 180))
	if inside==1:
		if lastmove=="F":
			screensurf.blit(PL, (160, 180))
		if lastmove=="B":
			screensurf.blit(PLB, (160, 180))
		if lastmove=="L":
			screensurf.blit(PLL, (160, 180))
		if lastmove=="R":
			screensurf.blit(PLR, (160, 180))
	if inside==0:
		yshad=(playy + 1)
		shadblk=lookpoint(playx, yshad)
		curblk=lookpoint(playx, playy)
		if shadblk=="1" or shadblk=="R"  or shadblk=="r"  or shadblk=="c"   or shadblk=="t" or shadblk=="Q" or shadblk=="P" or shadblk=="Z" or shadblk=="H" or shadblk=="C":
			if curblk!="1" and curblk!="R" and curblk!="c" and curblk!="t" and curblk!="r" and curblk!="Q" and curblk!="P" and curblk!="H" and curblk!="Z" and curblk!="C":
				if lastmove=="F":
					screensurf.blit(SPL, (160, 180))
				if lastmove=="B":
					screensurf.blit(SPLB, (160, 180))
				if lastmove=="L":
					screensurf.blit(SPLL, (160, 180))
				if lastmove=="R":
					screensurf.blit(SPLR, (160, 180))
			else:
				if lastmove=="F":
					screensurf.blit(PL, (160, 180))
				if lastmove=="B":
					screensurf.blit(PLB, (160, 180))
				if lastmove=="L":
					screensurf.blit(PLL, (160, 180))
				if lastmove=="R":
					screensurf.blit(PLR, (160, 180))
		else:
			if lastmove=="F":
				screensurf.blit(PL, (160, 180))
			if lastmove=="B":
				screensurf.blit(PLB, (160, 180))
			if lastmove=="L":
				screensurf.blit(PLL, (160, 180))
			if lastmove=="R":
				screensurf.blit(PLR, (160, 180))
	
filmscx1=pygame.Surface((400, 400), SRCALPHA)

def playcharfilmsc(ismoving=0):
	if ismoving==0:
		PL=tileplayer
		PLB=tileplayerB
		PLL=tileplayerL
		PLR=tileplayerR
		SPL=shadtileplayer
		SPLB=shadtileplayerB
		SPLL=shadtileplayerL
		SPLR=shadtileplayerR
	else:
		PL=tileplayerstep
		PLB=tileplayerBstep
		PLL=tileplayerLstep
		PLR=tileplayerRstep
		SPL=shadtileplayerstep
		SPLB=shadtileplayerBstep
		SPLL=shadtileplayerLstep
		SPLR=shadtileplayerRstep
	filmscx1.blit(playerfuzzshadSC, (160, 180))
	if inside==1:
		if lastmove=="F":
			filmscx1.blit(PL, (160, 180))
		if lastmove=="B":
			filmscx1.blit(PLB, (160, 180))
		if lastmove=="L":
			filmscx1.blit(PLL, (160, 180))
		if lastmove=="R":
			filmscx1.blit(PLR, (160, 180))
	if inside==0:
		yshad=(playy + 1)
		shadblk=lookpoint(playx, yshad)
		curblk=lookpoint(playx, playy)
		if shadblk=="1" or shadblk=="R"  or shadblk=="r"  or shadblk=="c"   or shadblk=="t" or shadblk=="Q" or shadblk=="P" or shadblk=="Z" or shadblk=="H" or shadblk=="C":
			if curblk!="1" and curblk!="R" and curblk!="c" and curblk!="t" and curblk!="r" and curblk!="Q" and curblk!="P" and curblk!="H" and curblk!="Z" and curblk!="C":
				if lastmove=="F":
					filmscx1.blit(SPL, (160, 180))
				if lastmove=="B":
					filmscx1.blit(SPLB, (160, 180))
				if lastmove=="L":
					filmscx1.blit(SPLL, (160, 180))
				if lastmove=="R":
					filmscx1.blit(SPLR, (160, 180))
			else:
				if lastmove=="F":
					filmscx1.blit(PL, (160, 180))
				if lastmove=="B":
					filmscx1.blit(PLB, (160, 180))
				if lastmove=="L":
					filmscx1.blit(PLL, (160, 180))
				if lastmove=="R":
					filmscx1.blit(PLR, (160, 180))
		else:
			if lastmove=="F":
				filmscx1.blit(PL, (160, 180))
			if lastmove=="B":
				filmscx1.blit(PLB, (160, 180))
			if lastmove=="L":
				filmscx1.blit(PLL, (160, 180))
			if lastmove=="R":
				filmscx1.blit(PLR, (160, 180))
def convdup(convtext):
	textchunk=""
	Qscrnx=scrnx
	Qscrny=scrny
	Qscrez=screz
	tiptextmask=simplefontB.render(tiptext, True, (0, 0, 0), (0, 0, 0))
	tiptextmaskbox = tiptextmask.get_rect()
	tiptextmaskbox.centerx=screensurf.get_rect().centerx
	tiptextmaskbox.centery=380
	
	screensurf.blit(tiptextmask, tiptextmaskbox)
	textcont=(convtext + "\n")
	screensurfbak=screensurf.copy()
	fodchange=0
	for texch in textcont:
		#print texch
		if texch=="\n":
			popuptext(textchunk)
			textchunk=""
			bdropQ=pygame.transform.scale(bdrop, (screz, screz))
			screensurfdex.blit(bdropQ, (0, 0))
			screensurfQ=pygame.transform.scale(screensurf, (Qscrez, Qscrez))
			screensurfdex.blit(screensurfQ, (0, 0))
			pygame.display.update()
			retwile=0
			Qcont=0
			while Qcont==0:
				retwile=convscreenwait(Qscrez, Qscrnx, Qscrny, 0)
				if retwile[0]==1:
					Qscrnx=retwile[1]
					Qscrny=retwile[2]
					fodchange=1
					Qscrez=retwile[3]
					#screensurfQ=pygame.transform.scale(screensurf, (Qscrez, Qscrez))
					#screensurfdex.blit(screensurfQ, (0, 0))
					#pygame.display.update()
				elif  retwile[0]==2:
					Qscrnx=retwile[1]
					Qscrny=retwile[2]
					Qscrez=retwile[3]
					bdropQ=pygame.transform.scale(bdrop, (screz, screz))
					screensurfdex.blit(bdropQ, (0, 0))
					screensurfQ=pygame.transform.scale(screensurf, (Qscrez, Qscrez))
					screensurfdex.blit(screensurfQ, (0, 0))
					pygame.display.update()
				else:
					Qcont=1
					bdropQ=pygame.transform.scale(bdrop, (screz, screz))
					screensurfdex.blit(bdropQ, (0, 0))
					screensurfQ=pygame.transform.scale(screensurf, (Qscrez, Qscrez))
					screensurfdex.blit(screensurfQ, (0, 0))
					pygame.display.update()
			
			screensurf.blit(screensurfbak, (0, 0))
			#print "ping"
		else:
			textchunk=(textchunk + texch)
			#print "pong"
	return(fodchange)

#paralax used by sky tiles
#dont use both axis at same time!
def surfscroll(texture, xoff, yoff):
	parjump=20
	tempsurf=pygame.Surface((80, 80))
	tempsurf.blit(texture, (0,0))
	if xoff=="+":
		tempsurf.blit(texture, (-60,0))
		tempsurf.blit(texture, (20,0))
	if xoff=="-":
		tempsurf.blit(texture, (-20,0))
		tempsurf.blit(texture, (60,0))
	if yoff=="+":
		tempsurf.blit(texture, (0, -60))
		tempsurf.blit(texture, (0, 20))
	if yoff=="-":
		tempsurf.blit(texture, (0, -20))
		tempsurf.blit(texture, (0, 60))
	return tempsurf

def cloudflow(texture, xoff, yoff):
	parjump=10
	tempsurf=pygame.Surface((80, 80))
	tempsurf.blit(texture, (0,0))
	if xoff=="+":
		tempsurf.blit(texture, (-70,0))
		tempsurf.blit(texture, (10,0))
	if xoff=="-":
		tempsurf.blit(texture, (-10,0))
		tempsurf.blit(texture, (70,0))
	if yoff=="+":
		tempsurf.blit(texture, (0, -70))
		tempsurf.blit(texture, (0, 10))
	if yoff=="-":
		tempsurf.blit(texture, (0, -10))
		tempsurf.blit(texture, (0, 70))
	return tempsurf

def fluidflow(texture, xoff, yoff):
	parjump=3
	tempsurf=pygame.Surface((80, 80))
	tempsurf.blit(texture, (0,0))
	if xoff=="+":
		tempsurf.blit(texture, (-77,0))
		tempsurf.blit(texture, (3,0))
	if xoff=="-":
		tempsurf.blit(texture, (-3,0))
		tempsurf.blit(texture, (77,0))
	if yoff=="+":
		tempsurf.blit(texture, (0, -77))
		tempsurf.blit(texture, (0, 3))
	if yoff=="-":
		tempsurf.blit(texture, (0, -3))
		tempsurf.blit(texture, (0, 77))
	return tempsurf

def fluidscroll(texture, xoff, yoff):
	parjump=2
	tempsurf=pygame.Surface((80, 80))
	tempsurf.blit(texture, (0,0))
	if xoff=="+":
		tempsurf.blit(texture, (-79,0))
		tempsurf.blit(texture, (1,0))
	if xoff=="-":
		tempsurf.blit(texture, (-1,0))
		tempsurf.blit(texture, (79,0))
	if yoff=="+":
		tempsurf.blit(texture, (0, -79))
		tempsurf.blit(texture, (0, 1))
	if yoff=="-":
		tempsurf.blit(texture, (0, -1))
		tempsurf.blit(texture, (0, 79))
	return tempsurf
#old test data
#if lookpoint(2, 2)==('0'):
#	print ('blah')
#print (lookpoint(2, 2))
cantmoveflg=0
#main loop
forksanity=0
tiptext=""
showtiptext=0
hudfacedef="1"
forksanitycheck=0
points=0
keylist=["null"]
keybak=["null"]
skiploop=1
usrentry="null"
loopskipstop=0
scoretext = simplefont.render(str(pointcnt), True, (0, 0, 0))

screensufbak=screensurf.copy()
hudfacesel=hudfacecasual

screz=resolvescreenscale()
while gameend==('0'):
	#POV coordinate determination
	#stageZ
	
	POVbackxZ = playx
	POVbackyZ = playy - 2
	POVleftxZ = playx + 1
	POVleftyZ = playy - 2
	fPOVleftxZ = playx + 2
	fPOVleftyZ = playy - 2
	POVrightxZ = playx - 1
	POVrightyZ = playy - 2
	fPOVrightxZ = playx - 2
	fPOVrightyZ = playy - 2
	#stage0
	POVleftx0 = playx + 1
	POVlefty0 = playy - 1
	fPOVleftx0 = playx + 2
	fPOVlefty0 = playy - 1
	POVrightx0 = playx - 1
	POVrighty0 = playy - 1
	fPOVrightx0 = playx - 2
	fPOVrighty0 = playy - 1
	#stage1
	POVforwardx = playx
	POVforwardy = playy + 1
	POVbackx = playx
	POVbacky = playy - 1
	POVleftx = playx + 1
	POVlefty = playy
	POVrightx = playx - 1
	POVrighty = playy
	fPOVleftx = playx + 2
	fPOVlefty = playy
	fPOVrightx = playx - 2
	fPOVrighty = playy
	#stage2
	POVleftx2 = playx + 1
	POVlefty2 = playy + 1
	POVrightx2 = playx - 1
	POVrighty2 = playy + 1
	fPOVleftx2 = playx + 2
	fPOVlefty2 = playy + 1
	fPOVrightx2 = playx - 2
	fPOVrighty2 = playy + 1
	POVforwardx2 = playx
	POVforwardy2 = playy + 2
	#stage3
	POVleftx3 = playx + 1
	POVlefty3 = playy + 2
	POVrightx3 = playx - 1
	POVrighty3 = playy + 2
	fPOVleftx3 = playx + 2
	fPOVlefty3 = playy + 2
	fPOVrightx3 = playx - 2
	fPOVrighty3 = playy + 2
	POVforwardx3 = playx
	POVforwardy3 = playy + 3
	#POV point lookup
	#stageZ
	LEFTWARDZ = lookpoint(POVleftxZ, POVleftyZ)
	LEFTWARDZx=POVleftxZ
	LEFTWARDZy=POVleftyZ
	RIGHTWARDZ = lookpoint(POVrightxZ, POVrightyZ)
	RIGHTWARDZx=POVrightxZ
	RIGHTWARDZy=POVrightyZ
	FARLEFTZ = lookpoint(fPOVleftxZ, fPOVleftyZ)
	FARLEFTZx=fPOVleftxZ
	FARLEFTZy=fPOVleftyZ
	FARRIGHTZ = lookpoint(fPOVrightxZ, fPOVrightyZ)
	FARRIGHTZx=fPOVrightxZ
	FARRIGHTZy=fPOVrightyZ
	BACKWARDZ = lookpoint(POVbackxZ, POVbackyZ)
	BACKWARDZx=POVbackxZ
	BACKWARDZy=POVbackyZ
	#stage0
	LEFTWARD0 = lookpoint(POVleftx0, POVlefty0)
	LEFTWARD0x=POVleftx0
	LEFTWARD0y=POVlefty0
	RIGHTWARD0 = lookpoint(POVrightx0, POVrighty0)
	RIGHTWARD0x=POVrightx0
	RIGHTWARD0y=POVrighty0
	FARLEFT0 = lookpoint(fPOVleftx0, fPOVlefty0)
	FARLEFT0x=fPOVleftx0
	FARLEFT0y=fPOVlefty0
	FARRIGHT0 = lookpoint(fPOVrightx0, fPOVrighty0)
	FARRIGHT0x=fPOVrightx0
	FARRIGHT0y=fPOVrighty0
	#stage1
	FORWARD = lookpoint(POVforwardx, POVforwardy)
	FORWARDx=POVforwardx
	FORWARDy=POVforwardy
	BACKWARD = lookpoint(POVbackx, POVbacky)
	BACKWARDx=POVbackx
	BACKWARDy=POVbacky
	LEFTWARD = lookpoint(POVleftx, POVlefty)
	LEFTWARDx=POVleftx
	LEFTWARDy=POVlefty
	RIGHTWARD = lookpoint(POVrightx, POVrighty)
	RIGHTWARDx=POVrightx
	RIGHTWARDy=POVrighty
	FARLEFT = lookpoint(fPOVleftx, fPOVlefty)
	FARLEFTx=fPOVleftx
	FARLEFTy=fPOVlefty
	FARRIGHT = lookpoint(fPOVrightx, fPOVrighty)
	FARRIGHTx=fPOVrightx
	FARRIGHTy=fPOVrighty
	#stage2
	FORWARD2 = lookpoint(POVforwardx2, POVforwardy2)
	FORWARD2x=POVforwardx2
	FORWARD2y=POVforwardy2
	LEFTWARD2 = lookpoint(POVleftx2, POVlefty2)
	LEFTWARD2x=POVleftx2
	LEFTWARD2y=POVlefty2
	RIGHTWARD2 = lookpoint(POVrightx2, POVrighty2)
	RIGHTWARD2x=POVrightx2
	RIGHTWARD2y=POVrighty2
	FARLEFT2 = lookpoint(fPOVleftx2, fPOVlefty2)
	FARLEFT2x=fPOVleftx2
	FARLEFT2y=fPOVlefty2
	FARRIGHT2 = lookpoint(fPOVrightx2, fPOVrighty2)
	FARRIGHT2x=fPOVrightx2
	FARRIGHT2y=fPOVrighty2
	#stage3
	FORWARD3 = lookpoint(POVforwardx3, POVforwardy3)
	FORWARD3x=POVforwardx3
	FORWARD3y=POVforwardy3
	LEFTWARD3 = lookpoint(POVleftx3, POVlefty3)
	LEFTWARD3x=POVleftx3
	LEFTWARD3y=POVlefty3
	RIGHTWARD3 = lookpoint(POVrightx3, POVrighty3)
	RIGHTWARD3x=POVrightx3
	RIGHTWARD3y=POVrighty3
	FARLEFT3 = lookpoint(fPOVleftx3, fPOVlefty3)
	FARLEFT3x=fPOVleftx3
	FARLEFT3y=fPOVlefty3
	FARRIGHT3 = lookpoint(fPOVrightx3, fPOVrighty3)
	FARRIGHT3x=fPOVrightx3
	FARRIGHT3y=fPOVrighty3
	
	CENTER = lookpoint(playx, playy)
	CENTERx=playx
	CENTERy=playy
	#leftscroll
	LBACKxPOV=playx -3
	LBACKyPOV=playy -2
	LBACK= lookpoint(LBACKxPOV, LBACKyPOV)
	#inside view tiles declared here (walls should not be specified)
	if CENTER=="c" or CENTER=="r" or CENTER=="t" or CENTER=="P" or CENTER=="Z" or CENTER=="H":
		inside=1
	elif CENTER=="3":
		print "nochange intereor flag"
	else:
		inside=0
	
	
	
	
	#if debugset==('1'):
	#	print ("F:" + FORWARD + " B:" + BACKWARD)
	#	print ("L:" + LEFTWARD + " R:" + RIGHTWARD)
	#	print ("F2:" + FORWARD2 + " L2:" + LEFTWARD2 + " R2:" + RIGHTWARD2)
	#	print ("F3:" + FORWARD3 + " L3:" + LEFTWARD3 + " R3:" + RIGHTWARD3)
	# 3 stage maze drawing function.
	#Maze shufflescroll. 
	
	
	if cantmoveflg==0 and movescrlflg==1 and skiploop==0 and forksanitycheck==0 and (usrentry==LEFTWORDBIND or usrentry==RIGHTWODBIND or usrentry==FORWARDWORDBIND or usrentry==BACKWARDWORDBIND):
		xgrdvar=0
		ygrdvar=0
		
		bdropQ=pygame.transform.scale(bdrop, (screz, screz)).convert()
		filmscx1.fill((0, 0, 0, 0))
		filmscx1.blit(gamebg, (0, 0))
		filmscx1.blit(hudfacesel, (54, 340))
		filmscx1.blit(huggem, (90, 340))
		filmscx1.blit(scoretext, (100, 340))
		playcharfilmsc(1)
		screensurfUI=pygame.transform.scale(filmscx1, (screz, screz)).convert_alpha()
		if scfast==1:
			scgrp=[1]
		else:
			scgrp=[1, 2]
		for f in scgrp:
			#screensurf.blit(screensufbak, (0, 0))
			screensurf.fill((0, 0, 0, 0))
			screenscrollbx.fill((0, 0, 0, 0))
			screensurf.blit(screensufbak, (0, 0))
			if usrentry==LEFTWORDBIND:

				xgrdvar += 20
				#xgrdvar=lgrdvar
			if usrentry==RIGHTWODBIND:
				xgrdvar -= 20
				#xgrdvar=rgrdvar
			if usrentry==FORWARDWORDBIND:
				ygrdvar += 20
				#ygrdvar=ugrdvar
			if usrentry==BACKWARDWORDBIND:
				ygrdvar -= 20
			#screensufbak=screensurf.copy()
			
			#playchar(1)
			screenscrollbx.blit(screensurf, (xgrdvar, ygrdvar))
			#screensurf.blit(filmscx1, (0, 0))
			screensurfQ=pygame.transform.scale(screenscrollbx, (screz, screz)).convert_alpha()
			#screensurfdex.fill((0, 0, 100))
			bdrect=screensurfdex.blit(bdropQ, (0, 0))
			screensurfdex.blit(screensurfQ, (0, 0))
			screensurfdex.blit(screensurfUI, (0, 0))
			pygame.display.update([bdrect])
			time.sleep(0.00025)
			#time.sleep(0.1)
	
		#paralax skybelow scrollers
	if cantmoveflg==0:
		tilesky1aqua.set_alpha(255)
		if usrentry==LEFTWORDBIND:
			tilesky1=surfscroll(tilesky1, "+", "0")
			tilesky1aqua=surfscroll(tilesky1aqua, "+", "0")
			tilelava=fluidscroll(tilelava, "+", "0")
			tilewater=fluidscroll(tilewater, "+", "0")
			tilegreengoo=fluidscroll(tilegreengoo, "+", "0")
		if usrentry==RIGHTWODBIND:
			tilesky1=surfscroll(tilesky1, "-", "0")
			tilesky1aqua=surfscroll(tilesky1aqua, "-", "0")
			tilelava=fluidscroll(tilelava, "-", "0")
			tilewater=fluidscroll(tilewater, "-", "0")
			tilegreengoo=fluidscroll(tilegreengoo, "-", "0")
		if usrentry==FORWARDWORDBIND:
			tilesky1=surfscroll(tilesky1, "0", "+")
			tilesky1aqua=surfscroll(tilesky1aqua, "0", "-")
			tilelava=fluidscroll(tilelava, "0", "+")
			tilewater=fluidscroll(tilewater, "0", "+")
			tilegreengoo=fluidscroll(tilegreengoo, "0", "+")
		if usrentry==BACKWARDWORDBIND:
			tilesky1=surfscroll(tilesky1, "0", "-")
			tilesky1aqua=surfscroll(tilesky1aqua, "0", "-")
			tilelava=fluidscroll(tilelava, "0", "-")
			tilewater=fluidscroll(tilewater, "0", "-")
			tilegreengoo=fluidscroll(tilegreengoo, "0", "-")
		tilesky1aqua.set_alpha(40)
	#screensurf.fill((100, 120, 100))
	#screensurf=pygame.Surface((400, 400), SRCALPHA)
	screensurf.fill((0, 0, 0, 0))
	tilegriddraw3()
	screensufbak=screensurf.copy()
	screensurf.blit(gamebg, (0, 0))
	
	scoretext = simplefont.render(str(pointcnt), True, (0, 0, 0))
	screensurf.blit(huggem, (90, 340))
	screensurf.blit(scoretext, (100, 340))
	
	#if cantmoveflg==1:
		#drawheadertext(CANTMOVE, 1)
	if showlooktext==1:
		#drawheadertext(looktext, 1)
		popuptext(looktext)
		if lookquiet=="0":
			mipfx.play()
	if showtiptext==1:
		#drawheadertext(looktext, 1)
		popuptext(tiptext)
		
	if hudface=="1":
		hudfacesel=hudfacecasual
	elif hudface=="2":
		hudfacesel=hudfacesad
	elif hudface=="3":
		hudfacesel=hudfaceangry
	elif hudface=="4":
		hudfacesel=hudfaceshock
	elif hudface=="5":
		hudfacesel=hudfacehappy
	elif hudface=="6":
		hudfacesel=hudfacebored
	#hudfacesel=pygame.transform.scale(hudfacesel, (30, 30))
	screensurf.blit(hudfacesel, (54, 340))
	hudface=hudfacedef
		
	#screensufbak=screensurf.copy()
	playchar()
	#drawheadertext(("Text-Maze 5 | " + mazetitle), 0)
	#print(libtextmaze.mazedraw3(FORWARD, BACKWARD, LEFTWARD, RIGHTWARD, FORWARD2, LEFTWARD2, RIGHTWARD2, FORWARD3, LEFTWARD3, RIGHTWARD3))
	#pygame.display.update()
	pygame.event.pump()
	#this should be here! it needs to happen after the screen update, and before the userentry stuff!
	for node in nodetag.findall("trigconv"):
		if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
			convtext=node.text
			hudface=node.attrib.get('face', "1")
			keyid=node.attrib.get('keyid', "0")
			takekey=node.attrib.get('takekey', "0")
			onkey=node.attrib.get('onkey', "0")
			offkey=node.attrib.get('offkey', "0")
			if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
				debugmsg("conv node:", 1)
				if hudface=="1":
					hudfacesel=hudfacecasual
				elif hudface=="2":
					hudfacesel=hudfacesad
				elif hudface=="3":
					hudfacesel=hudfaceangry
				elif hudface=="4":
					hudfacesel=hudfaceshock
				elif hudface=="5":
					hudfacesel=hudfacehappy
				if not keyid in keylist:
					keylist.extend([keyid])
				if takekey in keylist and takekey!="0":
					keylist.remove([takekey])
				screensurf.blit(hudfacesel, (54, 340))
				hudface=hudfacedef
				fodx=convdup(convtext)
				if fodx==1:
					scrnx=screensurfdex.get_width()
					scrny=screensurfdex.get_height()
					screz=resolvescreenscale()
				break
		
	
	usrentry = ('null')
	#user prompt loop
	pygame.event.clear()
	drawtime=0
	if skiploop==0:
		while (usrentry!=FORWARDWORDBIND and usrentry!=BACKWARDWORDBIND and usrentry!=LEFTWORDBIND and usrentry!=RIGHTWODBIND and usrentry!=QUITWORDBIND and usrentry!="l" and usrentry!="t" and usrentry!="debugF" and usrentry!="debugB" and usrentry!="debugL" and usrentry!="debugR" and usrentry!="space"):
			#drawfoottext(("forward:" + FORWARDWORDBIND + " | backward:" + 	BACKWARDWORDBIND + " | look around: l | talk: t"), 0)
			#drawfoottext(("left:" + LEFTWORDBIND + " | right:" + RIGHTWODBIND + " | quit:" + QUITWORDBIND), 1)
			if usrentry=="resize1":
				screensurfdex=pygame.display.set_mode((400, 400), RESIZABLE)
				scrnx=400
				scrny=400
				screz=resolvescreenscale()
			if usrentry=="resize2":
				screensurfdex=pygame.display.set_mode((600, 600), RESIZABLE)
				scrnx=600
				scrny=600
				screz=resolvescreenscale()
			if usrentry=="resize3":
				screensurfdex=pygame.display.set_mode((700, 700), RESIZABLE)
				scrnx=700
				scrny=700
				screz=resolvescreenscale()
			if usrentry=="resize4":
				screensurfdex=pygame.display.set_mode((800, 800), RESIZABLE)
				scrnx=800
				scrny=800
				screz=resolvescreenscale()
			if usrentry=="resize5":
				screensurfdex=pygame.display.set_mode((1000, 1000), RESIZABLE)
				scrnx=1000
				scrny=1000
				screz=resolvescreenscale()
			if usrentry=="resize6":
				screensurfdex=pygame.display.set_mode((1200, 1200), RESIZABLE)
				scrnx=1200
				scrny=1200
				screz=resolvescreenscale()
			if usrentry=="evresize":
				scrnx=screensurfdex.get_width()
				scrny=screensurfdex.get_height()
				screz=resolvescreenscale()
				#print scrny
				#print screz
			if usrentry=="debugrefresh":
				print ("DEBUGMODE: RELOADING NODES AND FORKS FROM XML FILE!")
				print ("loading data from:" + mazefilepath)
				tree = ET.parse(mazefilepath)
				root = tree.getroot()
				setuptag=root.find('setup')
				nodetag=root.find('nodes')
				forktag=root.find('forks')
				print ("DEBUGMODE: RELOADING main.grid FROM FILE")
				m = open(mazemodpath)
				break
				
				
				
			if usrentry=="debugcon":
				debugcon()
				break
			#drawtime += 1
			if usrentry=="redraw":
				tilesky1=cloudflow(tilesky1, "+", "0")
				tilelava=fluidflow(tilelava, "+", "0")
				tilewater=fluidflow(tilewater, "+", "0")
				tilegreengoo=fluidflow(tilegreengoo, "+", "0")
				screensurf=pygame.Surface((400, 400), SRCALPHA).convert_alpha()
				screensurf.fill((0, 0, 0, 0))
				tilegriddraw3()
				screensurf.blit(gamebg, (0, 0))
				screensurf.blit(huggem, (90, 340))
				screensurf.blit(scoretext, (100, 340))
				
				screensurf.blit(hudfacesel, (54, 340))
				if showlooktext==1:
					#drawheadertext(looktext, 1)
					popuptext(looktext)
					showlooktext=0
				if showtiptext==1:
					#drawheadertext(looktext, 1)
					popuptext(tiptext)
					showtiptext=0
				playchar()
				debugmsg("Input timeout, redraw display, flow fluids and clouds")
			
			screensurfQ=pygame.transform.scale(screensurf, (screz, screz))
			bdropQ=pygame.transform.scale(bdrop, (screz, screz))
			screensurfdex.blit(bdropQ, (0, 0))
			screensurfdex.blit(screensurfQ, (0, 0))
			pygame.display.update()
			usrentry=keyread()
	else:
		loopskipstop=1
		
	if showlooktext==1:
		#drawheadertext(looktext, 1)
		showlooktext=0
	if showtiptext==1:
					#drawheadertext(looktext, 1)
		showtiptext=0
	#print (chr(27) + "[2J" + chr(27) + "[H")
	#wall detection logic
	cantmoveflg=0
	if usrentry==BACKWARDWORDBIND:
		BIND1 = playy - 1
		if lookpointB(playx, BIND1)==('1'):
			cantmoveflg=1
			lastmove="B"
		elif lookpointB(playx, BIND1)==('0'):
			playy -= 1
			lastmove="B"
		elif lookpointB(playx, BIND1)==('3'):
			playy -= 1
			lastmove="B"
	if usrentry==FORWARDWORDBIND:
		BIND2 = playy + 1
		if lookpointB(playx, BIND2)==('1'):
			cantmoveflg=1
			lastmove="F"
		elif lookpointB(playx, BIND2)==('0'):
			playy += 1
			lastmove="F"
		elif lookpointB(playx, BIND2)==('3'):
			playy += 1
			lastmove="F"
	if usrentry==LEFTWORDBIND:
		BIND4 = playx + 1
		if lookpointB(BIND4, playy)==('1'):
			cantmoveflg=1
			lastmove="L"
		elif lookpointB(BIND4, playy)==('0'):
			playx += 1
			lastmove="L"
		elif lookpointB(BIND4, playy)==('3'):
			playx += 1
			lastmove="L"
	if usrentry==RIGHTWODBIND:
		BIND3 = playx - 1
		if lookpointB(BIND3, playy)==('1'):
			cantmoveflg=1
			lastmove="R"
		elif lookpointB(BIND3, playy)==('0'):
			playx -= 1
			lastmove="R"
		elif lookpointB(BIND3, playy)==('3'):
			playx -= 1
			lastmove="R"
	if usrentry=="debugF":
		playy += 1
		lastmove="F"
	if usrentry=="debugB":
		playy -= 1
		lastmove="B"
	if usrentry=="debugL":
		playx += 1
		lastmove="L"
	if usrentry=="debugR":
		playx -= 1
		lastmove="R"
	#misic user commands
	#print ("player x:" + str(playx) + "player y:" + str(playy))
	
	
	
	
	for node in nodetag.findall("trig"):
		if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
			keyid=node.attrib.get('keyid', "0")
			takekey=node.attrib.get('takekey', "0")
			onkey=node.attrib.get('onkey', "0")
			offkey=node.attrib.get('offkey', "0")
			lookquiet=node.attrib.get('quiet', "0")
			if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
				showlooktext=1
				if not keyid in keylist:
					keylist.extend([keyid])
				if takekey in keylist and takekey!="0":
					keylist.remove(takekey)
				looktext=node.attrib.get('text')
				hudface=node.attrib.get('face', "1")
				debugmsg("Triggered statement(trig): ", 1)
				break
	for node in nodetag.findall("gem"):
		if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
			onkey=node.attrib.get('onkey', "0")
			offkey=node.attrib.get('offkey', "0")
			if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
				gemtype=node.attrib.get('type', "gem")
				
				if gemtype=="gem":
					pointcnt += 100
				if gemtype=="redgem":
					pointcnt += 300
				if gemtype=="bluegem":
					pointcnt += 600
				if gemtype=="greengem":
					pointcnt += 1200
				if gemtype=="raingem":
					pointcnt += 10000
				nodetag.remove(node)
				if gemtype=="raingem":
					supergemfx.play()
				else:
					gemfx.play()
				#print pointcnt
	if usrentry=="l" or usrentry=="space":
		for node in nodetag.findall("look"):
			if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
				looktext=node.attrib.get('text')
				takekey=node.attrib.get('takekey', "0")
				keyid=node.attrib.get('keyid', "0")
				onkey=node.attrib.get('onkey', "0")
				offkey=node.attrib.get('offkey', "0")
				lookquiet=node.attrib.get('quiet', "0")
				if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
					showlooktext=1
					if not keyid in keylist:
						keylist.extend([keyid])
					if takekey in keylist and takekey!="0":
						keylist.remove(takekey)
					hudface=node.attrib.get('face', "1")
					debugmsg("look statement(look): ", 1)
					break
		for node in nodetag.findall("switch"):
			if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
				keyid=node.attrib.get('keyid', "0")
				if keyid!="0":
					if not keyid in keylist:
						switchonfx.play()
						keylist.extend([keyid])
						debugmsg("switchon")
					elif keyid in keylist:
						debugmsg("switchoff")
						switchofffx.play()
						keylist.remove(keyid)
		
		for node in nodetag.findall("itemlist"):
			if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
				onkey=node.attrib.get('onkey', "0")
				offkey=node.attrib.get('offkey', "0")
				if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
					itemlisth=45
					itemlisthjmp=16
					itemhead=node.attrib.get('listname')
					popuptext(itemhead)
					for listitm in node.findall("i"):
						hideon=listitm.attrib.get('hideon', "0")
						keyid=listitm.attrib.get('keyid')
						itemtext=listitm.attrib.get('text')
						
						if (hideon=="0" and keyid in keylist) or (hideon=="1" and keyid not in keylist):
							print itemtext
							itemtextren=simplefontB.render(itemtext, True, (255, 255, 255), (0, 0, 0))
							screensurf.blit(itemtextren, (10, itemlisth))
							itemlisth += itemlisthjmp
					screensurfQ=pygame.transform.scale(screensurf, (screz, screz))
					screensurfdex.blit(screensurfQ, (0, 0))
					pygame.display.update()
					retwile=convscreenwait(screz, scrnx, scrny, 1)
					if retwile[0]==1:
						scrnx=retwile[1]
						scrny=retwile[2]
						fodchange=1
							
				
	
	if usrentry=="t" or usrentry=="space":
		for node in nodetag.findall("conv"):
			if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
				convtext=node.text
				hudface=node.attrib.get('face', "1")
				keyid=node.attrib.get('keyid', "0")
				takekey=node.attrib.get('takekey', "0")
				onkey=node.attrib.get('onkey', "0")
				offkey=node.attrib.get('offkey', "0")
				if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
					debugmsg("conv node:", 1)
					if hudface=="1":
						hudfacesel=hudfacecasual
					elif hudface=="2":
						hudfacesel=hudfacesad
					elif hudface=="3":
						hudfacesel=hudfaceangry
					elif hudface=="4":
						hudfacesel=hudfaceshock
					elif hudface=="5":
						hudfacesel=hudfacehappy
					if not keyid in keylist:
						keylist.extend([keyid])
					if takekey in keylist and takekey!="0":
						keylist.remove([takekey])
					screensurf.blit(hudfacesel, (54, 340))
					hudface=hudfacedef
					fodx=convdup(convtext)
					if fodx==1:
						scrnx=screensurfdex.get_width()
						scrny=screensurfdex.get_height()
						screz=resolvescreenscale()
					break
	else:
		for node in nodetag.findall("conv"):
			if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
				
				onkey=node.attrib.get('onkey', "0")
				offkey=node.attrib.get('offkey', "0")
				if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
					showtiptext=1
					tiptext="press [action] to talk."
	
	if skiploop!=1:
		for node in nodetag.findall("teleport"):
			if int(node.attrib.get('x'))==playx and int(node.attrib.get('y'))==playy:
				onkey=node.attrib.get('onkey', "0")
				offkey=node.attrib.get('offkey', "0")
				if ((onkey=="0" and offkey=="0") or (onkey=="0" and offkey not in keylist) or (onkey in keylist and offkey=="0") or (onkey in keylist and offkey not in keylist)):
					debugmsg("Teleport node:")
					debugmsg("start pos:", 1)
					playx=int(node.attrib.get('destx'))
					playy=int(node.attrib.get('desty'))
					debugmsg("end pos:", 1)
					skiploop=1
					break
	if keylist!=keybak or forksanitycheck==1:
		#Forking logic
		debugmsg("keyid change detected. reparsing forks.")
		for fork in forktag.findall("ortrig"):
			#print "batchtrig"
			masterkey=fork.attrib.get("keyid")
			orflg=0
			for keyif in fork.findall("k"):
				ifpol=keyif.attrib.get("if")
				subkey=keyif.attrib.get("keyid")
				if subkey in keylist:
					if ifpol=="1":
						orflg=1
				elif not subkey in keylist:
					if ifpol=="0":
						orflg=1
			if orflg == 1:
				if not masterkey in keylist:
					keylist.extend([masterkey])
					#print keylist
					keyprint()
					forksanity=1
			else:
				if masterkey in keylist:
					keylist.remove(masterkey)
					#print keylist
					keyprint()
					forksanity=1
		for fork in forktag.findall("batchtrig"):
			#print "batchtrig"
			masterkey=fork.attrib.get("keyid")
			complist=[1] 
			for keyif in fork.findall("k"):
				ifpol=keyif.attrib.get("if")
				subkey=keyif.attrib.get("keyid")
				if subkey in keylist:
					if ifpol=="1":
						complist.extend([1])
					else:
						complist.extend([0])
				elif not subkey in keylist:
					if ifpol=="0":
						complist.extend([1])
					else:
						complist.extend([0])
			if len(set(complist)) == 1:
				if not masterkey in keylist:
					keylist.extend([masterkey])
					#print keylist
					keyprint()
					forksanity=1
			else:
				if masterkey in keylist:
					keylist.remove(masterkey)
					#print keylist
					keyprint()
					forksanity=1
		for fork in forktag.findall("batchset"):
			#print "batch"
			#print fork
			masterkey=fork.attrib.get("keyid")
			toggpol=fork.attrib.get("set")
			if masterkey in keylist:
				keylist.remove(masterkey)
				if toggpol=="1":
					for subkey in fork.findall("k"):
						subkeyid=subkey.attrib.get("keyid")
						if not subkeyid in keylist:
							keylist.extend([subkeyid])
							#print keylist
							keyprint()
					forksanity=1
				elif toggpol=="2":
					for subkey in fork.findall("k"):
						subkeyid=subkey.attrib.get("keyid")
						if not subkeyid in keylist:
							keylist.extend([subkeyid])
							#print keylist
							keyprint()
						elif subkeyid in keylist:
							keylist.remove(subkeyid)
							#print keylist
							keyprint()
					forksanity=1
				else:
					for subkey in fork.findall("k"):
						subkeyid=subkey.attrib.get("keyid")
						if subkeyid in keylist:
							keylist.remove(subkeyid)
							#print keylist
							keyprint()
					forksanity=1
		for fork in forktag.findall("triggerlock"):
			masterkey=fork.attrib.get("keyid")
			triggerkey=fork.attrib.get("trigger")
			lockkey=fork.attrib.get("lock")
			if masterkey in keylist:
				#keylist.remove(masterkey)
				if lockkey not in keylist:
					if triggerkey not in keylist:
						keylist.extend([triggerkey])
						keylist.extend([lockkey])
						forksanity=1
		for fork in forktag.findall("addpoints"):
			masterkey=fork.attrib.get("keyid")
			adpointscnt=int(fork.attrib.get("points"))
			if masterkey in keylist:
				pointcnt += adpointscnt
				keylist.remove(masterkey)
		for fork in forktag.findall("pointtrig"):
			masterkey=fork.attrib.get("keyid")
			pointthr=int(fork.attrib.get("points"))
			if masterkey not in keylist and pointcnt>=pointthr:
				keylist.extend([masterkey])
			else:
				if pointcnt<pointthr:
					keylist.remove(masterkey)
		if forksanity==1:
			forksanitycheck=1
			forksanity=0
			skiploop=1
		else:
			forksanitycheck=0
	keybak=list(keylist)
	if loopskipstop==1:
		skiploop=0
		loopskipstop=0
	if playx<1:
		playx=1
		debugmsg("ERROR: player x pos illegal value. correcting.")
	if playy<1:
		debugmsg("ERROR: player y pos illegal value. correcting.")
		playy=1
	if usrentry==QUITWORDBIND:
		gameend=('1')
		debugmsg("User Has Quit.")
	#plays footstep sound fx
	if (cantmoveflg==0 and usrentry!=QUITWORDBIND and usrentry!="l" and usrentry!="space"and usrentry!="t" and usrentry!="null"):
		stepfx.play()
		if usrentry=="debugF" or usrentry=="debugB" or usrentry=="debugL" or usrentry=="debugR":
			debugmsg("Player DEBUG move:", 1)
		else:
			debugmsg("Player move:", 1)
	#game win check
	if lookpoint(playx, playy)=='3':
		#print(WINGAME)
		pygame.mixer.music.stop()
		levelwinfx.play()
		debugmsg("User has reached an exit tile.")
		wintext = simplefont.render("Press a key.", True, (255, 255, 255), (0, 0, 0))
		wintextbox = wintext.get_rect()
		wintextbox.centerx = screensurf.get_rect().centerx
		wintextbox.centery = ((screensurf.get_rect().centery))
		winscreenbox = winscreen.get_rect()
		winscreenbox.centerx = screensurf.get_rect().centerx
		winscreenbox.centery = ((screensurf.get_rect().centery) - 60)
		screensurf.blit(winscreen, winscreenbox)
		screensurf.blit(wintext, wintextbox)
		screensurfQ=pygame.transform.scale(screensurf, (screz, screz))
		screensurfdex.blit(screensurfQ, (0, 0))
		pygame.display.update()
		pygame.event.clear()
		winscreenwait()
		gameend=1
		
		

