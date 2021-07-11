from tkinter import *
import random
import time


class GoL(object):

    CELL_SIDE = 25

    def __init__(self):
        self.root = Tk()
        self.root.resizable(False, False)
        self.root.title("Game of Life")

        self.start_button = Button(self.root, text='Start', command=self.start_press)
        self.start_button.grid(row=0, column=0)

        self.step_button = Button(self.root, text='Step', command=self.step_press)
        self.step_button.grid(row=0, column=1)

        self.clear_button = Button(self.root, text='Clear', command=self.clear_press)
        self.clear_button.grid(row=0, column=2)

        self.clear_button = Button(self.root, text='Random', command=self.rand_press)
        self.clear_button.grid(row=0, column=3)

        self.speed = Scale(self.root, from_=1, to=100, orient=HORIZONTAL)
        self.speed.grid(row=0, column=4)
        self.speed.set(33)

        self.c = Canvas(self.root, bg='white', width=1000, height=800)
        self.c.grid(row=1, columnspan=5)

        self.is_active = False
        self.cells = []
        self.btn_pressed = False

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.c.bind('<Button-1>', self.btn_press)
        self.c.bind('<ButtonRelease-1>', self.btn_release)
        self.c.bind('<B1-Motion>', self.btn_move)
        self.is_active = False
        self.create_grid()

    def start_press(self):
        if self.is_active:
            self.start_button["text"] = "Start"
            self.start_button.config(relief=RAISED)
            self.is_active = False
        else:
            self.start_button["text"] = "Stop"
            self.start_button.config(relief=SUNKEN)
            self.is_active = True
            self.tick()

    def tick(self):
        if self.is_active:
            self.iterate()
            self.root.after(3 * self.speed.get(), self.tick)

    def step_press(self):
        if not self.is_active:
            self.iterate()

    def clear_press(self):
        self.c.delete("all")
        self.create_grid()

    def rand_press(self):
        self.c.delete("all")
        self.create_grid()
        cells = []
        for line in self.cells:
            cells.append([])
            for cell in line:
                cells[-1].append(cell)
        for x in range(len(self.cells)):
            for y in range(len(self.cells[0])):
                cells[x][y] = False if random.randint(0, 1) == 0 else True
        self.cells = cells
        self.redraw()

    def create_grid(self):
        h = int(self.c["height"])
        w = int(self.c["width"])
        for i in range(h // self.CELL_SIDE + 1):
            self.c.create_line(0, i * self.CELL_SIDE, w, i * self.CELL_SIDE,
                               width=1)
        for i in range(w // self.CELL_SIDE + 1):
            self.c.create_line(i * self.CELL_SIDE, 0, i * self.CELL_SIDE, h,
                               width=1)

        self.cells = []
        for i in range(w // self.CELL_SIDE):
            self.cells.append([])
            for j in range(h // self.CELL_SIDE):
                self.cells[i].append(False)

    def redraw(self):
        self.c.delete("all")
        for x in range(len(self.cells)):
            for y in range(len(self.cells[0])):
                self.c.create_rectangle(
                    x * self.CELL_SIDE, y * self.CELL_SIDE,
                    (x + 1) * self.CELL_SIDE, (y + 1) * self.CELL_SIDE,
                    fill='black' if self.cells[x][y] else 'white'
                )

    def iterate(self):
        cells = []
        for line in self.cells:
            cells.append([])
            for cell in line:
                cells[-1].append(cell)
        for x in range(len(self.cells)):
            for y in range(len(self.cells[0])):
                n = self.count_neighbors(x, y)
                if n < 2 or n > 3:
                    cells[x][y] = False
                elif n == 3:
                    cells[x][y] = True
        self.cells = cells
        self.redraw()

    def count_neighbors(self, x, y) -> int:
        ret = 0
        for i in range(max(0, x - 1), min(x + 1, int(self.c["width"]) // self.CELL_SIDE - 1) + 1):
            for j in range(max(0, y - 1), min(y + 1, int(self.c["height"]) // self.CELL_SIDE - 1) + 1):
                if i != x or j != y:
                    ret += 1 if self.cells[i][j] else 0
        return ret

    def btn_release(self, event):
        self.btn_pressed = False

    def btn_move(self, event):
        if self.btn_pressed:
            self.set_cell(event, False)

    def btn_press(self, event):
        self.btn_pressed = True
        self.set_cell(event, True)

    def set_cell(self, event, invert):
        x = (event.x // self.CELL_SIDE)
        y = (event.y // self.CELL_SIDE)
        self.cells[x][y] = not self.cells[x][y]

        fill = 'black'
        if invert:
            print(self.cells[x][y])
            fill = 'black' if self.cells[x][y] else 'white'
        self.c.create_rectangle(
            x * self.CELL_SIDE,
            y * self.CELL_SIDE,
            (x + 1) * self.CELL_SIDE,
            (y + 1) * self.CELL_SIDE,
            fill=fill
        )


if __name__ == '__main__':
    random.seed()
    GoL()
