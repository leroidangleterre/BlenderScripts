# Create a torus with as many vertices as needed
# This is a replacement for the built-in command "primitive_torus_add", which is locked at 256 vertices for main ring.


import bpy
from bpy.app.translations import pgettext_data as data_
from bpy_extras import object_utils
from math import pi




major_radius = 80
minor_radius = 10.0
major_segments = 1250
minor_segments = 140
generate_uvs = True
trench_width = 6
trench_segments = 3
tile_size = 2*pi*minor_radius/minor_segments
trench_height = trench_segments * tile_size


indexB = int(trench_width/2)
indexC = int(trench_width/2 + trench_segments)
indexF = int(minor_segments + 2*trench_segments)

# actual number of minor segments must take trench into account
minor_segments_total = int(minor_segments + 2*trench_segments)

indexD = minor_segments_total - indexC
indexE = minor_segments_total - indexB

def add_uvs(mesh, minor_seg, major_seg):
    from math import fmod

    mesh.uv_layers.new()
    uv_data = mesh.uv_layers.active.data
    polygons = mesh.polygons
    u_step = 1.0 / major_seg
    v_step = 1.0 / minor_seg

    # Round UV's, needed when segments aren't divisible by 4.
    u_init = 0.5 + fmod(0.5, u_step)
    v_init = 0.5 + fmod(0.5, v_step)

    # Calculate wrapping value under 1.0 to prevent
    # float precision errors wrapping at the wrong step.
    u_wrap = 1.0 - (u_step / 2.0)
    v_wrap = 1.0 - (v_step / 2.0)

    vertex_index = 0

    u_prev = u_init
    u_next = u_prev + u_step
    for _major_index in range(major_seg):
        v_prev = v_init
        v_next = v_prev + v_step
        for _minor_index in range(minor_seg):
            loops = polygons[vertex_index].loop_indices
            uv_data[loops[0]].uv = u_prev, v_prev
            uv_data[loops[1]].uv = u_next, v_prev
            uv_data[loops[3]].uv = u_prev, v_next
            uv_data[loops[2]].uv = u_next, v_next

            if v_next > v_wrap:
                v_prev = v_next - 1.0
            else:
                v_prev = v_next
            v_next = v_prev + v_step

            vertex_index += 1

        if u_next > u_wrap:
            u_prev = u_next - 1.0
        else:
            u_prev = u_next
        u_next = u_prev + u_step


def get_angle(minor_index, minor_seg):
    from math import cos, sin, pi
    #print("minor_index: " + str(minor_index))
    # Original version for regular torus
    #return 2*pi * minor_index / minor_seg
    if minor_index <= indexB:
        return 2*pi*minor_index/minor_segments
    if minor_index <= indexC:
        angleBC = 2*pi*indexB/minor_segments
        return angleBC
    if minor_index <= indexD:
        return 2*pi*(minor_index-trench_segments)/minor_segments
    if minor_index <= indexE:
        angleBC = 2*pi*indexB/minor_segments
        #angleDE = 2*pi*(indexD-trench_segments)/minor_segments
        angleDE = -angleBC
        return angleDE
    angleEF = 2*pi*(minor_index-trench_width)/minor_segments
    return angleEF
    
    
    

def get_radius(minor_index, minor_seg):
    # Original version for regular torus
    #return minor_radius
    
    if minor_index <= indexB:
        return minor_radius - trench_height
    if minor_index <= indexC:
        return (minor_radius - trench_height) + trench_height*(minor_index-indexB)/(indexC-indexB)
    if minor_index <= indexD:
        return minor_radius
    if minor_index <= indexE:
        return minor_radius - trench_height*(minor_index-indexD)/(indexE-indexD)
    return minor_radius - trench_height



def add_torus(major_rad, minor_rad, major_seg, minor_seg):
    from math import cos, sin, pi
    from mathutils import Vector, Matrix

    pi_2 = pi * 2.0


    verts = []
    faces = []
    i1 = 0
    tot_verts = major_seg * minor_segments_total
    for major_index in range(major_seg):
        matrix = Matrix.Rotation((major_index / major_seg) * pi_2, 3, 'Z')

        for minor_index in range(minor_segments_total):
            angle = pi_2 * minor_index / minor_segments_total
            
            # Custom version (used to build trench)
            angle = get_angle(minor_index, minor_segments_total)
            current_minor_rad = get_radius(minor_index, minor_segments_total)

            
            vec = matrix @ Vector((
                major_rad + (cos(angle) * current_minor_rad),
                0.0,
                sin(angle) * current_minor_rad,
            ))
            

            verts.extend(vec[:])

            if minor_index + 1 == minor_segments_total:
                i2 = (major_index) * minor_segments_total
                i3 = i1 + minor_segments_total
                i4 = i2 + minor_segments_total
            else:
                i2 = i1 + 1
                i3 = i1 + minor_segments_total
                i4 = i3 + 1

            if i2 >= tot_verts:
                i2 = i2 - tot_verts
            if i3 >= tot_verts:
                i3 = i3 - tot_verts
            if i4 >= tot_verts:
                i4 = i4 - tot_verts

            faces.extend([i1, i3, i4, i2])

            i1 += 1

    return verts, faces



def execute():
    verts_loc, faces = add_torus(
        major_radius,
        minor_radius,
        major_segments,
        minor_segments,
    )

    mesh = bpy.data.meshes.new(data_("Torus"))

    mesh.vertices.add(len(verts_loc) // 3)

    nbr_loops = len(faces)
    nbr_polys = nbr_loops // 4
    mesh.loops.add(nbr_loops)
    mesh.polygons.add(nbr_polys)

    mesh.vertices.foreach_set("co", verts_loc)
    mesh.polygons.foreach_set("loop_start", range(0, nbr_loops, 4))
    mesh.polygons.foreach_set("loop_total", (4,) * nbr_polys)
    mesh.loops.foreach_set("vertex_index", faces)

    if generate_uvs:
        add_uvs(mesh, minor_segments, major_segments)

    mesh.update()

    object_utils.object_data_add(bpy.context, mesh) #, operator=self)



# Go !
execute()