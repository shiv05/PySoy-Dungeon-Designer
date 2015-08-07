from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import filedialog

import math
import time
import datetime

class DungeonDesigner:

    grid_width = 0
    grid_height = 0
    grid_unitsize = 0
    #point for first click
    point1 = [0.0, 0.0]
    #variable to store whether first click has been made or not
    first_click = False
    first_click_circle = None
    #list to store all rectangles
    rectangles = []
    #list to store all doors
    doors = []
    #mode  
    mode = "add/modify rooms"
    #variable to keep track of selected room in rectangles
    cur_rect_index = -1
    #variable to keep track of selected door in doors
    cur_door_index = -1
    #gui used by tk
    root = mainframe =  canvas =  canvas_hscroll =  canvas_vscroll = None
    options_frame = mode_frame = mode_dropdown = roomoptions_frame = None
    mat_dropdown = mouseover_circle = dooroptions_frame = door_dropdown = None
    console = console_font = fileooptions_frame = export_popup = None
    #current room's key
    cur_rk = None
    #current room height
    cur_rh = None
    #current wall width
    cur_ww = None
    #current material
    cur_mat = None
    #counter to keep automatic room keys unique
    rk_counter = 1
    #current room1's key
    room1key = None
    #current room2's key
    room2key = None
    #height of door above ground
    cur_dh = None
    #door dimensions
    cur_ddx = None
    cur_ddy = None
    #door ratio : door's center will be present at point specified by dr1:dr2
    cur_dr1 = None
    cur_dr2 = None
    #current door
    cur_door = None
    #floor height
    h_str = None
    floor_height = 0.0
    

    def __init__(self, gw, gh, gu):
        self.grid_width = gw
        self.grid_height = gh
        self.grid_unitsize = gu

        self.root = Tk()
        self.root.title("Dungeon Creator")

        #set up StringVar's
        self.cur_rk = StringVar()
        self.cur_rh = StringVar()
        self.cur_ww = StringVar()
        self.cur_mat = StringVar()
        self.room1key = StringVar()
        self.room2key = StringVar()
        self.cur_dh = StringVar()
        self.cur_ddx = StringVar()
        self.cur_ddy = StringVar()
        self.cur_dr1 = StringVar()
        self.cur_dr2 = StringVar()
        self.cur_door = StringVar()
        self.h_str = StringVar()
        self.cur_rk.set('room1')
        self.cur_rh.set('10')
        self.cur_ww.set('1.0')
        self.room1key.set('')
        self.room2key.set('')
        self.cur_dh.set('0')
        self.cur_ddx.set('4')
        self.cur_ddy.set('8')
        self.cur_dr1.set('1')
        self.cur_dr2.set('1')
        self.h_str.set('0.0')

        #add the main frame
        self.mainframe = ttk.Frame(self.root, width=900, height=650)
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))


        #scrollbars for canvas
        self.canvas_hscroll = ttk.Scrollbar(self.mainframe, orient=HORIZONTAL)
        self.canvas_vscroll = ttk.Scrollbar(self.mainframe, orient=VERTICAL)

        self.canvas_hscroll.grid(column = 1, row =2, sticky = (W, E))
        self.canvas_vscroll.grid(column = 2, row =1, sticky = (N, S))


        #add canvas
        self.canvas = Canvas(self.mainframe, scrollregion=(
                                0, 0, 20*self.grid_width, 20*self.grid_height), 
                                yscrollcommand=self.canvas_vscroll.set,
                                xscrollcommand=self.canvas_hscroll.set)

        self.canvas.grid(column=1, row=1, sticky=(N, W, S))
        self.canvas.configure(background = "white", width = 700, height = 600)

        self.canvas_hscroll['command'] = self.canvas.xview
        self.canvas_vscroll['command'] = self.canvas.yview

        #draw grid
        i=0
        j=0
        while i<=self.grid_width:
            j=0
            while j<=self.grid_height:
                self.canvas.create_oval(20*i-2, 20*j-2, 20*i+2, 20*j+2)
                j+=1
            i+=1

        #cirle to be drawn at the grid point closest to mouse position
        self.mouseover_circle = self.canvas.create_oval(-2, -2, 2, 2, 
                                                                fill="blue")

        #add mouse binding to canvas
        self.canvas.bind("<Button-1>", self.mouseclick)
        self.canvas.bind("<Motion>", self.mouseover)
        self.canvas.bind("<Button-3>", self.rightmouseclick)

        #create and set up the options frame
        self.options_frame = ttk.Labelframe(self.mainframe, text = "Options", 
                                                            padding = "5 2")
        self.options_frame.grid(column=3, row=1, sticky= (N, E, S))
        self.options_frame.configure(width = 200, height = 600)

        #labeled frame to hold combobox for modes
        self.mode_frame = ttk.Labelframe(self.options_frame, text = "Modes", 
                                                            padding = "5 5")
        self.mode_frame.grid(column=1, row=1, sticky= (N, W, E))
        self.mode_frame.configure(width = 200, height = 100)

        #combobox to set mode
        self.mode_dropdown = ttk.Combobox(self.mode_frame, 
                                    textvariable=self.mode, state = 'readonly')
        self.mode_dropdown['values'] = ('add/modify rooms', 'add doors')
        self.mode_dropdown.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mode_dropdown.bind("<<ComboboxSelected>>", self.mode_changed)
        self.mode_dropdown.current(0)

        #room options frame
        self.roomoptions_frame = ttk.Labelframe(self.options_frame, 
                                        text="Room Options",padding="12 5 5 5")
        self.roomoptions_frame.grid(column=1, row=2, sticky= (W, E))
        self.roomoptions_frame.configure(width = 200, height = 300)

        #room options labels
        ttk.Label(self.roomoptions_frame, text="room key:").grid(column=1, 
                                    row=1, sticky=(N, W, E, S), padx=2, pady=2)
        ttk.Label(self.roomoptions_frame, text="room height:").grid(column=1, 
                                    row=2, sticky=(N, W, E, S), padx=2, pady=2)
        ttk.Label(self.roomoptions_frame, text="wall width:").grid(column=1, 
                                    row=3, sticky=(N, W, E, S), padx=2, pady=2)
        ttk.Label(self.roomoptions_frame, text="material:", width = 7).grid(
                                    column=1, row=4, sticky= W, padx=2, pady=2)



        #room textboxes
        ttk.Entry(self.roomoptions_frame, width=8, 
                        textvariable=self.cur_rk).grid(column=2, row=1, 
                                                sticky = (N,E), padx=0, pady=5)
        ttk.Entry(self.roomoptions_frame, width=8, 
                        textvariable=self.cur_rh).grid(column=2, row=2, 
                                                sticky = E, padx=0, pady=5)
        ttk.Entry(self.roomoptions_frame, width=8, 
                        textvariable=self.cur_ww).grid(column=2, row=3, 
                                                sticky = E, padx=0, pady=5)

        #combobox to set room material        
        self.mat_dropdown = ttk.Combobox(self.roomoptions_frame, width=7,
                                state = 'readonly', textvariable=self.cur_mat)
        self.mat_dropdown.bind("<<ComboboxSelected>>", self.material_changed)
        self.mat_dropdown.grid(column=2, row=4, sticky = (E,S), columnspan = 1,
                                                                padx=0, pady=5)

        #set traces on cur_rk, cur_rh, cur_ww
        self.cur_rk.trace("w", self.rk_changed)
        self.cur_rh.trace("w", self.rh_changed)
        self.cur_ww.trace("w", self.ww_changed)

        #delete room button
        ttk.Button(self.roomoptions_frame, text="Delete Room",
                     command=self.delete_room).grid(column=1, row=5, sticky=S, 
                                                    columnspan = 2, pady =5)

        self.root.bind('<Delete>', self.delete_pressed)

        #frame for add door mode's options
        self.dooroptions_frame = ttk.Labelframe(self.options_frame, 
                                        text = "Door Options", padding = "5 5")
        self.dooroptions_frame.grid(column=1, row=2, sticky= (W, E))
        self.dooroptions_frame.configure(width = 200, height = 300)

        #door options labels
        ttk.Label(self.dooroptions_frame, text="height").grid(column=1, 
                                    row=1, sticky=(N, W, E, S), padx=0, pady=2)
        ttk.Label(self.dooroptions_frame, text="dimensions").grid(column=1, 
                                    row=2, sticky= W, padx=0, pady=2)
        ttk.Label(self.dooroptions_frame, text="ratio").grid(column=1, 
                                    row=3, sticky=(N, W, E, S), padx=0, pady=2)
        ttk.Label(self.dooroptions_frame, text="select\ndoor").grid(column=1, 
                                    row=4, sticky=(N, W, E, S), padx=0, pady=2)
        ttk.Label(self.dooroptions_frame, text=":", width=1).grid(column=2, 
                                    row=1, sticky=(N, W, E, S), padx=0, pady=2)
        ttk.Label(self.dooroptions_frame, text=":", width=1).grid(column=2, 
                                    row=2, sticky=(N, W, E, S), padx=0, pady=2)
        ttk.Label(self.dooroptions_frame, text=":", width=1).grid(column=2, 
                                    row=3, sticky=(N, W, E, S), padx=0, pady=2)
        ttk.Label(self.dooroptions_frame, text=":", width=1).grid(column=2, 
                                    row=4, sticky=(N, W, E, S), padx=0, pady=2)
        ttk.Label(self.dooroptions_frame, text="x", width=1).grid(column=4, 
                                    row=2, sticky=(N, W, E, S), padx=0, pady=2)
        ttk.Label(self.dooroptions_frame, text=":", width=1).grid(column=4, 
                                    row=3, sticky=(N, W, E, S), padx=0, pady=2)


        #door options textboxes
        ttk.Entry(self.dooroptions_frame, width=3, 
                        textvariable=self.cur_dh).grid(column=4, row=1, 
                                                sticky = E, padx=0, pady=2)
        ttk.Entry(self.dooroptions_frame, width=3, 
                        textvariable=self.cur_ddx).grid(column=3, row=2, 
                                                sticky = E, padx=0, pady=2)
        ttk.Entry(self.dooroptions_frame, width=3, 
                        textvariable=self.cur_ddy).grid(column=5, row=2, 
                                                sticky = E, padx=0, pady=2)
        ttk.Entry(self.dooroptions_frame, width=3, 
                        textvariable=self.cur_dr1).grid(column=3, row=3, 
                                                sticky = E, padx=0, pady=2)
        ttk.Entry(self.dooroptions_frame, width=3, 
                        textvariable=self.cur_dr2).grid(column=5, row=3, 
                                                sticky = E, padx=0, pady=2)

        #set traces on cur_dk, cur_ddx, cur_ddy, cur_dr1, cur_dr2
        self.cur_dh.trace("w", self.dh_changed)
        self.cur_ddx.trace("w", self.ddx_changed)
        self.cur_ddy.trace("w", self.ddy_changed)
        self.cur_dr1.trace("w", self.dr1_changed)
        self.cur_dr2.trace("w", self.dr2_changed)

        #combobox to select room        
        self.door_dropdown = ttk.Combobox(self.dooroptions_frame, width=6,
                                state = 'readonly', textvariable=self.cur_door)
        self.door_dropdown.bind("<<ComboboxSelected>>", self.door_changed)
        self.door_dropdown.grid(column=3, row=4, padx=0, pady=5, columnspan=3)

        #add another door button
        ttk.Button(self.dooroptions_frame, text="Add Another \nDoor",
                     command=self.add_another_door).grid(column=1, row=5, 
                                        sticky=S, padx=0, pady=2, columnspan=2)

        #delete door button
        ttk.Button(self.dooroptions_frame, text="Delete\nDoor",
                     command=self.delete_door, width=6).grid(column=3, row=5, 
                                        sticky=S, padx=1, pady=2, columnspan=3)

        #disable/hide add door mode's options
        self.dooroptions_frame.grid_remove()
        

        #add text widget for console
        self.console_font = font.Font(family="Consolas", size=8)
        self.console = Text(self.options_frame, width=22, height=21, 
                                                        font=self.console_font)
        self.console.grid(row=3, column=1, padx=4, pady=4, sticky=(W, E))
        self.console.insert(END, "             CONSOLE OUTPUT\n\n\n")

        #frame for file options. This will have options to load/save/export
        self.fileoptions_frame = ttk.Labelframe(self.options_frame, 
                                        text="File Options", padding = "2 2")
        self.fileoptions_frame.grid(column=1, row=4, sticky= (W, E))
        self.fileoptions_frame.configure(width = 200, height = 50)

        #load file button door button
        ttk.Button(self.fileoptions_frame, text="Load", 
                    command=self.load_file, width=6).grid(column=1, row=1, 
                                            sticky=(N,W,E,S), padx=2, pady=2)
        self.root.bind('l', self.load_file)

        #save file button door button
        ttk.Button(self.fileoptions_frame, text="Save", 
                    command=self.save_file, width=6).grid(column=2, row=1, 
                                            sticky=(N,W,E,S), padx=2, pady=2)
        self.root.bind('s', self.save_file)

        #export file button door button
        ttk.Button(self.fileoptions_frame, text="Export", 
                    command=self.export_file, width=6).grid(column=3, row=1,
                                            sticky=(N,W,E,S), padx=2, pady=2)
        self.root.bind('e', self.export_file)
        

        #set material dropdown values
        self.mat_dropdown['values'] = ('aliceblue',
                                        'antiquewhite',
                                        'aqua',
                                        'aquamarine',
                                        'azure',
                                        'beige',
                                        'bisque',
                                        'black',
                                        'blanchedalmond',
                                        'blue',
                                        'blueviolet',
                                        'brown',
                                        'burlywood',
                                        'cadetblue',
                                        'chartreuse',
                                        'chocolate',
                                        'coral',
                                        'cornflowerblue',
                                        'cornsilk',
                                        'crimson',
                                        'cyan',
                                        'darkblue',
                                        'darkcyan',
                                        'darkgoldenrod',
                                        'darkgray',
                                        'darkgreen',
                                        'darkgrey',
                                        'darkkhaki',
                                        'darkmagenta',
                                        'darkolivegreen',
                                        'darkorange',
                                        'darkorchid',
                                        'darkred',
                                        'darksalmon',
                                        'darkseagreen',
                                        'darkslateblue',
                                        'darkslategray',
                                        'darkslategrey',
                                        'darkturquoise',
                                        'darkviolet',
                                        'deeppink',
                                        'deepskyblue',
                                        'dimgray',
                                        'dimgrey',
                                        'dodgerblue',
                                        'firebrick',
                                        'floralwhite',
                                        'forestgreen',
                                        'fuchsia',
                                        'gainsboro',
                                        'ghostwhite',
                                        'gold',
                                        'goldenrod',
                                        'gray',
                                        'grey',
                                        'green',
                                        'greenyellow',
                                        'honeydew',
                                        'hotpink',
                                        'indianred',
                                        'indigo',
                                        'ivory',
                                        'khaki',
                                        'lavender',
                                        'lavenderblush',
                                        'lawngreen',
                                        'lemonchiffon',
                                        'lightblue',
                                        'lightcoral',
                                        'lightcyan',
                                        'lightgoldenrodyellow',
                                        'lightgray',
                                        'lightgreen',
                                        'lightgrey',
                                        'lightpink',
                                        'lightsalmon',
                                        'lightseagreen',
                                        'lightskyblue',
                                        'lightslategray',
                                        'lightslategrey',
                                        'lightsteelblue',
                                        'lightyellow',
                                        'lime',
                                        'limegreen',
                                        'linen',
                                        'magenta',
                                        'maroon',
                                        'mediumaquamarine',
                                        'mediumblue',
                                        'mediumorchid',
                                        'mediumpurple',
                                        'mediumseagreen',
                                        'mediumslateblue',
                                        'mediumspringgreen',
                                        'mediumturquoise',
                                        'mediumvioletred',
                                        'midnightblue',
                                        'mintcream',
                                        'mistyrose',
                                        'moccasin',
                                        'navajowhite',
                                        'navy',
                                        'oldlace',
                                        'olive',
                                        'olivedrab',
                                        'orange',
                                        'orangered',
                                        'orchid',
                                        'palegoldenrod',
                                        'palegreen',
                                        'paleturquoise',
                                        'palevioletred',
                                        'papayawhip',
                                        'peachpuff',
                                        'peru',
                                        'pink',
                                        'plum',
                                        'powderblue',
                                        'purple',
                                        'red',
                                        'rosybrown',
                                        'royalblue',
                                        'saddlebrown',
                                        'salmon',
                                        'sandybrown',
                                        'seagreen',
                                        'seashell',
                                        'sienna',
                                        'silver',
                                        'skyblue',
                                        'slateblue',
                                        'slategray',
                                        'slategrey',
                                        'snow',
                                        'springgreen',
                                        'steelblue',
                                        'tan',
                                        'teal',
                                        'thistle',
                                        'tomato',
                                        'turquoise',
                                        'violet',
                                        'wheat',
                                        'white',
                                        'whitesmoke',
                                        'yellow',
                                        'yellowgreen')
        self.mat_dropdown.current(10)

    def distance_sq(self, p1, p2):
        return (p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1])


    def get_position_on_canvas(self, x, y):
        return ((self.canvas_hscroll.get()[0])*self.grid_width*20+x, 
                (self.canvas_vscroll.get()[0])*self.grid_height*20+y)


    def get_nearest_gridpoint(self, point):
        #top left point
        tlp = [math.floor(point[0]/20)*20, math.floor(point[1]/20)*20]

        if tlp[0] > 20*self.grid_width-20:
            tlp[0] = 20*self.grid_width-20

        if tlp[1] > 20*self.grid_height-20:
            tlp[1] = 20*self.grid_height-20

        #tuple of candidate points
        cp = ( (tlp[0],tlp[1]), (tlp[0]+20,tlp[1]), (tlp[0]+20,tlp[1]+20), 
                                                        (tlp[0],tlp[1]+20) )

        min_dist = self.distance_sq(point, cp[0])
        min_ind = 0
        for i in range(1,4):
            dist = self.distance_sq(point, cp[i])
            if dist < min_dist:
                min_dist = dist
                min_ind = i
        return cp[min_ind]


    #function to check if rectangle defined by point1 and point2 intersects 
    #any of the existing rectangles. The function also checks that the
    #rectangle is actually a rectangle and not a line/point
    def check_rectangles(self, point1, point2):
        p1 = [min(point1[0],point2[0]), min(point1[1],point2[1])]
        p2 = [max(point1[0],point2[0]), max(point1[1],point2[1])]
        #if width or height of rectangle is 0, return false
        if (p1[0] == p2[0]) or (p1[1] == p2[1]):
            return False
        for rect in self.rectangles:
            if (self.canvas.coords(rect[0])[0] < p2[0]) and (
                                self.canvas.coords(rect[0])[2] > p1[0]) and (
                                self.canvas.coords(rect[0])[1] < p2[1]) and (
                                self.canvas.coords(rect[0])[3] > p1[1]):
                return False
        return True


    #function that checks if a given point lies in any of the existing 
    #rectangles. If such a rectangle exists, the rectangle's index in
    #self.rectangles is returned, else -1 is  returned
    def in_rectangles(self, point):
        for rect in self.rectangles:
            if (point[0]>self.canvas.coords(rect[0])[0]) and (
                                point[0]<self.canvas.coords(rect[0])[2]) and (
                                point[1]>self.canvas.coords(rect[0])[1]) and (
                                point[1]<self.canvas.coords(rect[0])[3]):
                return self.rectangles.index(rect)
        return -1


    #function that checks whether a given point lies on a door. If such door
    #exists, it's index in doors is added to a dropdown. A dropdown is used
    #since multiple doors may exist at a given point (at different heights)
    def on_doors(self, point):
        dropdown_values = []
        for door in self.doors:
            #door coordinates
            dc = self.canvas.coords(door[0])
            #if door is vertical
            if (dc[0]==dc[2]) and (point[0]<dc[0]+5) and (
                    point[0]>dc[0]-5) and (point[1]>=min(dc[1], dc[3])) and (
                    point[1]<=max(dc[1], dc[3])):
                dropdown_values.append('door '+str(self.doors.index(door)))
            #if door is horizontal
            elif (dc[1]==dc[3]) and (point[1]<dc[1]+5) and (
                    point[1]>dc[1]-5) and (point[0]>=min(dc[0], dc[2])) and (
                    point[0]<=max(dc[0], dc[2])):
                dropdown_values.append('door '+str(self.doors.index(door)))
        return dropdown_values


    #function that returns true if given line lies on the common wall of 2 
    #rectangles
    def on_walls(self, line):
        for i in range(0, self.rectangles.__len__()):
            rp = self.canvas.coords(self.rectangles[i][0])
            #if 2 endpoints of line lie of rect.x1 edge
            if (line[0][0]==rp[0]) and (line[0][1]>=rp[1]) and (
                            line[0][1]<=rp[3]) and (line[1][0]==rp[0]) and (
                            line[1][1]>=rp[1]) and (line[1][1]<=rp[3]):
                #if 2 endpnts of line lie on rect.x2 edge of another rectangle
                for j in range(i+1, self.rectangles.__len__()):
                    rp = self.canvas.coords(self.rectangles[j][0])
                    if (line[0][0]==rp[2]) and (line[0][1]>=rp[1]) and (
                            line[0][1]<=rp[3]) and (line[1][0]==rp[2]) and (
                            line[1][1]>=rp[1]) and (line[1][1]<=rp[3]):
                        return (i,j,1)

            #if 2 endpoints of line lie of rect.x2 edge
            if (line[0][0]==rp[2]) and (line[0][1]>=rp[1]) and (
                            line[0][1]<=rp[3]) and (line[1][0]==rp[2]) and (
                            line[1][1]>=rp[1]) and (line[1][1]<=rp[3]):
                #if 2 endpnts of line lie on rect.x1 edge of another rectangle
                for j in range(i+1, self.rectangles.__len__()):
                    rp = self.canvas.coords(self.rectangles[j][0])
                    if (line[0][0]==rp[0]) and (line[0][1]>=rp[1]) and (
                            line[0][1]<=rp[3]) and (line[1][0]==rp[0]) and (
                            line[1][1]>=rp[1]) and (line[1][1]<=rp[3]):
                        return (i,j,2)

            #if 2 endpoints of line lie of rect.y1 edge
            if (line[0][1]==rp[1]) and (line[0][0]>=rp[0]) and (
                            line[0][0]<=rp[2]) and (line[1][1]==rp[1]) and (
                            line[1][0]>=rp[0]) and (line[1][0]<=rp[2]):
                #if 2 endpnts of line lie on rect.y2 edge of another rectangle
                for j in range(i+1, self.rectangles.__len__()):
                    rp = self.canvas.coords(self.rectangles[j][0])
                    if (line[0][1]==rp[3]) and (line[0][0]>=rp[0]) and (
                            line[0][0]<=rp[2]) and (line[1][1]==rp[3]) and (
                            line[1][0]>=rp[0]) and (line[1][0]<=rp[2]):
                        return (i,j,3)

            #if 2 endpoints of line lie of rect.y2 edge
            if (line[0][1]==rp[3]) and (line[0][0]>=rp[0]) and (
                            line[0][0]<=rp[2]) and (line[1][1]==rp[3]) and (
                            line[1][0]>=rp[0]) and (line[1][0]<=rp[2]):
                #if 2 endpnts of line lie on rect.y2 edge of another rectangle
                for j in range(i+1, self.rectangles.__len__()):
                    rp = self.canvas.coords(self.rectangles[j][0])
                    if (line[0][1]==rp[1]) and (line[0][0]>=rp[0]) and (
                            line[0][0]<=rp[2]) and (line[1][1]==rp[1]) and (
                            line[1][0]>=rp[0]) and (line[1][0]<=rp[2]):
                        return (i,j,4)
        return None


    #deslects a rectangle if one is selected
    def deselect_rectangle(self):
        if self.cur_rect_index != -1:
            self.canvas.itemconfig(self.rectangles[self.cur_rect_index][0], 
                                                                    fill = '')
            self.cur_rect_index = -1


    #deslects a door if one is selected
    def deselect_door(self):
        if self.cur_door_index != -1:
            self.canvas.itemconfig(self.doors[self.cur_door_index][0], width = 1)
            self.cur_door_index = -1


    def mouseclick(self, event):
        mousepos = self.get_position_on_canvas(event.x,event.y)
        near_gridpoint = self.get_nearest_gridpoint(mousepos)
        #if add/modify rooms mode is selected
        if self.mode == 'add/modify rooms':
            index = self.in_rectangles(mousepos)
            #if the mouse clicks an existing rectangle, select the rectangle
            if index != -1:
                #deselect previous rectange
                self.deselect_rectangle()
                #load selected room's properties in GUI
                self.cur_rk.set(self.rectangles[index][1])
                self.cur_rh.set(self.rectangles[index][2])
                self.cur_ww.set(self.rectangles[index][3])
                self.mat_dropdown.current(self.rectangles[index][4])
                self.mat_dropdown.selection_clear()
                #select rectangle specified by index
                self.canvas.itemconfig(self.rectangles[index][0], fill = 'cyan')
                self.cur_rect_index = index
                #set first_click to false
                self.first_click = False
                self.canvas.delete(self.first_click_circle)
            #if this is the 2nd click for making a room
            elif(self.first_click):
                #if the new room doesn't intersect old rooms, add the room
                if self.check_rectangles(self.point1, near_gridpoint):
                    #add rectangle such that (x1,y1) < (x2,y2)
                    self.rectangles.append([self.canvas.create_rectangle(
                                min(self.point1[0], near_gridpoint[0]), 
                                min(self.point1[1],near_gridpoint[1]), 
                                max(self.point1[0], near_gridpoint[0]), 
                                max(self.point1[1],near_gridpoint[1]), 
                                outline = "blue", fill = 'cyan'),
                                "room"+str(self.rk_counter), 
                                self.cur_rh.get(), self.cur_ww.get(), 
                                self.mat_dropdown.current()
                                            ])
                    self.cur_rk.set("room"+str(self.rk_counter))
                    self.mat_dropdown.selection_clear()
                    self.rk_counter += 1
                    #set current rect index
                    self.cur_rect_index = (self.rectangles.__len__() -1)
                else:
                    self.write_to_console("room intersects with exisitng room"+
                                " or has zero width/depth. No room added.")
                self.first_click = False
                self.canvas.delete(self.first_click_circle)
            #if this is the first click for making a room
            else:
                #save the point for future use
                self.point1 = near_gridpoint
                #deselect any selected rectangles
                self.deselect_rectangle()
                self.first_click = True
                self.first_click_circle = self.canvas.create_oval(
                                                near_gridpoint[0]-5, 
                                                near_gridpoint[1]-5, 
                                                near_gridpoint[0]+5, 
                                                near_gridpoint[1]+5, 
                                                fill = 'blue')

 
       #if add doors mode is selected
        elif self.mode == 'add doors':
            dropdown_values = self.on_doors(mousepos)
            #if existing door is selected
            if (dropdown_values.__len__() > 0):
                self.door_dropdown['values'] = dropdown_values
                self.door_dropdown.current(0)
                self.door_changed(None)
                #set first_click to false
                self.first_click = False
                self.canvas.delete(self.first_click_circle)
            #if this is the 2nd click for making a door
            elif self.first_click:
                if (self.point1[0] == near_gridpoint[0]) and (
                                        self.point1[1] == near_gridpoint[1]):
                    self.write_to_console('size of door added is 0. '+
                                                            'No door added')
                elif self.on_walls(( self.point1, near_gridpoint )) != None:
                    self.doors.append([self.canvas.create_line(
                                    min(self.point1[0], near_gridpoint[0]), 
                                    min(self.point1[1], near_gridpoint[1]), 
                                    max(self.point1[0], near_gridpoint[0]), 
                                    max(self.point1[1], near_gridpoint[1]), 
                                    fill='red', width = 4), 
                                    self.cur_dh.get(), self.cur_ddx.get(), 
                                    self.cur_ddy.get(), self.cur_dr1.get(), 
                                    self.cur_dr2.get()
                                        ])
                    #deselect already selected door
                    self.deselect_door()
                    #select current door
                    self.cur_door_index = self.doors.__len__() - 1
                    #add the door to dropdown in gui
                    dropdown_values = self.on_doors(self.point1)
                    self.door_dropdown['values'] = dropdown_values
                    self.door_dropdown.current(dropdown_values.__len__()-1)
                else:
                    self.write_to_console("the door specidfied doesn't lie " +
                                            " on the common wall of 2 rooms." +
                                            " No door added.")
                self.first_click = False
                self.canvas.delete(self.first_click_circle)
            #if this is the 1st click for making a door
            else:
                #save the point for future use
                self.point1 = near_gridpoint
                #deselect any selected doors
                self.deselect_door()
                self.first_click = True
                self.first_click_circle = self.canvas.create_oval(
                                                near_gridpoint[0]-5, 
                                                near_gridpoint[1]-5, 
                                                near_gridpoint[0]+5, 
                                                near_gridpoint[1]+5, 
                                                fill = 'red')
                

    def rightmouseclick(self, event): 
            if self.first_click:
                self.first_click = False
                self.canvas.delete(self.first_click_circle)


    def mouseover(self, event):
        mousepos = self.get_position_on_canvas(event.x,event.y)
        near_gridpoint = self.get_nearest_gridpoint(mousepos)
        self.canvas.delete(self.mouseover_circle)
        if self.mode == 'add/modify rooms':
            color = 'blue'
        elif self.mode == 'add doors':
            color = 'red'
        self.mouseover_circle = self.canvas.create_oval(near_gridpoint[0]-5, 
                                                near_gridpoint[1]-5, 
                                                near_gridpoint[0]+5, 
                                                near_gridpoint[1]+5, 
                                                fill = color)


    def mode_changed(self, event):
        self.mode = self.mode_dropdown.get()
        #forget clicks already made
        self.first_click = False
        self.canvas.delete(self.first_click_circle)
        if self.mode == "add/modify rooms":
            self.dooroptions_frame.grid_remove()
            self.deselect_door()
            self.roomoptions_frame.grid()
        elif self.mode == "add doors":
            self.roomoptions_frame.grid_remove()
            self.deselect_rectangle()
            self.dooroptions_frame.grid()


    def material_changed(self, event):
        self.cur_mat.set(self.mat_dropdown.get())
        #if any rectangle is selected, change it's material in self.rectangles
        if (self.cur_rect_index != -1):
            self.rectangles[self.cur_rect_index][4]=self.mat_dropdown.current()


    def door_changed(self, event):
        #if another door is selected, deselect it
        self.deselect_door()
        #calculate selected door's index in self.doors
        self.cur_door.set(self.door_dropdown.get())
        door_index = int(self.cur_door.get().split()[1])
        #select the  current door in gui
        self.cur_door_index = door_index
        self.canvas.itemconfig(self.doors[self.cur_door_index][0], width = 4)
        #load selected door's data in gui      
        self.cur_dh.set(self.doors[door_index][1])
        self.cur_ddx.set(self.doors[door_index][2])
        self.cur_ddy.set(self.doors[door_index][3])
        self.cur_dr1.set(self.doors[door_index][4])
        self.cur_dr2.set(self.doors[door_index][5])


    #callbacks for when room key/height/wall width is changed
    def rk_changed(self, *args):
        #if any rectangle is selected, change it's key in self.rectangles
        if (self.cur_rect_index != -1):
            self.rectangles[self.cur_rect_index][1]=self.cur_rk.get()


    def rh_changed(self, *args):
        #if any rectangle is selected, change it's height in self.rectangles
        if (self.cur_rect_index != -1):
            self.rectangles[self.cur_rect_index][2]=self.cur_rh.get()


    def ww_changed(self, *args):
        #if any rectangle is selected, change it's height in self.rectangles
        if (self.cur_rect_index != -1):
            self.rectangles[self.cur_rect_index][3]=self.cur_ww.get()


    #callbacks for when door properties are changed
    def dh_changed(self, *args):
        #if any door is selected, change it's height in self.doors
        if (self.cur_door_index != -1):
            self.doors[self.cur_door_index][1]=self.cur_dh.get()


    def ddx_changed(self, *args):
        #if any door is selected, change it's x dimension in self.doors
        if (self.cur_door_index != -1):
            self.doors[self.cur_door_index][2]=self.cur_ddx.get()


    def ddy_changed(self, *args):
        #if any door is selected, change it's y dimension in self.doors
        if (self.cur_door_index != -1):
            self.doors[self.cur_door_index][3]=self.cur_ddy.get()


    def dr1_changed(self, *args):
        #if any door is selected, change it's 1st ratio value in self.doors
        if (self.cur_door_index != -1):
            self.doors[self.cur_door_index][4]=self.cur_dr1.get()


    def dr2_changed(self, *args):
        #if any door is selected, change it's 2st ratio value in self.doors
        if (self.cur_door_index != -1):
            self.doors[self.cur_door_index][5]=self.cur_dr2.get()


    def delete_room(self, *args):
        #if room is selected, delete the room
        if (self.cur_rect_index != -1):
            self.canvas.delete(self.rectangles[self.cur_rect_index][0])
            self.rectangles.pop(self.cur_rect_index)
            self.cur_rect_index = -1


    def delete_door(self, *args):
        #if door is selected, delete the room
        if (self.cur_door_index != -1):
            self.canvas.delete(self.doors[self.cur_door_index][0])
            self.doors.pop(self.cur_door_index)
            self.cur_door_index = -1


    def delete_pressed(self, *args):
        if self.mode == 'add/modify rooms':
            self.delete_room()
        elif self.mode == 'add doors':
            self.delete_door()


    def add_another_door(self, *args):
        #another door will be added only if an existing door is selected
        #the new door added will be a duplicate of the existing door
        #till the time its properties are changed by the user
        if self.cur_door_index != -1:
            door_coords = self.canvas.coords(self.doors[self.cur_door_index][0])
            self.doors.append([self.canvas.create_line(door_coords[0], 
                                    door_coords[1], door_coords[2], 
                                    door_coords[3], fill='red', width = 4),
                                    self.cur_dh.get(), self.cur_ddx.get(), 
                                    self.cur_ddy.get(), self.cur_dr1.get(), 
                                    self.cur_dr2.get()
                                        ])
            #deselect already selected door
            self.deselect_door()
            #select current door
            self.cur_door_index = self.doors.__len__() - 1
            #add the door to dropdown in gui
            dropdown_values = self.on_doors((door_coords[0], door_coords[1]))
            self.door_dropdown['values'] = dropdown_values
            self.door_dropdown.current(dropdown_values.__len__()-1)


    def load_file(self, *args):
        filename = filedialog.askopenfilename()
        if not filename:
            return
        #delete existing rooms and doors to load new ones
        for rect in self.rectangles:
            self.canvas.delete(rect[0])
        for door in self.doors:
            self.canvas.delete(door[0])
        del self.rectangles[:]
        del self.doors[:]
        #variable to control whether we are looking at rooms or doors
        state = 0
        fh = open(filename, "r")
        for line in fh:
            if state == 0:
                if line == "initialparams\n":
                    continue
                else:
                    line = line.rstrip()
                    contents = line.split(' ')
                    self.grid_width = int(contents[0])
                    self.grid_height = int(contents[1])
                    self.grid_unitsize = float(contents[2])
                    self.canvas.configure(scrollregion=(0, 0, 
                                    20*self.grid_width, 20*self.grid_height))
                    self.canvas.delete("all")
                    state = 1
                    #draw grid
                    i=0
                    j=0
                    while i<=self.grid_width:
                        j=0
                        while j<=self.grid_height:
                            self.canvas.create_oval(20*i-2, 20*j-2, 20*i+2, 20*j+2)
                            j+=1
                        i+=1
            elif state == 1:
                if line == "roomsbegin\n":
                    state = 2
                else:
                    continue
            elif state == 2:
                if line == "roomsend\n":
                    state = 3
                else:
                    line = line.rstrip()
                    contents = line.split(' ')
                    #add rectangle
                    self.rectangles.append([self.canvas.create_rectangle(
                                float(contents[0]), float(contents[1]), 
                                float(contents[2]), float(contents[3]), 
                                outline = "blue"), contents[4], 
                                contents[5], contents[6], int(contents[7])
                                            ])
            elif state == 3:
                if line == "doorsbegin\n":
                    state = 4
                else:
                    continue
            elif state == 4:
                if line == "doorsend\n":
                    break
                else:
                    line = line.rstrip()
                    contents = line.split(' ')
                    #add door
                    self.doors.append([self.canvas.create_line(
                                float(contents[0]), float(contents[1]), 
                                float(contents[2]), float(contents[3]), 
                                fill = 'red'), contents[4],contents[5], 
                                contents[6], contents[7], contents[8]
                                            ])
        fh.close()
        self.write_to_console("file loaded successfully!")


    def save_file(self, *args):
        fh = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
        if fh is None:
            return
        #write grid_Width, grid_height and grid_unitsize to file
        fh.write("initialparams\n")
        fh.write(str(self.grid_width) + " " + str(self.grid_height) + " " + 
                                                str(self.grid_unitsize) + "\n")
        #write rooms to file
        fh.write("roomsbegin\n")
        for rect in self.rectangles:
            coords = self.canvas.coords(rect[0])
            fh.write(str(coords[0]) + " " + str(coords[1]) + " " + 
                            str(coords[2]) + " " + str(coords[3]) + " " + 
                            rect[1] + " " + rect[2] + " " + rect[3] + " " + 
                            str(rect[4]) + "\n")
        fh.write("roomsend\n")
        #write doors to file
        fh.write("doorsbegin\n")
        for door in self.doors:
            coords = self.canvas.coords(door[0])
            fh.write(str(coords[0]) + " " + str(coords[1]) + " " + 
                            str(coords[2]) + " " + str(coords[3]) + " " + 
                            door[1] + " " + door[2] + " " + door[3] + " " + 
                            door[4] + " " + door[5] + "\n")
        fh.write("doorsend\n")
        fh.close()
        self.write_to_console("file saved successfully!")


    def export_dungeon(self, *args):
        try:
            self.floor_height = float(self.h_str.get())
            self.export_popup.destroy()

            fh = filedialog.asksaveasfile(mode='w', defaultextension=".py")
            if fh is None:
                return

            #add initial comment
            fh.write("#file created using PySoy Dungeon Desinger\n")
            fh.write("#https://github.com/shiv05/PySoy-Dungeon-Designer\n")

            #add starting statements
            fh.write("import soy\n")
            fh.write("from time import sleep\n")
            fh.write("\n")
            fh.write("dungeon = soy.scenes.Dungeon()\n")
            fh.write("client = soy.Client()\n\n")
            fh.write("camera = soy.bodies.Camera((0,0,0))\n\n")

            roomkeyarray = []
            roomsizearray = []
            roomwallwidtharray = []
            roomposarray = []
            roommatarray = []
        
            #set up arrays for roomkeys, roomsize, wallwidth and roomposition
            for  rect in self.rectangles:
                #append to room key
                roomkeyarray.append(rect[1])

                coords = self.canvas.coords(rect[0])
                #append to room size
                roomsizearray.append((coords[2]-coords[0])/20*
                                                            self.grid_unitsize)
                roomsizearray.append(float(rect[2]))
                roomsizearray.append((coords[3]-coords[1])/20*
                                                            self.grid_unitsize)

                #append to wall width
                roomwallwidtharray.append(float(rect[3]))

                #append to room position
                roomposarray.append((coords[0]+coords[2])/2/20*
                                                            self.grid_unitsize)
                roomposarray.append(self.floor_height+(float(rect[2])/2))
                roomposarray.append((coords[1]+coords[3])/2/20*
                                                            self.grid_unitsize)

                #append to room material
                roommatarray.append(self.mat_dropdown['values'][rect[4]])

            #right the arrays to file
            fh.write("roomkeyarray = ")
            fh.write(str(roomkeyarray))
            fh.write("\n")
            fh.write("roomsizearray = ")
            fh.write(str(roomsizearray))
            fh.write("\n")
            fh.write("roomwallwidtharray = ")
            fh.write(str(roomwallwidtharray))
            fh.write("\n")
            fh.write("roomposarray = ")
            fh.write(str(roomposarray))
            fh.write("\n")
            fh.write("roommatarray = ")
            fh.write(str(roommatarray))
            fh.write("\n\n")

            #write loop to add rooms to file
            fh.write("for i in range(0," + str(self.rectangles.__len__())+"):"+
                            "\n    dungeon.rooms[roomkeyarray[i]] = soy.sce"+
                                "nes.Room(\n            soy.atoms.Size((rooms"+
                                "izearray[3*i], \n            roomsizearray[3"+
                                "*i+1], roomsizearray[3*i+2])), \n           "+
                                " roomwallwidtharray[i], roomposarray[3*i],\n"+
                                "            roomposarray[3*i+1], roomposarra"+
                                "y[3*i+2])\n")
            fh.write("    dungeon.rooms[roomkeyarray[i]].material = ")
            fh.write("soy.materials.Colored(roommatarray[i])\n")
            fh.write("    dungeon.rooms[roomkeyarray[i]]['light1'] = ")
            #TODO modify to get lights from GUI/room dimensions
            fh.write("soy.bodies.Light((4,4,4))\n")
            fh.write("    dungeon.rooms[roomkeyarray[i]]['light2'] = ")
            fh.write("soy.bodies.Light((-4,4,-4))\n\n")

            #set up parameter arrays to add doors
            room1array = []
            room2array = []
            doorXarray = []
            doorYarray = []
            doorWarray = []
            doorHarray = []

            for door in self.doors:
                coords = self.canvas.coords(door[0])
                doorflag = self.on_walls((
                                            (coords[0], coords[1]), 
                                            (coords[2], coords[3])
                                        ))
                #if door is not present on common walls, continue
                if doorflag == None:
                    continue
                #set up door arrays
                else:
                    room1array.append(roomkeyarray[doorflag[0]])
                    room2array.append(roomkeyarray[doorflag[1]])
                    doorWarray.append(float(door[2]))
                    doorHarray.append(float(door[3]))
                    doorYarray.append(float(door[1]))
                    r1 = float(door[4])
                    r2 = float(door[5])
                    doorcenter = ((r1*coords[2]+r2*coords[0])/(r1+r2), 
                                            (r1*coords[3]+r2*coords[1])/(r1+r2))
                    r1coords = self.canvas.coords(
                                            self.rectangles[doorflag[0]][0])
                    r2coords = self.canvas.coords(
                                            self.rectangles[doorflag[1]][0])
                    #left wall of room1, right wall of room2
                    if doorflag[2] == 1:
                        commoncenter = ( max(r1coords[1], r2coords[1]) + 
                                            min(r1coords[3], r2coords[3]) )/2
                        doorXarray.append((commoncenter-doorcenter[1])/20*
                                                            self.grid_unitsize)
                    #right wall of room1, left wall of room2
                    elif doorflag[2] == 2:
                        commoncenter = ( max(r1coords[1], r2coords[1]) + 
                                            min(r1coords[3], r2coords[3]) )/2
                        doorXarray.append((doorcenter[1]-commoncenter)/20*
                                                            self.grid_unitsize)
                    #top (less positive z) wall of room1, bottom wall of room2
                    elif doorflag[2] == 3:
                        commoncenter = ( max(r1coords[0], r2coords[0]) + 
                                            min(r1coords[2], r2coords[2]) )/2
                        doorXarray.append((doorcenter[0]-commoncenter)/20*
                                                            self.grid_unitsize)
                    #bottom (more positive z) wall of room1, top wall of room2
                    elif doorflag[2] == 4:
                        commoncenter = ( max(r1coords[0], r2coords[0]) + 
                                            min(r1coords[2], r2coords[2]) )/2
                        doorXarray.append((commoncenter-doorcenter[0])/20*
                                                            self.grid_unitsize)

            #right the arrays for doors to file
            fh.write("room1array = ")
            fh.write(str(room1array))
            fh.write("\n")
            fh.write("room2array = ")
            fh.write(str(room2array))
            fh.write("\n")
            fh.write("doorXarray = ")
            fh.write(str(doorXarray))
            fh.write("\n")
            fh.write("doorYarray = ")
            fh.write(str(doorYarray))
            fh.write("\n")
            fh.write("doorWarray = ")
            fh.write(str(doorWarray))
            fh.write("\n")
            fh.write("doorHarray = ")
            fh.write(str(doorHarray))
            fh.write("\n\n")

            #write loop to add doors to file
            fh.write("for i in range(0," + str(doorWarray.__len__())+"):"+
                        "\n    dungeon.connect_rooms(dungeon.rooms[room1a"+
                        "rray[i]], \n                            dungeon."+
                        "rooms[room2array[i]], \n                        "+
                        "    doorXarray[i], doorYarray[i], \n            "+
                        "                doorWarray[i], doorHarray[i])\n\n")

            #add camera
            fh.write("dungeon.rooms[roomkeyarray[0]]['cam'] = camera\n")
            fh.write("client.window.append(soy.widgets.Projector(camera))\n\n")

            #add motion
            fh.write("# Events init\n")
            fh.write("soy.events.KeyPress.init()\n")
            fh.write("soy.events.KeyRelease.init()\n")
            fh.write("soy.events.Motion.init()\n")
            fh.write("#Forces\n")
            fh.write("Rforce = soy.atoms.Vector((10, 0, 0))\n")
            fh.write("Lforce = soy.atoms.Vector((-10, 0, 0))\n")
            fh.write("Uforce = soy.atoms.Vector((0, 10, 0))\n")
            fh.write("Dforce = soy.atoms.Vector((0, -10, 0))\n")
            fh.write("Fforce = soy.atoms.Vector((0, 0, -20))\n")
            fh.write("Bforce = soy.atoms.Vector((0, 0, 20))\n")
            fh.write("# Actions\n")
            fh.write("RThrust = soy.actions.Thrust(camera, Rforce)\n")
            fh.write("LThrust = soy.actions.Thrust(camera, Lforce)\n")
            fh.write("FThrust = soy.actions.Thrust(camera, Fforce)\n")
            fh.write("BThrust = soy.actions.Thrust(camera, Bforce)\n")
            fh.write("UThrust = soy.actions.Thrust(camera, Uforce)\n")
            fh.write("DThrust = soy.actions.Thrust(camera, Dforce)\n")
            fh.write("# Events\n")
            fh.write("soy.events.KeyPress.addAction(\"D\", RThrust)\n")
            fh.write("soy.events.KeyPress.addAction(\"A\", LThrust)\n")
            fh.write("soy.events.KeyPress.addAction(\"W\", FThrust)\n")
            fh.write("soy.events.KeyPress.addAction(\"S\", BThrust)\n")
            fh.write("soy.events.KeyPress.addAction(\"Up\", UThrust)\n")
            fh.write("soy.events.KeyPress.addAction(\"Down\", DThrust)\n\n")

            #add main loop
            fh.write("if __name__ == '__main__':\n")
            fh.write("    while client:\n")
            fh.write("        sleep(.1)\n")


            #close the file
            fh.close()
            self.write_to_console("file exported successfully")


        except ValueError:
            self.write_to_console("incorrect value for room height entered")



    def export_file(self, *args):
        self.export_popup = Toplevel()
        self.export_popup.title('EXPORT')
        ttk.Label(self.export_popup, text="enter floor height").grid(column=1, 
                                    row=1, sticky=(N,W,E,S), padx=25, pady=5)
        height_entry = ttk.Entry(self.export_popup, width=5, 
                                                    textvariable=self.h_str)
        height_entry.grid(column=1, row=2, padx=25, pady=5)
        ttk.Button(self.export_popup, text="Export", 
                                command=self.export_dungeon).grid(column=1, 
                                            row=3, sticky=S, padx=25, pady=5)
        self.export_popup.bind('<Return>', self.export_dungeon)


    def write_to_console(self, message):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime(
                                        '%Y-%m-%d %H:%M:%S')
        self.console.insert(END, str(st)+">>"+message+"\n\n")
        self.console.see(END)


    def draw(self):
        self.root.mainloop()


if __name__ == '__main__':
    draw(20, 20, 5)

