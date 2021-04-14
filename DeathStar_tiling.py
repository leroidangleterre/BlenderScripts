# Create a tiling of the surface of the Death Star

import random
import bpy
import math
import mathutils

nbLines = 10
nbCols = 10

x = 0
y = 0

nbTileTypes = 4
tileSize = 10

cloneLayer = 15

random.seed()

# Save the active layers and deactivate all of them except for the clones layer.
activeLayers = [False]*20
for i in range(1,20):
    activeLayers[i] = bpy.context.scene.layers[i]
    if(i == cloneLayer):
        bpy.context.scene.layers[i] = True;
    else:
        bpy.context.scene.layers[i] = False;
    


def clonePart(initPart, name, scene, newLocation):
    me_new = bpy.data.meshes.new(name)
    ob_new = bpy.data.objects.new(name,me_new)
    ob_new.data = initPart.data.copy()
    ob_new.location = newLocation
    ob_new.parent = bpy.data.objects["Empty.World"]
    bpy.context.scene.objects.link(ob_new)




for i in range(1, nbCols):
    print("Creating row " + str(i) + " of " + str(nbCols))
    for j in range(1, nbLines):

        try:
            randomVal = random.randrange(nbTileTypes)
            
            # Choose the tile that is being cloned.
            originalTile = bpy.data.objects["Empty.Panels.Initial.4"].children[randomVal]
            originalName = originalTile.name
            originalData = originalTile.data
            print("Cloning " + str(originalTile) + " of name " + originalName)
            
            #bpy.data.objects[tilename].select = True
            #bpy.context.scene.objects.active = bpy.data.objects[tilename]

            x = (i - nbCols/2) * tileSize
            y = (j - nbLines/2) * tileSize

            # Do not replace the tile that contains the TV screen.
            if not(i==nbCols/2 and j==nbLines/2):
                # Duplicate the tile
                
                newName = "Tile_" + str(i) + "_" + str(j)
                newLocation = mathutils.Vector((x, y, 0))
                clonePart(originalTile, newName, bpy.ops.scene, newLocation)
                
                #newMesh = bpy.data.meshes.new(originalName)
                #print(" copied mesh: " + str(newMesh))
                #newObject = bpy.data.objects.new(newName, originalTile)
                #bpy.context.scene.objects.link(newObject)


                #clone = bpy.context.active_object
                #clone.location = (x, y, 0)
                
                # Randomly rotate the tile
                #angle = random.randrange(4) * math.radians(90)
                #newTile.rotation_euler[2] = angle
                
                # Clear the parent of the new tile
                #bpy.ops.object.parent_clear(type='CLEAR')
                
                # Move the new tile to the last layer
                #OBJECT_OT_move_to_layer(bpy.data.window_managers["WinMan"])
                #tile = Blender.Object.Get('
                
                # Deselect everything
                bpy.ops.object.select_all(action='DESELECT')
        except KeyError:
            print("key not found...")

# Reset the active layers.
for i in range(1,20):
    bpy.context.scene.layers[i] = activeLayers[i]




