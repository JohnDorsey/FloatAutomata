
import math


printChars = " -~+#&0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
basicFun = lambda value: math.sin(value)



class World:
  def __init__(self,layerCount=2,size=(32,32),wrap="torus"):
    assert wrap=="torus"
    self.size = size
    self.wrap = wrap
    self.t = 0
    self.layerCount = layerCount
    self.reset()
    
  def reset(self):
    self.cells = [[[0.0 for x in range(self.size[0])] for y in range(self.size[1])] for layerIndex in range(self.layerCount)]
    #self.cells[0][self.size[1]/2][self.size[0]/2] = 1.0
    
  def multiply(self,a):
    for layerIndex in range(self.layerCount):
      for y in range(self.size[1]):
        for x in range(self.size[0]):
          self.cells[layerIndex][y][x] *= a
    
  def evalNeighborhood(self,layerIndex,x,y):
    return sum(self.cells[layerIndex][(y+j)%self.size[1]][(x+i)%self.size[0]] for i,j in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)])
    
  def advance(self,fun):
    self.t += 1
    for y in range(self.size[1]):
      for x in range(self.size[0]):
        self.cells[self.t%self.layerCount][y][x] = fun(self.evalNeighborhood((self.t-1)%self.layerCount,x,y),x,y,self.t)

  def prettyPrint(self):
    print("  +"+"-"*(self.size[0]-4))
    print("  | t="+str(self.t))
    print("+-+"+"-"*(self.size[0]-4)+"--+")
    for y,row in enumerate(self.cells[self.t%self.layerCount]):
      print("|"+"".join(printChars[int(min(math.floor(6*cellState),5))] for cellState in row)+"|")
    print("+"+"-"*self.size[0]+"+")

  def simulate(self,fun,targetTime,printModulus=1,stimulusFun=None):
    """if stimulusFun == None:
      stimulusFun = lambda t: 0"""
    while True:
      if self.t%printModulus==0:
        self.prettyPrint()
      if stimulusFun:
        self.cells[self.t%self.layerCount][self.size[1]/2][self.size[0]/2] += stimulusFun(self.t)
      self.advance(fun)
      if self.t >= targetTime:
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
