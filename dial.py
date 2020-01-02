import math

def distance(x1, y1, x2, y2):
    return math.sqrt(((x2-x1)**2)+((y2-y1)**2))

class dial:
    def __init__(self, canvas, x, y, radius, label):
        self.canvas = canvas
        # x and y will store current position, xBase and yBase will store initial
        self.x = x
        self.y = y
        self.radius = radius
        self.dragging = False
        self.mix = 0
        self.miy = 0
        self.value = 0
        self.initialValue = self.value;      
        self.circle = canvas.create_oval(0, 0, 0, 0)
        self.line = canvas.create_line(x, y, x+10, y+10)
        self.label = canvas.create_text(x, y+radius+10, text=label)
        
    def movingD(self, event):
        if self.dragging:
            self.value = (self.miy - event.y) + self.initialValue
        if self.value < 0:
            self.value = 0
        elif self.value > 100:
            self.value = 100
            
    def clickedD(self, event):
        if distance(self.x, self.y, event.x, event.y) < self.radius:
            self.dragging = True
            self.mix = event.x
            self.miy = event.y
            self.initialValue = self.value
            
    def releasedD(self, event):
        self.dragging = False
        
    def drawD(self):
        self.canvas.coords(self.circle, self.x-self.radius, self.y-self.radius, self.x+self.radius, self.y+self.radius)
        angle = (self.value * 3) + 125
        angle = angle * (math.pi / 180)
        self.canvas.coords(self.line, self.x, self.y, self.x+math.cos(angle)*self.radius, self.y+math.sin(angle)*self.radius)

