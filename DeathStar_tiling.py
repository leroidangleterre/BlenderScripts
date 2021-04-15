# Create a tiling of the surface of the Death Star

import random
import bpy
import math
import mathutils

nbLines = 20
nbCols = 10

x = 0
y = 0

nbTileTypes = 4
tileSize = 10

cloneLayer = 15

pi = math.pi

random.seed()

# Save the active layers and deactivate all of them except for the clones layer.
activeLayers = [False]*20
for i in range(1,20):
    activeLayers[i] = bpy.context.scene.layers[i]
    if(i == cloneLayer):
        bpy.context.scene.layers[i] = True;
    else:
        bpy.context.scene.layers[i] = False;
    


def clonePart(initPart, name, scene, currentLocation):
    me_new = bpy.data.meshes.new(name)
    ob_new = bpy.data.objects.new(name,me_new)
    ob_new.data = initPart.data.copy()
    ob_new.parent = bpy.data.objects["Empty.World"]

    # Randomly rotate the tile
    angle = random.randrange(4) * math.radians(90)
    ob_new.rotation_euler[2] = angle
    
    # Test: spherical effect

    # Part location
    #x = newLocation[0]
    #y = newLocation[1]
    #z = 50*(math.cos(math.sqrt(x*x+y*y)/60) - 1)
    #ob_new.location[2] = z
    
    # Torus effect
    R0 = 100
    R1 = 10
    
    H = nbLines * tileSize
    L = nbCols * tileSize
    
    x0 = currentLocation[0]
    y0 = currentLocation[1]
    
    x1 = -R1 * math.sin(2*pi*y0/H) + R0
    y1 = 0
    z1 = R1 * math.cos(2*pi*y0/H)
    
    xf = x1 * math.cos(2*pi*x0/L)
    yf = x1 * math.sin(2*pi*x0/L)
    zf = z1
    
    ob_new.location[0]=xf
    ob_new.location[1]=yf
    ob_new.location[2]=zf
    
    

    bpy.context.scene.objects.link(ob_new)




for i in range(0, nbCols):
    print("Creating row " + str(i) + " of " + str(nbCols))
    for j in range(0, nbLines):

        try:
            randomVal = random.randrange(nbTileTypes)
            
            # Choose the tile that is being cloned.
            #originalTile = bpy.data.objects["Empty.Panels.Initial.4"].children[randomVal]
            # Test: clone only a sphere
            originalTile = bpy.data.objects["Empty.test.balls"].children[0]
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




