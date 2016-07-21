from matplotlib import colors

class ColorPalettes:
    simple_escalating_5 = [colors.cnames['blue'], colors.cnames['green'], colors.cnames['yellow'], colors.cnames['orange'], colors.cnames['red']]
    
    def hex_to_rgb(palette, scalar):
        return list(map(lambda x: list(map(lambda y: round(y * scalar,0), colors.hex2color(x))), palette))

    def even_value_breaks(values, num_breaks):
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
                
    