import cadquery as cq
from ocp_vscode import show

# Parameters for CP Accessibility
bottom_radius = 30
top_radius = 55   # Wide flare so it rests on the hand
height = 110
thickness = 4

# Create the flared body using Solid.makeCone
cone_solid = cq.Solid.makeCone(bottom_radius, top_radius, height)
cup = cq.Workplane("XY").add(cone_solid)

# Hollow it out using shell
cup_hollow = cup.faces(">Z").shell(-thickness)

show(cup_hollow)

# To export this one, uncomment below:
# cq.exporters.export(cup_hollow, "CP_Gravity_Cup.stl")