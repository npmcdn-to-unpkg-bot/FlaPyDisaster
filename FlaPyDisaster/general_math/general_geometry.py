def hello():
    ret_string = "This is the general geometry package! This will contain some help text."
    print(ret_string)

def FindHypotenuseRightTriangle(side1, side2):
    """
    Find the hypotenuse of a triangle.
    :returns: Hypotenuse or -1 if error
    """
    if (Side1 != 0 and Side2 != 0):
        return math.sqrt( (Side1 * Side1) + (Side2 * Side2) )
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
