from solid2.core.builtins.openscad_primitives import _OpenSCADObject
from solid2 import cube
from enum import Enum

# START TYPES
PartType = Enum('PartType', ['plate',  'spacer', 'base'])

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
    """ Holds data related to a 1U MX key. """
    switch_hole_side_length_mm = 14
    keycap_side_length_mm = 18
    # Provides breathing space between keycaps.
    keycap_space_side_length_mm = 19.05
# END TYPES

def build_part() -> Part:
    """ Returns a Part that can be rendered.  The Part is built up in a
        manually-specified sequence from hardcoded values inside this function.
    """

    # START HARDCODED CONFIGURATION
    # Actual input data for finger columns.
    # Order: pinky, ring, middle, inner index, outer index
    finger_cols_num_cols = 5
    finger_col_x_offsets_mm: list[float] = [
            4.5, 1.5, 0.0, 1.5, 3.0]
    finger_col_nums_keys : list[int] = [4, 4, 4, 4, 3]
    finger_col_key_lengths_U : list[int] = [
            1 for i in range(finger_cols_num_cols)]

    # Actual input data for finger column group.
    finger_col_gp_top_padding_mm: float = 0.0
    finger_col_gp_bottom_padding_mm: float = 0.0
    finger_col_gp_left_padding_mm: float = 0.0
    finger_col_gp_right_padding_mm: float = 0.0
    finger_col_gp_x_start_pos: float = 0.0
    finger_col_gp_y_start_pos: float = 0.0
    finger_col_gp_rotation_CW_degrees: float = 0.0

    # Actual input data for thumb columns.
    # Order: inner thumb, outer thumb
    thumb_cols_num_cols = 2
    thumb_col_x_offsets_mm: list[float] = [0.0, 0.0]
    thumb_col_nums_keys : list[int] = [1, 1]
    thumb_col_key_lengths_U : list[int] = [
            2 for i in range(thumb_cols_num_cols)]
    
    # Actual input data for thumb column group.
    thumb_col_gp_top_padding_mm: float = 0.0
    thumb_col_gp_bottom_padding_mm: float = 0.0
    thumb_col_gp_left_padding_mm: float = 0.0
    thumb_col_gp_right_padding_mm: float = 0.0
    thumb_col_gp_x_start_pos: float = 100.0 # TODO : Needs tuning.
    thumb_col_gp_y_start_pos: float = 100.0 # TODO : Needs tuning.
    thumb_col_gp_rotation_CW_degrees: float = 45.0
    
    # Actual input data for part.
    part_thickness_mm: float = 4
    part_type: PartType = 'plate'
    # END HARDCODED CONFIGURATION

    # Process all config.
    finger_columns_params: list[ColumnParams] = [
            ColumnParams(
                finger_col_x_offsets_mm[i],
                finger_col_nums_keys[i],
                finger_col_key_lengths_U[i]
                ) for i in range(finger_cols_num_cols)
            ]
    finger_column_group_params = ColumnGroupParams(
            finger_col_gp_top_padding_mm,
            finger_col_gp_bottom_padding_mm,
            finger_col_gp_left_padding_mm,
            finger_col_gp_right_padding_mm,
            finger_col_gp_x_start_pos,
            finger_col_gp_y_start_pos,
            finger_col_gp_rotation_CW_degrees)
    finger_column_group = ColumnGroup(
            finger_column_group_params,
            finger_columns_params)
    thumb_columns_params: list[ColumnParams] = [
            ColumnParams(
                thumb_col_x_offsets_mm[i],
                thumb_col_nums_keys[i],
                thumb_col_key_lengths_U[i]
                ) for i in range(thumb_cols_num_cols)
            ]
    thumb_column_group_params = ColumnGroupParams(
            thumb_col_gp_top_padding_mm,
            thumb_col_gp_bottom_padding_mm,
            thumb_col_gp_left_padding_mm,
            thumb_col_gp_right_padding_mm,
            thumb_col_gp_x_start_pos,
            thumb_col_gp_y_start_pos,
            thumb_col_gp_rotation_CW_degrees)
    thumb_column_group = ColumnGroup(
            thumb_column_group_params,
            thumb_columns_params)
    # Ordering of these two column groups is not important.
    part_column_groups: list[ColumnGroup] = [
            finger_column_group, thumb_column_group]
    part: Part = Part(
            part_thickness_mm,
            part_column_groups,
            part_type)

    return part

