from backend import *

c = Rect(200,200, 50,50)
c.dr = 4

def onStep():
  c.rotateAngle += 5
  c.width += c.dr
  if not (0 < c.width + c.dr < 800):
    c.dr *= -1

app.__canvas__.doClear = False
app.__canvas__.subPx = 2

app.drawingsPerSecond = 10
app.__run__(onStep)
