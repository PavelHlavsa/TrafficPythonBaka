from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.agent import Agent
import numpy as np
from mesa.datacollection import DataCollector
import random

class TrafficModel(Model):
    def __init__(self,number_of_cars,acceleration,deceleration,max_patience):
        self.init_mesa()

        self.lanes=[7,9]
        self.max_patience=max_patience
        self.acceleration=acceleration
        self.deceleration=deceleration

        self.set_up_patches(40,16)

        # self.set_up_cars(number_of_cars)
        self.number_of_cars=number_of_cars
        self.cars=[]
        self.create_or_remove_cars()

        self.datacollector = DataCollector(
            model_reporters={
                "AverageSpeed":self.get_average_speed,
                "MinSpeed":self.get_min_speed,
                "MaxSpeed":self.get_max_speed,
                "AveragePatience":self.get_average_patience,
                "MinPatience":self.get_min_patience,
                "MaxPatience":self.get_max_patience,
                "CarsOnLane1":self.get_lane_1_cars,
                "CarsOnLane2":self.get_lane_2_cars,
            }, agent_reporters={}
        )
    def get_lane_1_cars(self):
        num=0
        for car in self.cars:
            if car.target_lane==self.lanes[0]:num+=1
        return num
    def get_lane_2_cars(self):
        num=0
        for car in self.cars:
            if car.target_lane==self.lanes[1]:num+=1
        return num
    def get_average_patience(self):
        patience=0
        for car in self.cars:
            patience+=car.patience
        return patience/len(self.cars)
    def get_min_patience(self):
        patiences=[]
        for car in self.cars:
            patiences.append(car.patience)
        return min(patiences)
    def get_max_patience(self):
        patiences=[]
        for car in self.cars:
            patiences.append(car.patience)
        return max(patiences)
    def get_average_speed(self):
        speed=0
        for car in self.cars:
            speed+=car.speed
        return speed/len(self.cars)
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
        self.width, self.height=7000,3400
        self.space=ContinuousSpace(self.width,self.height,True)
        self.schedule=RandomActivation(self)
        self.running=True
        self.current_id=0
    
    # def set_up_cars(self,number_of_cars):
    #     self.cars=[]
    #     for _ in range(number_of_cars):
    #         car=Car(self.next_id(),self)
    #         self.schedule.add(car)
    #         self.space.place_agent(car,(car.x,350))
    #         self.cars.append(car)
    #         self.separate_cars(car)
    
    def create_or_remove_cars(self):
        road_patches=[patch for patch in self.patches if patch.y in self.lanes]

        self.number_of_cars=min(self.number_of_cars,len(road_patches))

        free_patches=[patch for patch in road_patches if not patch.agents]

        for i in range(self.number_of_cars-len(self.cars)):
            car=Car(self.next_id(),self)
            free_patch=random.choice(free_patches)
            free_patches.remove(free_patch)
            car.patch_coords=(free_patch.x,free_patch.y)
            car.x=free_patch.x*self.patch_dimension[0]+self.patch_dimension[0]/2
            car.y=free_patch.y*self.patch_dimension[1]+self.patch_dimension[1]/2
            free_patch.agents.append(car)
            car.update_pos()
            self.schedule.add(car)
            self.space.place_agent(car,(car.x,car.y))
            self.cars.append(car)

            car.target_lane=free_patch.y
            car.top_speed=random.uniform(0.5,1.0)
            car.speed=0.5
            car.patience=random.random()*self.max_patience
        # deleting cars is this even nececarry, i dont get what does it do
        # if len(self.cars)>self.number_of_cars:
        #     n=len(self.cars)-self.number_of_cars
        # if count turtles > number-of-cars [
        #     let n count turtles - number-of-cars
        #     ask n-of n [ other turtles ] of selected-car [ die ]
        # ]

    def step(self):
        self.create_or_remove_cars()
        self.schedule.step()
        self.datacollector.collect(self)
    
    
    def set_up_patches(self,x,y):
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
    
    def separate_cars(self,car):
        if len(self.patch_grid[car.patch_coords[0]][car.patch_coords[1]].agents)>1:
            car.x+=self.patch_size[1]
            if car.x>=self.width:
                car.x-=self.width
            self.space.move_agent(car,np.array([car.x,car.y]))
            car.update_pos()
            self.separate_cars(car)
        
class Patch:
    def __init__(self,x,y):
        self.color="green"
        self.x=x
        self.y=y
        self.agents=[]

        if y>8 and y<12:
            self.color="white"

