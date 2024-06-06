from enum import Enum

PartType = Enum('PartType', ['plate',  'spacer', 'base', 'keycaps'])

class ColumnParams:
    def __init__(
            self,
            x_offset_mm: float,
            numkeys : int,
            key_length_U: int):
        """ The trivial constructor. """
        self.x_offset_mm = x_offset_mm
        self.numkeys = numkeys
        # All keys in a column are constrained to having the same length.
        #
        #                                        +---+ +---+
        #   E.g. you can have a column           | 1u| |   |
        #        like either of these.           +---+ | 2u|
        #                                        | 1u| |   |
        #                                        +---+ +---+
        #                                        | 1u| |   |
        #                                        +---+ | 2u|
        #                                        | 1u| |   |
        #                                        +---+ +---+
        #                          
        #                                        +---+
        #                                        |   |
        #         But not like this.             + 2u|
        #                                        |   |
        #                                        +---+
        #                                        | 1u|
        #                                        +---+
        self.key_length_U = key_length_U

class ColumnGroupParams:
    def __init__(
            self,
            top_padding_mm: float,
            bottom_padding_mm: float,
            left_padding_mm: float,
            right_padding_mm: float,
            x_start_pos: float,
            y_start_pos: float,
            rotation_CW_degrees: float):
        """ The trivial constructor. """
        self.top_padding_mm = top_padding_mm  
        self.bottom_padding_mm = bottom_padding_mm
        self.left_padding_mm = left_padding_mm
        self.right_padding_mm = right_padding_mm
        self.x_start_pos = x_start_pos
        self.y_start_pos = y_start_pos
        self.rotation_CW_degrees = rotation_CW_degrees

class ColumnGroup:
    def __init__(
            self,
            column_group_params: ColumnGroupParams,
            columns_params: list[ColumnParams]):
        """ Not just the trivial constructor.  Does some error checking. """
        self.column_group_params = column_group_params
        smallest_column_x_offset  = min([
            col_params.x_offset_mm for col_params in columns_params])
        if smallest_column_x_offset < 0.0:
            msg = "Column x-offsets should always be non-negative."
            raise ValueError(msg)
        if smallest_column_x_offset > 0.0:
            # This constraint on the configuration UI is to simplify padding
            # calculations for the column groups.
            msg = "At least one column x-offset is always expected to be zero."
            raise ValueError(msg)
        self.columns_params = columns_params

class Part:
    def __init__(
            self,
            thickness_mm: float,
            column_groups: list[ColumnGroup],
            part_type: PartType):
        """ The trivial constructor. """
        self.thickness_mm = thickness_mm
        self.column_groups = column_groups
        self.part_type = part_type

class MX_Key:
    """ Holds data related to an MX key. """
    switch_hole_side_length_mm = 14
    # For a 1U key.
    keycap_side_length_mm = 18
    # Provides breathing space between keycaps.
    keycap_space_side_length_mm = 19.05
    # From Cherry MX data.
    # See https://www.cherry-world.com/cherry-mx/developer
    keyswitch_descend_below_switch_plate_top_mm = 8.3

    @staticmethod
    def arbit_long_keycap_side_length_mm(num_units: int) -> float:
        """ Evaluates the length in mm of the long side of a keycap, which
            may be more than 1U long - arbitrarily long.
        """
        full_length_of_space: float = (MX_Key.keycap_space_side_length_mm
                                      * num_units)
        # Need to reduce length at *both* ends of the long side.  So we don't
        # half the difference calculated here.
        subtrahend: float = (MX_Key.keycap_space_side_length_mm
                            - MX_Key.keycap_side_length_mm)
        return full_length_of_space - subtrahend
    
    @staticmethod
    def keycap_protrusion_mm(switch_plate_thickness_mm: float) -> float:
        """ Returns the number of mm that the keyswitch descends
            below the bottom of the switch plate.
        """    
        return (MX_Key.keyswitch_descend_below_switch_plate_top_mm
               - switch_plate_thickness_mm)

class MCU:
    """ Describes physical dimensions of a rpi pcio, obtained from a mix
        of sources, without giving consideration to tolerances +-.
    """
    # Imperfect.  From measuring a rpi pico with a ruler. Includes USB jack.
    # The plugs on many cables would be thicker than this though.
    # In other words, if not considering plug height, the jack should really
    # be placed at the very edge of the spacer.
    thickness_mm: float = 4.0
    
    # TODO : account for width of outwards-facing MCU edge.
    # TODO : alternatively, consider not mounting the MCU.  It could sit loose
    # in the spacer cavity, and a short USB type C to micro USB female-to-male
    # adapter could be glued to the spacer, with the female side facing out.

class TRRS_Jack:
    """ Describes physical dimensions of an ordinary TRRS jack, obtained from a
        mix of sources, giving only rough consideration to tolerances +-.
        Dimensions are listed for the purposes of allowing enough space for
        the jack, not for the purposes of specifying its exact size.
    """
    # This distance provides a small buffer around the jack, plus its pins.
    # This would allow the jack to be glued into a cutout at the edge of
    # the spacer.
    height_mm: float = 8.0
    
    # Includes an approximate 0.75mm buffer each side for glue or similar.
    width_mm: float = 6.5
