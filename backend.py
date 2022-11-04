import math
import os
import sys
import time
from intensities import _intensities
from rules import *
import asciiDefs

class Canvas:

  def __init__(self, size, *, debug=False):
    self.size = size  # width/height of canvas
    self.doClear = True
    self.__prevRender__ = ""
    self.subPx = 1
    self.superPx = 1

    self.yStep = 400 * 2 / (self.size * self.subPx)

    self.mapSet = asciiDefs.standard1

    if debug:
      self.mapSet = asciiDefs.debug1

  # TODO: NEEDS optimization  
  def __draw__(self):
    buffer = []
    yStep = 400 * 2 / (self.size * self.subPx)
    self.yStep = yStep
    xStep = 400 / (self.size * self.subPx)

    app.group.__resolveConflicts__()
    for y in range(0, int(self.size * self.subPx / 2) + 1):
      buffer.append([])
      for x in range(0, self.size*self.subPx + 1):
        buffer[y].append(0)
        val = app.group.__getPxAt__(x * xStep, y * yStep)
        buffer[y][x] = val[0] * val[1]  # treats background as white

    if self.subPx > 1:
      avgBuffer = []
      subPxSq = self.subPx ** 2
      for i in range(0, len(buffer) - self.subPx, self.subPx):
        avgBuffer.append([])
        for j in range(0, len(buffer[i]) - self.subPx, self.subPx):
          total = 0
          for x in range(self.subPx):
            for y in range(self.subPx):
              total += buffer[i+x][j+y]
          avgBuffer[-1].append(total / subPxSq)
      buffer = avgBuffer
    
    render = ""
    for row in buffer:
      subRender = ""
      for col in row:
        for set in self.mapSet:
          if col >= set[0]:
            subRender += set[1] * self.superPx
            break
        else:
          if (self.mapSet[-1][1] == "\\s"):
            subRender += str(int(col)) * self.superPx
          else:
            subRender += self.mapSet[-1][1] * self.superPx
      render += (subRender + "\n") * self.superPx

    if render != self.__prevRender__:
      if self.doClear:
        os.system("cls")
      sys.stdout.write(render)
      sys.stdout.flush()

    self.__prevRender__ = render


class Shape:

  def __init__(self, /, cx, cy, **kwargs):
    self.centerX = cx
    self.centerY = cy
    self.fill = kwargs.get("fill", "black")
    self.rotateAngle = kwargs.get("rotateAngle", 0)
    self.opacity = kwargs.get("opacity", 100)

    if self.fill is None:
      self.fill = "black"

    self.__old__ = {}

    self.__setProps__()

    align = kwargs.get("align", "center")
    ValidAlign.validityCheck(align, "in Shape.align")

    # if cx == 0:
      # raise ValueError("stop")
    if "left" in align:
      self.left = self.centerX
    elif "right" in align:
      self.right = self.centerY
    if "top" in align:
      self.top = self.centerX
    elif "bottom" in align:
      self.bottom = self.centerX
    self.__resolveConflicts__()

    if (kwargs.get("_add", True)):
      app.group.add(self)

  def __setProps__(self):
    self.__setDims__()

    ValidColor.validityCheck(self.fill, "Shape.fill")
    ValidNum0To100.validityCheck(self.opacity, "Shape.opacity")

    self._fill = _intensities.get(self.fill, 0)

    self.__old__ = {
      "centerX": self.centerX,
      "centerY": self.centerY,
      "top": self.top,
      "bottom": self.bottom,
      "right": self.right,
      "left": self.left,
      "fill": self.fill,
      "rotateAngle": self.rotateAngle,
      "opacity": self.opacity,
      "updateFlag": False
    }

  def __setDims__(self):
    self.top = self.centerY
    self.bottom = self.centerY
    self.left = self.centerX
    self.right = self.centerX

    self._cos = math.cos(self.rotateAngle * math.pi / 180)
    self._sin = math.sin(self.rotateAngle * math.pi / 180)

  def __resolveConflicts__(self):
    old = self.__old__
    modified = False

    if old["left"] != self.left:
      modified = True
      self.centerX += self.left - old["left"]
    elif old["right"] != self.right:
      modified = True
      self.centerX += self.right - old["right"]
    if old["top"] != self.top:
      modified = True
      self.centerY += self.top - old["top"]
    elif old["bottom"] != self.bottom:
      modified = True
      self.centerY += self.bottom - old["bottom"]

    # if old["rotateAngle"] != self.rotateAngle or old["fill"] != self.fill:
    #   modified = True

    if old["rotateAngle"] != self.rotateAngle:
      modified = True

    if modified or old["updateFlag"]:
      self.__setProps__()

  def __getPxAt__(x, y):
    return 0, 0  # black, invisible


