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
    

charts = [mesa.visualization.ChartModule(
    [
        # Cars per Lane
        {"Label": "CarsOnLane1", "Color": "#ff0000"},
        {"Label": "CarsOnLane2", "Color": "#00ff00"},
]
),mesa.visualization.ChartModule(
    [
        # Car Speeds
        {"Label": "AverageSpeed", "Color": "#ff0000"},
        {"Label": "MaxSpeed", "Color": "#00ff00"},
        {"Label": "MinSpeed", "Color": "#0000ff"},
    ]
),mesa.visualization.ChartModule(
    [
        # Driver Patience
        {"Label": "AveragePatience", "Color": "#ff0000"},
        {"Label": "MaxPatience", "Color": "#00ff00"},
        {"Label": "MinPatience", "Color": "#0000ff"},
    ]
)]
params={
    "number_of_cars": mesa.visualization.Slider("Number of Cars", 40, 1, 82),
    "acceleration": mesa.visualization.Slider("Acceleration", 0.005, 0.001, 0.01,0.001),
    "deceleration": mesa.visualization.Slider("Deceleration", 0.02, 0, 0.01,0.01),
    "max_patience": mesa.visualization.Slider("Max Patience", 50, 1, 100),
}

canvas = SimpleCanvas(agent_portrayal, 700, 210)
server = ModularServer(TrafficModel,[canvas]+charts,"Traffic Model",params)

server.port = 8524 # The default
server.launch()