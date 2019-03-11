from mandelbrot import Mandelbrot
import sys
import config as cfg
import tkinter as tk
from utils import current_ms_time, min_max
from interface import UserInterface

class Main:

    def __init__(self):
        # Initialize the pygame window
        self.master = tk.Tk()
        self.master.title(cfg.TITLE)
        self.master.resizable(0, 0)
        self.canvas = tk.Canvas(self.master, width=cfg.WIDTH, height=cfg.HEIGHT, bd=0, relief="ridge", highlightthickness=0)
        self.canvas.pack()

        # Initialize the Mandelbrot set
        self.calculating = False
        self.graph = Mandelbrot(-2, 1, -1, 1, cfg.WIDTH, cfg.HEIGHT)
        self.graph_image = self.graph.generate_image()
        self.graph.export()

        # Initialize UI
        self.ui = UserInterface(self)

        frame_timer = current_ms_time() # Helps control the speed of the program
        while True:
            if current_ms_time() - frame_timer >= 1000/cfg.FPS:
                self.tick()
                frame_timer = current_ms_time()

    def tick(self):
        # Frame loops
        self.logic()
        self.draw(self.canvas)

        self.ui.tick(self.canvas)

        # Update Tkinter window
        self.master.update_idletasks()
        self.master.update()

    def logic(self):
        pass

    def draw(self, canvas):
        if self.calculating:
            # Clear the screen
            self.canvas.create_rectangle(0, 0, cfg.WIDTH, cfg.HEIGHT, fill="black")
        else:
            # Draw the Mandelbrot graph
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.graph_image)

    def new_set(self, j1, i1, j2, i2):
        self.calculating = True
       
        x1, y1 = self.graph.get_point_at_index(i1, j1)
        x2, y2 = self.graph.get_point_at_index(i2, j2)
        
        x_min, x_max = min_max(x1, x2)
        y_min, y_max = min_max(y1, y2)
        
        self.graph = Mandelbrot(x_min, x_max, y_min, y_max, cfg.WIDTH, cfg.HEIGHT)
        self.graph_image = self.graph.generate_image()
        
        self.calculating = False


if __name__ == "__main__":
    Main()