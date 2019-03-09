# interface.py


class UserInterface:
    """Handles user input and provides more information to the user on the Mandelbrot set."""

    def __init__(self, main):
        self.main = main
        self.on = False

        self.mouse_x, self.mouse_y = 0, 0
        self.selecting = False
        self.select = [(0, 0), (0, 0)]

        # Initialize mouse event handler
        main.master.bind("<Motion>", self.on_mouse_motion)
        main.master.bind('<Button-1>', self.select_p0)
        main.master.bind('<ButtonRelease-1>', self.select_p1)
        main.master.bind('<Button-3>', self.select_cancel)

        # Initialize key event handler
        main.master.bind('q', self.turn_on)
        main.master.bind('<KeyRelease-q>', self.turn_off)

    def tick(self, canvas):
        self.logic()
        self.draw(canvas)

    def select_p0(self, event):
        x, y = event.x, event.y
        self.select[0] = (x, y)
        self.selecting = True
        print(x, y)

    def select_p1(self, event):
        if self.selecting:
            x, y = event.x, event.y
            self.select[1] = (x, y)
            self.selecting = False
            print(x, y)
            self.main.new_set(self.select[0][0], self.select[0][1], self.select[1][0], self.select[1][1])

    def select_cancel(self, event):
        self.selecting = False
        print("selection canceled")

    def on_mouse_motion(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y
        # print(self.main.graph.get_point_at_index(self.mouse_y, self.mouse_x))

    def turn_on(self, event):
        self.on = True

    def turn_off(self, event):
        self.on = False

    def logic(self):
        if self.on:
            self.point = self.main.graph.get_point_at_index(self.mouse_x, self.mouse_y)
            self.mandelbrot_set_point = self.main.graph.in_set(self.point)

    def draw(self, canvas):
        if self.on:
            canvas.create_rectangle(self.mouse_x-155, self.mouse_y-55, 
                                self.mouse_x-5, self.mouse_y-5, 
                                fill="black", outline="white")
        if self.selecting:
            canvas.create_rectangle(self.select[0][0], self.select[0][1],
                                    self.mouse_x, self.mouse_y,
                                    outline="white")