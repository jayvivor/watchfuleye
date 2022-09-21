import random
import math

def ranged(value, maximum=100, minimum=0, whole=True):
    fixed = max(minimum, min(maximum, value))
    return int(fixed) if whole else fixed

def softmax_pick(dataset, temperature=10):  #TODO: random choice density function
    for point in dataset:
        for label, score in point:
            pass

def return_self(item):  #This probably already exists in some form but whatever
    return item

def listed(items: list):
    size = len(items)
    if size == 1:
        return f"{items[0]}"
    elif size == 2:
        return f"{items[0]} and {items[1]}"
    else:
        return f"{''.join([i+', ' for i in items[0:size-1]])} and {items[size-1]}"

def random_within_circle(diameter=100):
    radius = diameter/2
    x = random.uniform(-1*radius, radius)
    y = random.uniform(-1*radius, radius)
    if math.sqrt(x**2+y**2) <= radius:
        return x+radius,y+radius
    return random_within_circle(diameter)

class Timestamp:

    def __init__(self, hour, day):
        self.hour = hour
        self.day = day

class Dataset:  #Datatype for handling scoreboards and sorting players by certain values etc.

    def __init__(self, labels, key, label_display_key=None):
        self.label_display_key = label_display_key if label_display_key else return_self
        self.data_dict = {}
        for l in labels:
            self.data_dict.update({l:key(l)})
    
    def sort(self):
        sorted_keys = sorted(self.data_dict.keys(), key=lambda l: self.data_dict[l])
        return [(key,self.data_dict[key]) for key in sorted_keys]

    def display(self):
        return "".join([f"{self.label_display_key(label)} - {score}\n" for label, score in self.sort()])