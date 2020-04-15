# Maze Game - Jason Cassells 28/11/2019

# M - Monster (Player won't see this on map)
# E - Exit (Player won't see this on map)
# T - Treasure (Player won't see this on map)
# R - Room
# Y - You
# G - Gold (Player won't see this on map)

import random
from tkinter import *
from tkinter import ttk
import time
import os

#Maze layout
layout = []

#Global Array to track key values
Stats = {"Position":[], # Players current position
         "Health":10, # Players current health
         "Items":"", # Players current items
         "Map":"", # Players current surroundings
         "Gold":0, # Players current gold
         "Message":"", # Info for players action
         "isExit":False, # Will show ExitPage if True
         "roomSafe":True, # Will show AttackPage if False
         "hasMap":False, # Will show full map if True
         "confirmExit":False, # Will exit all windows if True
         "Prev":"0", # Holds the previously played config file number
         "squareCount":0, # Counts all the valid squares on the map
         "invalidConfig":False, # Will create an error message if True
         "validSquares":[], # Contains co-ordinates for each valid square
         "confirmRes":False, # Will restart the currently running game if True
         "dropCoin":False, # Will drop a coin if True and "OnMove" is also True
	 "onMove":False} # Will drop a coin in the space the player is currently on before moving

#Global Array to track monsters and weaknesses
Monsters = [{"Name":"Ogre", "Weakness":["Onions", "Sword"], "Health":5},
            {"Name":"Medusa", "Weakness":["Mirror", "Shield"], "Health":5},
            {"Name":"Shadow Beast", "Weakness":["Torch", "Mirror"], "Health":2},
            {"Name":"Beholder", "Weakness":["D20", "Sword"], "Health":4},
            {"Name":"Hydra", "Weakness":["Sword", "Shield"], "Health":3},
            {"Name":"Frankenstein", "Weakness":["Sword", "Torch"], "Health":4},
            {"Name":"Goblin", "Weakness":["Sword", "Bribe"], "Health":3},
            {"Name":"Slime", "Weakness":["Shield", "Torch"], "Health":2},
            {"Name":"Splay of Tentacles", "Weakness":["Sword", "D20"], "Health":5},
            {"Name":"Dracula", "Weakness":["Stake", "Mirror"], "Health":4}]

#Global List to track items (Will not be changed)
Items = ["Onions", "Mirror", "Torch", "Map", "D20", "Shield", "Sword", "Stake"]

#Used to update the Stats Array
def updateStats(name, value):
    Stats[name] = value

##Used to check the status of the current room
def checkRoom():
        pos = Stats["Position"]
        if layout[pos[0]][pos[1]] == "E": # E is exit
            updateStats("Message", "You have found the Exit!")
            updateStats("isExit", True)
            updateStats("roomSafe", True)
            
        elif layout[pos[0]][pos[1]] == "M": # M is monster
            updateStats("Message", "You have encountered a foul beast!")
            updateStats("roomSafe", False)
            updateStats("isExit", False)

        elif layout[pos[0]][pos[1]] == "G": # G is gold
            updateStats("Message", "You have picked up some gold")

            currentGold = Stats["Gold"]
            newGold = currentGold + random.randint(1,100) # Adds a random gold value from 1 - 100
            updateStats("Gold", newGold)
            layout[pos[0]][pos[1]] = 1
            
            updateStats("isExit", False)
            updateStats("roomSafe", True)
            
        elif layout[pos[0]][pos[1]] == "T": # T is treasure
            updateStats("Message", "You have found a Treasure")

            itemKey = random.randint(0, len(Items)-1) # Will pick a random treasure from the list of "Items" (Treasures)
            if Items[itemKey] == "Map":
                updateStats("hasMap", True)
                
            itemList = Stats["Items"]
            itemList += Items[itemKey] + "\n"
            updateStats("Items", itemList)
            Items.pop(itemKey) # Removes this item from the list (So that you can't get the same item twice)
            
            layout[pos[0]][pos[1]] = 1

            updateStats("isExit", False)
            updateStats("roomSafe", True)

        elif layout[pos[0]][pos[1]] == "D": # D is dropped gold
            updateStats("Message", "You have found dropped coin")
            currentGold = Stats["Gold"]
            updateStats("Gold", currentGold + 1)
            layout[pos[0]][pos[1]] = 1
            
        else:
            if Stats["dropCoin"] and Stats["onMove"]:
                if Stats["Gold"] > 0:
                    currentGold = Stats["Gold"]
                    updateStats("Gold", currentGold - 1)
                    layout[pos[0]][pos[1]] = 1
                    layout[pos[0]][pos[1]] = "D"
            
            updateStats("isExit", False)
            updateStats("roomSafe", True)

