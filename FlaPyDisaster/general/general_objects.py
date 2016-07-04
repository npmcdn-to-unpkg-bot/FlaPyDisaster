class BoundingBox:
    """
    Class to represent a bounding box.  Contians a Top and Bottom Latitude, and a Left and Right Longitude.
    Also contains some methods for describing the Bounding Box, such as a get width and height function.
    Assumes lat and long are -180 to 180
    :param top_lat_y: Top/maximum latitude, Y axis
    :param bot_lat_y: Bottom/minimum latitude, Y axis
    :param right_lon_x: Right/maximim longitude, X axis
    :param left_lon_x: Left/minimum logitude, X axis
    :method get_width: Returns the width of the bounding box in degrees (right minus left)
    :method get_height: Returns the height of the bounding box in degrees (top minus bottom)
    :method translate: STUB Returns a copy of the current bounding box, translated by x, y degrees 
    """
    def __init__(self, top_lat_y, bot_lat_y, right_lon_x, left_lon_x):
        self.top_lat_y = top_lat_y
        self.bot_lat_y = bot_lat_y
        self.right_lon_x = right_lon_x
        self.left_lon_x = left_lon_x

    def get_width(self):
        return self.right_lon_x - self.left_lon_x
    def get_height(self):
        return self.top_lat_y - self.bot_lat_y

class LatLonGrid(BoundingBox):
    """
    Class to decribe a grid in lat/long space, and methods to operate on that space.  Extends bounding box.
    Blocks describe a grid space
    :param block_per_degree_y: Number of grid spaces per degree in the Y/Latitude direction
    :param block_per_degree_x: Number of grid spaces per degree in the X/Longitude direction
    :method get_block_index: Get the index (X#, Y#) of a block given a lat/long coordinate
    :method get_lat_lon: Get the lat/long (top left of box) given a blocks index
    :method get_block_width: Get the block width in degrees (all blocks are the same width)
    :method get_block_height: Get the block height in degrees (all blocks are the same height)
    """
    def __init__(self, top_lat_y, bot_lat_y, left_lon_x, right_lon_x, block_per_degree_x, block_per_degree_y):
        self.block_per_degree_y = block_per_degree_y
        self.block_per_degree_x = block_per_degree_x

        return super().__init__(top_lat_y, bot_lat_y, right_lon_x, left_lon_x)

    def get_block_index(self, lat_y, lon_x):
        block_x = (lon_x - self.left_lon_x) * self.block_per_degree_x
        block_y = (lat_y - self.bot_lat_y) * self.block_per_degree_y

        return (block_x, block_y)

    def get_lat_lon(self, block_x, block_y):
        lat_y = self.bot_lat_y + (block_y / self.block_per_degree_y)
        lon_x = self.left_lon_x + (block_x / self.block_per_degree_x)

        return (lat_y, lon_x)

    def get_block_width_x(self):
        return self.get_width() * self.block_per_degree_x

    def get_block_width_y(self):
        return self.get_height() * self.block_per_degree_y