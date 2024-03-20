from solid2 import cube

def emptysolid():
    return cube(0, 0, 0)

class keydata:
    """ 
        Stores data related to a 1U keycap and switch.
        Sources: 
          - https://youtu.be/7azQkSu0m_U?t=71
          - https://www.cherry-world.com/cherry-mx/developer
    """
    cap_width = 18 # mm.
    cap_space_width = 19.05 # mm.
    switch_hole_width = 14 # mm.
    switch_hole_separation = 5.05 # mm, apart.

class switch_hole_column:
    """ A column of disjoint rectangular prisms that can be subtracted from a
        switch plate to form the keyswitch holes for an entire column of keys
        Successive keys are placed along the x-axis.  The collection of prisms
        will be one keycap space wide along the y-axis. It is expected that
        the switch holes will be punched out of the switch plate parallel to
        the z-axis.
    """

    def __init__(self, num_keys=3, cut_depth=5):
        """ Keyword arguments:
        num_keys -- the number of keys to put in the column.
        cut_depth -- how deep, in millimetres, to cut each keyswitch hole.
                     Should be no less than the thickness of switch plate.

        Default values are fairly aribitrary.
        """
        self.cut_depth = cut_depth
        self.num_keys = num_keys 

    def subtrahend(self):
        """ 
            Returns a sum of rectangular prisms.
            This prism sum can be taken away from a switch plate to
            cut the holes needed for a key column's keyswitch holes.
        """
        hole_w = keydata.switch_hole_width
        space_w = keydata.cap_space_width
        prisms = [
            cube(hole_w, hole_w, self.cut_depth) \
            .translate(i * space_w, 0, 0)   \
            for i in range(self.num_keys)]

        # Seems we can't just sum the list of prisms.  Do things the long way.
        prism_sum = emptysolid()
        for prism in prisms:
            prism_sum += prism
        return prism_sum

class switch_hole_thumb_cluster:
    """ A pair of disjoint rectangular prisms that can be subtracted from a
        switch plate to form the keyswitch holes for two 2U thumb keys.
        Successive keys are placed along the y-axis.  The collection of prisms
        will be two keycap spaces wide along the x-axis. It is expected that
        the switch holes will be punched out of the switch plate parallel to
        the z-axis.  The subtrahend exposed will not be rotated w.r.t. axes.
    """

    def __init__(self, cut_depth=5):
        """ Keyword arguments:
        cut_depth -- how deep, in millimetres, to cut each keyswitch hole.
                     Should be no less than the thickness of switch plate.

        Default value is fairly aribitrary.
        """
        self.cut_depth = cut_depth
        self.num_keys = 2 

    def subtrahend(self):
        """ 
            Returns a sum of rectangular prisms.
            This prism sum can be taken away from a switch plate to
            cut the holes needed for the thumb cluster's keyswitch holes.
        """
        hole_w = keydata.switch_hole_width
        space_w = keydata.cap_space_width
        prisms = [
            cube(hole_w, hole_w, self.cut_depth) \
            .translate(0, i * space_w, 0)   \
            for i in range(self.num_keys)]

        # Seems we can't just sum the list of prisms.  Do things the long way.
        prism_sum = emptysolid()
        for prism in prisms:
            prism_sum += prism
        return prism_sum

# Make uncut switch plate.
switch_plate = cube(500, 500, 5)

# Cut holes out of switch plate for columns of 1U keys.
z_offset = -0.5 # Prevent z-fighting.
switch_plate -= switch_hole_column(num_keys=4, cut_depth=6).subtrahend().translate(0, 0, z_offset)
switch_plate -= switch_hole_column(num_keys=4, cut_depth=6).subtrahend().translate(0, keydata.cap_space_width, z_offset)
switch_plate -= switch_hole_column(num_keys=4, cut_depth=6).subtrahend().translate(0, 2 * keydata.cap_space_width, z_offset)
switch_plate -= switch_hole_column(num_keys=4, cut_depth=6).subtrahend().translate(0, 3 * keydata.cap_space_width, z_offset)
# Intentionally one less 1U key in innermost column, to make room for thumb keys.
switch_plate -= switch_hole_column(num_keys=3, cut_depth=6).subtrahend().translate(0, 4 * keydata.cap_space_width, z_offset)

# Cut holes out of switch plate for 2X 2U thumb keys.
z_offset = -0.5 # Prevent z-fighting.
# TODO : position properly.  Somehow account for 2U keycap size too.
switch_plate -= switch_hole_thumb_cluster(cut_depth=7).subtrahend().translate(0, 0, z_offset).rotate(0,0,-45).translate(100,100,z_offset)

model = switch_plate 
model.save_as_scad()
