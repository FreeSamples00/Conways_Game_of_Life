"""
Rule of Conway's Game of Life:
   Cell | neighbors | result
1.  1   |    < 2    |   0
2.  1   |   2 or 3  |   1
3.  1   |    > 3    |   0
4.  0   |     3     |   1
"""

# imports
import tkinter as tk
import math as m
import time as t


# functions
def rectangle(x, y, color):  # toggles rectangle related to xy coords
    canvas.itemconfig(cells[x][y][1], fill=color, outline='')


def grid_clicked(event):
    if not playing:
        x, y = event.x, event.y  # coords pulled from onclick event
        x_round, y_round = m.floor(x / 10), m.floor(y / 10)
        if cells[x_round][y_round][0] == 1:  # if cell is live, switch it
            rectangle(x_round, y_round, '')
            cells[x_round][y_round][0] = 0
        else:
            rectangle(x_round, y_round, active_color)  # if cell is dead, switch it
            cells[x_round][y_round][0] = 1


def toggle_gridlines():  # hides or reveals the grey gridlines
    global show_grid
    if show_grid:  # setting color
        color = ''
        show_grid = False
    else:
        color = grid_color
        show_grid = True
    for line in gridlines:  # setting each line to blank or grey
        canvas.itemconfig(line, fill=color)
    canvas.update()


def cell_check(x, y):
    adjacent_cells = [[(x - 1), (y - 1)], [x, (y - 1)], [(x + 1), (y - 1)],  # sets xy of adjacent cells
                      [(x - 1), y],                     [(x + 1), y],
                      [(x - 1), (y + 1)], [x, (y + 1)], [(x + 1), (y + 1)]]
    total = 0
    for i in adjacent_cells:  # if coord is out of bounds, set it to the opposite side
        if i[0] < 0:  # i.e. 118 goes to 0, 75 goes to 0 and reversed
            i[0] = int(grid_width / 10) - 1
        if i[1] < 0:
            i[1] = int(grid_height / 10) - 1
        if i[0] >= (grid_width / 10):
            i[0] = 0
        if i[1] >= (grid_height / 10):
            i[1] = 0
        total += cells[i[0]][i[1]][0]  # counting alive neighbors
    cell = cells[x][y][0]
    if cell == 1:  # applying rules to determine what the cell should be
        if total < 2 or total > 3:  # rules 1 & 3
            return 0
        if (total == 2) or (total == 3):  # rule 2
            return 1
    else:  # rule 4
        if total == 3:
            return 1
        else:
            return 0


def tick(run_once=False):  # the looping function that constitutes a generation / tick of the game
    global stop_request, playing, count, cells, wait_slider
    while not stop_request:
        count += 1
        # generational math
        playing = True
        changelist = []
        for x, i in enumerate(cells):  # loop for column
            for y, j in enumerate(cells[x]):  # loop for row
                cell_new, cell_old = cell_check(x, y), cells[x][y][0]
                if cell_new != cell_old:
                    changelist.append([cell_new, x, y])  # add to list change later as to not change other outcomes
                    if cell_new == 0:
                        rectangle(x, y, '')
                    else:
                        rectangle(x, y, active_color)
        for i in changelist:  # changing cell data to reflect calculations
            cells[i[1]][i[2]][0] = int(i[0])
        counter.config(text=f'Generations:\n{str(count)}')  # update display counter
        UI.update()
        canvas.update()
        if run_once:
            break
        t.sleep(sleep_time)
    if stop_request:
        playing, stop_request = False, False


def playpause(z=1):  # pause or resume tick cycle
    global playing, stop_request
    if playing:
        toggle_gridlines()
        stop_request = True  # set variable to interrupt tick() loop
        playpause_button.config(text='PLAY')
    else:  # resumes tick() loop
        playing = True
        toggle_gridlines()
        playpause_button.config(text='PAUSE')
        tick()


def one_tick(z=1):  # runs one generation without looping
    global playing
    if not playing:
        tick(run_once=True)
        playing = False


def update_wait(event):  # call from slider, changes the time_sleep variable accordingly
    global sleep_time
    sleep_time = float(wait_slider.get())


def clear():  # resets count and grid data, clears rectangles
    global playing, count
    if not playing:
        for x, i in enumerate(cells):
            for y, j in enumerate(cells[x]):
                if j[0] == 1:
                    j[0] = 0
                    rectangle(x, y, '')
        count = 0
        counter.config(text=f'Generations:\n{str(count)}')
        window.update()


# definitions
playing = False
stop_request = False
show_grid = True

grid_height = 750
grid_width = 1180
count = 0
sleep_time = 0.1

'''
UI_bg = 'tan'
canvas_color = 'white'
active_color = 'black'
grid_color = 'gray'
'''
UI_bg = 'grey'
canvas_color = 'black'
active_color = 'white'
grid_color = 'grey'

# tkinter setup
window = tk.Tk()
window.config(background=UI_bg)
window.title("Conway's Game of Life")
canvas = tk.Canvas(width=grid_width, height=grid_height)
canvas.pack(side='left')
canvas.config(background=canvas_color)
UI = tk.Frame(window, width=80, height=(grid_height), background=UI_bg)
UI.pack(side='right')

playpause_button = tk.Button(UI, text='PLAY', command=playpause)
tick_button = tk.Button(UI, text='ONE TICK', command=one_tick)
counter = tk.Label(UI, width=20, text='Generations:\n0', background=UI_bg)
wait_slider = tk.Scale(UI, from_=1, to=0, resolution=0.1, length=100, sliderlength=15, command=update_wait)
slider_label = tk.Label(UI, text='Sec.\nper\ntick', background=UI_bg)
clear_button = tk.Button(UI, text='CLEAR', command=clear)

counter.place(x=40, y=50, anchor='center')
wait_slider.place(x=60, y=100, anchor='n')
playpause_button.place(x=40, y=250, anchor='center')
tick_button.place(x=40, y=300, anchor='center')
slider_label.place(x=20, y=150, anchor='center')
clear_button.place(x=40, y=350, anchor='center')
wait_slider.set(0.1)

# creates a list of columns in the grid, arranged by x coordinate
# each element is a cell, containing its state (1 = alive, 0 = dead) and its accompanying tkinter rectangle
cells = []
x, y = 0, 0
for i in range(int(grid_width / 10)):
    cells.append([])
    y = 0
    for j in range(int(grid_height / 10)):
        cells[i].append([0, canvas.create_rectangle(x, y, (x + 10), (y + 10), fill='', outline='')])
        y += 10
    x += 10

# creates a list of lines on the tkinter canvas, forming a grid
gridlines = []
for x in range(int(grid_width / 10)):
    gridlines.append(canvas.create_line(x * 10, 0, x * 10, 760, fill=grid_color))
for y in range(int(grid_height / 10)):
    gridlines.append(canvas.create_line(0, y * 10, 1290, y * 10, fill=grid_color))

# calls
canvas.bind("<Button-1>", grid_clicked)
window.bind("<space>", playpause)
window.mainloop()
