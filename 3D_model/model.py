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
        """ Does some error checking. """
        self.column_group_params = column_group_params
        smallest_column_x_offset  = min([
            col_params.x_offset_mm for col_params in columns_params])
        if smallest_column_x_offset < 0.0:
            msg = "Column x-offsets should always be non-negative."
            raise ValueError(msg)
        if smallest_column_x_offset > 0.0:
            # This is to simplify padding calculations etc.
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
# END TYPES

def build_part() -> Part:
    """ Returns a Part that can be rendered.
        The Part is built up in a manually-specified
        sequence from hardcoded values inside this function.

        The implicit config schema could be made into a UI, and
        the logic for sequentially creating the components of the
        Part could be left in this function.

        But for now we live with a pile of hardcoded values,
        variables, constructor calls, and implicit sequencing.
    """

    # START HARDCODED CONFIGURATION
    # Actual input data for finger columns.
    # Order: pinky, ring, middle, inner index, outer index
    finger_cols_num_cols = 5
    finger_col_x_offsets_mm: list[float] = [
            0.0, 3.0, 4.5, 3.0, 1.5]
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
    thumb_col_gp_x_start_pos: float = 300.0 # Needs tuning
    thumb_col_gp_y_start_pos: float = 300.0
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
    # Order of these is not important.
    part_column_groups: list[ColumnGroup] = [
            finger_column_group, thumb_column_group]
    part: Part = Part(
            part_thickness_mm,
            part_type,
            part_column_groups)

    return part

# TODO : delete this dummy call.  It was just for error checking.
build_part()

# 
# # START UTILITY FUNCTIONS
# def render(part: Part) ->  _OpenSCADObject:
#     minuend = render_minuend(part)
#     subtrahend = render_subtrahend(part)
#     return minuend - subtrahend
# 
def render_minuend(part: Part) -> _OpenSCADObject:
    """ Invariant w.r.t. part type. Exploits the fact we're just
        rendering one rectangular prism with no holes for each
        column group.
    """
    # TODO
    minuend: _OpenSCADObject = cube(0, 0, 0)
    for column_group in part.column_groups:
        minuend += render_minuend_column_group(column_group)
    return minuend 

# 
# def render_subtrahend(part: Part) -> _OpenSCADObject:
#     # TODO
# # END UTILITY FUNCTIONS
# 
# def main():
#     """ Disobeying convention here while throwing things together.
#     """
#     model = render(build_part())
#     model.save_as_scad()
