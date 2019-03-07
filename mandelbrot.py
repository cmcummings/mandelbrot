# mandelbrot.py
from threading import Thread


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
        
        self.calculate()
        
        # Testing
        # print(self.calculate_point((-1.04039, 0.2509294j)))
        # print(self.calculate_point((-0.1155989, 0.7639405j)))
        # print(self.calculate_point((0, 0)))
        
    def calculate(self):
        """Calculates the Mandelbrot set based on the parameters from the constructor. 
           This function is called on initialization of the Mandelbrot class.
           Returns a 2D array containing the set."""
        # Initialize the set array
        self.set = [[0] * self.x_scl] * self.y_scl
        self.points = [[0] * self.x_scl] * self.y_scl

        x_increment = (self.x_max - self.x_min) / self.x_scl
        y_decrement = (self.y_max - self.y_min) / self.y_scl

        for i in range(self.y_scl):
            for j in range(self.x_scl):
                x = self.x_min + j * x_increment
                y = self.y_max - i * y_decrement
                self.points[i][j] = (x, y)

        num_threads = 4
        rows_per_thread = int(self.y_scl / num_threads)
        thread_list = []
        for i in range(num_threads):
            start = i*rows_per_thread
            thread = Thread(target=self.threaded_calculate, args=(self.set[start:start+rows_per_thread],))
            thread_list.append(thread)
            thread.start()

    def threaded_calculate(self, part):
        for i in range(len(part)):
            for j in range(len(part[i])):
                self.set[i][j] = self.calculate_point(self.points[i][j])
    
    def calculate_point(self, point):
        """Determines if the point is a part of the Mandelbrot set.
           Returns the number of iterations that it takes for the magnitude of Z to surpass 2, or -1 if the point is a part of the set."""
        c = point[0] + point[1]
        iters = 0
        max_iters = 1000
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
        pass