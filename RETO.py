import agentpy as ap
from queue import Queue
import requests
import json
import time
    
class Semaforo(ap.Agent):
    def setup(self):
        self.color = 0
        self.durations = [10, 15]
        self.directionFlag = 0
        self.timer = 0
        self.running = False
    def doColorCycle(self):
        self.color = 1
        self.timer = self.durations[self.color]
        self.running = True
    def update(self):
        if not self.running:
            self.color = 0
        else:
            if self.timer <= 0:
                self.color += 1
                if self.color >=2:
                    self.color = 0
                    self.running = False
                    self.model.lightRunning = False
                self.timer = self.durations[self.color]
            self.timer -= 1

class Avenue(ap.Model):
    def setup(self):
        self.url = "http://127.0.0.1:5000/"
        self.x = any
        self.postData = []
        self.x=requests.post(self.url+"reset",json=self.postData)
        print(self.x.text)
        self.cola = Queue()
        self.lightRunning = False
        self.semaforos = ap.AgentList(self, 4, Semaforo)
        for i in range(len(self.semaforos)):
            self.semaforos[i].directionFlag = i

        self.carrosUp = ap.AgentList(self, self.p.cars, Car, direction=0)
        self.carrosDown = ap.AgentList(self, self.p.cars, Car, direction=1)
        self.carrosRight = ap.AgentList(self, self.p.cars, Car, direction=2)
        self.carrosLeft = ap.AgentList(self, self.p.cars, Car, direction=3)

        self.carrosUp.currentDirection = [0,1]
        self.carrosDown.currentDirection = [0,-1]
        self.carrosRight.currentDirection = [1,0]
        self.carrosLeft.currentDirection = [-1,0]

        self.arregloCoches = [self.carrosUp, self.carrosDown, self.carrosRight, self.carrosLeft]

        xFirstValid = range(0, int(self.p.x/2)-5, int(int(self.p.x/2)/len(self.carrosRight)))
        yFirstValid = range(0, int(self.p.y/2)-5, int(int(self.p.y/2)/len(self.carrosUp)))
        xSecondValid = range(int(self.p.x/2)+5, self.p.x, int(int(self.p.x/2)/len(self.carrosDown)))
        ySecondValid = range(int(self.p.x/2)+5, self.p.y, int(int(self.p.y/2)/len(self.carrosLeft)))

        validXFirstCarLocation = [(x,int(self.p.y/2)-5) for x in xFirstValid]
        validXSecondCarLocation = [(x,int(self.p.y/2)+5) for x in xSecondValid]
        validYFirstCarLocation = [(int(self.p.y/2)+5,y) for y in yFirstValid]
        validYSecondCarLocation = [(int(self.p.y/2)-5,y) for y in ySecondValid]

        self.crux = ap.Grid(self, [self.p.x, self.p.y], torus=True)

        self.semaforosPos = [[int(self.p.x/2), int(self.p.y/2) - 5], [int(self.p.x/2), int(self.p.y/2) + 5], [int(self.p.x/2) -5, int(self.p.y/2)],  [int(self.p.x/2) +5, int(self.p.y/2)]]
        self.crux.add_agents(self.semaforos, self.semaforosPos)
        self.crux.add_agents(self.carrosUp, validYFirstCarLocation)
        self.crux.add_agents(self.carrosDown, validYSecondCarLocation)
        self.crux.add_agents(self.carrosRight, validXFirstCarLocation)
        self.crux.add_agents(self.carrosLeft, validXSecondCarLocation)

        # for agent in self.crux.agents.to_list():
        #     tmp = {"Agente":[{"x":self.crux.positions[agent][0], "z":self.crux.positions[agent][1], "color":agent.color}]}
        #     self.postData.append(tmp)
        # self.postData = {"Datos":self.postData}
        # data=json.dumps(self.postData)
        # print(data)
        # with open('datos.json', 'w') as f:
        #     json.dump(self.postData, f, indent=4)
        # self.postData = []

    def step(self):
        if not self.cola.empty() and not self.lightRunning:
            self.cola.get().doColorCycle()
            self.lightRunning = True
        self.semaforos.update()
        self.carrosUp.update_position()
        self.carrosDown.update_position()
        self.carrosRight.update_position()
        self.carrosLeft.update_position()

    def update(self):
        pos_up = []
        pos_down = []
        pos_left = []
        pos_right = []
        for car in self.carrosUp:
            pos_up.append(self.crux.positions[car])
        for car in self.carrosDown:
            pos_down.append(self.crux.positions[car])
        for car in self.carrosLeft:
            pos_left.append(self.crux.positions[car])
        for car in self.carrosRight:
            pos_right.append(self.crux.positions[car])
        self.record('Semaforos', self.semaforosPos)
        self.record('SemaforoColor', self.semaforos.color)
        self.record('PosCarsUp', pos_up)
        self.record('PosCarsDown', pos_down)
        self.record('PosCarsLeft', pos_left)
        self.record('PosCarsRight', pos_right)
        self.postData = []

        for agent in self.crux.agents.to_list():
            tmp = {"Agente":[{"x":self.crux.positions[agent][0], "z":self.crux.positions[agent][1], "color":agent.color}]}
            self.postData.append(tmp)
        self.postData = {"Datos":self.postData}
        data=json.dumps(self.postData)
        with open('datos.json', 'w') as f:
            json.dump(self.postData, f, indent=4)
        self.x=requests.post(self.url,json=self.postData)
        time.sleep(0.5)

