from tkinter import *
from tkinter import filedialog


class Program(object):
    def __init__(self, d):
        self.varDicts = d
        #self.heapDict = {1: {"w": Variable("w", "$B", True, 0), "z": None, "m": Variable("m", "$P", 2, 0)},
                         #2: {"agh": Variable("agh", "$F", -2.34, 0)}}
        self.heapDict = {1: {'x': Variable("x", "$I", 40, 1), 'y': Variable("y", "$I", 2, 1)},
                         2: {'0': Variable("0", "$I", 1, 1), '1': Variable("1", "$P", 3, 1),
                             '2': Variable("2", "$I", None, 1)},
                         3: {"ree": Variable("ree", "$I", 2, 0), "bee": Variable("bee", "$P", 5, 0)},
                         #4: {"w": Variable("w", "$B", True, 0), "z": None, "m": Variable("m", "$I", 2, 0)},
                         5: {"agh": Variable("agh", "$F", -2.34, 0), "b": Variable("b", "$P", 6, 0)},
                         6: {'x': Variable("x", "$I", 40, 1), 'y': Variable("y", "$I", 2, 1)},
                         7: {'0': Variable("0", "$I", 1, 1), '1': Variable("1", "$P", 8, 1), '2': Variable("2", "$I",
                                                                                                           None, 1)},
                         8: {"ree": Variable("ree", "$I", 2, 0), "bee": Variable("bee", "$P", 7, 0)}}


class Variable:
    def __init__(self, name, mtype, value, scope):
        self.name = name
        self.type = mtype  # if not $p, then simple type
        self.value = value
        self.scope = scope  # if variableScope > functionScope, this var should be deleted
        self.x = 0
        self.y = 0
        self.drawx = 0
        self.drawy = 0


programVariable = Program([{"x": Variable("x", "$I", 46, 0), "y": Variable("y", "$S", "boop", 0),
                            "z": Variable("z", "$P", 1, 0), "zz": Variable("zz", "$P", None, 0),
                            "BLAH": Variable("BLAH", "$I", None, 0),
                            "point1": Variable("point1", "$P", 1, 0),
                           "point2": Variable("point2", "$P", 2, 0)}])

# programVariable.varDicts = [{'n1': Variable('n1', '$P', 0, 1), 'n2': Variable('n2', '$P', 1, 1), 'n3': Variable('n3',
#                                                                                                                 '$P', 2, 1), 'n4': Variable('n4', '$P', 3, 1)}]
# programVariable.heapDict = {0: {'value': Variable('-', '$$I', 5, 1), 'next': Variable('-', '$P', 1, 1)}, 1: {'value':
#                                                                                                                  Variable('-', '$$I', 10, 1), 'next': Variable('-', '$P', 2, 1)}, 2: {'value': Variable('-', '$$I', 15, 1), 'next': Variable('-', '$P', 3, 1)}, 3: {'value': Variable('-', '$$I', 20, 1), 'next': Variable('-', '$P', None, 1)}}
#
# programVariable.varDicts = [{'n1': Variable('n1', '$P', 0, 1), 'n2': Variable('n2', '$P', 1, 1), 'n3': Variable(
#     'n3', '$P', 2, 1), 'n4': Variable('n4', '$P', 3, 1), 'myFavoriteVals': Variable('myFavoriteVals', '$P', 4, 1)}]
# programVariable.heapDict = {0: {'value': Variable('-', '$$I', 5, 1), 'next': Variable('-', '$P', 1, 1)}, 1: {'value': Variable('-', '$$I', 10, 1), 'next': Variable('-', '$P', 3, 1)}, 2: {'value': Variable('-', '$$I', 15, 1), 'next': Variable('-', '$P', 3, 1)}, 3: {'value': Variable('-', '$$I', 20, 1), 'next': Variable('-', '$P', 2, 1)}, 4: {'0': Variable('-', '$I', 1, 1), '1': Variable('-', '$I', 3, 1), '2': Variable('-', '$I', 100, 1), '3': Variable('-', '$I', None, 1)}}