class Group(Shape):

  def __init__(self, *shapes, _add=True):
    self.centerX = 0
    self.centerY = 0

    self._shapes = []
    super().__init__(0, 0, fill=None, _add=_add)

    for shape in shapes:
      self.add(shape)

  def __setProps__(self):
    self.centerX = 0
    self.centerY = 0
    super().__setProps__()
    for shape in self._shapes:
      self.centerX += shape.centerX
      self.centerY += shape.centerY

      self.top = min(shape.top, self.top)
      self.bottom = max(shape.bottom, self.bottom)
      self.left = min(shape.left, self.left)
      self.right = max(shape.right, self.right)

    if len(self._shapes) != 0:
      self.centerX /= len(self._shapes)
      self.centerY /= len(self._shapes)

    self.__old__ = {
      "centerX": self.centerX,
      "centerY": self.centerY,
      "top": self.top,
      "bottom": self.bottom,
      "right": self.right,
      "left": self.left,
      "fill": self.fill,
      "rotateAngle": self.rotateAngle,
      "opacity": self.opacity
    }

  def __resolveConflicts__(self):
    old = self.__old__

    modified = False
    for shape in self._shapes:
      if old["centerX"] != self.centerX:
        modified = True
        shape.centerX += self.centerX - old["centerX"]
      elif old["left"] != self.left:
        modified = True
        shape.centerX += self.left - old["left"]
      elif old["right"] != self.right:
        modified = True
        shape.centerX += self.right - old["right"]
      if old["centerY"] != self.centerY:
        modified = True
        shape.centerY += self.centerY - old["centerY"]
      elif old["top"] != self.top:
        modified = True
        shape.top += self.top - old["top"]
      elif old["bottom"] != self.bottom:
        modified = True
        shape.bottom += self.bottom - old["bottom"]

      if old["rotateAngle"] != self.rotateAngle:
        modified = True

      if old["opacity"] != self.opacity:
        modified = True
        shape.opacity = self.opacity

      # if modified:
      #   shape.__setProps__()
      shape.__resolveConflicts__()
      # if old["fill"] != self.fill:
      #   shape.fill = self.fill
      # if old["rotateAngle"] != self.rotateAngle:
      #   shape.rotateAngle = self.rotateAngle

    if modified:
      self.__setProps__()

  def __getPxAt__(self, x, y):
    x_m = (x - self.centerX) * self._cos + (
      y - self.centerY) * self._sin + self.centerX
    y_m = (y - self.centerY) * self._cos - (
      x - self.centerX) * self._sin + self.centerY

    # self.__resolveConflicts__()

    value = 0, 0
    for shape in reversed(self._shapes):
      if value[1] == 1:
        break

      pxVal = shape.__getPxAt__(x_m, y_m)
      if pxVal[1] > 0:
        opacity = value[1] + (1 - value[1])*pxVal[1]

        newVal = value[0]
        if opacity != 0:
          newVal = (pxVal[0] * pxVal[1]*(1-value[1]) + value[0] * value[1]) / opacity
        value = newVal, opacity

    return value

  def __iter__(self):
    return self._shapes.__iter__()

  def __next__(self):
    return self._shapes.__next__()

  def add(self, shape):
    ValidClass.validityCheck(shape, "shape in Group.add(shape)", Shape)

    try:
      app.group.remove(shape)
    except:
      pass
    self._shapes.append(shape)
    self.__setProps__()

  def remove(self, shape):
    self._shapes.remove(shape)
    self.__setProps__()

  def clear(self):
    self._shapes.clear()
    self.__setProps__()


class Circle(Shape):

  def __init__(self, /, cx, cy, radius, **kwargs):
    self.radius = radius
    
    super().__init__(cx, cy, **kwargs)

  def __setProps__(self):
    ValidPositiveNum.validityCheck(self.radius, "Circle.radius")
    super().__setProps__()

  def __setDims__(self):
    self.top = self.centerY - self.radius
    self.bottom = self.centerY + self.radius
    self.left = self.centerX - self.radius
    self.right = self.centerX + self.radius

    self._cos = math.cos(self.rotateAngle * math.pi / 180)
    self._sin = math.sin(self.rotateAngle * math.pi / 180)

  def __getPxAt__(self, x, y):
    if (x - self.centerX)**2 + (y - self.centerY)**2 <= self.radius**2:
      return self._fill, (self.opacity / 100)
    return 0, 0

  def __str__(self):
    return "Circle"


class Oval(Shape):

  def __init__(self, /, cx, cy, width, height, **kwargs):
    self.width = width
    self.height = height

    ValidPositiveNum.validityCheck(width, "Oval.width")
    ValidPositiveNum.validityCheck(height, "Oval.height")
    
    super().__init__(cx, cy, **kwargs)

  def __setProps__(self):
    # self.__setDims__()
    super().__setProps__()

  def __getDims__(self):
    self.top = self.centerY - self.height / 2
    self.bottom = self.centerY + self.height / 2
    self.left = self.centerX - self.width / 2
    self.right = self.centerX + self.width / 2

  def __getPxAt__(self, x, y):
    # self.__resolveConflicts__()
    x -= self.centerX
    y -= self.centerY

    if ((x * self._cos + y * self._sin) / (self.width / 2))**2 + ((x * self._sin - y * self._cos) / (self.height / 2))**2 <= 1:
      return self._fill, (self.opacity / 100)
    return 0, 0

  def __str__(self):
    return "Oval"


