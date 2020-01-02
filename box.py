import math

def distance(x1, y1, x2, y2):
    return math.sqrt(((x2-x1)**2)+((y2-y1)**2))

class box:
    def __init__(self, canvas, x, y, size, label):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.checked = False
        
        self.square = canvas.create_rectangle(x, y, x+size, y+size)
        self.cX1 = x+(size/4)
        self.cY1 = y+(size/4)
        self.cX2 = x+(size*3/4)
        self.cY2 = y+(size*3/4)
        self.circle = canvas.create_oval(self.cX1, self.cY1, self.cX2, self.cY2, fill="black")
        self.label = canvas.create_text(self.x-(len(label)*2)-10, self.y+(size/2), text=label)
        
    def drawD(self):
        if not self.checked:
            self.canvas.coords(self.circle, 400, 400, 400, 400)
        else:
            self.canvas.coords(self.circle, self.cX1, self.cY1, self.cX2, self.cY2)
    def clickedD(self, event):
        if event.x > self.x and event.x < self.x + self.size:
            if event.y > self.y and event.y < self.y + self.size:
                self.checked = (not self.checked)

class radioBox:
    def __init__(self, canvas, x, y, size, labels, values):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.values = values
        
        self.boxes = []
        for i in range(0, len(labels)):
            self.boxes.append(box(canvas, x, y+(i*size*1.5), size, labels[i]))
        self.selected = 0
        self.boxes[self.selected].checked = True
        self.value = self.values[self.selected]
        
    def drawD(self):
        for b in self.boxes:
            b.drawD()
            
    def clickedD(self, event):
        for b in range(0, len(self.boxes)):
            self.boxes[b].clickedD(event)
            if self.boxes[b].checked:
                self.selected = b
                for d in range(0, len(self.boxes)):
                    if not d==b:
                        self.boxes[d].checked = False
        self.value = self.values[self.selected]