programVariable.varDicts = [{'n1': Variable('n1', '$P', 0, 1), 'n2': Variable('n2', '$P', 1, 1), 'n3': Variable('n3', '$P', None, 1), 'n4': Variable('n4', '$P', 3, 1), 'myFavoriteVals': Variable('myFavoriteVals', '$P', 4, 1)}]
programVariable.heapDict = {0: {'value': Variable('-', '$$I', 5, 1), 'next': Variable('-', '$P', 1, 1)}, 1: {'value':Variable('-', '$$I', 10, 1), 'next': Variable('-', '$P', 3, 1)}, 2: None, 3: {'value': Variable('-', '$$I', 20, 1), 'next': Variable('-', '$P', 2, 1)}, 4: {'0': Variable('-', '$I', 1, 1), '1': Variable('-', '$I', 3, 1), '2': Variable('-', '$I', 100, 1), '3': Variable('-', '$I', None, 1)}}


def drawButton(canvas, x, y, width, height, color, border=0):
    x1 = x - width/2
    y1 = y - height/2
    x2 = x + width/2
    y2 = y + height/2
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=border)


def drawFakeButton(canvas, x, y, width, height, border=0):
    x1 = x - width / 2
    y1 = y - height / 2
    x2 = x + width / 2
    y2 = y + height / 2
    canvas.create_line(x1, y1, x2, y2, width=border)
    canvas.create_line(x1, y2, x2, y2, width=border)


def checkButtonBounds(x0, y0, x, y, width, height):
    x1 = x - width / 2
    y1 = y - height / 2
    x2 = x + width / 2
    y2 = y + height / 2
    if x1 < x0 < x2 and y1 < y0 < y2:
        return True
    return False


def drawGroundSymbol(data, canvas, x1, y1, length):
    w = data.pointerWidth
    canvas.create_line(x1, y1, x1+length, y1, width=w)
    x = x1+length
    canvas.create_line(x, y1+length/4, x, y1-length/4, width=w)
    x += length/8
    canvas.create_line(x, y1 + length/8, x, y1 - length/8, width=w)
    x += length/8
    canvas.create_line(x, y1 + length/16, x, y1 - length/16, width=w)

####################################
# customize these functions
####################################

def init(data):
    #data.tempList = ["x", "y", "z", "zz", "BLAH"]
    data.counter = 0
    data.variableNames = ['n1','n2','n3','n4','myFavoriteVals'] #["x", "y", "z", "zz", "BLAH", "point1", "point2"]
    data.nextVariables = []
    data.program = programVariable
    data.heapDict = {}
    data.drawn = {}
    data.pointerCoordinates = {}
    data.lines = []

    ### graphics ###
    data.ratio = 1/3
    data.bgColor = "gray20"
    data.textColor = "light grey"
    data.textFont = "Arial 15"

    # next button
    data.buttonx = data.ratio*data.width*3/4
    data.buttony = data.height - 40
    data.buttonWidth = 100
    data.buttonHeight = 40

    # upload button
    data.uploadButtonx = data.ratio*data.width/2
    data.uploadButtony = data.height - 40
    data.uploadButtonWidth = 100
    data.uploadButtonHeight = 40

    # variable boxes
    data.variableInterval = 60
    data.variableHeight = 40
    data.variableWidthdx = 20
    data.boxVariableDistance = 10

    # pointers
    data.pointerWidth = 2


def keyPressed(event, data):
    # use event.char and event.keysym
    pass


def mousePressed(event, data):
    # use event.x and event.y
    print("PRESSED")

    # next button
    if checkButtonBounds(event.x, event.y, data.buttonx, data.buttony, data.buttonWidth, data.buttonHeight):
        print("Next button pressed!")

    # upload file
    if checkButtonBounds(event.x, event.y, data.uploadButtonx, data.uploadButtony, data.uploadButtonWidth,
                         data.uploadButtonHeight):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("text files", "*.txt"), ("C files", "*.c"), ("all files", "*.*")))
        f = open(filename, 'r')
        fileContents = str(f.read())
        f.close()


def leftDragged(event, data):
    #print(event.x, event.y)
    pass


def timerFired(data):
    # data.counter += 1
    # if data.counter % 10 == 0:
    #     i = data.counter//10
    #     if i < 5:
    #         data.variableNames += [data.tempList[i]]
    pass


