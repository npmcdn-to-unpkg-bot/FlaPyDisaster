from matplotlib import colors

class ColorPalettes:
    simple_escalating_5 = [colors.cnames['blue'], colors.cnames['green'], colors.cnames['yellow'], colors.cnames['orange'], colors.cnames['red']]
    
    def hex_to_rgb(palette, scalar = 1, as_int = True):
        """
        convert a list of hex strings to rgb values scaled to the input scalar (default is 1)
        :param palette: List of color hex strings.  Expects one of the class Palettes, but can be generated through other means
        :param scalar: Number to scale the rgb values.  255 gives the channel values scaled from 0-255
        :param as_int: Boolean whether to truncate numbers to an int or not.
        """        
        return list(map(lambda x: list(map(lambda y: int(y * scalar) if as_int else (y * scalar), colors.hex2color(x))), palette))

    def even_value_breaks(values, num_breaks):
        """
        Returns a list of values that has the breaks for a (relatively) even split into bins
        :param values: A sorted list of values
        :param num_breaks: The number of desired bins
        :returns: List of values, each value is the top of its bin range
        :example: usage of breaks (break_vals) to find bin number of a value
            for pos in range(break_vals):
                if value <= break_vals[pos]:
                    return pos
        """
        break_num = int(len(values) / num_breaks)
        ret_breaks = []
        pos = break_num
        iter = 0
        for pos in range(len(values)):
            if(iter + 1 == break_num):
                ret_breaks.append(values[pos])
                iter = 0
            else:
                iter = iter + 1

        return ret_breaks
                
    