from KicadModTree import *

spacing = 0.127
finger_y = 1*0.127
finger_x = 3*0.127
base_x = 1*0.127
base_y = 1*0.127
short_width = 0.127
bridged = True
mask_inset = -0.127/2

width = 2*base_x + spacing + finger_x
height = 2*base_y + 3*spacing + 2*finger_y

footprint_name = f'SolderJumper_2_C_{width}x{height}mm_{spacing}' + ('_bridged' if bridged else '_open')
print(footprint_name)

kicad_mod = Footprint(footprint_name)
kicad_mod.setDescription(f'SMD Solder Jumper, C shape, {width}x{height}mm, {spacing}mm gap, ' + ('bridged' if bridged else 'open'))
kicad_mod.setTags('net tie solder jumper' + (' bridged' if bridged else ' open'))

points = [
    [0,0],
    [width, 0],
    [width, -base_y],
    [base_x, -base_y],
    [base_x, -(base_y + 2*spacing + finger_y)],
    [base_x + finger_x, -(base_y + 2*spacing + finger_y)],
    [base_x + finger_x, -(base_y + 2*spacing + 2*finger_y)],
    [0, -(base_y + 2*spacing + 2*finger_y)],
]

a = Polygon(nodes=points, layer='F.Cu', width=0)
a.translate([-width/2, height/2])
kicad_mod.append(a)

b = Polygon(nodes=points, layer='F.Cu', width=0)
b.rotate(angle=180, use_degrees=True)
b.translate([width/2, -height/2])
kicad_mod.append(b)

pad_x = base_x*0.9
pad_y = 2*(height/2 - base_y - spacing)*0.9
kicad_mod.append(Pad(number=1, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=['F.Cu'], at=[-width/2 + base_x/2, 0], size=[pad_x, pad_y]))
kicad_mod.append(Pad(number=2, type=Pad.TYPE_SMT, shape=Pad.SHAPE_RECT, layers=['F.Cu'], at=[width/2 - base_x/2, 0], size=[pad_x, pad_y]))

mask_x = width/2 - mask_inset
mask_y = height/2 - mask_inset
kicad_mod.append(Polygon(nodes=[[mask_x, mask_y], [-mask_x, mask_y], [-mask_x, -mask_y], [mask_x, -mask_y]], layer='F.Mask', width=0.0))

silk_x = width/2 + 0.25
silk_y = height/2 + 0.25
kicad_mod.append(RectLine(start=[silk_x, silk_y], end=[-silk_x, -silk_y], layer='F.SilkS', width=0.12))

courtyard_x = width/2 + 0.48
courtyard_y = height/2 + 0.48
kicad_mod.append(RectLine(start=[courtyard_x, courtyard_y], end=[-courtyard_x, -courtyard_y], layer='F.CrtYd', width=0.05))

text_offset = height/2 + 1/2 + 0.25 + 0.2
kicad_mod.append(Text(type='reference', text='REF**', at=[0, -text_offset], layer='F.SilkS'))
kicad_mod.append(Text(type='value', text=footprint_name, at=[1.5, text_offset], layer='F.Fab'))

if bridged:
    short_x = short_width/2
    short_y = (spacing + finger_y)/2
    kicad_mod.append(Polygon(
        nodes=[[short_x, short_y], [-short_x, short_y], [-short_x, -short_y], [short_x, -short_y]],
        layer='F.Cu',
        width=0))

file_handler = KicadFileHandler(kicad_mod)
file_handler.writeFile(footprint_name + '.kicad_mod')
