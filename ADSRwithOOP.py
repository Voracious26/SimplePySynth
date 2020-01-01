from tkinter import Tk, Canvas
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

class envelope:
    def __init__(self, canvas):
        self.canvas = canvas
        fs = 2
        seconds = 1
        attack = 0.5
        decay = 0.25
        sustain = 0.5
        release = 0.5

        A = attack * fs
        B = (attack + decay) * fs
        C = seconds * fs
        D = (seconds + release) * fs

        #multiplier literally just so we can fit in in the canvas
        self.m = 100
        
        self.base = 250

        self.points = []
        self.s = 10
        
        height = int(canvas.cget("height"))
        self.points.append(point(canvas, 20, self.base, self.s, "", 0, 0, 0, 0, 0, 0))
        self.points.append(point(canvas, A*self.m, 15, self.s, "x", 100, 0, 0, 0, 50, 0))
        self.points.append(point(canvas, B*self.m, sustain*self.m, self.s, "xy", 100, 100, 0, 0, 50, height-self.s))
        self.points.append(point(canvas, C*self.m, sustain*self.m, self.s, "y", 0, 100, 0, 0, 0, 50))
        self.points.append(point(canvas, D*self.m, self.base, self.s, "x", 100, 0, 0, 0, 50, 0))

        # 0 Base (Z)
        # 1 A
        # 2 B
        # 3 C
        # 4 D
        self.points[1].tiedX = [self.points[2], self.points[3], self.points[4]]
        self.points[2].tiedX = [self.points[3], self.points[4]]
        self.points[2].tiedY = [self.points[3]]
        self.points[3].tiedY = [self.points[2]]


        self.lines = []
        self.lines.append(canvas.create_line(self.points[0].x, self.points[0].y, self.points[1].x, self.points[1].y))
        for d in range(1, len(self.points)-1):
            self.lines.append(canvas.create_line(self.points[d].x, self.points[d].y, self.points[d+1].x, self.points[d+1].y))

        self.attackD = canvas.create_text(300,10,fill="darkblue",font="Times 12",
                                text="Attack: ")
        self.decayD = canvas.create_text(300,25,fill="darkblue",font="Times 12",
                                text="Decay: ")
        self.sustainD = canvas.create_text(300,40,fill="darkblue",font="Times 12",
                                text="Sustain: ")
        self.releaseD = canvas.create_text(300,55,fill="darkblue",font="Times 12",
                                text="Release: ")
        
    def draw(self):
        self.canvas.itemconfig(self.attackD, text="Attack: "+str(self.points[1].valueX))
        self.canvas.itemconfig(self.decayD, text="Decay: "+str(self.points[2].valueX))
        self.canvas.itemconfig(self.sustainD, text="Sustain: "+str(self.points[2].valueY))
        self.canvas.itemconfig(self.releaseD, text="Release: "+str(self.points[4].valueX))
        self.canvas.coords(self.lines[0], self.points[0].x, self.points[0].y, self.points[1].x, self.points[1].y)
        for d in range(1, len(self.points)-1):
            self.canvas.coords(self.lines[d], self.points[d].x, self.points[d].y, self.points[d+1].x, self.points[d+1].y)
        for a in self.points:
            a.drawD()

    def clickedD(self, event):  
        for a in self.points:
            a.clickedD(event)
            
    def movingD(self, event):    
        for a in self.points:
            a.movingD(event)
            
    def releasedD(self, event): 
        for a in self.points:
            a.releasedD(event)


root = Tk()
paint = Canvas(root)  
volumeEnvelope = envelope(paint)


def drawEverything():
    global volumeEnvelope
    volumeEnvelope.draw()

def key(event):
    repr(event.char)
    
def callback(event):
    global volumeEnvelope
    drawEverything()
    volumeEnvelope.clickedD(event)

def moving(event):
    global volumeEnvelope
    drawEverything()
    volumeEnvelope.movingD(event)

def released(event):
    global volumeEnvelope
    drawEverything()
    volumeEnvelope.releasedD(event)

paint.bind("<Key>", key)
paint.bind("<Button-1>", callback)
paint.bind("<ButtonRelease-1>", released)
paint.bind("<B1-Motion>", moving)
paint.pack()



while True:
    drawEverything()
    root.update()
#root.mainloop()