class Car(ap.Agent):
    def setup(self, direction):
        self.MaxVelocity = 10
        self.currentVelocity = 0
        self.directionFlag = direction
        self.currentDirection = [0,0]
        self.index = 0
        self.queued = False
        self.color = 5
    def update_position(self):
        self.modify_velocity()
        distance = [self.currentVelocity * self.currentDirection[0], self.currentVelocity * self.currentDirection[1]]
        self.model.crux.move_by(self, distance)
    def modify_velocity(self):
        modelInstance = self.model
        nextSemaforo = modelInstance.semaforos[self.directionFlag]

        posSemaforo = modelInstance.crux.positions[nextSemaforo]

        posActual = modelInstance.crux.positions[self]
        
        distEntreCocheYCocheEnfrente = modelInstance.p.x*3
        for car in modelInstance.arregloCoches[self.directionFlag]:
            if car != self:
                posNextCar = modelInstance.crux.positions[car]
                dist = (posNextCar[0]-posActual[0])*self.currentDirection[0] + (posNextCar[1]-posActual[1])*self.currentDirection[1]
                if dist<distEntreCocheYCocheEnfrente and dist>0:
                    distEntreCocheYCocheEnfrente = dist
        diffEntreCocheYSemaforo = [posSemaforo[0] - posActual[0], posSemaforo[1] - posActual[1]]
        distEntreCocheYSemaforo = (diffEntreCocheYSemaforo[0] * self.currentDirection[0]) + (diffEntreCocheYSemaforo[1] * self.currentDirection[1])

        if distEntreCocheYSemaforo > 0:
            if nextSemaforo.color == 1:
                self.currentVelocity = min(self.currentVelocity + 5, self.MaxVelocity)
            elif nextSemaforo.color == 2 or nextSemaforo.color == 0:
                self.currentVelocity = max(self.currentVelocity - 5, 5)
                if distEntreCocheYSemaforo < 20:
                    self.currentVelocity = 0
                    if not self.queued:
                        modelInstance.cola.put(nextSemaforo)
                        self.queued = True
                elif distEntreCocheYSemaforo < 40:
                    self.currentVelocity = int(self.currentVelocity/2)
        else:
            self.currentVelocity = min(self.currentVelocity + 5, self.MaxVelocity)
            self.queued = False
        
        if distEntreCocheYCocheEnfrente > 0 and distEntreCocheYCocheEnfrente <=10:
            self.currentVelocity = 0

parameters = {
    'step_time': 1,
    'x': 200,
    'y': 200,
    'steps': 100,
    'cars':5,
    'yellowTime':10,
    'greenTime':15
}

model = Avenue(parameters)
results = model.run()
results.variables.Avenue.to_json(r'data.json')

print(model.x.text)

