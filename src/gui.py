import wx
import time
import copy
import random
import worldKarel


app = wx.App()

frame = wx.Frame(None, -1, 'Aladdin - Karel Game')
size = (720 , 740)
frame.SetSize(size)
frame.Show()

# Paint world
aladdinDown = wx.Image('images/down.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
aladdinUp = wx.Image('images/up.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
aladdinRight = wx.Image('images/right.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
aladdinLeft = wx.Image('images/left.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
aladdinDownBeep = wx.Image('images/downbeeper.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
aladdinUpBeep = wx.Image('images/upbeeper.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
aladdinRightBeep = wx.Image('images/rightbeeper.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
aladdinLeftBeep = wx.Image('images/leftbeeper.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
free = wx.Image('images/free.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
bad = wx.Image('images/bad1.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
beeper = wx.Image('images/beeper.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()
bad2 = wx.Image('images/bad2.png', wx.BITMAP_TYPE_ANY).ConvertToBitmap()


copyWorld = list()

def repaint(world):
    '''
        This function update the world to its current state
    '''
    global frame, copyWorld
    if not copyWorld:
        print "no tengo un copyworld"
        newWorldPrint(world)
    else:
        for i,row in enumerate(world):
            for j,val in enumerate(row):
                if not copyWorld[i][j] == val:
                    if any(isinstance(x, worldKarel.Karel) for x in val):
                        copyVal=val[:]
                        last=copyVal.pop()
                        while(not isinstance(last,worldKarel.Karel)):
                            last=copyVal.pop() 
                        if last.beepers > 0:
                            if last.facing=="up":
                                wx.StaticBitmap(frame,-1, aladdinUpBeep, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                            elif last.facing=="down":
                                wx.StaticBitmap(frame,-1, aladdinDownBeep, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                            elif last.facing=="right":
                                wx.StaticBitmap(frame,-1, aladdinRightBeep, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                            else:
                                wx.StaticBitmap(frame,-1, aladdinLeftBeep, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                        else:
                            if last.facing=="up":
                                wx.StaticBitmap(frame,-1, aladdinUp, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                            elif last.facing=="down":
                                wx.StaticBitmap(frame,-1, aladdinDown, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                            elif last.facing=="right":
                                wx.StaticBitmap(frame,-1, aladdinRight, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                            else:
                                wx.StaticBitmap(frame,-1, aladdinLeft, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                    elif 'B' in val:
                        wx.StaticBitmap(frame,-1, beeper, (j*70,i*70), (beeper.GetWidth(), beeper.GetHeight()))
                    else:
                        wx.StaticBitmap(frame,-1, free, (j*70,i*70), (free.GetWidth(), free.GetHeight()))
        copyWorld = copy.deepcopy(world)

def newWorldPrint(world):
    '''
        This function paints the first state of the world
    '''
    global frame,copyWorld
    for i,row in enumerate(world):
        for j,val in enumerate(row):
            if 'x' in val:
                wx.StaticBitmap(frame,-1, bad, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
            elif any(isinstance(x, worldKarel.Karel) for x in val):
                copyVal=val[:]
                last=copyVal.pop()
                while(not isinstance(last,worldKarel.Karel)):
                    last=copyVal.pop() 
                if last.beepers > 0:
                    if last.facing=="up":
                        wx.StaticBitmap(frame,-1, aladdinUpBeep, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                    elif last.facing=="down":
                        wx.StaticBitmap(frame,-1, aladdinDownBeep, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                    elif last.facing=="right":
                        wx.StaticBitmap(frame,-1, aladdinRightBeep, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                    else:
                        wx.StaticBitmap(frame,-1, aladdinLeftBeep, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                else:
                    if last.facing=="up":
                        wx.StaticBitmap(frame,-1, aladdinUp, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                    elif last.facing=="down":
                        wx.StaticBitmap(frame,-1, aladdinDown, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                    elif last.facing=="right":
                        wx.StaticBitmap(frame,-1, aladdinRight, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                    else:
                        wx.StaticBitmap(frame,-1, aladdinLeft, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
            elif 'B' in val:
                wx.StaticBitmap(frame,-1, beeper, (j*70,i*70), (beeper.GetWidth(), beeper.GetHeight()))
            else:
                wx.StaticBitmap(frame,-1, free, (j*70,i*70), (free.GetWidth(), free.GetHeight()))

    #time.sleep(0.1)
    #frame.Refresh()
    copyWorld = copy.deepcopy(world)

def paintFinalWorld(world):
    '''
        This function paints the final state of the world
    '''
    global frame
    for i,row in enumerate(world):
        for j,val in enumerate(row):
            if 'x' in val:
                wx.StaticBitmap(frame,-1, bad, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
            elif any(isinstance(x, worldKarel.Karel) for x in val):
                copyVal=val[:]
                last=copyVal.pop()
                while(not isinstance(last,worldKarel.Karel)):
                    last=copyVal.pop() 
                if last.beepers > 0:
                    if last.facing=="up":
                        wx.StaticBitmap(frame,-1, aladdinUpBeep, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                    elif last.facing=="down":
                        wx.StaticBitmap(frame,-1, aladdinDownBeep, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                    elif last.facing=="right":
                        wx.StaticBitmap(frame,-1, aladdinRightBeep, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                    else:
                        wx.StaticBitmap(frame,-1, aladdinLeftBeep, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                else:
                    if last.facing=="up":
                        wx.StaticBitmap(frame,-1, aladdinUp, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                    elif last.facing=="down":
                        wx.StaticBitmap(frame,-1, aladdinDown, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                    elif last.facing=="right":
                        wx.StaticBitmap(frame,-1, aladdinRight, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
                    else:
                        wx.StaticBitmap(frame,-1, aladdinLeft, (j*70,i*70), (bad.GetWidth(), bad.GetHeight()))
            elif 'B' in val:
                wx.StaticBitmap(frame,-1, beeper, (j*70,i*70), (beeper.GetWidth(), beeper.GetHeight()))
            else:
                wx.StaticBitmap(frame,-1, free, (j*70,i*70), (free.GetWidth(), free.GetHeight()))
    print
    print "End of program"
    app.MainLoop()


