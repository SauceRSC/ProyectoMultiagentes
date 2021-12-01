# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
#Libraries
import agentpy as ap
import numpy as np
import queue


# %%
#Flag o Indice de direccion
UpMove = 0
DownMove = 1
RightMove = 2
LeftMove = 3

#Arreglo con las posibles direcciones
Moves = [[0,1], [0,-1], [1, 0], [-1, 0]]

maxVels = [20, 30, 40, 50]


# %%
class Semaforo(ap.Agent):
    def setup(self, greenTime, redTime, yellowTime):
        #Color: red = 0, green = 1, yellow = 2
        self.color = 0
        self.durations = [redTime, greenTime, yellowTime] #Arreglo con las duraciones de cada color
        self.directionFlag = 0 #Direccion que controla el semaforo
        self.timer = 0 #El contador para el tiempo
        self.running = False #Bandera para saber si debe de hacer el ciclo o no
    def doColorCycle(self):
        #poner semaforo en verde y el timer en la duracion del verde
        self.color = 1
        self.timer = self.durations[self.color]
        self.running = True
    def update(self):
        #Si no debe de hacer el ciclo poner el semaforo en rojo
        if not self.running:
            self.color = 0
        #Si debe de hacer el ciclo
        else:
            #revisar si mi timer termino
            if self.timer <= 0:
                #cambiar color
                self.color += 1
                #si ya termine mis colores reiniciar y settear banderas a False
                if self.color >=3:
                    self.color = 0
                    self.running = False
                    self.model.lightRunning = False
                #Actualizar el timer a la siguiente duracion
                self.timer = self.durations[self.color]
            #restar 1 al timer en cada paso
            self.timer -= 1


# %%
class Avenue(ap.Model):
    def setup(self):
        #Se crea la cola
        self.cola = queue.Queue()
        #Bandera para saber si hay un semaforo corriendo
        self.lightRunning = False
        #Lista con los agentes semaforos
        self.semaforos = ap.AgentList(self, 4, Semaforo, greenTime=self.p.greenTime, redTime=self.p.redTime, yellowTime=self.p.yellowTime)
        
        #Se pone a cada semaforo la direccion que controla
        for i in range(len(self.semaforos)):
            self.semaforos[i].directionFlag = i

        #Se crean las listas de los agentes carros para cada calle, el nombre es a la direccion que va
        self.carrosUp = ap.AgentList(self, self.p.cars, Car, lenArray=self.p.cars, direction=0)
        self.carrosDown = ap.AgentList(self, self.p.cars, Car, lenArray=self.p.cars, direction=1)
        self.carrosRight = ap.AgentList(self, self.p.cars, Car, lenArray=self.p.cars, direction=2)
        self.carrosLeft = ap.AgentList(self, self.p.cars, Car, lenArray=self.p.cars, direction=3)

        #Se crea arreglo con todos los arreglos de los agentes
        self.arregloCoches = [self.carrosUp, self.carrosDown, self.carrosRight, self.carrosLeft]

        #De forma dinamica se crean las posiciones de los coches
        xFirstValid = range(0, int(self.p.x/2)-20, int(int(self.p.x/2)/len(self.carrosRight)))
        yFirstValid = range(0, int(self.p.y/2)-20, int(int(self.p.y/2)/len(self.carrosUp)))
        xSecondValid = range(int(self.p.x/2)+20, self.p.x, int(int(self.p.x/2)/len(self.carrosDown)))
        ySecondValid = range(int(self.p.x/2)+20, self.p.y, int(int(self.p.y/2)/len(self.carrosLeft)))

        validXFirstCarLocation = [(x,int(self.p.y/2)-10) for x in xFirstValid]
        validXSecondCarLocation = [(x,int(self.p.y/2)+10) for x in xSecondValid]
        validYFirstCarLocation = [(int(self.p.y/2)+10,y) for y in yFirstValid]
        validYSecondCarLocation = [(int(self.p.y/2)-10,y) for y in ySecondValid]

        #Se crea el entorno
        self.crux = ap.Grid(self, [self.p.x, self.p.y], torus=True)

        #Posiciones de los semaforos
        self.semaforosPos = [[int(self.p.x/2), int(self.p.y/2) - 10], 
                        [int(self.p.x/2), int(self.p.y/2) + 10],
                        [int(self.p.x/2) -10, int(self.p.y/2)], 
                        [int(self.p.x/2) +10, int(self.p.y/2)]]
        #Se añaden los semaforos al entorno
        self.crux.add_agents(self.semaforos, self.semaforosPos)
        #Se añaden los coches en cada calle del entorno
        self.crux.add_agents(self.carrosUp, validYFirstCarLocation)
        self.crux.add_agents(self.carrosDown, validYSecondCarLocation)
        self.crux.add_agents(self.carrosRight, validXFirstCarLocation)
        self.crux.add_agents(self.carrosLeft, validXSecondCarLocation)

        #Arreglo para tener a todos los coches juntos
        self.carros = self.carrosUp + self.carrosDown + self.carrosLeft + self.carrosRight
    def step(self):
        #Si la cola no esta vacia y no hay algun semaforo corriendo 
        if not self.cola.empty() and not self.lightRunning:
            #el semaforo que sigue en la cola empieza a correr
            self.cola.get().doColorCycle()
            self.lightRunning = True
        #actualizar los coches y semaforos
        self.semaforos.update()
        self.carros.update_position()

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


