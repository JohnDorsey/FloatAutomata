

import math


printChars = " -~+#&0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
basicFun = lambda value: math.sin(value)

def product(arr):
  """return the product of all numbers in an array - useful for constructing new rules for cell updates."""
  result = 1.0
  for item in arr:
    result *= item
  return result


class World:
  def __init__(self,layerCount=2,size=(32,32),wrap="torus"):
    assert wrap=="torus" #world wrap cannot be turned off in this design.
    self.size = size
    self.wrap = wrap
    self.t = 0
    self.layerCount = layerCount #layers are used to store world 
    self.reset()
    
  def reset(self):
    self.cells = [[[0.0 for x in range(self.size[0])] for y in range(self.size[1])] for layerIndex in range(self.layerCount)]
    #self.cells[0][self.size[1]/2][self.size[0]/2] = 1.0
    
  def multiply(self,a):
    """multiply every cell in the world by a."""
    for layerIndex in range(self.layerCount):
      for y in range(self.size[1]):
        for x in range(self.size[0]):
          self.cells[layerIndex][y][x] *= a
          
  def fill(self,a):
    """set every cell in the world to a."""
    for layerIndex in range(self.layerCount):
      for y in range(self.size[1]):
        for x in range(self.size[0]):
          self.cells[layerIndex][y][x] = a
          
  def spawn(self,arr):
    """spawn the 2d array of numbers into the world with its top-left corner at the center of the world."""
    for xOff,arrRow in enumerate(arr):
      for yOff,arrItem in enumerate(arrRow):
        self.cells[self.t%self.layerCount][int(self.size[1]/2+yOff)][int(self.size[0]/2+xOff)] = arrItem
    print("spawn completed.")
    
  def getNeighborhood(self,layerIndex,x,y):
    return (self.cells[layerIndex][(y+j)%self.size[1]][(x+i)%self.size[0]] for i,j in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)])
    
  def evalNeighborhood(self,layerIndex,x,y):
    """This function turns an array of neighbors into a single number for functions that need it, as in World.advance(...,isFunOfArr=False)"""
    return sum(self.getNeighborhood(layerIndex,x,y))
    
  def advance(self,fun,isFunctionOfArr=False):
    """advance the whole world by one iteration."""
    self.t += 1
    inputProviderFun = (self.getNeighborhood if isFunctionOfArr else self.evalNeighborhood) #choose either a function that gives an array or a function that gives the result of evaluating an array, depending on what the world rule provided in the argument _fun_ needs as an argument.
    for y in range(self.size[1]):
      for x in range(self.size[0]):
        self.cells[self.t%self.layerCount][y][x] = fun(inputProviderFun((self.t-1)%self.layerCount,x,y),x,y,self.t)

  def prettyPrint(self):
    print("  +"+"-"*(self.size[0]-4)) #info tab top border.
    print("  | t="+str(self.t)) #info tab content.
    print("+-+"+"-"*(self.size[0]-4)+"--+") #divider between info tab and printed frame.
    for y,row in enumerate(self.cells[self.t%self.layerCount]):
      print("|"+"".join(printChars[int(min(math.floor(6*cellState),5))] for cellState in row)+"|") #a line of the printed frame.
    print("+"+"-"*self.size[0]+"+") #printed frame bottom border.

  def simulate(self,fun,targetTime,renderModulus=1,stimulusFun=None):
    """This method provides a simple way to loop World.advance with adjustable monitoring."""
    while True:
      if self.t%renderModulus==0:
        self.prettyPrint()
      if stimulusFun:
        self.cells[self.t%self.layerCount][self.size[1]/2][self.size[0]/2] += stimulusFun(self.t) #if provided, use the stimulus function (a function of time) to increase the value of the cell at the center of the world, to help detect world rules that can sustain life.
      self.advance(fun)
      if self.t >= targetTime: #always print the world when finished.
        self.prettyPrint()
        return



"""
fun = lambda x: sin(x/a)**b
  (a,b,start) | result
  ----------------------
    2.0,2,1.0 | chaos?
    2.5,2,1.0 | dead.
    2.4,2,2.0 | chaos?
    2.6,2,2.0 | chaos?
    6.0,2,4.0 | dead.
fun = lambda x,t: math.sin(x/(5.0-t/(256*128.0)))**2
  empty at t=65280
  circle shape at t=65408
  almost full of shapes at t=65536
fun = lambda x,t: math.sin(x/(a-t/(131072.0)))**2
  chaotic at a=3.2 t=25856
fun = lambda x,t: math.sin(x/(a-t/(524288.0)))**2
  dead at a=3.1 t=49152
  chaotic at a=3.1 t=49280
"""



"""
for iter in range(256):
  pr.draw(world.cells[world.t%world.layerCount],pr.basicPaletteFun,saving=True,filename=("FloatAutomata_exp(abs(sin(x))y)_at_iter_"+str(iter)))
  world.advance(lambda value,x,y,t: abs(math.sin(value)*(x/100.0))**(y/100.0))
"""