## Used to find the surroundings of the players current position
def findSurrounding(value):
    try:
        value = layout[value[0]][value[1]]
        if value == 0:
            value = "X"
        else:
            value = "R" 
    except:
        value = "X"
    return value


## Generates items within the maze ##
class GenMaze:
    def __init__(self, Retry):
        global Stats
        Stats = {"Position":[], # Players current position
                 "Health":10, # Players current health
                 "Items":"", # Players current items
                 "Map":"", # Players current surroundings
                 "Gold":0, # Players current gold
                 "Message":"", # Info for players action
                 "isExit":False, # Will show ExitPage if True
                 "roomSafe":True, # Will show AttackPage if False
                 "hasMap":False, # Will show full map if True
                 "confirmExit":False, # Will exit all windows if True
                 "Prev":Stats["Prev"], # Holds the previously played config file number
                 "invalidConfig":False, # Will create an error message if True
                 "validSquares":[], # Contains co-ordinates for each valid square.
                 "confirmRes":False, # Will restart the currently running game if True
                 "dropCoin":False, # Will drop a coin if True and "OnMove" is also True
                 "onMove": False,} # Will drop a coin in the space the player is currently on before moving
        
        fileCount = len([name for name in os.listdir('./Config')]) # Counts the number of files in the Config directory.
        global layout
        try:
            if Retry and Stats["Prev"] != "0": # Uses map from previous game, if user selects "Retry" on main page.
                prev = Stats["Prev"]
                layout = []
                file = open("./Config/Conf"+str(prev)+".txt", "r")
                lines = file.readlines()

                for i in range(len(lines)):
                    line = lines[i].replace(" ", "")
                    line = line.strip("\n").split(",")
                    for j in range(len(line)):
                        line[j] = int(line[j])
                    layout.append(line)
                file.close()

            else:    
                layout = [] 
                chance = str(random.randint(1,fileCount)) # Picks a random map using the number of files in the Config directory.
                
                file = open("./Config/Conf"+chance+".txt", "r")
                lines = file.readlines()
                updateStats("Prev", chance)
                    
                for i in range(len(lines)):
                    line = lines[i].replace(" ", "")
                    line = line.strip("\n").split(",")
                    for j in range(len(line)):
                        line[j] = int(line[j])
                    layout.append(line)
                file.close()
            
            self.countSquares()
            if len(Stats["validSquares"]) >= 25:
                playerPos = self.getStartingPos() #Adds players inital position
                updateStats("Position", playerPos)

                self.addExit() #Places Exit
                self.addTreasures() #Places Treasures
                self.addMonsters() #Places Monsters
                self.addGold() #Adds Gold
                
            else: # If maze is not large enough
                    updateStats("Message", "Mapped Maze: Config/Conf"+Stats["Prev"]+".txt Does not contain enough squares")
                    updateStats("invalidConfig", True)
            
        except FileNotFoundError: # If file doesn't Exist
            updateStats("Message", "File: Code/Config/Conf"+Stats["Prev"]+".txt Does not exist")
            updateStats("invalidConfig", True)
        

    def getStartingPos(self): # Gets positions for objects and player on startup
        values = Stats["validSquares"]
        
        chance = random.randint(0, len(values)-1) # picks a square from validSquare list
        val = Stats["validSquares"][chance]
        values.pop(chance)
        updateStats("validSquares", values)
        return val

    def addExit(self): # Marks an Exit spot
					   # At this point the minimum amount of remaining valid squares is 25
        value = self.getStartingPos()
        layout[value[0]][value[1]] = "E"

    def addMonsters(self): # Marks all Monster spots
        monsterCount = random.randint(2, len(Monsters)-1) # Picks an amount of monsters from inbetween 2 and 9
														  # At this point the minimum amount of remaining valid squares is 24
        for i in range(monsterCount):
            value = self.getStartingPos()
            layout[value[0]][value[1]] = "M"
        
    def addTreasures(self): # Marks all Treasure spots
        itemCount = random.randint(2, len(Items)-1) # Picks an amount of monsters from inbetween 2 and 7 
													# At this point the minimum amount of remaining valid squares is 14
        for i in range(itemCount):
            value = self.getStartingPos()
            layout[value[0]][value[1]] = "T"

    def addGold(self): # Marks all Gold spots
        goldCount = random.randint(2, len(Stats["validSquares"])-2) # Picks an amount of Squares from inbetween 2 and the remaining valid squares - 2
																	# At this point the minimum amount of remaining valid squares is 6 
        for i in range(goldCount):
            value = self.getStartingPos()
            layout[value[0]][value[1]] = "G"

    def countSquares(self): # Counts how many squares == 1 and adds the positions of these squares to global Stats list
        for i in range(len(layout)):
            for j in range(len(layout[0])):
                if layout[i][j] == 1:
                    valid = Stats["validSquares"]
                    valid.append([i, j])
                    updateStats("validSquares", valid)

