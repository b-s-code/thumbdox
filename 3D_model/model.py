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

class keyholecolumn:
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

# Make uncut switch plate.
switch_plate = cube(500, 500, 5)

# Cut holes out of switch plate.
#switch_plate -= keyholecolumn(num_keys=4, cut_depth=6).subtrahend()
switch_plate -= keyholecolumn(num_keys=4, cut_depth=6).subtrahend().translate(0,0,-0.5)

model = switch_plate 
model.save_as_scad()
