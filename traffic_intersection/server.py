from mesa.visualization.ModularVisualization import ModularServer
import mesa
from simple_continuous_module import SimpleCanvas
from model import TrafficModel



def agent_portrayal(agent):
    portrayal = {
        "Shape": "rect2",
        # "Color": "red",
        "Color": agent.color,
        "scale": 1,
    }
    return portrayal
    

charts = [mesa.visualization.ChartModule(
    [
        {"Label": "Waiting", "Color": "#ff0000"},
        {"Label": "Wait_east", "Color": "#00ff00"},
        {"Label": "Wait_north", "Color": "#0000ff"},
    ]
)]
params={
    "speed_limit": mesa.visualization.Slider("Speed Limit", 5, 1, 10),
    "freq_north": mesa.visualization.Slider("Freq North", 60, 0, 100),
    "freq_east": mesa.visualization.Slider("Freq East", 100, 0, 100),
    "max_accel": mesa.visualization.Slider("Max Accel", 2, 1, 10),
    "max_brake": mesa.visualization.Slider("Max Brake", 4, 1,10),
    "green_length": mesa.visualization.Slider("Green Length", 12, 1,50),
    "yellow_length": mesa.visualization.Slider("Yellow Length", 3, 0,10),
}

canvas = SimpleCanvas(agent_portrayal, 700, 700)
server = ModularServer(TrafficModel,[canvas]+charts,"Traffic Model",params)

server.port = 8524 # The default
server.launch()