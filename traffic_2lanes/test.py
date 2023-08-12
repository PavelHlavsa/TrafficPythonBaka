import timeit
import numpy as np

def dist1(lanes=[6,7],lane=7):
    return min(map(lambda y:abs(y-lane),lanes))
           
def dist2(lanes=[6,7],lane=7):
    return min(lanes,key=lambda y:abs(y-lane))

class Car():
    def __init__(self) -> None:
        self.speed=np.random.uniform(0.1,1.0)
        
    def __lt__(self, other):
        return self.speed < other.speed

    def __eq__(self, other):
        return self.speed == other.speed
cars=[Car() for _ in range(5000)]

def min_speed_1(cars): #1.01
    min_speed=10
    for car in cars:
        if car.speed<min_speed:
            min_speed=car.speed
    return min_speed 

def min_speed_2(cars): #2.14
    return min(map(lambda car: car.speed,cars))

def min_speed_3(cars): # 1.91
    return min(cars,key=lambda car: car.speed)

def min_speed_4(cars): # 4.14
    min_speed=10
    for car in cars:
        min_speed=min(min_speed,car.speed)
    return min_speed

def min_speed_5(cars): # 1.19
    return min([car.speed for car in cars])

def min_speed_6(cars): # 2.51
    return min(cars) #dunder methods

def min_speed_7(cars): # 2.23
    return np.min([car.speed for car in cars])


print(timeit.timeit(min_speed_1,number=5000))      
print(timeit.timeit(min_speed_2,number=5000))      
print(timeit.timeit(min_speed_3,number=5000))      
print(timeit.timeit(min_speed_4,number=5000))      
print(timeit.timeit(min_speed_5,number=5000))     
print(timeit.timeit(min_speed_6,number=5000))     
print(timeit.timeit(min_speed_7,number=5000))     