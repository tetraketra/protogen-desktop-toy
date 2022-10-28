from ctypes import windll, Structure, c_long, byref
from time import time


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def getMousePos():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return [pt.x, pt.y]

tracker = {"t1":0, "t2":0, "pos1":[0,0], "pos2":[0,0], "vel1":[0,0], "vel2":[0,0], "acc":[0,0]} #t1 always older than t2

def update_time():
    tracker["t1"] = tracker["t2"]
    tracker["t2"] = time()
def update_pos():
    tracker["pos1"] = tracker["pos2"]
    tracker["pos2"] = getMousePos()
def update_vel():
    tracker["vel1"] = tracker['vel2']
    tracker["vel2"] = [(tracker["pos2"][0] - tracker["pos1"][0]) / (tracker["t2"] - tracker["t1"]), (tracker["pos2"][1] - tracker["pos1"][1]) / (tracker["t2"] - tracker["t1"])]
def update_acc():
    tracker["acc"] = ((tracker["vel2"][0] - tracker["vel1"][0]) / (tracker["t2"] - tracker["t1"]), (tracker["vel2"][1] - tracker["vel1"][1]) / (tracker["t2"] - tracker["t1"]))

n = 0
def update_tracker(update_every_n_frames):
    global n
    if not n:
        update_time()
        update_pos()
        update_vel()
        update_acc()
    n = (n + 1) % update_every_n_frames