def redrawAll(canvas, data):
    # draw background
    canvas.create_rectangle(0, 0, data.width, data.height, fill=data.bgColor)

    # draw dividers
    x = data.ratio*data.width
    canvas.create_line(x, 0, x, data.height, width=4)
    y = 40
    canvas.create_line(0, y, data.width, y, width=3)

    # text "stack" & "heap"
    x = data.ratio*data.width/2
    y = 21
    canvas.create_text(x, y, text="stack", font="Arial 25", fill=data.textColor)
    x = (1-data.ratio)*data.width/2 + data.ratio*data.width
    canvas.create_text(x, y, text="heap", font="Arial 25", fill=data.textColor)

    # draw next button
    drawButton(canvas, data.buttonx, data.buttony, data.buttonWidth, data.buttonHeight, "LightBlue1")
    canvas.create_text(data.buttonx, data.buttony, text="Next line", font=data.textFont, fill=data.bgColor)

    # draw upload button
    drawButton(canvas, data.uploadButtonx, data.uploadButtony, data.uploadButtonWidth, data.uploadButtonHeight,
               "LightSkyBlue1")
    canvas.create_text(data.uploadButtonx, data.uploadButtony, text="Upload file", fill=data.bgColor,
                       font=data.textFont)

    data.drawn = {}
    # draw the first layer of variables (button, value, variable name)
    varDict = data.program.varDicts[-1]
    x = data.ratio * data.width / 2
    y = y0 = 80
    r = 5
    for variableName in data.variableNames:
        variable = varDict[variableName]
        # draw button
        if variable.type != "$P" and variable.value is not None:
            text = str(variable.value)
            width = data.variableWidthdx * len(text)
        else:
            width = data.variableWidthdx * 2
        variable.x, variable.y = x, y
        drawButton(canvas, x, y, width, data.variableHeight, "seashell3")
        # draw value
        if variable.type != "$P" and variable.value is not None:
            canvas.create_text(x, y, text=text, font=data.textFont, fill=data.bgColor)
        else:
            if variable.type == "$P":
                if variable.value is None:
                    drawGroundSymbol(data, canvas, x, y, 60)
                canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")
            elif variable.value is None:
                canvas.create_text(x, y, text="?", font=data.textFont, fill=data.bgColor)
        # draw variable name
        textX = x - width / 2 - data.boxVariableDistance
        canvas.create_text(textX, y, text=variable.name, font=data.textFont, fill=data.textColor, anchor="e")

        x0 = data.ratio*data.width * 3/2
        pointerDrawn = False
        if variable.type == "$P" and variable.value is not None:
            if variable.value in data.drawn:
                oldx, oldy = data.drawn[variable.value][0], data.drawn[variable.value][1]
                data.lines += [[variable.x, variable.y, oldx, oldy]]
                pointerDrawn = True
            else:
                nextVariablesDict = data.program.heapDict[variable.value]
                iter(nextVariablesDict.items())
                nextVariables = []
                for key, value in nextVariablesDict.items():
                    nextVariables += [value]
                data.nextVariables += nextVariables
                for i in range(len(nextVariables)):
                    nextVariable = nextVariables[i]
                    # draw button
                    if nextVariable != None:
                        if nextVariable.type != "$P" and nextVariable.value is not None:
                            text = str(nextVariable.value)
                            width = data.variableWidthdx * len(text)
                        else:
                            width = data.variableWidthdx * 2
                        x0 += width/2
                        if not pointerDrawn:
                            data.lines += [[x, y, x0-width/2, y0]]
                            data.drawn[variable.value] = [x0-width/2, y0]
                            pointerDrawn = True
                        nextVariable.x, nextVariable.y = x0, y0
                        drawButton(canvas, x0, y0, width, data.variableHeight, "seashell3", border=1)
                        # draw value
                        if nextVariable.type != "$P" and nextVariable.value is not None:
                            canvas.create_text(x0, y0, text=text, font=data.textFont, fill=data.bgColor)
                        else:
                            if nextVariable.type == "$P":
                                if nextVariable.value is None:
                                    drawGroundSymbol(data, canvas, x0, y0, 60)
                                canvas.create_oval(x0 - r, y0 - r, x0 + r, y0 + r, fill="black")
                            elif nextVariable.value is None:
                                canvas.create_text(x0, y0, text="?", font=data.textFont, fill=data.bgColor)
                        # no variable names to draw
                    # else:
                    #     width = data.variableWidthdx * 2
                    #     drawFakeButton(canvas, x, y, width, data.variableHeight, border=1)
                    x0 += width/2
                y0 += data.variableInterval

        y += data.variableInterval

    # draw the second layer of variables
    y1 = 80
    while data.nextVariables != []:
        newNextVariables = []
        for startVariable in data.nextVariables:
            pointerDrawn = False
            if startVariable is not None and startVariable.type == "$P":
                x1 = data.ratio * data.width * 2
                #print(startVariable.value, data.drawn)
                if startVariable.value in data.drawn:
                    oldx, oldy = data.drawn[startVariable.value][0], data.drawn[startVariable.value][1]
                    data.lines += [[startVariable.x, startVariable.y, oldx, oldy]]
                    pointerDrawn = True
                elif startVariable.value is None:
                    pass
                else:
                    endVariablesDict = data.program.heapDict[startVariable.value]
                    if endVariablesDict is None:
                        pass
                    else:
                        iter(endVariablesDict.items())
                        endVariables = []
                        for key, value in endVariablesDict.items():
                            endVariables += [value]
                        newNextVariables += endVariables
                        for endVariable in endVariables:
                            # draw button
                            if endVariable != None:
                                if endVariable.type != "$P" and endVariable.value is not None:
                                    text = str(endVariable.value)
                                    width = data.variableWidthdx * len(text)
                                else:
                                    width = data.variableWidthdx * 2
                                x1 += width / 2
                                if not pointerDrawn:
                                    data.lines += [[startVariable.x, startVariable.y, x1 - width / 2, y1]]
                                    data.drawn[startVariable.value] = [x1 - width / 2, y1]
                                    pointerDrawn = True
                                endVariable.x, endVariable.y = x1, y1
                                drawButton(canvas, x1, y1, width, data.variableHeight, "seashell3", border=1)
                                # draw value
                                if endVariable.type != "$P" and endVariable.value is not None:
                                    canvas.create_text(x1, y1, text=text, font=data.textFont, fill=data.bgColor)
                                else:
                                    if endVariable.type == "$P":
                                        if endVariable.value is None:
                                            drawGroundSymbol(data, canvas, x1, y1, 60)
                                        canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill="black")
                                    elif endVariable.value is None:
                                        canvas.create_text(x1, y1, text="?", font=data.textFont, fill=data.bgColor)
                                # no variable names to draw
                            x1 += width / 2
                y1 += data.variableInterval
        data.nextVariables = newNextVariables

    # draw all the other variables in the heap
    y = 80
    for varI in data.program.heapDict:
        if varI not in data.drawn:
            x = data.ratio * data.width * 2.5
            varDict = data.program.heapDict[varI]
            if varDict is None:
                pass
            else:
                iter(varDict.items())
                varList = []
                for key, value in varDict.items():
                    varList += [value]
                for var in varList:
                    # draw button
                    if var is not None:
                        if var.type != "$P" and var.value is not None:
                            text = str(var.value)
                            width = data.variableWidthdx * len(text)
                        else:
                            width = data.variableWidthdx * 2
                        x += width / 2
                        var.x, var.y = x, y
                        if varI not in data.pointerCoordinates:
                            data.pointerCoordinates[varI] = [x - width/2, y]
                            print(varI, data.pointerCoordinates[varI])
                        drawButton(canvas, x, y, width, data.variableHeight, "seashell3", border=1)
                        # draw value
                        if var.type != "$P" and var.value is not None:
                            canvas.create_text(x, y, text=text, font=data.textFont, fill=data.bgColor)
                        else:
                            if var.type == "$P":
                                if var.value is None:
                                    drawGroundSymbol(data, canvas, x, y, 60)
                                canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")
                            elif var.value is None:
                                canvas.create_text(x, y, text="?", font=data.textFont, fill=data.bgColor)
                    x += width/2
            y += data.variableInterval

    # draw pointers for the other variables in the heap
    for var2I in data.program.heapDict:
        if var2I not in data.drawn:
            var2Dict = data.program.heapDict[var2I]
            if var2Dict is None:
                pass
            else:
                iter(var2Dict.items())
                var2List = []
                for key, value in var2Dict.items():
                    var2List += [value]
                for var2 in var2List:
                    if var2 is not None and var2.type == "$P":
                        print(var2I, var2.name)
                        newx, newy = data.pointerCoordinates[var2.value][0], data.pointerCoordinates[var2.value][1]
                        data.lines += [[var2.x, var2.y, newx, newy]]

    # draw all the pointers
    for x1, y1, x2, y2 in data.lines:
        canvas.create_line(x1, y1, x2, y2, width=data.pointerWidth, arrow=LAST)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def leftDraggedWrapper(event, canvas, data):
        leftDragged(event, data)
        redrawAllWrapper(canvas, data)

    # def timerFiredWrapper(canvas, data):
    #     timerFired(data)
    #     redrawAllWrapper(canvas, data)
    #     # pause, then call timerFired again
    #     canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    #data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind('<B1-Motion>', lambda event: leftDraggedWrapper(event, canvas, data))
    #timerFiredWrapper(canvas, data)
    redrawAllWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1437, 783)