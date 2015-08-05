#file created using PySoy Dungeon Desinger
#https://github.com/shiv05/PySoy-Dungeon-Designer
import soy
from time import sleep

dungeon = soy.scenes.Dungeon()
client = soy.Client()

camera = soy.bodies.Camera((0,0,0))

roomkeyarray = ['room1', 'room2', 'room3', 'room4', 'room5', 'room6', 'room7', 'room8', 'room9', 'room10', 'room11', 'room12', 'room13', 'room14', 'room15', 'room16', 'room17', 'room18', 'room19', 'room20', 'room21', 'room22']
roomsizearray = [20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0, 20.0, 10.0, 20.0]
roomwallwidtharray = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
roomposarray = [85.0, 5.0, 140.0, 75.0, 5.0, 120.0, 95.0, 5.0, 120.0, 105.0, 5.0, 100.0, 85.0, 5.0, 100.0, 65.0, 5.0, 100.0, 55.0, 5.0, 80.0, 75.0, 5.0, 80.0, 95.0, 5.0, 80.0, 115.0, 5.0, 80.0, 45.0, 5.0, 60.0, 65.0, 5.0, 60.0, 85.0, 5.0, 60.0, 105.0, 5.0, 60.0, 125.0, 5.0, 60.0, 55.0, 5.0, 40.0, 75.0, 5.0, 40.0, 95.0, 5.0, 40.0, 115.0, 5.0, 40.0, 65.0, 5.0, 20.0, 85.0, 5.0, 20.0, 105.0, 5.0, 20.0]
roommatarray = ['cornflowerblue', 'cornsilk', 'forestgreen', 'darkmagenta', 'darkslateblue', 'goldenrod', 'ivory', 'lightblue', 'lightskyblue', 'mediumslateblue', 'linen', 'navajowhite', 'purple', 'sandybrown', 'sienna', 'tomato', 'yellowgreen', 'hotpink', 'thistle', 'lemonchiffon', 'blueviolet', 'oldlace']

for i in range(0,22):
    dungeon.rooms[roomkeyarray[i]] = soy.scenes.Room(
            soy.atoms.Size((roomsizearray[3*i], 
            roomsizearray[3*i+1], roomsizearray[3*i+2])), 
            roomwallwidtharray[i], roomposarray[3*i],
            roomposarray[3*i+1], roomposarray[3*i+2])
    dungeon.rooms[roomkeyarray[i]].material = soy.materials.Colored(roommatarray[i])
    dungeon.rooms[roomkeyarray[i]]['light1'] = soy.bodies.Light((4,4,4))
    #dungeon.rooms[roomkeyarray[i]]['light2'] = soy.bodies.Light((-4,4,-4))

room1array = ['room1', 'room1', 'room2', 'room2', 'room3', 'room3', 'room6', 'room6', 'room5', 'room5', 'room4', 'room4', 'room7', 'room7', 'room8', 'room8', 'room9', 'room9', 'room10', 'room10', 'room11', 'room12', 'room12', 'room13', 'room13', 'room14', 'room14', 'room15', 'room16', 'room17', 'room17', 'room18', 'room18', 'room19', 'room20', 'room21', 'room2', 'room5', 'room4', 'room7', 'room8', 'room9', 'room13', 'room14', 'room12', 'room11', 'room17']
room2array = ['room2', 'room3', 'room6', 'room5', 'room5', 'room4', 'room7', 'room8', 'room8', 'room9', 'room9', 'room10', 'room11', 'room12', 'room12', 'room13', 'room13', 'room14', 'room14', 'room15', 'room16', 'room16', 'room17', 'room17', 'room18', 'room18', 'room19', 'room19', 'room20', 'room20', 'room21', 'room21', 'room22', 'room22', 'room21', 'room22', 'room3', 'room6', 'room5', 'room8', 'room9', 'room10', 'room14', 'room15', 'room13', 'room12', 'room18']
doorXarray = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
doorYarray = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0]
doorWarray = [4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 15.0, 15.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0]
doorHarray = [8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 8.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0]

for i in range(0,47):
    dungeon.connect_rooms(dungeon.rooms[room1array[i]], 
                            dungeon.rooms[room2array[i]], 
                            doorXarray[i], doorYarray[i], 
                            doorWarray[i], doorHarray[i])

dungeon.rooms[roomkeyarray[0]]['cam'] = camera
client.window.append(soy.widgets.Projector(camera))

# Events init
soy.events.KeyPress.init()
soy.events.KeyRelease.init()
soy.events.Motion.init()
#Forces
Rforce = soy.atoms.Vector((10, 0, 0))
Lforce = soy.atoms.Vector((-10, 0, 0))
Uforce = soy.atoms.Vector((0, 10, 0))
Dforce = soy.atoms.Vector((0, -10, 0))
Fforce = soy.atoms.Vector((0, 0, -20))
Bforce = soy.atoms.Vector((0, 0, 20))
# Actions
RThrust = soy.actions.Thrust(camera, Rforce)
LThrust = soy.actions.Thrust(camera, Lforce)
FThrust = soy.actions.Thrust(camera, Fforce)
BThrust = soy.actions.Thrust(camera, Bforce)
UThrust = soy.actions.Thrust(camera, Uforce)
DThrust = soy.actions.Thrust(camera, Dforce)
# Events
soy.events.KeyPress.addAction("D", RThrust)
soy.events.KeyPress.addAction("A", LThrust)
soy.events.KeyPress.addAction("W", FThrust)
soy.events.KeyPress.addAction("S", BThrust)
soy.events.KeyPress.addAction("Up", UThrust)
soy.events.KeyPress.addAction("Down", DThrust)

if __name__ == '__main__':
    while client:
        sleep(.1)
