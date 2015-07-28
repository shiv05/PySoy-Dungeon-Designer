from tkinter import *
from tkinter import ttk

from drawing import DungeonDesigner

root = Tk()
root.title("Dungeon Creator")

#variables for width, height and step size of grid
width_str = StringVar()
height_str = StringVar()
unitsize_str = StringVar()

#initial frame to set up grid
initialframe = ttk.Frame(root, borderwidth = 5)
initialframe.grid(column=0, row=0, sticky=(N, W, E, S))

#add labels
ttk.Label(initialframe, text="grid width").grid(column=1, row=2, 
                                                    sticky=(N, W, E, S))
ttk.Label(initialframe, text="grid height").grid(column=2, row=2, 
                                                    sticky=(N, W, E, S))
ttk.Label(initialframe, text="grid unit size").grid(column=3, row=2, 
                                                    sticky=(N, W, E, S))

#add text boxes
width_entry = ttk.Entry(initialframe, width=7, textvariable=width_str)
height_entry = ttk.Entry(initialframe, width=7, textvariable=height_str)
unitsize_entry = ttk.Entry(initialframe, width=7, textvariable=unitsize_str)
width_entry.grid(column=1, row=1)
height_entry.grid(column=2, row=1)
unitsize_entry.grid(column=3, row=1)

#add default values to text boxes
width_entry.insert(0, "35")
height_entry.insert(0, "30")
unitsize_entry.insert(0, "5")

#function to store values of width, height and unitsize
def initial_setup(*args):
    try:
        grid_width = int(width_str.get())
        grid_height = int(height_str.get())
        grid_unitsize = int(unitsize_str.get())
        #destroy initial frame
        root.destroy()
        d = DungeonDesigner(grid_width, grid_height, grid_unitsize)
        d.draw()

    except ValueError:
        print("incorrect values entered")

#add button
ttk.Button(initialframe, text="Enter", command=initial_setup).grid(column=2, 
                                                            row=3, sticky=S)
root.bind('<Return>', initial_setup)

#add padding to intial frame
for child in initialframe.winfo_children(): child.grid_configure(padx=5,pady=5)

root.mainloop()
