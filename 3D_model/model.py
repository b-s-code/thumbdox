from solid2.core.builtins.openscad_primitives import _OpenSCADObject
from solid2 import cube
from create_keyboard import *
from keyboard_types import *

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
    # Nonzero padding means that the spacer part actually fit to exist
    # in the real world.
    finger_col_gp_top_padding_mm: float = 3.0
    finger_col_gp_bottom_padding_mm: float = 3.0
    finger_col_gp_left_padding_mm: float = 3.0
    finger_col_gp_right_padding_mm: float = 3.0
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
    # Nonzero padding means that the spacer part actually fit to exist
    # in the real world.
    thumb_col_gp_top_padding_mm: float = 3.0
    thumb_col_gp_bottom_padding_mm: float = 3.0
    thumb_col_gp_left_padding_mm: float = 3.0
    thumb_col_gp_right_padding_mm: float = 3.0
    # TODO : might be easier to do the tuning below by adding a crude
    # keycap rendering function.  (It is critical to avoid keycap
    # collisions in the design.)
    thumb_col_gp_x_start_pos: float = 60.0
    thumb_col_gp_y_start_pos: float = 97.0
    thumb_col_gp_rotation_CW_degrees: float = 30.0
    
    # Actual input data for part.
    part_thickness_mm: float = 4
    # TODO : clean up.  (Will continue changing this enum manually, while
    # writing subtrahend render function.)
    part_type: PartType = 'plate'
    part_type: PartType = 'plate_and_caps'
    #part_type: PartType = 'spacer'
    #part_type: PartType = 'base'
    
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

def main():
    """ Disobeying convention here while throwing things together.
    """
    model = render(build_part())
    model.save_as_scad()
main()
