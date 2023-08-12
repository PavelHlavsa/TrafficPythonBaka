from mesa.visualization.ModularVisualization import ModularServer
import mesa
from simple_continuous_module import SimpleCanvas
from model import TrafficModel



def agent_portrayal(agent):
    portrayal = {
        "Shape": "rect2",
        "Color": "red" if agent.unique_id==1 else "blue",
        "scale": 1,
    }
    return portrayal
    

charts = [mesa.visualization.ChartModule(
    [
        {"Label": "RedCar", "Color": "#ff0000"},
        {"Label": "MinSpeed", "Color": "#00ff00"},
        {"Label": "MaxSpeed", "Color": "#0000ff"},
    ]
)]
params={
    "number_of_cars": mesa.visualization.Slider("Number of Cars", 1, 0, 41),
    "acceleration": mesa.visualization.Slider("Acceleration", 0.0045, 0, 0.0099,0.0001),
    "deceleration": mesa.visualization.Slider("Deceleration", 0.026, 0, 0.099,0.001),
}

canvas = SimpleCanvas(agent_portrayal, 700, 210)
server = ModularServer(TrafficModel,[canvas]+charts,"Traffic Model",params)

server.port = 8524 # The default
server.launch()