class Car(Agent):


    def __init__(self,unique_id,model,**kwargs):
        super().__init__(unique_id,model)
        self.model=model
        # self.x=np.random.randint(0,self.model.width)
        # self.x=np.random.randint(0,self.model.patch_size[0])*self.model.patch_dimension[0]
        # self.y=self.model.height/2
        # self.heading=0*np.pi/180
        self.heading=0
        self.speed=np.random.uniform(0.1,1.0)
        # self.cone_up=[(-1,0),(-1,1),(-1,2),(0,1),(0,2),(1,0),(1,1),(1,2)]
        # self.cone_down=[(-1,0),(-1,-1),(-1,-2),(0,-1),(0,-2),(1,0),(1,-1),(1,-2)]
        # self.cone_up=[(-1,0),(-1,1),(0,1),(1,0),(1,1)]
        # self.cone_down=[(-1,0),(-1,-1),(0,-1),(1,0),(1,-1)]
        self.cone_up=[(-1,0),(0,1),(1,0)]
        self.cone_down=[(-1,0),(0,-1),(1,0)]
        self.cone_right2=[(1,0),(2,0),(0,-1),(1,-1),(0,1),(1,1)]
        self.cone_right=[(1,0),(0,-1),(0,1)]
        
        # self.patch_coords=(int(self.model.patch_size[0]/self.model.width*self.x),int(self.model.patch_size[1]/self.model.height*self.y))
        # self.model.patch_grid[self.patch_coords[0]][self.patch_coords[1]].agents.append(self)

    
    def update_pos(self):
        patch_coords_org=self.patch_coords
        self.patch_coords=(int(self.model.patch_size[0]/self.model.width*self.x),int(self.model.patch_size[1]/self.model.height*self.y))
        if not patch_coords_org==self.patch_coords:
            self.model.patch_grid[patch_coords_org[0]][patch_coords_org[1]].agents.remove(self)
            self.model.patch_grid[self.patch_coords[0]][self.patch_coords[1]].agents.append(self)
            
        self.model.space.move_agent(self,np.array([self.x,self.y]))
    
    def step(self):
        self.move_forward()
        if self.patience<=0: self.choose_new_lane()
        if not self.patch_coords[1]==self.target_lane:self.move_to_target_lane()
        self.update_pos()
    
    def move_to_target_lane(self):
        up=self.target_lane<self.patch_coords[1]
        # self.heading=3.14/2 if up else -3.14/2
        blocking_cars=self.get_cone(self.cone_up if up else self.cone_down)
        # blocking_car=min(
        #     map(lambda agent: abs(agent.x-self.x)+abs(agent.y-self.y),blocking_cars)
        # ) if blocking_cars else None
        blocking_cars=list(filter(lambda car:abs(car.x-self.x)+abs(car.y-self.y),blocking_cars))
        blocking_car=min(
            blocking_cars,key=lambda agent: abs(agent.x-self.x)+abs(agent.y-self.y)
        ) if blocking_cars else None
        if not blocking_car:
            self.y+=self.speed*28*4 *(-1 if up else 1)
            round(self.y,1)
        else:
            self.slow_down_car() if blocking_car.x>self.x else self.speed_up_car()
            # ifelse towards blocking-car <= 180 [ slow-down-car ] [ speed-up-car ]

    def choose_new_lane(self):
        other_lanes=self.model.lanes.copy()
        # other_lanes.remove(self.patch_coords[1])
        other_lanes.remove(self.target_lane)
        if other_lanes:
            min_dist=min(map(lambda y:abs(y-self.patch_coords[1]),other_lanes))
            closest_lanes=list(filter(lambda y:abs(y-self.patch_coords[1])==min_dist,other_lanes))
            self.target_lane=random.choice(closest_lanes)
            self.patience=self.model.max_patience
    def move_forward(self):
        self.speed_up_car()
        # blocking_cars=self.agents_in_cone()
        blocking_cars=self.get_cone(self.cone_right2 if self.speed>0.5 else self.cone_right)
        blocking_cars=list(filter(lambda car:car.x>self.x,blocking_cars))
        blocking_car=min(blocking_cars,key=lambda agent: abs(agent.x-self.x)+abs(agent.y-self.y)) if blocking_cars else None
        # blocking_car=min(
        #     map(lambda agent: abs(agent.x-self.x)+abs(agent.y-self.y),blocking_cars)
        # )
        if blocking_car:
            self.speed=blocking_car.speed
            self.slow_down_car()
        self.x+=self.speed*140
        if self.x>=self.model.width: self.x-=self.model.width
    def get_cone(self,cone_type):
        agents=[]
        for i in cone_type:
            agents+=(self.get_patch(self.patch_coords[0]+i[0],self.patch_coords[1]+i[1]).agents)
        return agents
    # def agents_in_cone(self):
    #     return self.get_patch(self.patch_coords[0]+1,self.patch_coords[1]).agents+\
    #         self.get_patch(self.patch_coords[0]+2,self.patch_coords[1]).agents+\
    #         self.get_patch(self.patch_coords[0]+1,self.patch_coords[1]-1).agents+\
    #         self.get_patch(self.patch_coords[0]+1,self.patch_coords[1]+1).agents+\
    #         self.get_patch(self.patch_coords[0],self.patch_coords[1]+1).agents+\
    #         self.get_patch(self.patch_coords[0],self.patch_coords[1]-1).agents
       
    
    def get_patch(self,x,y):
        if x>=self.model.patch_size[0]: x-=self.model.patch_size[0]
        if y>=self.model.patch_size[1]: y-=self.model.patch_size[1]
        return self.model.patch_grid[x][y]

    def stepOLD(self):
        patch_ahead=self.model.patch_grid[self.patch_coords[0]+1][self.patch_coords[1]] if self.patch_coords[0]+1<self.model.patch_size[0] else self.model.patch_grid[0][self.patch_coords[1]]
        car_ahead=None if not patch_ahead.agents else patch_ahead.agents[-1]
        if car_ahead:
            self.slow_down_car()
        else:
            self.speed_up_car()
        # self.speed=max(self.speed,speed_min)
        # self.speed=min(self.speed,speed_limit)

        self.x+=self.speed*140
        if self.x>=self.model.width:
            self.x-=self.model.width
        self.model.space.move_agent(self,np.array([self.x,self.y]))
        self.update_pos()

    
    def slow_down_car(self):
        self.speed-=self.model.deceleration
        # self.speed=max(0,self.speed)
        if self.speed<0: self.speed=self.model.deceleration
        self.patience-=1

    def speed_up_car(self):
        self.speed+=self.model.acceleration
        self.speed=min(self.speed,self.top_speed)
