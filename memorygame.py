from tkinter import *
import random
import string

#making a memory game.

class Circle(object):
    def __init__(self,x,y,val):
        self.x = x
        self.y = y
        self.r = 50
        self.color = "blue"
        self.value = val
    def drawball(self,canvas):
        canvas.create_oval(self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r, fill = self.color)
        canvas.create_text(self.x,self.y,text=str(self.value))


####################################
# customize these functions
####################################

def initialize():
    spotlist = []
    spotlist.append(Circle(70+(0*150),70+(0*150),'a'))
    spotlist.append(Circle(70+(1*150),70+(0*150),'b'))
    spotlist.append(Circle(70+(2*150),70+(0*150),'c'))
    spotlist.append(Circle(70+(0*150),70+(1*150),'d'))
    spotlist.append(Circle(70+(1*150),70+(1*150),'e'))
    spotlist.append(Circle(70+(2*150),70+(1*150),'f'))
    spotlist.append(Circle(70+(0*150),70+(2*150),'g'))
    spotlist.append(Circle(70+(1*150),70+(2*150),'h'))
    spotlist.append(Circle(70+(2*150),70+(2*150),'i'))
    return spotlist

    #value = 1
    #for i in range(3):
    #    for j in range(3):
    #      spotlist.append(Circle(70+(j*150),70+(i*150),value))
    #      value += 1
    #return spotlist

def init(data):
    data.count = 1
    data.blist = initialize()
    data.qlist = [data.blist[random.randint(0,8)]]

    data.index = 0
    data.showindex = 0
    data.lose = False

    data.show = True
    data.complete = False


def mousePressed(event, data):
    init(data)

def keyPressed(event, data):
    print(event.keysym)
    if not data.show and not data.lose:
        if event.keysym == data.qlist[data.index].value:
            data.qlist[data.index].color = "yellow"
            data.index += 1
            if data.index-1 > 0:
                data.qlist[data.index - 2].color = "blue"
            if data.index == len(data.qlist):
                data.qlist[data.index-1].color = "blue"
                data.show = True
                data.showindex = 0
                data.index = 0
                data.qlist.append(data.blist[random.randint(0,8)])
                data.count += 1
                data.complete = True
        else:
            data.lose = True
    

def timerFired(data):
    print(data.index)
    if data.show and not data.lose:
        data.complete = False
        if data.showindex < len(data.qlist):
            data.qlist[data.showindex].color = "yellow"
            if data.showindex > 0:
                data.qlist[data.showindex-1].color = "blue"
            data.showindex += 1
        else:
            data.showindex = 0
            data.show = False
            data.qlist[data.showindex-1].color = "blue"


    

    

def redrawAll(canvas, data):

    for circle in data.blist:
        circle.drawball(canvas)
    if data.lose:
        canvas.create_text(data.width//2,data.height//2,text="Game Over, Click anywhere to restart")
        canvas.create_text(500,20,text="Count = "+str(data.count))
        return
    canvas.create_text(500,20,text="Count = "+str(data.count))
    if data.complete:
        canvas.create_text(500,120,text="NICE!")


        

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 700 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)