## Splash screen for fanciness ##
class SplashScreen:
    def __init__(self, splashPage):
        splashPage.title("Loading")
        mainframe = Frame(splashPage)
        mainframe.grid()
        ttk.Label(mainframe, text="Olde World Phunne", font="Calbri 30").grid(column=0, row=0)
        ttk.Label(mainframe, text="Presents:", font="Calbri 20").grid(column=0, row=1)
        splashPage.after(1000, MainPage, splashPage)

## Start Page for the game ##
class MainPage:
    def __init__(self, splashPage):        
        splashPage.destroy()

        mainPage = Tk()
        mainPage.title("Maze Game")
        mainframe = Frame(mainPage, padx="25", pady="25")
        mainframe.grid()

        message = Label(mainframe, text="")
        message.grid(column=2, row=2)
        
        ttk.Label(mainframe, text="Maze Game", font="Calbri 30").grid(column=2, row=0)
        ttk.Button(mainframe, text="Start", command=lambda: self.startup(mainPage, False, message)).grid(column=1, row=1)
        retry = ttk.Button(mainframe, text="Retry", command=lambda: self.startup(mainPage, True, message))
        retry.grid(column=2, row=1)

        if Stats["Prev"] == "0":
            retry.config(state=DISABLED) #Button on window is greyed out
        else:
            retry.config(state=NORMAL)
            
        ttk.Button(mainframe, text="Quit", command=mainPage.destroy).grid(column=3, row=1)

    def startup(self, mainPage, Retry, message):
            message.config(text="")
            GenMaze(Retry)
            if not Stats["invalidConfig"]:
                NavigationPage()
                MapPage()
                InfoPage()
                InventoryPage()
                RestartPage()
                mainPage.destroy()
            else:
                message.config(text="Could not start game due to the following error:\n"+Stats["Message"])
                

