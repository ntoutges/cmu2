from backend import *

Rect(0,0, 400,400, fill="silver")
c = Rect(200,200, 50,50, align="center")
c.dr = 2

# l = Line(100,100, 300,300)

def onStep():
    # l.rotateAngle += 5
  c.rotateAngle += 5
  c.width += c.dr
  if not (0 < c.width + c.dr < 350):
    c.dr *= -1

app.__canvas__.doClear = False
app.__canvas__.subPx = 2
app.__canvas__.superPx = 1
app.__canvas__.size = 114

app.drawingsPerSecond = 30
app.__run__(onStep)
