import pygame
import pygame.event



size = [4096,2048]

showingWindow = False
screen = None
basicPaletteFun = lambda value: [0,min(max(0,int(255*value)),255),0]
signedPaletteFun = lambda value: [0,min(max(int(255*(0.5+0.5*value)),0),255),0]
coloredSignedPaletteFun = lambda value: [min(max(int(255*-value),0),255),min(max(int(255*value),0),255),0]

pygame.init()
if showingWindow:
  screen = pygame.display.set_mode(size)
  pygame.display.set_caption("FloatAutomata")
back = pygame.Surface(size)

def close():
  if showWindow:
    pygame.display.quit()
  pygame.quit()
  del back




def draw(arr,paletteFun,saving=False,filename=None):
  if saving:
    assert not filename==None
  if showingWindow:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        close()
        return
        assert False
  for y,row in enumerate(arr):
    for x,item in enumerate(row):
      back.set_at((x,y),paletteFun(item))
  if showingWindow:
    screen.blit(back, (0,0))
    pygame.display.flip()
  if saving:
    pygame.image.save(back, filename + ".png")
  if showingWindow:
    screen.fill([0,0,0]) #clean for next frame