## Handles Monsters ##
class AttackPage:
    def __init__(self):
        attPage = Tk()
        attPage.title("DANGER!")
        mainframe = Frame(attPage, padx="25", pady="25")
        mainframe.grid()

        self.drawWidgets(mainframe, attPage)
        
    def drawWidgets(self, mainframe, attPage):
        monster = self.pickMonster()
        
        ttk.Label(mainframe, text="You are fighting "+ monster["Name"], font="Calibri 20").grid(column=0, row=1)
        ttk.Label(mainframe, text="Health: ").grid(column=1, row=0)

        health = Label(mainframe, text="")
        health.grid(column=2, row=0)
        message = Label(mainframe, text="")
        message.grid(column=0, row=2)
        effect = Label(mainframe, text="")
        effect.grid(column=0, row=3)
        warning = Label(mainframe, text="")
        warning.grid(column=0, row=4)

        self.drawButtons(mainframe, attPage, message, effect, warning, health, monster)

    def drawButtons(self, mainframe, attPage, message, effect, warning, health, monster):  
        ttk.Button(mainframe, text="Punch", command=lambda: self.useItem(monster, warning, message, effect, "punch", attPage)).grid(column=0, row=5)
        ttk.Button(mainframe, text="Run", command=lambda: self.runAway(message, effect, warning, attPage, monster)).grid(column=0, row=6)

        if monster["Name"] == "Goblin" and Stats["Gold"] > 50:
            button = ttk.Button(mainframe, text="Bribe", command=lambda: self.useItem(monster, warning, message, effect, "Bribe", attPage))
            button.grid(column=0, row=7)

        playerItems=Stats["Items"].split("\n")
        for i in range(len(playerItems)):
            currentItem = playerItems[i]
            if currentItem != "" and currentItem != "Map":
                button = ttk.Button(mainframe, text=currentItem, command=lambda item=currentItem: self.useItem(monster, warning, message, effect, item, attPage))
                button.grid(column=0, row=8+i)

        self.checkHealth(attPage, monster, health)
    
    def checkHealth(self, attPage, monster, health):
        if Stats["confirmExit"]:
            updateStats("roomSafe", True)
            attPage.after(10, attPage.destroy)
        else:
            if Stats["Health"] == 0:
                attPage.after(500, ExitPage.gameOver, attPage)
            else:
                health.config(text=monster["Health"])
            attPage.after(10, self.checkHealth, attPage, monster, health)
    
    def pickMonster(self):
        monsterKey = random.randint(0, len(Monsters)-1)
        monster = Monsters[monsterKey]
        Monsters.pop(monsterKey)
        return monster
    
    def useItem(self, monster, warning, message, effect, item, attPage): # Item based combat system
        attack = "You attack " + monster["Name"] + " with " + item
        message.config(text=attack)
        if item in monster["Weakness"]:
            effect.config(text="It was super effective!")
            warning.config(text="")
            
            if item == "Bribe":
                currentGold = Stats["Gold"]
                newGold = currentGold - random.randint(0,50) 
                updateStats("Gold", newGold)
                warning.config(text="But you lost gold")
                
            attPage.after(500, self.killMonster, attPage)
            
        elif item == "punch":
            effect.config(text="You hurt the gruesome beast")
            monster["Health"] = monster["Health"]-1
            chance = random.randint(0, 20)
            if chance > 12:
                warning.config(text = "But the monster attacks back, you take 1 damage")
                updateStats("Health", Stats["Health"]-1)
            else:
                warning.config(text = "")
                    
            if monster["Health"] < 1:
                attPage.after(500, self.killMonster, attPage)

        else:
            effect.config(text="It seemed to do nothing")
            warning.config(text = "The monster attacks you in revenge, you take 1 damage")
            updateStats("Health", Stats["Health"]-1)
        
    def killMonster(self, attPage):
        currentGold = Stats["Gold"]
        newGold = currentGold + random.randint(0,50) 
        updateStats("Gold", newGold)
            
        pos = Stats["Position"]
        layout[pos[0]][pos[1]] = 1
        updateStats("roomSafe", True)
        NavigationPage()
        attPage.destroy()
        
    def runAway(self, message, effect, warning, attPage, monster): # Will run away in a random direction, including towards a wall, while keeping monster 'alive'
        message.config(text="You try to run away")
        chance = random.randint(0, 20)
        direction = random.randint(0, 4)
        Monsters.append(monster)
        if chance > 6:
            effect.config(text = "and succeed")
            warning.config(text="")
            attPage.after(500, attPage.destroy)
            if direction == 1:
                NavigationPage.north(NavigationPage)
                NavigationPage()
                
            elif direction == 2:
                NavigationPage.east(NavigationPage)
                NavigationPage()
                
            elif direction == 3:
                NavigationPage.south(NavigationPage)
                NavigationPage()
                
            else:
                NavigationPage.west(NavigationPage)
                NavigationPage()
                
        else:
            effect.config(text = "and failed")
            warning.config(text = "The monster attacks you in response, you take 1 damage")
            updateStats("Health", Stats["Health"]-1)
        
