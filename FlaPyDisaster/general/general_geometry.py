import math

def hello():
    ret_string = "This is the general geometry package! This will contain some help text."
    print(ret_string)

def FindHypotenuseRightTriangle(side1, side2):
    """
    Find the hypotenuse of a triangle.
    :returns: Hypotenuse or -1 if error
    """
    if (side1 != 0 and side2 != 0):
        return math.sqrt( (side1 * side1) + (side2 * side2) )
    else:
        return -1

def FindBottomRightTriangle(Height, Hypotenuse):
    """
    Find third non-hypotenuse side of a triangle.
    :returns: Side length or -1 if error
    """
    if (Height != 0 and Hypotenuse != 0 and Hypotenuse > Height):
        return math.sqrt( (Hypotenuse * Hypotenuse) - (Height * Height) )
    else:
        return -1