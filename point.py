import math

def distance(x1, y1, x2, y2):
    return math.sqrt(((x2-x1)**2)+((y2-y1)**2))

class point:
    def __init__(self, canvas, x, y, size, dirDrag, rangeValueX, rangeValueY, valueX, valueY, rangeX, rangeY):
        self.canvas = canvas
        # x and y will store current position, xBase and yBase will store initial
        self.x = x
        self.y = y
        self.rangeX = rangeX
        self.rangeY = rangeY
        self.xBase = x
        self.yBase = y
        
        # int (20 recommended)
        self.size = size
        
        #dirDrag is a string ("x", "y", or "xy")
        self.dirDrag = dirDrag
        
        #tiedX, tiedY are arrays
        self.tiedX = []
        self.tiedY = []

        #value is "how far the knob is turned", a function of position, and position is a function of value
        self.valueX = valueX
        self.valueY = valueY
        self.rangeValueX = rangeValueX
        self.rangeValueY = rangeValueY
        
        #is this object being dragged right now
        self.dragging = False
        
        self.circle = canvas.create_oval(0, 0, 0, 0)

    def updateValue(self, valueX, valueY):
        # update both self.position and self.value
        self.valueX = valueX
        self.valueY = valueY
        self.x = valueX * (self.rangeX / self.rangeValueX) + self.xBase
        self.y = valueY * (self.rangeY / self.rangeValueY) + self.yBase
        
    def updatePosition(self, x, y):
        if x is not None:          
            #update all objects in self.tiedX array
            for tied in self.tiedX:
                #print(str(tied.x)+"b "+str(x)+"b "+str(self.x))
                tied.x += (x - self.x)
            # update both self.position and self.value
            self.x = x
            self.valueX = (self.rangeValueX / self.rangeX)*(self.x - self.xBase)
                
        if y is not None:            
            #update all objects in self.tiedY array
            for tied in self.tiedY:
                tied.y += (y - self.y)
            # update both self.position and self.value
            self.y = y
            self.valueY = (self.rangeValueY / self.rangeY)*(self.y - self.yBase)
        
    def movingD(self, event):
        if self.dragging:
            if "x" in self.dirDrag:
                if event.x > self.size + 1 and abs(self.xBase - event.x) < self.rangeX:
                    self.updatePosition(event.x, None)
            if "y" in self.dirDrag:
                if event.y > self.size + 1 and event.y < self.rangeY:
                    self.updatePosition(None, event.y)
            
    def clickedD(self, event):
        if distance(self.x, self.y, event.x, event.y) < self.size:
            self.dragging = True
            
    def releasedD(self, event):
        self.dragging = False
        
    def drawD(self):
        self.canvas.coords(self.circle, self.x-self.size, self.y-self.size, self.x+self.size, self.y+self.size)