## Handles Compass ##
class NavigationPage:
    def __init__(self):
        navPage = Tk()
        navPage.title("compass")
        mainframe = Frame(navPage, padx="25", pady="25")
        mainframe.grid()    
        self.drawButtons(mainframe, navPage)
        
    def drawButtons(self, mainframe, navPage):
        ttk.Button(mainframe, text="Toggle Dropping Coins", command=self.toggleDrop).grid(column=1, row=0, sticky=N)
        coins = Label(mainframe, text="Current status: "+str(Stats["dropCoin"]))
        coins.grid(column=1, row=1, sticky=N)

        #Goes North
        ttk.Button(mainframe, text="North", command=self.north).grid(column=1, row=2, sticky=N)

        #Goes East
        ttk.Button(mainframe, text="East", command=self.east).grid(column=2, row=3, sticky=E)

        #Goes South
        ttk.Button(mainframe, text="South", command=self.south).grid(column=1, row=4, sticky=S)

        #Goes West
        ttk.Button(mainframe, text="West", command=self.west).grid(column=0, row=3, sticky=W)

        self.checkHealth(navPage, coins)

    def toggleDrop(self):
        pos = Stats["Position"]
        updateStats("dropCoin", not Stats["dropCoin"])
        
    def checkHealth(self, navPage, coins):
        coins.config(text="Current status: "+str(Stats["dropCoin"]))
                
        if Stats["confirmExit"]:
            navPage.after(10, navPage.destroy)
            
        if not Stats["roomSafe"]:
            navPage.after(10, navPage.destroy)
            AttackPage()
                
        elif Stats["isExit"]:
            ExitPage(navPage)
            
        else:
            navPage.after(10, self.checkHealth, navPage, coins)
    
    def north(self):
        pos = Stats["Position"]
        if findSurrounding([pos[0]-1, pos[1]]) == "X":
            updateStats("Message", "It appears there is a wall here")
            updateStats("Position", pos)
        else:
            updateStats("Message", "You walk North")
            updateStats("onMove", True)
            checkRoom()
            
            updateStats("Position", [pos[0]-1, pos[1]])

    def east(self):
        pos = Stats["Position"]
        if findSurrounding([pos[0], pos[1]+1]) == "X":
            updateStats("Message", "It appears there is a wall here")
            updateStats("Position", pos)
        else:
            updateStats("Message", "You walk East")
            updateStats("onMove", True)
            checkRoom()
            
            updateStats("Position", [pos[0], pos[1]+1])

    def south(self):
        pos = Stats["Position"]
        if findSurrounding([pos[0]+1, pos[1]]) == "X":
            updateStats("Message", "It appears there is a wall here")
            updateStats("Position", pos)
        else:
            updateStats("Message", "You walk South")
            updateStats("onMove", True)
            checkRoom()
            
            updateStats("Position", [pos[0]+1, pos[1]])

    def west(self):
        pos = Stats["Position"]
        if findSurrounding([pos[0], pos[1]-1]) == "X":
            updateStats("Message", "It appears there is a wall here")
            updateStats("Position", pos)
        else:
            updateStats("Message", "You walk West")
            updateStats("onMove", True)
            checkRoom()
            
            updateStats("Position", [pos[0], pos[1]-1])
            

