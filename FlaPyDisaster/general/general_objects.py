class BoundingBox:
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