class Rect(Shape):

  def __init__(self, /, cx, cy, width, height, **kwargs):
    # cx = x + width / 2
    # cy = y + height / 2

    self.width = width
    self.height = height

    ValidPositiveNum.validityCheck(width, "Rect.width")
    ValidPositiveNum.validityCheck(height, "Rect.height")
    
    kwargs.setdefault("align", "left-top")
    super().__init__(cx, cy, **kwargs)

  def __setProps__(self):
    # self.__setDims__()
    super().__setProps__()

  def __setDims__(self):
    self.top = self.centerY - self.height / 2
    self.bottom = self.centerY + self.height / 2
    self.left = self.centerX - self.width / 2
    self.right = self.centerX + self.width / 2

    self._cos = math.cos(self.rotateAngle * math.pi / 180)
    self._sin = math.sin(self.rotateAngle * math.pi / 180)

  def __getPxAt__(self, x, y):
    # self.__resolveConflicts__()
    x_m = (x - self.centerX) * self._cos + (y - self.centerY) * self._sin
    y_m = (y - self.centerY) * self._cos - (x - self.centerX) * self._sin

    width2 = self.width * 0.5
    height2 = self.height * 0.5

    if -width2 <= x_m <= width2 and -height2 <= y_m <= height2:
      return self._fill, (self.opacity / 100)
    return 0, 0

class Line(Shape):
  def __init__(self, x1,y1, x2,y2, **kwargs):
    self.x1 = x1
    self.x2 = x2
    self.y1 = y1
    self.y2 = y2

    super().__init__(x1,x2, **kwargs)
  
  def __resolveConflicts__(self):
    if self.__old__["x1"] != self.x1 or self.__old__["x2"] != self.x2 or self.__old__["y1"] != self.y1 or self.__old__["y2"] != self.y2:
      self.__old__["updateFlag"] = True
    super().__resolveConflicts__()

  def __setProps__(self):
    super().__setProps__()
    
    self.__old__["x1"] = self.x1
    self.__old__["x2"] = self.x2
    self.__old__["y1"] = self.y1
    self.__old__["y2"] = self.y2

  def __setDims__(self):
    self.left = min(self.x1, self.x2)
    self.right = max(self.x1, self.x2)
    self.top = min(self.y1, self.y2)
    self.bottom = max(self.y1, self.y2)

    self._length = ((self.x1 - self.x2)**2 + (self.y1 - self.y2) ** 2) ** 0.5

    self._angleOff = math.pi * 0.5
    if self.x1 != self.x2:
      self._angleOff = math.atan( (self.y2-self.y1) / (self.x1-self.x2) )

    self._cos = math.cos(self.rotateAngle * math.pi / 180 - self._angleOff)
    self._sin = math.sin(self.rotateAngle * math.pi / 180 - self._angleOff)
    
    self.centerX = (self.x1 + self.x2) / 2
    self.centerY = (self.y1 + self.y2) / 2

  def __getPxAt__(self, x, y):
    x_m = (x - self.centerX) * self._cos + (y - self.centerY) * self._sin
    y_m = (y - self.centerY) * self._cos - (x - self.centerX) * self._sin

    width2 = self._length * 0.5
    height2 = app.__canvas__.yStep * 0.5
    
    if -width2 <= x_m <= width2 and -height2 <= y_m <= height2:
      return self._fill, (self.opacity / 100)
    return 0, 0


class App:

  def __init__(self, *, subPx=1):
    self.group = Group(_add=False)
    self.test = "I\'m a teacup"
    self.paused = False
    self.stepsPerSecond = 30

    self.drawingsPerSecond = 5

    self.__timers__ = [0,0,0]
    self.__canvas__ = Canvas(50, debug=False)
    self.__stepTimeout__ = 100

  def __run__(self, /, looper=None):
    for i, item in enumerate(self.__timers__):
      self.__timers__[i] = time.time()

    while not self.paused:
      now = time.time()

      if self.__timers__[0] < now:
        self.__timers__[2] = now + self.__stepTimeout__
        while self.__timers__[0] < now and not self.paused and not (looper is None):
          looper()
          self.__timers__[0] += 1 / self.__getSPS__()

          if self.__timers__[2] < time.time():
            self.__timers__[0] = time.time()
            break

      if self.__timers__[1] < now:
        self.__canvas__.__draw__()
        self.__timers__[1] += (1 / self.__getDPS__()) * math.ceil(
          (now - self.__timers__[1]) / self.__getDPS__())

  def __getSPS__(self):
    if self.stepsPerSecond <= 0:
      self.stepsPerSecond = 1
    return self.stepsPerSecond

  def __getDPS__(self):
    if self.drawingsPerSecond <= 0:
      self.drawingsPerSecond = 1
    return self.drawingsPerSecond


app = App()
