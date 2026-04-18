import cadquery as cq
from ocp_vscode import show

# --- MODEL 1: UPDATED MODULAR SERVO PLATE ---
plate_l = 90  # Long dimension (Wrist to Knuckles, along X-axis)
plate_w = 60  # Short dimension (Across the back of hand, along Y-axis)
plate_t = 4   # Thickness

# 1. Base Plate (Oriented so the long edge runs horizontally)
base = cq.Workplane("XY").box(plate_l, plate_w, plate_t)

# 2. Velcro Slits (Rotated 90 degrees, centered on the 90mm edges)
# 25mm long (X) and 3.5mm wide (Y), placed at the extreme top/bottom edges
slit_l = 3
slit_w = 15
slit_offset_x = 35
slit_offset_y = -12
holes_offset_x = 32
holes_offset_y = 8
slits = cq.Workplane("XY").pushPoints([(slit_offset_x, slit_offset_y), (-slit_offset_x, slit_offset_y)]).box(slit_l, slit_w, plate_t * 3)
plate = base.cut(slits)

# 3. Flush Rope Tunnels (Moved to the same edges as the straps)
# Positioned near the knuckle edge (X = -35)
tunnel_offset_x = -35
tunnel_blocks = cq.Workplane("XY").workplane(offset=plate_t/2).pushPoints([(holes_offset_x, holes_offset_y), (-holes_offset_x, holes_offset_y)]).box(12, 10, 10).translate((0,0,5))
plate = plate.union(tunnel_blocks)

# Cut BIGGER holes (6mm diameter) through the tunnels along the X-axis
# FIX: Using holes_offset_y because we are on the YZ plane!
tunnel_holes = cq.Workplane("YZ").pushPoints([(holes_offset_y, plate_t/2 + 5)]).circle(3).extrude(150, both=True)
plate = plate.cut(tunnel_holes)

# 4. Modular Servo Mount & Spool Peg
# Central axle peg for you to drop your custom gear/spool onto
spool_peg = cq.Workplane("XY").workplane(offset=plate_t/2).center(0, 0).cylinder(15, 4).translate((0,0,7.5))

# Modular bracket for the micro-servo
# Orbited 90 degrees around the center (0,0) to sit on the positive Y-axis
servo_mount = cq.Workplane("XY").workplane(offset=plate_t/2).center(0, 22).box(28, 16, 10).translate((0,0,5))
servo_cavity = cq.Workplane("XY").workplane(offset=plate_t/2).center(0, 22).box(23.5, 12.5, 10).translate((0,0,5))
servo_bracket = servo_mount.cut(servo_cavity)

# Combine everything
model1_updated = plate.union(spool_peg).union(servo_bracket)

show(model1_updated)

# cq.exporters.export(model1_updated, "Backplate_Modular_Servo_Final.stl")