from point import point
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
        
        self.initialA = attack
        self.initialD = decay
        self.initialS = sustain
        self.initialR = release

        self.currentA = attack
        self.currentD = decay
        self.currentS = sustain
        self.currentR = release
        
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

        #self.canvas.itemconfig(self.attackD, text="Attack: "+str(self.points[1].valueX))
        #self.canvas.itemconfig(self.decayD, text="Decay: "+str(self.points[2].valueX))
        #self.canvas.itemconfig(self.sustainD, text="Sustain: "+str(self.points[2].valueY))
        #self.canvas.itemconfig(self.releaseD, text="Release: "+str(self.points[4].valueX))
        
        self.currentA = ((self.points[1].valueX + 100)/200) * self.initialA
        self.currentD = ((self.points[2].valueX + 100)/200) * self.initialD
        self.currentS = ((self.points[2].valueY + 100)/200) * self.initialS
        self.currentR = ((self.points[4].valueX + 100)/200) * self.initialR

        
        self.canvas.itemconfig(self.attackD, text="Attack: "+str(round(self.currentA, 2)))
        self.canvas.itemconfig(self.decayD, text="Decay: "+str(round(self.currentD, 2)))
        self.canvas.itemconfig(self.sustainD, text="Sustain: "+str(round(self.currentS, 2)))
        self.canvas.itemconfig(self.releaseD, text="Release: "+str(round(self.currentR, 2)))
        
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




