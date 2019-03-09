# utils.py
import time

def current_ms_time():
    return int(round(time.time()* 1000))

def min_max(a, b):
    minim = a
    maxim = b
    if b < a:
        minim = b
        maxim = a
    return minim, maxim