from mesa.visualization.ModularVisualization import ModularServer
import mesa
from simple_continuous_module import SimpleCanvas
from model import TrafficModel



def agent_portrayal(agent):
    # if type(agent)==Car:
    portrayal = {
        "Shape": "rect2",
        "Color": "red" if list(agent.model.schedule.agent_buffer())[0]==agent else "blue",
        # "Color": "red",
        "scale": 0.66*1.5,
    }
    return portrayal
    

charts = [ 
    mesa.visualization.ChartModule(
        [
            {"Label": "StoppedCars", "Color": "#ff0000"},
        ]
    ),
    mesa.visualization.ChartModule(
        [
            {"Label": "AverageSpeed", "Color": "#ff0000"},
        ]
    ),
    mesa.visualization.ChartModule(
        [
            {"Label": "AverageWaitTime", "Color": "#ff0000"},
        ]
    )
]
params={
    "grid_size_x":mesa.visualization.Slider("Grid Size X",5,1,9),
    "grid_size_y":mesa.visualization.Slider("Grid Size Y",5,1,9),
    "num_cars":mesa.visualization.Slider("Number of Cars",200,1,400),
    "power": mesa.visualization.Checkbox("Power", True),
    "ticks_per_cycle": mesa.visualization.Slider("Ticks per Cycle", 20,1,100),
    "speed_limit": mesa.visualization.Slider("Speed Limit", 1.0,0.1,1.0,0.1),
}

canvas = SimpleCanvas(agent_portrayal, 700, 700)
server = ModularServer(TrafficModel,[canvas]+charts,"Traffic Model",params)

server.port = 8524 # The default
server.launch()