## Handles Map ##
class MapPage:
    def __init__(self):
        mapPage = Tk()
        mapPage.title("Map")
        mainframe = Frame(mapPage, padx="25", pady="25")
        mainframe.grid()
        
        ttk.Label(mainframe, text="MAP:").grid(column=0, row=0)        
        mapLabel = Label(mainframe, text = "", font="Arial 30")
        mapLabel.grid(column=0, row=1)
        self.drawMap(mapLabel, mapPage)
        
    def drawMap(self, mapLabel, mapPage):
        if Stats["confirmExit"]:
            mapPage.after(10, mapPage.destroy)
        else:
            self.openMap()
            mapLabel.config(text=Stats["Map"])
            mapPage.after(100, self.drawMap, mapLabel, mapPage)
        
    
    def fullMap(self): #If "Stats[hasMap]" show the full map
        fullStr = ""
        for i in range(len(layout)):
            for j in range(len(layout[0])):
                if [i,j] == Stats["Position"]:
                    fullStr += "Y "        
                else:
                    square = str(layout[i][j])
                    if square == "0":
                        fullStr += "X "
                    else: 
                        fullStr += "R "
            fullStr += "\n"
        updateStats("Map", fullStr)
    
    def openMap(self):
        if Stats["hasMap"]:
            self.fullMap()
        else:
            pos = Stats["Position"]
            up = findSurrounding([pos[0]-1, pos[1]]) # In an 3-Dimensional array E.g. [[0,0,0], [0,1,0], [0,0,0]]
                                                     # If the 1 was your current position; pos would equal [1,1]
                                                     # Therefore "up" would equal to [0, 1] or the "square" north of 1
                                                     # If you are still struggling with this visualise the array as a 3 x 3 grid. 
                                                     # [ [ 0, 0, 0 ],
                                                     #   [ 0, 1, 0 ],
                                                     #   [ 0, 0, 0 ] ]
		
            upleft = findSurrounding([pos[0]-1, pos[1]-1])
            upright = findSurrounding([pos[0]-1, pos[1]+1])
            
            down = findSurrounding([pos[0]+1, pos[1]])
            downleft = findSurrounding([pos[0]+1, pos[1]-1])
            downright = findSurrounding([pos[0]+1, pos[1]+1])
        
            left = findSurrounding([pos[0], pos[1]-1])
            right = findSurrounding([pos[0], pos[1]+1])
            current = layout[pos[0]][pos[1]]

            currentMap = upleft + " " + up + " " + upright + "\n" + left + " Y " + right + "\n" + downleft + " " + down + " " + downright
            updateStats("Map", currentMap)

## Handles Info ##
class InfoPage:
    def __init__(self):
        infoPage = Tk()
        infoPage.title("Message")
        mainframe = Frame(infoPage, padx="25", pady="25")
        mainframe.grid()

        ttk.Label(mainframe, text="Info:", font="Calibri 10").grid(column=0, row=0)        
        infoLabel = Label(mainframe, text = "", font="Calibri 10")
        infoLabel.grid(column=0, row=1)
        self.drawMessage(infoLabel, infoPage)

    def drawMessage(self, infoLabel, infoPage):
        if Stats["confirmExit"]:
            infoPage.after(10, infoPage.destroy)
        else:
            updateStats("onMove", False)
            checkRoom()
            infoLabel.config(text=Stats["Message"])
            infoPage.after(100, self.drawMessage, infoLabel, infoPage)
        
## Handles Exit ##
class ExitPage:
    def __init__(self, navPage):
        extPage = Tk()
        extPage.title("An Exit")
        mainframe = Frame(extPage, padx="25", pady="25")
        mainframe.grid()

        ttk.Button(mainframe, text="Exit", command=self.stopGame).grid(column=0, row=0)
        self.checkHealth(extPage, navPage)

    def checkHealth(self, extPage, navPage):
        if Stats["confirmExit"]:
            navPage.destroy()
            extPage.after(10, extPage.destroy)

        if not Stats["isExit"]:
            navPage.destroy()
            extPage.destroy()
            NavigationPage()
        
        extPage.after(10, self.checkHealth, extPage, navPage)
        
    def stopGame(self):
        updateStats("confirmExit", True)
        ResultsPage(True)

    def gameOver(attPage):
        attPage.destroy()
        updateStats("confirmExit", True)
        ResultsPage(False)
    
