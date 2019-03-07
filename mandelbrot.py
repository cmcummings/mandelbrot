# mandelbrot.py
from threading import Thread
from PIL import Image, ImageDraw, ImageTk
import config as cfg
import os


class Mandelbrot:
    """Calculates the Mandelbrot set within a given area and scale. 
       Also calculates the colors to draw the set."""

    def __init__(self, x_min, x_max, y_min, y_max, x_scl, y_scl):
        # Store the constructor values
        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max
        self.x_scl, self.y_scl = x_scl, y_scl # The scale is how many points on each axis should be calculated within the constraints

        # Initialize the arrays
        self.set = [[]]
        self.colors = [[]]
        
        # Testing
        # print(self.calculate_point((-1.04039, 0.2509294j)))
        # print(self.calculate_point((-0.1155989, 0.7639405j)))
        # print(self.calculate_point((0, 0)))

    def calculate(self):
        """Calculates the Mandelbrot set based on the parameters from the constructor. 
           This function is called on initialization of the Mandelbrot class.
           Returns a 2D array containing the set."""
        # Initialize the set array
        self.set = [[0 for i in range(self.x_scl)] for j in range(self.y_scl)]
        self.points = [[0 for i in range(self.x_scl)] for j in range(self.y_scl)]
        print(len(self.set), len(self.set[0]))
        print(len(self.points), len(self.points[0]))

        x_increment = (self.x_max - self.x_min) / self.x_scl
        y_decrement = (self.y_max - self.y_min) / self.y_scl

        for i in range(self.y_scl):
            for j in range(self.x_scl):
                x = self.x_min + j * x_increment
                y = self.y_max - i * y_decrement
                self.points[i][j] = (x, complex(0, y))

        num_threads = 1
        rows_per_thread = int(self.y_scl / num_threads)
        thread_list = []
        for i in range(num_threads):
            start = i*rows_per_thread
            thread = Thread(target=self.threaded_calculate, args=(start, self.points[start:start+rows_per_thread]))
            thread_list.append(thread)
            thread.start()
            thread.join() # Make sure main thread waits for other threads
        print("done calculating")

        print(self.set[0] == self.set[50])
        print(self.points[0] == self.points[50])

    def threaded_calculate(self, start, part):
        for i in range(len(part)):
            for j in range(len(part[i])):
                self.set[start+i][j] = self.calculate_point(part[i][j])
    
    def calculate_point(self, point):
        """Determines if the point is a part of the Mandelbrot set.
           Returns the number of iterations that it takes for the magnitude of Z to surpass 2, or -1 if the point is a part of the set."""
        c = point[0] + point[1]
        iters = 0
        max_iters = 160
        z = 0
        while iters < max_iters:
            iters += 1
            z = z ** 2 + c
            magnitude = abs(z)
            if magnitude > 2:
                return iters
        return -1

    def calculate_colors(self):
        """Calculates and the colors based on the current Mandelbrot set.
           Returns a 2D array containing RGB tuples."""
        self.colors = [[0 for i in range(self.x_scl)] for j in range(self.y_scl)]
        print(len(self.colors[0]), len(self.colors))

        for i in range(self.y_scl):
            for j in range(self.x_scl):
                point = self.set[i][j]
                if point == -1:
                    self.colors[i][j] = cfg.BLACK
                else:
                    self.colors[i][j] = (point*5, 0, 0)
        
        return self.colors

    def export(self):
        """Exports the Mandelbrot set into a PNG image.
           Returns a Tkinter PhotoImage object."""
        file_name = "Mandelbrot_x:(" + str(self.x_min) + ":" + str(self.x_max) + ")_y:(" + str(self.y_min) + ":" + str(self.y_max) + ")_scl:(" + str(self.x_scl) + "x" + str(self.y_scl) + ")"
        self.file_path = os.path.join(cfg.CAPTURES_DIR, file_name + ".png")

        self.image = Image.new("RGB", (self.x_scl, self.y_scl), color=cfg.BLACK)
        draw = ImageDraw.Draw(self.image)

        num_threads = 1
        rows_per_thread = int(self.y_scl / num_threads)
        thread_list = []
        for i in range(num_threads):
            start = i*rows_per_thread
            thread = Thread(target=self.threaded_draw, args=(draw, start, self.colors[start:start+rows_per_thread]))
            thread_list.append(thread)
            thread.start()
            thread.join() # Make sure main thread waits for all other threads
        print("done drawing")

        return ImageTk.PhotoImage(self.image)

    def threaded_draw(self, draw, start, part):
        for i in range(len(part)):
            for j in range(len(part[i])):
                color = self.colors[i+start][j]
                draw.point((j, i+start), color)

    def save(self):
        self.image.save(self.file_path, "PNG")
        print("Saved to:", self.file_path)

