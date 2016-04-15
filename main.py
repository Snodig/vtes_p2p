#! python3

'''
 * Date: 14-12-07
 * Desc: entry-point
 * Author: H. Skjevling
'''

import sys, time, traceback, datetime
import threading

import pygame
from pygame.locals import *

from PyVtes import Drawables
from Utilities import CardListCsvParser

s_phases = ["Untap", "Master", "Action", "Influence"]

#Scary multithreaded test-code
class InputThread(threading.Thread):
  def __init__(self, game):
    self.game = game
    threading.Thread.__init__(self, daemon=True)

  def run(self):
    try:
      while(1):
        card = input(">")
        if not card == "":
          print("\nLoading test-card, " + card + ":\n")
          self.game.loadCard(card)
          card = ""
    except KeyboardInterrupt:
      pass

class Game:
  def __init__(self):
    self.mutex = threading.Lock()
    self._running = False
    self.screen = None
    self.size = self.width, self.height = 1600, 900

    self.__startTime = time.mktime(time.localtime())
    self._loopStart = time.time()
    self._fps = 0

    self._csvParser = CardListCsvParser.CardListCsvParser()
    self._csvParser.initialize()
    self.drawables = list()

  def on_init(self):
    pygame.init()
    self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
    pygame.display.set_caption("Py_vtes")
    self._running = True

    self.bg = pygame.Surface(self.screen.get_size())
    self.bg = self.bg.convert()
    self.bg.fill((0,0,0))
    self.screen.blit(self.bg, (0,0))

    self.playmat = Drawables.Drawable("Resources/playmat.jpg")
    self.playmat.rescale(size=self.size)
    #self.playmat.image = pygame.transform.scale(self.playmat.image, self.size)
    #self.playmat.rect = self.screen.get_rect()

    self.mousePointer = Drawables.MousePointer()
    pygame.mouse.set_visible(False)

    self.cardBackLibrary = Drawables.Drawable("Resources/LibraryBack.jpg")
    self.cardBackCrypt = Drawables.Drawable("Resources/CryptBack.jpg")

    return self._running

  def addDrawable(self, drawable):
    self.drawables.append(drawable)

  def loadCard(self, cardName): #Volatile test-code
    try:
      self.mutex.acquire()
      card = self._csvParser.getCard(cardName)
      if card == None:
        return
      if "Abbrev" in card.keys():
        return
      drawableCard = Drawables.Card(card)
      self.addDrawable(drawableCard)
    finally:
      self.mutex.release()

  def on_event(self, event):
    if event.type == QUIT:
      self._running = False

    elif event.type == KEYDOWN:
      print("Key dn: " + pygame.key.name(event.key))
      if event.key == K_ESCAPE:
        self._running = False

    elif event.type == KEYUP:
      print("Key up: " + pygame.key.name(event.key))

    elif event.type == MOUSEMOTION:
      self.mousePointer.move(event.pos)

    #LMouse down
    elif event.type == MOUSEBUTTONDOWN and event.button == 1:
      for drawable in self.drawables:
        if drawable.rect.collidepoint(event.pos):

          if pygame.key.get_mods() & KMOD_CTRL:
            self.mousePointer.highlight(drawable)
          else:
            self.mousePointer.grab(drawable)
          break

    #LMouse up
    elif event.type == MOUSEBUTTONUP and event.button == 1:
      self.mousePointer.drop()

    #Middle mouse down
    elif event.type == MOUSEBUTTONDOWN and event.button == 2:
      # Maybe only do this if the mouse stays still for some time?
      collision = False
      for drawable in self.drawables:
        if drawable.rect.collidepoint(event.pos):
          self.mousePointer.highlight(drawable)
          collision = True
      if not collision:
        self.mousePointer.highlight(None)

    #RMouse down
    elif event.type == MOUSEBUTTONDOWN and event.button == 3:
      for drawable in self.drawables:
        if drawable.rect.collidepoint(event.pos) and type(drawable) == Drawables.Card:

          if pygame.key.get_mods() & KMOD_CTRL:
            drawable.flip()
          else:
            drawable.toggleTap()
          break

  def on_update(self):
    for drawable in self.drawables:
      drawable.update()      
    #print("Current loop took " + str(self.getLoopTime()) + " seconds")
    return 

  def on_render(self):
    #Draw the "table"
    self.playmat.draw(self.screen)

    #TODO: How to handle depth (stacks)?
    for drawable in self.drawables:
      drawable.draw(self.screen)

    font = pygame.font.SysFont("copperplate gothic", 35)
    fpsLabel = font.render("FPS: " + str(self._fps), 1, (255,255,0))
    self.screen.blit(fpsLabel, (10, 10))

    self.mousePointer.draw(self.screen)

    pygame.display.flip()

  def on_cleanup(self):
    pygame.quit()

  def on_execute(self):
    if self.on_init() == False:
      self._running = False

    numFrames = 0
    frame = 0

    while( self._running ):
      if self.getLoopTime() > 0.003: #Should probably be replaced with pygame.Clock
        frame += self.getLoopTime()
        numFrames += 1
        if frame > 1:
          self._fps = numFrames
          #print("Running for " + str(int(self.getRunningTime())) + " seconds, FPS: " + str(numFrames) + "\t", end="\r")
          #print("Running for " + str(int(self.getRunningTime())) + " seconds, FPS: " + str(numFrames))
          frame = 0
          numFrames = 0
        self._loopStart = time.time()

        for event in pygame.event.get():
          self.on_event(event)
        self.on_update()
        self.on_render()

  def getLoopTime(self):
    t = time.time()
    return t - self._loopStart

  def getRunningTime(self):
    localSeconds = time.mktime(time.localtime())
    elapsed = localSeconds - self.__startTime
    return elapsed

def main():
  try:
    t0 = time.localtime()
    game = Game()
    in_thread = InputThread(game) #The game and input-threads should probably be swapped
    in_thread.start()
    game.on_execute()

  except KeyboardInterrupt:
    print ("\n-- Ctrl^C ---")

  except:
    ex = sys.exc_info()[0]
    print ("\n")
    traceback.print_exc()

  finally:
    print("\nTime is now\t", time.strftime("%H:%M:%S"))
    totalTime = time.mktime(time.localtime()) - time.mktime(t0)
    print("Running since\t", time.strftime("%H:%M:%S", t0), "(", totalTime, "seconds )")
    game.on_event(pygame.event.Event(QUIT))

if __name__ == "__main__":
  exit(main())