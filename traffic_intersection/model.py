from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.agent import Agent
import numpy as np
from mesa.datacollection import DataCollector

class TrafficModel(Model):
    def __init__(self,**params):
        self.init_mesa()

        # self.acceleration=acceleration
        # self.deceleration=deceleration
        self.freq_north=params["freq_north"]
        self.freq_east=params["freq_east"]
        self.ticks_at_last_change=0
        self.green_length=params["green_length"]
        self.yellow_length=params["yellow_length"]
        self.max_brake=params["max_brake"]
        self.max_accel=params["max_accel"]
        self.speed_limit=params["speed_limit"]

        self.accidents=[]
        self.cars=[]

        self.setup_patches(34,34)

        self.lights=[]

        self.lights.append(self.patch_grid[17][18])
        self.lights[-1].color="green"
        self.lights.append(self.patch_grid[16][17])
        self.lights[-1].color="red"

        # self.setup_cars(number_of_cars)

        self.datacollector = DataCollector(
            model_reporters={
                "Waiting":self.get_waiting,
                "Wait_east":self.get_wait_east,
                "Wait_north":self.get_wait_north,
            }, agent_reporters={}
        )
    def get_waiting(self):
        num=0
        for car in self.cars:
            if car.speed==0:
                num+=1
        return num 
    def get_wait_east(self):
        num=0
        for car in self.cars:
            if car.speed==0 and car.heading==0:
                num+=1
        return num 
    def get_wait_north(self):
        num=0
        for car in self.cars:
            if car.speed==0 and not car.heading==0:
                num+=1
        return num 
    

    def init_mesa(self):
        self.width, self.height=7000,7000
        self.space=ContinuousSpace(self.width,self.height,True)
        self.schedule=RandomActivation(self)
        self.running=True
        self.current_id=0
    
    def make_new_car(self,freq,x,y,heading):
        if np.random.uniform(0,100)<freq and not self.patch_grid[x][y].agents:
            car=Car(self.next_id(),self,x,y,heading)
            self.schedule.add(car)
            self.space.place_agent(car,(car.x,car.y))
            self.cars.append(car)


    def is_elapsed(self,time_length):
        return self.schedule.time-self.ticks_at_last_change>time_length

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.check_for_collisions()
        self.make_new_car(self.freq_north,17,33,90)
        self.make_new_car(self.freq_east,0,17,0)
        if self.is_elapsed(self.green_length):
            self.change_to_yellow()
        for light in self.lights:
            if light.color=="yellow" and self.is_elapsed(self.yellow_length):
                self.change_to_red()

    def check_for_collisions(self):
        for_removal=[]
        for accident in self.accidents:
            accident.clear_in-=1
            if accident.clear_in<=0:
                for_removal.append(accident)
        for accident in for_removal:
            self.accidents.remove(accident)
        for patch in self.patches:
            if len(patch.agents)>1:
                self.accidents.append(patch)
                patch.clear_in=5
                for car in patch.agents.copy():
                    car.die()

    def change_to_yellow(self):
        for light in self.lights:
            if light.color=="green":
                light.color="yellow"
                self.ticks_at_last_change=self.schedule.time
    def change_to_red(self):
        for light in self.lights:
            if light.color=="yellow":
                light.color="red"
            else:
                light.color="green"
            self.ticks_at_last_change=self.schedule.time

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
        self.x=x
        self.y=y
        self.agents=[]
        self.clear_in=0

        if y<=18 and y>=16 or x<=18 and x>=16:
            self.color="black"
        else:
            self.color="green"


speed_min=0
speed_limit=1

class Car(Agent):
    def __init__(self,unique_id,model,x,y,heading):
        super().__init__(unique_id,model)
        self.model=model
        self.x=x*model.patch_dimension[0]+model.patch_dimension[0]/2
        self.y=y*model.patch_dimension[1]+model.patch_dimension[1]/2
        self.heading=heading*np.pi/180
        # self.speed=np.random.uniform(0.1,1.0)
        self.color=np.random.choice(["brown","blue","orange","teal","white","grey","purple","cyan","magenta"])
        self.speed=0
        self.dead=False
        
        self.patch_coords=(int(self.model.patch_size[0]/self.model.width*self.x),int(self.model.patch_size[1]/self.model.height*self.y))
        # self.model.patch_grid[self.patch_coords[0]][self.patch_coords[1]].agents.append(self)
        self.current_patch=self.model.patch_grid[self.patch_coords[0]][self.patch_coords[1]]
        self.current_patch.agents.append(self)
        self.adjust_speed()

    def adjust_speed(self):
        min_speed=max(self.speed-self.model.max_brake,0)
        max_speed=min(self.speed+self.model.max_accel,self.model.speed_limit)

        target_speed=max_speed
        blocked_patch=self.next_blocked_patch()
        if not blocked_patch==None:
            space_ahead=self.distance(blocked_patch)-1
            while(self.breaking_distance_at(target_speed)>space_ahead and target_speed>min_speed):
                target_speed-=1
        self.speed=target_speed

    def breaking_distance_at(self,speed_at_this_step):
        min_speed_at_next_step=max(speed_at_this_step-self.model.max_brake,0)
        return speed_at_this_step+min_speed_at_next_step
    
    def distance(self,patch):
        return abs(self.patch_coords[0]-patch.x)+abs(self.patch_coords[1]-patch.y)

    def patch_ahead(self,dist):
        if self.heading==0:
            if self.patch_coords[0]+dist>=self.model.patch_size[0]:
                return None
            return self.model.patch_grid[self.patch_coords[0]+dist][self.patch_coords[1]]
        else:
            # if self.patch_coords[1]+dist>=self.model.patch_size[1]:
            if self.patch_coords[1]-dist<0:
                return None
            return self.model.patch_grid[self.patch_coords[0]][self.patch_coords[1]-dist]

    def next_blocked_patch(self):
        patch_to_check=self.current_patch
        while not patch_to_check==None and not self.is_blocked(patch_to_check):
            patch_to_check=self.patch_ahead(self.distance(patch_to_check)+1)
        return patch_to_check

    def is_blocked(self,patch):
        for car in patch.agents:
            if not car==self:
                return True
        for accident in self.model.accidents:
            if accident==patch:
                return True
        if patch.color=="red":
            return True
        if patch.color=="yellow" and not patch==self.current_patch:
            return True
        return False


    def update_pos(self):
        patch_coords_org=self.patch_coords
        self.patch_coords=(int(self.model.patch_size[0]/self.model.width*self.x),int(self.model.patch_size[1]/self.model.height*self.y))
        if not patch_coords_org==self.patch_coords:
            self.model.patch_grid[patch_coords_org[0]][patch_coords_org[1]].agents.remove(self)
            self.current_patch=self.model.patch_grid[self.patch_coords[0]][self.patch_coords[1]]
            self.current_patch.agents.append(self)

    def die(self):
        if not self in self.model.cars:return
        self.model.space.remove_agent(self)
        self.model.cars.remove(self)
        self.model.schedule.remove(self)
        self.current_patch.agents.remove(self)

    def step(self):
        self.adjust_speed()
        for _ in range(self.speed):
            if self.heading==0:
                self.x+=self.model.patch_dimension[0]
            else:
                self.y-=self.model.patch_dimension[1]
            # if self.x>=self.model.width or self.y>=self.model.height:
            if self.x>=self.model.width or self.y<0:
                self.die()
                return
            self.model.space.move_agent(self,np.array([self.x,self.y]))
            self.update_pos()
            if self.current_patch in self.model.accidents:
                self.current_patch.clear_in=5
                self.die()   