# # START UTILITY FUNCTIONS
def world_transform(column_group_params: ColumnGroupParams,
                    obj: _OpenSCADObject) -> _OpenSCADObject:
    """ Applies the ColumnGroupParams' world transformation to the input
        _OpenSCADObject and returns the result.  The transformation is
        encapsulated in a function to keep rotation/translation order
        consistent.  I've chosen for rotation to occur first since I find
        rotation-then-translation more useful in this context.

        The "world transformation" does not include padding.  It just chains
        into one transformation the required rotation and translation
        required by:
          - x_start_pos,
          - y_start_pos, and
          - rotation_CW_degrees.
    """
    # We flip the sign of the rotation so that a clockwise rotation about
    # the positive z-axis does actually result.
    resultant: _OpenSCADObject = (obj
        .rotateZ(-column_group_params.rotation_CW_degrees)
        .translate(column_group_params.x_start_pos,
            column_group_params.y_start_pos,
            0))
    return resultant

def render(part: Part) ->  _OpenSCADObject:
    """ The highest-level render function. """
    return render_minuend(part) - render_subtrahend(part)
    return minuend - subtrahend

def render_minuend_column_group(part: Part, i: int) -> _OpenSCADObject:
    """ Returns one rectangular prism, transformed into world space,
        according to the ColumnGroup's ColumnGroupParams.
    """
    column_group: ColumnGroup = part.column_groups[i]

    # Determine x side length of the resultant.
    columns_x_lengths_required_mm: list[float] = []
    for column_params in column_group.columns_params:
        column_length_mm: float = (column_params.numkeys 
                                   * column_params.key_length_U
                                   * MX_Key.keycap_space_side_length_mm)
        x_length_required_mm: float = (column_length_mm
                                       + column_params.x_offset_mm)
        columns_x_lengths_required_mm.append(x_length_required_mm)
    column_group_x_length_required_mm:float = (
        max(columns_x_lengths_required_mm)
        + column_group.column_group_params.top_padding_mm
        + column_group.column_group_params.bottom_padding_mm)

    # Determine y side length of the resultant.
    num_cols = len(column_group.columns_params)
    column_group_y_length_required_mm: float = (
        num_cols
        * MX_Key.keycap_space_side_length_mm
        + column_group.column_group_params.left_padding_mm
        + column_group.column_group_params.right_padding_mm) 

    # Determine z side length of the resultant.
    thickness_mm: float = part.thickness_mm
   
    # We now understand enough to construct the untransformed minuend for this 
    # column group.
    object_space_resultant: _OpenSCADObject = cube(
            column_group_x_length_required_mm,
            column_group_y_length_required_mm,
            thickness_mm)
    
    world_space_resultant: _OpenSCADObject = world_transform(
            column_group.column_group_params, object_space_resultant)

    return world_space_resultant

def render_minuend(part: Part) -> _OpenSCADObject:
    """ Invariant w.r.t. part type. Exploits the fact we're just
        rendering one rectangular prism per column group with no
        holes in it.
        
        The returned object has been transformed into world space.
    """
    minuend: _OpenSCADObject = cube(0, 0, 0)
    num_column_groups: int = range(len(part.column_groups))
    # Finger column group minuend in red, thumb column group minuend in blue.
    colors = ('red', 'blue')
    for i in num_column_groups:
        minuend += render_minuend_column_group(part, i).color(colors[i])
    return minuend

