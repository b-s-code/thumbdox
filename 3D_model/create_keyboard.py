from solid2.core.builtins.openscad_primitives import _OpenSCADObject
from solid2 import cube, cylinder
from keyboard_types import *
from util_fns import *

def _world_transform(column_group_params: ColumnGroupParams,
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
    """ The top-level render function. """
    resultant: _OpenSCADObject = (_render_minuend(part)
                                 - _render_subtrahend(part))
    return resultant

def _render_minuend_column_group(part: Part, i: int) -> _OpenSCADObject:
    """ Returns one rectangular prism, transformed into world space,
        according to the ColumnGroup's ColumnGroupParams.
        
        LHS of keyboard only.
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
    
    world_space_resultant: _OpenSCADObject = _world_transform(
            column_group.column_group_params, object_space_resultant)

    return world_space_resultant

def _render_minuend(part: Part) -> _OpenSCADObject:
    """ Invariant w.r.t. part type. Exploits the fact we're just
        rendering one rectangular prism per column group with no
        holes in it.
        
        Gives minuend for LHS of the keyboard only.  The returned object
        has been transformed into world space.
    """
    # We get less branching logic here by just farming out keycap minuend
    # construction to a separate function.
    if (part.part_type == "keycaps"):
        return _render_keycaps(part)

    minuend: _OpenSCADObject = cube(0, 0, 0)
    num_column_groups: int = range(len(part.column_groups))
    
    # In an exploded view, it's nice if adjacent parts can be differentiated
    # visually.
    part_color = 'red'
    if (part.part_type == 'spacer'):
        part_color = 'blue'

    for i in num_column_groups:
        # Can instead have a list of colours, passing list elements to color()
        # below, if wanting to differentiate the sections of the part
        # constructed for different column groups.
        minuend += _render_minuend_column_group(part, i).color(part_color)
    return minuend

def _render_subtrahend(part: Part) -> _OpenSCADObject:
    """ Varies w.r.t. part type.
 
        Returned object is either:
          - a disjoint matrix of rectangular prisms representing
            the volumes to punch out of the switch plate to create holes
            for all key switches in all column groups, plus cylinders for
            bolt holes,
          - one big prismic volume to punch out of the spacer to make its
            space, plus cylinders for bolt holes, plus volumes to be removed
            for cable connectors, or
          - just cylinders for bolt holes, in the case of the base plate.
 
        Gives subtrahend for LHS of the keyboard only.  The returned object
        has been transformed into world space.
    """
    # Accumulator object for all sub-subtrahends.
    # E.g. for the switch plate, this includes the the sum of world space
    # ColumnGroup hole prism matrices.
    # Note that different parts may require different hardcoded cutouts.
    subtrahend = part.special_cutouts
    
    # Nothing else should be cut out of these parts.
    if (part.part_type in ("keycaps", "base")):
        return subtrahend

    # Define a prism representing one key switch hole.  The prism is
    # transformed within the object space of the key's entire space (i.e. in MX
    # key systems, the 19.05mm by 19.05mm square), to be centered within the
    # key's entire space.
    hole_side_length: float = MX_Key.switch_hole_side_length_mm
    # Prevent z-fighting with plate.
    z_buffer_mm: float = 5
    hole_prism_uncentered_plate: _OpenSCADObject = (cube(
        hole_side_length,
        hole_side_length,
        part.thickness_mm + z_buffer_mm)
        .translate(0, 0, -z_buffer_mm / 2))
    
    # Bigger than MX_Key.keycap_space_side_length_mm because real world
    # experience implies wiring may extend beyond key space boundaries.
    padding_around_keyspace_mm: float = 10.0 # For spacer part only.
    spacer_part_key_space_allocation_mm: float = (
            MX_Key.keycap_space_side_length_mm
            + padding_around_keyspace_mm)
    hole_prism_uncentered_spacer: _OpenSCADObject = (cube(
        spacer_part_key_space_allocation_mm,
        spacer_part_key_space_allocation_mm,
        part.thickness_mm + z_buffer_mm)
        .translate(
            -(spacer_part_key_space_allocation_mm - hole_side_length) / 2,
            -(spacer_part_key_space_allocation_mm - hole_side_length) / 2,
            -z_buffer_mm / 2))
    
    hole_prism_uncentered: _OpenSCADObject = cube(0, 0, 0)
    if (part.part_type == "plate"):
         hole_prism_uncentered = hole_prism_uncentered_plate
    elif (part.part_type == "spacer"):
         hole_prism_uncentered = hole_prism_uncentered_spacer
    else:
        raise ValueError

    # Center hole within key space.  Colour the hole for visibility against
    # plate.
    hole_color = 'pink'
    offset_mm: float = (MX_Key.keycap_space_side_length_mm
        - MX_Key.switch_hole_side_length_mm) / 2
    hole_prism_centered = (hole_prism_uncentered
                           .translate(offset_mm, offset_mm, 0)
                           .color(hole_color))

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
        world_space_switch_hole_matrix: _OpenSCADObject = _world_transform(
            column_group.column_group_params, switch_hole_matrix)
        
        subtrahend += world_space_switch_hole_matrix

    return subtrahend

def _get_keycap_centered(keycap_units: int,
                         plate_thickness_mm: float) -> _OpenSCADObject:
    """ Returns a keycap (1U, 2U, ..., depending on keycap_units),
        centered within keycap space.  If greater than one unit long,
        the long side of the keycap runs parallel to the x-axis.

        Note that the "keycap" is really just an extruded rectangle.
        It has no "curve", nor vertical taper.  It is intended only to be
        viewed for diagnosing and avoiding keycap collisions by eye.
    """
    # Define a prism representing one keycap.  The prism is
    # transformed within the object space of the key's entire space (i.e. in MX
    # key systems, for a 1u keycap, this would be the 19.05mm by 19.05mm
    # square), to be centered within the key's entire space.

    # Prevent z-fighting with plate.
    z_buffer_mm: float = 5
    keycap_prism_uncentered: _OpenSCADObject = (cube(
        MX_Key.arbit_long_keycap_side_length_mm(keycap_units),
        MX_Key.keycap_side_length_mm,
        plate_thickness_mm + z_buffer_mm)
        .translate(0, 0, -z_buffer_mm / 2))

    # Center keycap within key space.  Colour the keycap for visibility against
    # plate.
    offset_mm: float = (MX_Key.keycap_space_side_length_mm
        - MX_Key.keycap_side_length_mm) / 2
    keycap_color = 'white'
    # Set to less than 1.0 if need transparency.  This can be useful for
    # checking switch holes are positioned as expected under keycaps.
    keycap_opacity = 1.0
    keycap_prism_centered = (keycap_prism_uncentered
                           .translate(offset_mm, offset_mm, 0)
                           .color(keycap_color, keycap_opacity))
    return keycap_prism_centered

def _render_keycaps(part: Part) -> _OpenSCADObject:
    """ Varies w.r.t. part type.
 
        Returned object is :
          - a disjoint matrix of rectangular prisms approximating
            the volumes of the keycaps, for all keys in all column groups.
          - of imperfect height.  It's intended to be used only for ensuring
            no keycaps collide, on a flat keyboard plate.
 
        Gives keycaps for LHS of the keyboard only.  The returned object
        has been transformed into world space.
    """
    # Accumulator for the sum of world space ColumnGroup hole prism matrices.
    keycaps: _OpenSCADObject = cube(0, 0, 0)

    for column_group in part.column_groups:
        keycap_matrix: _OpenSCADObject = cube(0, 0, 0)

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
                adjustment_for_long_keys_mm: float = 0
                x_coord: float = (row_index
                                  * MX_Key.keycap_space_side_length_mm
                                  * column.key_length_U
                                  + column.x_offset_mm
                                  + adjustment_for_long_keys_mm
                                  + column_group
                                    .column_group_params
                                    .top_padding_mm)
                # Transform a new keycap prism into the ColumnGroup's object
                # space.
                keycap_matrix += (_get_keycap_centered(
                                  column.key_length_U,
                                  part.thickness_mm)
                                  .translate(x_coord, y_coord, 0))

        # Get the world transform of the ColumnGroup.
        # Apply it to the accumulated keycap_matrix.
        world_space_keycap_matrix: _OpenSCADObject = _world_transform(
            column_group.column_group_params, keycap_matrix)
        
        keycaps += world_space_keycap_matrix

    return keycaps
