import cadquery as cq
from ocp_vscode import show

# --- 1. PARAMETERS (All measurements in mm unless noted) ---
# A. Wrist Band
wrist_radius_avg = 32     
cuff_wall_t = 5          
cuff_width = 30          
cuff_slit_w = 4          

# B. Rings (Customized to Amit's measurements)
ring_widths = [10, 10, 10, 10]  # Index, Middle, Ring, Pinky
ring_thickness = 2.5 

# Finger Diameters in INCHES
finger_diams_in = [0.5930, 0.5955, 0.5720, 0.5290]
# Automatically convert inches to mm, then divide by 2 to get the radius!
finger_rads = [(d * 25.4) / 2 for d in finger_diams_in]

hand_len_wrist_to_base = 110 

# C. Palm Platform Lever
lever_len = 80           
lever_wid = 50           
lever_thick = 8          

# --- 2. HELPER FUNCTIONS ---
def make_parametric_ring(radius, width, thickness):
    """Creates a simple, crash-proof rigid ring, extruded from Z=0 up."""
    # Extruding upwards guarantees a flat bottom
    ring_outer = cq.Workplane("XY").circle(radius + thickness).extrude(width)
    ring_hollow = ring_outer.faces(">Z").workplane().circle(radius).cutThruAll()
    return ring_hollow 

# --- 3. BUILD COMPONENTS ---
# A. Wrist Band Cuff (Extruded from Z=0)
cuff_base = cq.Workplane("XY").circle(wrist_radius_avg + cuff_wall_t).extrude(cuff_width)
cuff_cutout = cuff_base.faces(">Z").workplane().circle(wrist_radius_avg).cutThruAll()

# Create the slit box separately and subtract it
slit = cq.Workplane("XY").rect(wrist_radius_avg * 4, cuff_slit_w).extrude(cuff_width)
cuff_final = cuff_cutout.cut(slit)

# Combine Block on the back (Extruded from Z=0)
combine_block = (
    cq.Workplane("XY")
    .center(0, -wrist_radius_avg - cuff_wall_t/2)
    .rect(30, cuff_wall_t + 15)
    .extrude(cuff_width)
)
cuff_with_combine = cuff_final.union(combine_block)

# B. Build 4 Rings and Position Them (No Thumb, Centered Layout)
finger_centers = [
    ((-35.5, hand_len_wrist_to_base, 0), finger_rads[0], ring_widths[0]), # Index
    ((-0.5, hand_len_wrist_to_base, 0),  finger_rads[1], ring_widths[1]), # Middle
    ((22.5, hand_len_wrist_to_base, 0),   finger_rads[2], ring_widths[2]), # Ring
    ((45.5, hand_len_wrist_to_base, 0),  finger_rads[3], ring_widths[3]), # Pinky
]

all_rings = []
for center, rad, width in finger_centers:
    r = make_parametric_ring(rad, width, ring_thickness).translate(center)
    all_rings.append(r)

final_rings = all_rings[0]
for r in all_rings[1:]:
    final_rings = final_rings.union(r)

# C. Model the Palm Platform (Lever)
living_hinge_thick = 1
# Using rect() + extrude() forces the bottom to sit perfectly at Z=0
platform = (
    cq.Workplane("XY")
    .center(0, -wrist_radius_avg - (wrist_radius_avg * 1.5))
    .rect(lever_wid, lever_len)
    .extrude(lever_thick)
)

# Anchor eyelet (Extruded upwards from Z=0 so it shares the flat base)
eyelet = (
    cq.Workplane("XY")
    .center(0, -wrist_radius_avg - (wrist_radius_avg * 1.5) - lever_len/2)
    .circle(2)
    .extrude(lever_thick + 10)
)
platform_final = platform.union(eyelet)

# --- 4. ASSEMBLE ---
exoskeleton_rigid = cuff_with_combine.union(final_rings).union(platform_final)

# --- 5. SEND TO VIEWER & EXPORT ---
show(exoskeleton_rigid)

# Remove the hashtag below to generate the file for the 3D printer!
cq.exporters.export(exoskeleton_rigid, "GripForce_Exoskeleton_Custom.stl")