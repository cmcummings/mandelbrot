from mandelbrot import Mandelbrot
import pygame


SIZE = WIDTH, HEIGHT = 1280, 720


pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Mandelbrot Set")

graph = Mandelbrot(-2, 1, -1, 1, WIDTH, HEIGHT)
m_set = graph.set

for y, row in enumerate(m_set):
    for x, magnitude in enumerate(row):
        rect = pygame.Rect(x, y, 1, 1)
        if magnitude == -1: 
            color = (0, 0, 0)
        else:
            color = (255, 255, 255)
        pygame.draw.rect(screen, color, rect)