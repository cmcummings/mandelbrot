# mandelbrot.py
from threading import Thread
from multiprocessing import Pool as ThreadPool
from PIL import Image, ImageDraw, ImageTk
import config as cfg
import os, time
from math import log
from colorsys import hsv_to_rgb

class Mandelbrot:

    def __init__(self, x_min, x_max, y_min, y_max, x_scl, y_scl):
        # Time measurement
        ti = time.time()

        # Store the constructor values
        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max
        self.x_scl, self.y_scl = x_scl, y_scl # The scale is how many points on each axis should be calculated within the bounds

        # Initialize the colors array
        self.colors = [[0 for i in range(self.x_scl)] for j in range(self.y_scl)]

        # Distance between each point that will be calculated
        self.x_increment = (self.x_max - self.x_min) / self.x_scl
        self.y_decrement = (self.y_max - self.y_min) / self.y_scl

        # Split calculations into threads
        rows_per_thread = int(self.y_scl / cfg.THREADS)
        thread_list = []
        for i in range(cfg.THREADS):
            start = i*rows_per_thread
            thread = Thread(target=self.calculate_thread, args=(start, rows_per_thread))
            thread_list.append(thread)
            thread.start()
        for thread in thread_list:
            thread.join()
                    
        # If there are leftover rows that need to be calculated
        leftover = self.y_scl - rows_per_thread * cfg.THREADS
        if leftover > 0:
            self.calculate_thread(self.y_scl - leftover, leftover)
        
        tf = time.time()
        print("Done in", tf-ti, "seconds.")

    def calculate_thread(self, start, num_rows):
        print("Calculating from y=", start, "to y=", start+num_rows-1)
        """Calculates the set and colors."""
        for i in range(start, start+num_rows):
            for j in range(self.x_scl):
                x, y = self.get_point_at_index(i, j) # Convert the array index to a point on the graph
                point = (x, complex(0, y)) # Get the complex point
                set_point = self.in_set(point) # If the point is in the set
                color = self.get_set_point_color(set_point) # Get the color of the point
                self.colors[i][j] = color # Save the color

    def get_point_at_index(self, i, j):
        """Calculates the real point at an array index."""
        x = self.x_min + j * self.x_increment
        y = self.y_max - i * self.y_decrement
        return x, y

    def in_set(self, point):
        """Determines if the point is a part of the Mandelbrot set.
           Returns the number of iterations that it takes for the magnitude of Z to surpass 2, or -1 if the point is a part of the set."""
        c = point[0] + point[1]
        iters = 0
        max_iters = cfg.MAX_ITERATIONS
        z = 0
        while iters < max_iters:
            iters += 1
            z = z ** 2 + c
            magnitude = abs(z)
            if magnitude > 2:
                return iters
        return -1

    def get_set_point_color(self, point):
        """Returns the color that should be drawn based on the result of the Mandelbrot function."""
        if point == -1: # If part of set
            return cfg.BLACK
        hue = int(255 * point / cfg.MAX_ITERATIONS)
        saturation = 255
        value = 255 if point < cfg.MAX_ITERATIONS else 0
        return (hue, saturation, value)

    def generate_image(self):
        """Generates a PIL image of the set. Returns a Tkinter image."""
        self.image = Image.new("HSV", (self.x_scl, self.y_scl), color=cfg.BLACK)
        draw = ImageDraw.Draw(self.image)

        num_threads = cfg.THREADS
        rows_per_thread = int(self.y_scl / num_threads)
        thread_list = []
        for i in range(num_threads):
            start = i*rows_per_thread
            thread = Thread(target=self.threaded_tk_image_creation, args=(draw, start, rows_per_thread))
            thread_list.append(thread)
            thread.start()
            thread.join() # Make sure main thread waits for all other threads
        print("Image created.")

        self.image = self.image.convert("RGB")

        return ImageTk.PhotoImage(self.image)

    def threaded_tk_image_creation(self, draw, start, num_rows):
        """Drawing of the image."""
        for i in range(start, start+num_rows):
            for j in range(self.x_scl):
                color = self.colors[i][j]
                draw.point((j, i), color)

    def export(self):
        """Saves an image of the Mandelbrot set in captures/. 
            generate_image() must be ran before this."""
        file_name = "Mandelbrot_x=(" + str(self.x_min) + " to " + str(self.x_max) + ")_y=(" + str(self.y_min) + " to " + str(self.y_max) + ")_scl=(" + str(self.x_scl) + "x" + str(self.y_scl) + ")"
        file_path = os.path.join(cfg.CAPTURES_DIR, file_name + ".png")
        
        self.image.save(file_path, "PNG")
        print("Saved to:", file_path)