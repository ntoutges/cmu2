from intensities import _intensities


class ValidNum0To100:

  @staticmethod
  def validityCheck(value, name):
    if not (type(value) == int or type(value) == float or 0 <= value <= 100):
      typeName = str(type(value)).split("\'")[1]
      raise ValueError(
        f"{name} should be number-in-range-0-100, (but {value} is of type {typeName})"
      )

  def getName():
    return

class ValidPositiveNum:
  @staticmethod
  def validityCheck(value, name):
    if not (type(value) == int or type(value) == float or value > 0):
      typeName = str(type(value)).split("\'")[1]
      raise ValueError(f"{name} should be positive-number (but {value} is of type {typeName})")

class ValidColor:

  @staticmethod
  def validityCheck(value, name):
    if not (value in _intensities):
      raise ValueError(
        f"{name} should be a color, and {value} is not a legal color name")

class ValidAlign:

  @staticmethod
  def validityCheck(value, name):
    if not value in ("center", "left", "right", "top", "bottom", "left-top", "left-bottom", "right-top", "right-bottom"):
      raise ValueError( f"{name}, {value} is not a legal align value" )

class ValidClass:

  @staticmethod
  def validityCheck(value, name, cls):
    if not isinstance(value, cls):
      typeName = str(type(value)).split("\'")[1]
      clsTypeName = str(type(cls)).split("\'")[1]
      raise ValueError(
        f"{name} should be {clsTypeName} (but {value} is of type {typeName})")