def render_subtrahend_plate(part: Part):
    """ Returns a matrix of (nearly always disjoint) prisms, to be
        punched out of the switch plate.  This removal of material creates
        holes for all key switches in all column groups.  Gives subtrahend
        for LHS of the keyboard only.

        The returned object has been transformed into world space.
    """

    # Accumulator for the sum of world space ColumnGroup hole prism matrices.
    subtrahend: _OpenSCADObject = cube(0, 0, 0)

    # Define a prism representing one key switch hole.  The prism is
    # transformed within the object space of the key's entire space (i.e. in MX
    # key systems, the 19.05mm by 19.05mm square), to be centered within the
    # key's entire space.
    hole_side_length: float = MX_Key.switch_hole_side_length_mm
    # Prevent z-fighting with plate.
    z_buffer_mm: float = 5
    hole_prism_uncentered: _OpenSCADObject = (cube(
        hole_side_length,
        hole_side_length,
        part.thickness_mm + z_buffer_mm)
        .translate(0, 0, -z_buffer_mm / 2))
    # Center hole within key space.  Colour the hole for visibility against
    # plate.
    offset_mm: float = (MX_Key.keycap_space_side_length_mm
        - MX_Key.switch_hole_side_length_mm) / 2
    hole_prism_centered = (hole_prism_uncentered
                           .translate(offset_mm, offset_mm, 0)
                           .color('green'))

    for column_group in part.column_groups:
        switch_hole_matrix: _OpenSCADObject = cube(0, 0, 0)

        # Get a list of the top-LHS corner of each key in the ColumnGroup.
        # Each key corner is represented as a translation from the origin.
        # (This is where each column's user-specified vertical offset is
        #  dealt with, as well as each column's implicit horizontal offset,
        #  and the column group's padding.)
        top_left_corners_coords: list[tuple(float, float)] = []
        for column_index, column in enumerate(column_group.columns_params):
            y_coord: float = (column_index
                              * MX_Key.keycap_space_side_length_mm
                              + column_group
                                .column_group_params
                                .left_padding_mm)
            for row_index in range(column.numkeys):
                # Evaluates to zero for 1U keys.
                adjustment_for_long_keys_mm: float = (
                    MX_Key.keycap_space_side_length_mm
                    * (column.key_length_U - 1) 
                    * 0.5)
                x_coord: float = (row_index
                                  * MX_Key.keycap_space_side_length_mm
                                  * column.key_length_U
                                  + column.x_offset_mm
                                  + adjustment_for_long_keys_mm
                                  + column_group
                                    .column_group_params
                                    .top_padding_mm)
                top_left_corners_coords.append((x_coord, y_coord))

        # (Accumulate transformed key switch holes.)
        # For as many keys as there are in the ColumnGroup.
        for corner in top_left_corners_coords:
            # Transform a new hole prism into the ColumnGroup's object space.
            switch_hole_matrix += (hole_prism_centered
                .translate(corner[0], corner[1], 0))

        # Get the world transform of the ColumnGroup.
        # Apply it to the accumulated switch_hole_matrix.
        world_space_switch_hole_matrix: _OpenSCADObject = world_transform(
            column_group.column_group_params, switch_hole_matrix)
        
        subtrahend += world_space_switch_hole_matrix

    return subtrahend

def render_subtrahend(part: Part) -> _OpenSCADObject:
    """ Varies w.r.t. part type.
 
        Returned object is either:
          - a disjoint amalgamation of rectangular prisms representing
            the volumes to punch out of the switch plate to create holes
            for all key switches in all column groups,
          - one big prismic volume to punch out of the spacer to make its
            space, or
          - very little, in the case of the base plate.
 
        The returned object has been transformed into world space.
    """
    if part.part_type == "plate":
        return render_subtrahend_plate(part)
#    elif part.part_type == "spacer":
#        # TODO : write a function to deal with this.
#    elif part.part_type == "base":
#        # TODO : write a function to deal with this.
    else:
        raise ValueError

# # END UTILITY FUNCTIONS
 
def main():
    """ Disobeying convention here while throwing things together.
    """
    model = render(build_part())
    model.save_as_scad()
main()
