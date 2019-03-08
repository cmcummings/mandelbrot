from mandelbrot import Mandelbrot
import sys
import config as cfg
import tkinter as tk


class Main:

    def __init__(self):
        # Initialize the pygame window
        self.master = tk.Tk()
        self.master.title("Mandelbrot")
        self.master.resizable(0, 0)
        self.canvas = tk.Canvas(self.master, width=cfg.WIDTH, height=cfg.HEIGHT, bd=0, relief="ridge", highlightthickness=0)
        self.canvas.pack()

        # Intialize the Mandelbrot set
        graph = Mandelbrot(-2, 1, -1, 1, cfg.WIDTH, cfg.HEIGHT)
        self.graph_image = graph.generate_image()
        graph.export()

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.graph_image)

        while True:
            self.tick()

    def tick(self):
        self.logic()
        self.draw(self.canvas)

        self.master.update_idletasks()
        self.master.update()

    def logic(self):
        pass

    def draw(self, canvas):
        pass


if __name__ == "__main__":
    Main()