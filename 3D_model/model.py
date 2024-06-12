import os
from solid2.core.builtins.openscad_primitives import _OpenSCADObject
from solid2 import cube
from create_keyboard import *
from keyboard_types import *

# START HARDCODED CONFIGURATION
def get_bolt_holes() -> _OpenSCADObject:
    """ Returns a object composed of cylinders representing bolt holes. """
    # Radius derived from *outer* diameter.
    M3_bolt_radius_mm: float = 3.0 / 2

    # Positions mentioned in comments are with respect to LHS half of keyboard.
    # z component of translations prevents z-fighting.
    cylinders: list[_OpenSCADObject] = [
        # Top left.
        cylinder(r=M3_bolt_radius_mm, h=15, _fn=30).translate(4.5, 4.5, -1),
        # Bottom left.
        cylinder(r=M3_bolt_radius_mm, h=15, _fn=30).translate(99, 4.5, -1),
        # Bottom right.
        cylinder(r=M3_bolt_radius_mm, h=15, _fn=30).translate(90, 138, -1),
        # Top right.
        cylinder(r=M3_bolt_radius_mm, h=15, _fn=30).translate(4.5, 113.5, -1)
    ]
    combined_cylinders: _OpenSCADObject = cube(0,0,0)
    for elt in cylinders:
        combined_cylinders += elt
    return combined_cylinders

def get_spacer_cutouts() -> _OpenSCADObject:
    """ Returns a object composed of prisms representing pieces of
        material to remove from the spacer.  This provides space for:
        (1) MCU USB connector (2) USB cable connector (3) TRRS jack
        (4) space permitting thumb key switches to be wired to everything else.
    """
    spacer_cutouts: list[_OpenSCADObject] = [
        # (1)(2) TRRS jack. x-value is arbitrarily long.
        cube(30, MCU.cable_slot_width_mm,100).translate(-1, 53, -1),

        # (3) TRRS jack. x-value is arbitrarily long.
        cube(30, TRRS_Jack.width_mm, 100).translate(-1, 88, -1),

        # (4) Removes island between finger keys and thumb keys.
        # These values are all just tuned by eye, based on the specific
        # geometry of the keyboard created thus far.
        cube(30,20,100).translate(60, 90, -1)
    ]
    spacer_cutout: _OpenSCADObject = cube(0,0,0)
    for elt in spacer_cutouts:
        spacer_cutout += elt
    return spacer_cutout

def build_part(part_type: PartType) -> Part:
    """ Returns a Part that can be rendered.  The Part is built up in a
        manually-specified sequence from hardcoded values inside this function.
        The Part returned belongs to the left-hand side of a keyboard.
    """
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
    finger_col_gp_top_padding_mm: float = 11.5
    finger_col_gp_bottom_padding_mm: float = 11.5
    finger_col_gp_left_padding_mm: float = 11.5
    finger_col_gp_right_padding_mm: float = 11.5
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
    thumb_col_gp_top_padding_mm: float = 9.0
    thumb_col_gp_bottom_padding_mm: float = 9.0
    thumb_col_gp_left_padding_mm: float = 9.0
    thumb_col_gp_right_padding_mm: float = 9.0
    thumb_col_gp_x_start_pos: float = 60.0
    thumb_col_gp_y_start_pos: float = 96.5
    thumb_col_gp_rotation_CW_degrees: float = 30.0
    
    # Actual input data for part.
    special_cutouts: _OpenSCADObject = cube(0,0,0) 
    part_thickness_mm: float = 5
    switch_plate_thickness_mm: float = 5
    if part_type == "plate":
        part_thickness_mm == switch_plate_thickness_mm
        special_cutouts = get_bolt_holes()
    if part_type == "spacer":
        # A typical TRRS jack is probaby taller than  most MCUs, can probably
        # use a TRRS jack part as a lower bound for height required in spacer.

        # Seems like the right expression for a spacious build to me.
        # I'm assuming wiring will fit happily within this space.  So, if
        # anything, the thickness of the spacer could even be **increased**.
        part_thickness_mm = (max(MX_Key.keycap_protrusion_mm(
                                            switch_plate_thickness_mm)
                                   + MCU.thickness_mm,
                                   TRRS_Jack.height_mm)
                                   + 2.0)

        special_cutouts = get_spacer_cutouts() + get_bolt_holes()
    if part_type == "base":
        special_cutouts = get_bolt_holes()
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
            part_type,
            special_cutouts)

    return part

def export_whole_3D_model():
    """ Writes a .scad file, with entire keyboard rendered. """
    model_LHS = cube(0,0,0)

    # When a model consisting off all parts is created,
    # appropriate vertical offsets need to be set.
    part_types_and_offsets_mm: dict[str, float] = {
        "base" : 0,
        "spacer" : 5,
        "plate" : 5 + 10,
        "keycaps" : 5 + 10 + 5
    }

    # Create and vertically translate all parts.
    parts: list[_OpenSCADObject] = [
        render(build_part(key))
        .translate(0,0,value)
        for key, value in part_types_and_offsets_mm.items()
    ]

    # Mirror, rotate, then translate LHS to produce RHS.
    for i in range(len(parts)):
        model_LHS += parts[i]
    model_RHS: _OpenSCADObject = (
        model_LHS.mirror(1,0,0).rotate(0,0,200).translate(-54,300,0))
    
    # Save
    model: _OpenSCADObject = model_LHS + model_RHS
    fname: str = "full_model.scad"
    model.save_as_scad(
        filename=fname,
        outdir=os.path.dirname(os.path.realpath(__file__))
    )

def export_part_3D_models():
    """ Writes 1 .scad file per keyboard part.
        Each file contains both LHS and RHS versions of the part.
    """
    model_LHS = cube(0,0,0)
    
    part_types: list[str] =[
        "base",
        "spacer",
        "plate"
    ]

    # Create all parts, LHS only.
    parts: list[_OpenSCADObject] = [
        render(build_part(key))
        for key in part_types
    ]

    # Add RHS to each part.
    parts = [p + p.mirror(1,0,0).translate(-10,0,0) for p in parts]

    # Save
    for i, p in enumerate(parts):
        fname: str = part_types[i] + ".scad"
        dir: str = os.path.dirname(os.path.realpath(__file__))
        full_path: str = f"{dir}/{fname}"

        # Writes 3D scad file.
        p.save_as_scad(
            filename=fname,
            outdir=dir
        )

        # Prepend to .scad file so that its contents represent a 2D view.
        original_contents: str = ""
        with open(full_path, "rt") as f:
            original_contents = f.read()
        with open(full_path, "w") as f:
            f.write("projection()\n" + original_contents)

if __name__ == "__main__":
    export_whole_3D_model()
    export_part_3D_models()
