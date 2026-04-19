import cadquery as cq
from ocp_vscode import show

# --- 1. PARAMETERS ---
# Overall dimensions
handle_len = 160
handle_rad = 28
wall_t = 3

# --- 2. BUILD THE OUTER SHELL ---
# Create a solid cylinder along the X axis
solid_body = cq.Workplane("YZ").workplane(offset=-handle_len/2).circle(handle_rad).extrude(handle_len)

# Cut the top half off to make it a bottom shell
top_cutter = cq.Workplane("XY").center(0,0).box(handle_len * 2, handle_rad * 2, handle_rad * 2).translate((0, 0, handle_rad))
bottom_half = solid_body.cut(top_cutter)

# Create a smaller cylinder to hollow out the inside
inner_solid = cq.Workplane("YZ").workplane(offset=-handle_len/2 + wall_t).circle(handle_rad - wall_t).extrude(handle_len - wall_t * 2)
inner_cutter = cq.Workplane("XY").center(0,0).box(handle_len * 2, handle_rad * 2, handle_rad * 2).translate((0, 0, handle_rad))
inner_half = inner_solid.cut(inner_cutter)

# Subtract the inner half from the bottom half to get the empty shell
shell = bottom_half.cut(inner_half)

# --- 3. ADD INTERNAL COMPARTMENTS ---

# A. Battery Compartment (Back)
# Build a solid block, then hollow it out to the exact size of a 9V battery
bat_mount = cq.Workplane("XY").center(-50, 0).box(55, 30, handle_rad).translate((0, 0, -handle_rad/2))
bat_cavity = cq.Workplane("XY").center(-50, 0).box(48, 27, handle_rad).translate((0, 0, -handle_rad/2))
bat_block = bat_mount.cut(bat_cavity)
shell = shell.union(bat_block)

# B. Circuit Board Compartment (Middle)
# Sized for a generic 60x40mm prototype board
pcb_mount = cq.Workplane("XY").center(10, 0).box(64, 44, handle_rad/2).translate((0, 0, -handle_rad/2 - 5))
pcb_cavity = cq.Workplane("XY").center(10, 0).box(62, 42, handle_rad/2).translate((0, 0, -handle_rad/2 - 5))
pcb_block = pcb_mount.cut(pcb_cavity)
shell = shell.union(pcb_block)

# C. Servo Motor Mount (Front)
# Sized for a standard SG90 Micro Servo
servo_mount = cq.Workplane("XY").center(65, 0).box(30, 20, handle_rad).translate((0, 0, -handle_rad/2))
servo_cavity = cq.Workplane("XY").center(65, 0).box(24, 13.5, handle_rad).translate((0, 0, -handle_rad/2))
servo_block = servo_mount.cut(servo_cavity)
shell = shell.union(servo_block)

# Cut a hole through the front wall for the motor shaft to poke out
shaft_hole = cq.Workplane("YZ").workplane(offset=80).circle(6).extrude(-15)
shell = shell.cut(shaft_hole)

# --- 4. SCREW PEGS (ASSEMBLY BOSSES) ---
# Add four posts in the corners to screw the case together
screw_x_positions = [-70, 50]
screw_y_positions = [22, -22]

for cx in screw_x_positions:
    for cy in screw_y_positions:
        # Create the solid peg
        peg = cq.Workplane("XY").center(cx, cy).cylinder(handle_rad, 4).translate((0, 0, -handle_rad/2))
        shell = shell.union(peg)
        # Drill a 2.8mm pilot hole for M3 screws
        hole = cq.Workplane("XY").center(cx, cy).cylinder(handle_rad, 1.4).translate((0, 0, -handle_rad/2))
        shell = shell.cut(hole)

# --- 5. BUTTON HOLES ---
# Cut two 16mm diameter holes on the side for panel-mount buttons
button_holes = cq.Workplane("XZ").workplane(offset=handle_rad).pushPoints([(20, -10), (-10, -10)]).circle(8).extrude(-handle_rad * 2)
shell = shell.cut(button_holes)

# --- 6. DISPLAY ---
show(shell)

# Remove the hashtag below to generate the printable file
# cq.exporters.export(shell, "KeyTurner_BottomShell.stl")