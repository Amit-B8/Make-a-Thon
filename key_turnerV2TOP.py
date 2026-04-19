import cadquery as cq
from ocp_vscode import show

# --- 1. MAXIMUM SPEED PARAMETERS ---
handle_len = 180  # FULL LENGTH: Matches the bottom shell exactly!
handle_rad = 32   # FULL WIDTH: Matches the bottom shell exactly!
wall_t = 0.8      # FAST PRINT: Paper thin (2 nozzle passes)
max_h = 12        # FAST PRINT: Flattens the top to save massive Z-height print time!

# --- 2. BUILD THE OUTER LOW-PROFILE SHAPE ---
# Start with the standard full cylinder
solid_body = cq.Workplane("YZ").workplane(offset=-handle_len/2).circle(handle_rad).extrude(handle_len)

# Cut everything below Z = 0
bottom_cutter = cq.Workplane("XY").center(0,0).box(200, 200, 100).translate((0, 0, -50))
top_half = solid_body.cut(bottom_cutter)

# CHOP the top off to make it a low-profile flat roof at Z = 12
top_chopper = cq.Workplane("XY").center(0,0).box(200, 200, 100).translate((0, 0, max_h + 50))
low_profile_outer = top_half.cut(top_chopper)


# --- 3. BUILD THE INNER HOLLOW SHAPE ---
inner_solid = cq.Workplane("YZ").workplane(offset=-handle_len/2 + wall_t).circle(handle_rad - wall_t).extrude(handle_len - wall_t * 2)
inner_half = inner_solid.cut(bottom_cutter)

# Chop the inner air space slightly lower to leave a 0.8mm solid roof
inner_chopper = cq.Workplane("XY").center(0,0).box(200, 200, 100).translate((0, 0, max_h - wall_t + 50))
inner_low_profile = inner_half.cut(inner_chopper)


# --- 4. THE FINAL COVER ---
speed_cover = low_profile_outer.cut(inner_low_profile)

# --- 5. MATCHING CUTOUTS ---
# Add the front shaft hole so it doesn't block the key!
shaft_hole = cq.Workplane("YZ").workplane(offset=85).circle(6).extrude(10)
speed_cover = speed_cover.cut(shaft_hole)

# --- 6. DISPLAY & EXPORT ---
show(speed_cover)

# Uncomment below to export to STL immediately!
cq.exporters.export(speed_cover, "KeyTurner_LowProfile_180mm.stl")