from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.agent import Agent
import numpy as np
from mesa.datacollection import DataCollector

class TrafficModel(Model):
    def __init__(self,number_of_cars,acceleration,deceleration):
        self.init_mesa()

        self.acceleration=acceleration
        self.deceleration=deceleration

        self.setup_patches(50,8)

        self.setup_cars(number_of_cars)

        self.datacollector = DataCollector(
            model_reporters={
                "RedCar":self.get_first_car_speed,
                "MinSpeed":self.get_min_speed,
                "MaxSpeed":self.get_max_speed,
            }, agent_reporters={}
        )
    def get_first_car_speed(self):
        return self.cars[0].speed
    def get_min_speed(self):
        speeds=[]
        for car in self.cars:
            speeds.append(car.speed)
        return min(speeds)
    def get_max_speed(self):
        speeds=[]
        for car in self.cars:
            speeds.append(car.speed)
        return max(speeds)

    def init_mesa(self):
        self.width, self.height=7000,700
        self.space=ContinuousSpace(self.width,self.height,True)
        self.schedule=RandomActivation(self)
        self.running=True
        self.current_id=0
    
    def setup_cars(self,number_of_cars):
        self.cars=[]
        for _ in range(number_of_cars):
            car=Car(self.next_id(),self)
            self.schedule.add(car)
            self.space.place_agent(car,(car.x,350))
            self.cars.append(car)
            self.separate_cars(car)
    def separate_cars(self,car):
        if len(self.patch_grid[car.patch_coords[0]][car.patch_coords[1]].agents)>1:
            car.x+=self.patch_size[1]
            if car.x>=self.width:
                car.x-=self.width
            self.space.move_agent(car,np.array([car.x,car.y]))
            car.update_pos()
            self.separate_cars(car)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
    
    
    def setup_patches(self,x,y):
        self.patches=[]
        self.patch_grid=[]
        self.patch_size=(x,y)
        self.patch_dimension=(self.width/self.patch_size[0],self.height/self.patch_size[1])
        for x in range(0,self.patch_size[0]):
            self.patch_grid.append([])
            for y in range(0,self.patch_size[1]):
                patch=Patch(x,y)
                self.patches.append(patch)
                self.patch_grid[x].append(patch)
                # patch.setup_patch()

    
        
class Patch:
    def __init__(self,x,y):
        self.color="green"
        self.x=x
        self.y=y
        self.agents=[]

        if y>2 and y<5:
            self.color="white"
    # def setup_patch(patch,x,y):   
    #     if y>2 and y<5:
    #         patch.color="white"

speed_min=0
speed_limit=1

class Car(Agent):


    def __init__(self,unique_id,model,**kwargs):
        super().__init__(unique_id,model)
        self.model=model
        self.x=np.random.randint(0,self.model.width)
        self.y=self.model.height/2
        self.heading=0*np.pi/180
        self.speed=np.random.uniform(0.1,1.0)

        
        self.patch_coords=(int(self.model.patch_size[0]/self.model.width*self.x),int(self.model.patch_size[1]/self.model.height*self.y))
        self.model.patch_grid[self.patch_coords[0]][self.patch_coords[1]].agents.append(self)

    
    def update_pos(self):
        patch_coords_org=self.patch_coords
        self.patch_coords=(int(self.model.patch_size[0]/self.model.width*self.x),int(self.model.patch_size[1]/self.model.height*self.y))
        if not patch_coords_org==self.patch_coords:
            self.model.patch_grid[patch_coords_org[0]][patch_coords_org[1]].agents.remove(self)
            self.model.patch_grid[self.patch_coords[0]][self.patch_coords[1]].agents.append(self)
    
    def step(self):
        patch_ahead=self.model.patch_grid[self.patch_coords[0]+1][self.patch_coords[1]] if self.patch_coords[0]+1<self.model.patch_size[0] else self.model.patch_grid[0][self.patch_coords[1]]
        car_ahead=None if not patch_ahead.agents else patch_ahead.agents[-1]
        if car_ahead:
            self.slow_down_car(car_ahead)
        else:
            self.speed_up_car()
        self.speed=max(self.speed,speed_min)
        self.speed=min(self.speed,speed_limit)

        self.x+=self.speed*140
        if self.x>=self.model.width:
            self.x-=self.model.width
        self.model.space.move_agent(self,np.array([self.x,self.y]))
        self.update_pos()

    
    def slow_down_car(self,car_ahead):
        self.speed=car_ahead.speed-self.model.deceleration

    def speed_up_car(self):
        self.speed+=self.model.acceleration