# Create a tiling of the surface of the Death Star

import random
import bpy
import math
import mathutils
import numpy

# needed for matrices ?
from math import *
from mathutils import *


x = 0
y = 0

nbTileTypes = 9
tileSize = 1


pi = math.pi

random.seed()

nbLines = 16
nbCols = 16

# Torus physical dimensions
R0 = 50
R1 = 10
# Amount of tiles in rings
nbLines = int(2*pi*R1 / tileSize) # Length of small ring
nbCols = int(2*pi*R0 / tileSize) # Length of large ring
print(str(nbLines) + " lines, " + str(nbCols) + " columns.")

x = 0
y = 0

Rpos = Matrix.Translation((1,0,0))
MrotX = Matrix.Rotation(pi/2, 4, 'X')
MrotY = Matrix.Rotation(pi/2, 4, 'Y')
MrotZ = Matrix.Rotation(pi/2, 4, 'Z')
MrotTotal = numpy.matmul(numpy.matmul(MrotX, MrotY), MrotZ)

def clonePart(initPart, name, scene, currentLocation):
    # print("Calling clonePart()")
    me_new = bpy.data.meshes.new(name)
    copy = bpy.data.objects.new(name,me_new)
    copy.data = initPart.data.copy()
    copy.parent = bpy.data.objects["Empty.World"]

    
    H = nbLines * tileSize
    L = nbCols * tileSize
    
    ##########################################
    x0 = currentLocation[0]
    y0 = currentLocation[1]
    z0 = currentLocation[2]
    
    x = (R0 + R1 * sin(2*pi*y0/H)) * sin(2*pi*x0/L)
    y = R1 * cos(2*pi*y0/H)
    z = (R0 + R1 * sin(2*pi*y0/H)) * cos(2*pi*x0/L)
    
    copy.name = newName
    parent = bpy.data.objects['Empty.World']
    copy.parent = parent
    # The init tile is not rendered, but the copy must be.
    copy.hide_render = False
    ##########################################
    
    
    copy.location[0]=x
    copy.location[1]=y
    copy.location[2]=z
    
    angleX = 2*pi*y0/H - pi/2
    angleZ = 2*pi*x0/L
    
    Rx = mathutils.Matrix.Rotation(angleX, 3, 'X')
    Rz = mathutils.Matrix.Rotation(angleZ, 3, 'Z')
    R = Rz * Rx
    #copy.setMatrix(copy.matrix * R)
    
    copy.rotation_euler.rotate_axis('Y', angleZ)
    copy.rotation_euler.rotate_axis('X', angleX)
    
    
    bpy.data.collections['Cloned_tiles'].objects.link(copy)
    #bpy.context.scene.objects.link(ob_new)
    


for i in range(0, nbCols):
    print("Creating row " + str(i) + " of " + str(nbCols))
    for j in range(0, nbLines):

        try:
            randomVal = random.randrange(nbTileTypes)
            
            # Choose the tile that is being cloned.
            #originalTile = bpy.data.objects["Empty.Panels.Initial.4"].children[randomVal]
            # Test: clone only a sphere
            tile_collection = bpy.data.collections.get("Tiles")
            #print("Collection: " + str(tile_collection))
            
            tile_name = "Tile.init.00" + str(randomVal)
            #print("Looking for tile " + tile_name)
            originalTile = tile_collection.all_objects.get(tile_name)
            
            originalName = originalTile.name
            originalData = originalTile.data

            x = (i - nbCols/2) * tileSize
            y = (j - nbLines/2) * tileSize

            # Duplicate the tile
            newName = "Tile_" + str(i) + "_" + str(j)
            newLocation = mathutils.Vector((x, y, 0))
            clonePart(originalTile, newName, bpy.ops.scene, newLocation)
            
        except KeyError:
            print("key not found...")

# Reset the active layers.
#for i in range(1,20):
#    bpy.context.scene.layers[i] = activeLayers[i]