## Handles Results on Exit ##
class ResultsPage:
    def __init__(self, winState):
        resPage = Tk()
        if winState:
            resPage.title("You Win!")
            mainframe = Frame(resPage, padx="25", pady="25")
            mainframe.grid()    
            ttk.Label(mainframe, text="Congratulations!", font="Calibri 30").grid(column=0, row=0)
            self.calcResults(mainframe, resPage)
            
        else:
            resPage.title("Game Over")
            mainframe = Frame(resPage, padx="25", pady="25")
            mainframe.grid()
            ttk.Label(mainframe, text="Better luck next time!", font="Calibri 30").grid(column=0, row=0)
            self.calcResults(mainframe, resPage)
        
    def destroy(self, resPage):
        MainPage(resPage)

    def calcResults(self, mainframe, resPage):
        ttk.Label(mainframe, text="You finished the game with:", font="Calibri 20").grid(column=0, row=1)
            
        ttk.Label(mainframe, text="Gold").grid(column=0, row=2)
        ttk.Label(mainframe, text=Stats["Gold"]).grid(column=1, row=2)
        
        ttk.Label(mainframe, text="Health").grid(column=0, row=3)
        ttk.Label(mainframe, text=Stats["Health"]).grid(column=1, row=3)
        
        ttk.Label(mainframe, text="Items").grid(column=0, row=4)

        items = "None"
        if Stats["Items"].replace("\n", ", ") != "":
            items = Stats["Items"].replace("\n", ", ")
        
        ttk.Label(mainframe, text=items).grid(column=1, row=4)

        ttk.Label(mainframe, text="Total Score").grid(column=0, row=5)
        
        itemCount = 0
        if len(Stats["Items"].split("\n")) != "":
            itemCount = len(Stats["Items"].split("\n"))
        score = Stats["Gold"]+Stats["Health"]+itemCount   
        ttk.Label(mainframe, text=score).grid(column=1, row=5)
         
        ttk.Button(mainframe, text="Quit", command=lambda: self.destroy(resPage)).grid(column=0, row=6)
        
## Handles Inventory ##
class InventoryPage:
    def __init__(self):
        invPage = Tk()
        invPage.title("Inventory")
        mainframe = Frame(invPage, padx="25", pady="25")
        mainframe.grid()

        ttk.Label(mainframe, text="Health:", font="Calibri 10").grid(column=0, row=0)
        hrtsLabel = Label(mainframe, text = "", font="Calibri 10")
        hrtsLabel.grid(column=1, row=0)

        ttk.Label(mainframe, text="Gold:", font="Calibri 10").grid(column=0, row=1)
        gldLabel = Label(mainframe, text = "", font="Calibri 10")
        gldLabel.grid(column=1, row=1)
        
        ttk.Label(mainframe, text="Inventory:", font="Calibri 10").grid(column=0, row=2)        
        invLabel = Label(mainframe, text = "", font="Calibri 10")
        invLabel.grid(column=0, row=3)
        
        self.drawMessage(hrtsLabel, gldLabel, invLabel, invPage)

    def drawMessage(self, hrtsLabel, gldLabel, invLabel, invPage):
        if Stats["confirmExit"]:
            invPage.after(10, invPage.destroy)
            
        else:
            hrtsLabel.config(text=Stats["Health"])
            gldLabel.config(text=Stats["Gold"])
            invLabel.config(text=Stats["Items"])
            invPage.after(100, self.drawMessage, hrtsLabel, gldLabel, invLabel, invPage)
        
## Handles Mid-Game Restart ##
class RestartPage:
    def __init__(self):
        resPage = Tk()
        resPage.title("Restart")
        mainframe = Frame(resPage, padx="25", pady="25")
        mainframe.grid()
        
        ttk.Button(mainframe, text="Restart", command=lambda: self.destroy(True, resPage, mainframe)).grid(column=0, row=6)
        self.checkHealth(resPage, mainframe)
        
    def destroy(self, restart, resPage, mainframe):
        if restart:
            updateStats("confirmRes", True)
            updateStats("confirmExit", True)
            message = Label(mainframe, text="")
            message.grid(column=2, row=2)
            resPage.after(100, MainPage.startup, MainPage, resPage, True, message)
        else:
            resPage.destroy()

    def checkHealth(self, resPage, mainframe):
        if Stats["confirmExit"] and not Stats["confirmRes"]:
            resPage.after(10, self.destroy, False, resPage, mainframe)
            
        elif Stats["Health"] == 0:
            resPage.after(10, resPage.destroy)
        
        else:
            resPage.after(10, self.checkHealth, resPage, mainframe)
        
if __name__ == "__main__":
    splashPage = Tk()
    SplashScreen(splashPage)
    splashPage.mainloop()