# %%
class Car(ap.Agent):
    def setup(self, lenArray, direction):
        self.MaxVelocity = np.random.choice(maxVels) #velocidad maxima del coche
        self.currentVelocity = 0 #velocidad actual del coche
        self.directionFlag = direction #indice de la direccion a la que va
        self.currentDirection = Moves[self.directionFlag] #direccion a la que va
        self.index = 0 #indice del coche en el arreglo de coches en esa calle
        self.carsInLane = lenArray #cantidad de coches en esa calle
        self.queued = False #bandera para solo poner el semaforo en la queue 1 vez
    def update_position(self):
        #modificar la velocidad 
        self.modify_velocity()
        #ver cuanto me voy a mover segun la velocidad actual
        distance = [self.currentVelocity * self.currentDirection[0], self.currentVelocity * self.currentDirection[1]]
        #moverme
        self.model.crux.move_by(self, distance)
    def modify_velocity(self):
        #obtener el semaforo que le toca al coche
        modelInstance = self.model #type:Avenue
        nextSemaforo = modelInstance.semaforos[self.directionFlag] #type: Semaforo

        #posicion del semaforo que le toca
        posSemaforo = modelInstance.crux.positions[nextSemaforo] #type: list[tuple[int, int]]

        #posicion del coche actual
        posActual = modelInstance.crux.positions[self] #type: list[tuple[int, int]]
        
        distEntreCocheYCocheEnfrente = modelInstance.p.x*3
        for car in modelInstance.arregloCoches[self.directionFlag]:
            if car != self:
                posNextCar = modelInstance.crux.positions[car]
                dist = (posNextCar[0]-posActual[0])*self.currentDirection[0] + (posNextCar[1]-posActual[1])*self.currentDirection[1]
                if dist<distEntreCocheYCocheEnfrente and dist>0:
                    distEntreCocheYCocheEnfrente = dist

        #revisar si ya pase el semaforo o no
            #sacar diferencia en las posiciones
        diffEntreCocheYSemaforo = [posSemaforo[0] - posActual[0], posSemaforo[1] - posActual[1]]
            #sacar el escalar de la diferencia multiplicado por la direccion
        distEntreCocheYSemaforo = (diffEntreCocheYSemaforo[0] * self.currentDirection[0]) + (diffEntreCocheYSemaforo[1] * self.currentDirection[1]) #type: int

        #Si no he pasado la pos del semaforo
        if distEntreCocheYSemaforo > 0:
            #si el semaforo esta en verde
            if nextSemaforo.color == 1:
                self.currentVelocity = np.minimum(self.currentVelocity + 5, self.MaxVelocity)
            #si el semaforo esta en amarillo o rojo
            elif nextSemaforo.color == 2 or nextSemaforo.color == 0:
                #voy desacelerando
                self.currentVelocity = np.maximum(self.currentVelocity - 5, 5)
                #Si estoy cerca del semaforo freno y pongo el semaforo en la queue
                if distEntreCocheYSemaforo < 15:
                    self.currentVelocity = 0
                    if not self.queued:
                        modelInstance.cola.put(nextSemaforo)
                        self.queued = True

        #si ya lo pase acelero
        else:
            self.currentVelocity = np.minimum(self.currentVelocity + 5, self.MaxVelocity)
            self.queued = False
        
        #Si estoy cerca del coche de enfrente me freno
        if distEntreCocheYCocheEnfrente > 0 and distEntreCocheYCocheEnfrente <=20:
            self.currentVelocity = 0
        elif distEntreCocheYCocheEnfrente > 0 and distEntreCocheYCocheEnfrente <=50:
            self.currentVelocity = int(self.currentVelocity/2)


# %%
parameters = {
    'step_time': 0.1,
    'x': 600,
    'y': 600,
    'steps': 400,
    'cars':4,
    'yellowTime':10,
    'greenTime':15,
    'redTime':10
}

# %%
model = Avenue(parameters)
results = model.run()
#results
# %%
#results.variables.Avenue.iloc[2:5].to_json()
for i in range(model.p.steps):
    destinations = "JSON/" + str(i) + ".json"
    results.variables.Avenue.iloc[i].to_json(destinations)
