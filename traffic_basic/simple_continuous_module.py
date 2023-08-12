import mesa
import math
import numpy as np

class SimpleCanvas(mesa.visualization.VisualizationElement):
    local_includes = ["simple_continuous_canvas2.js"]
    portrayal_method = None
    canvas_height = 500
    canvas_width = 500

    def __init__(self, portrayal_method, canvas_height=500, canvas_width=500):
        """
        Instantiate a new SimpleCanvas
        """
        self.portrayal_method = portrayal_method
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        new_element = "new Simple_Continuous_Module({}, {})".format(
            self.canvas_width, self.canvas_height
        )
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):

        space_state = []

        space_state.append({
            "Shape":"rect2",
            "Color": "black",
            "scale": 1,
            "x":0.5,
            "y":0.5,
            "w":700,
            "h":210,
        })

        for patch in model.patches:
            space_state.append({
                "Shape":"rect2",
                "Color": patch.color,
                "scale": 1,
                "x": (patch.x*model.patch_dimension[0]+model.patch_dimension[0]/2)/model.width,
                "y": (patch.y*model.patch_dimension[1]+model.patch_dimension[1]/2)/model.height,
                "w":model.patch_dimension[0]*700/7000,
                "h":model.patch_dimension[1]*210/700+1,
            })
        
        for car in model.schedule.agents:
            portrayal = self.portrayal_method(car)
            x, y = car.pos

            x = (x - model.space.x_min) / (model.space.x_max - model.space.x_min)
            y = (y - model.space.y_min) / (model.space.y_max - model.space.y_min)
            portrayal["x"] = x
            portrayal["y"] = y
            # portrayal["w"] = car.l/10*portrayal["scale"]
            portrayal["w"] = 170/10*portrayal["scale"]
            portrayal["h"] = portrayal["w"]/2
            portrayal["dir"]=car.heading
            space_state.append(portrayal)


        return space_state
    
