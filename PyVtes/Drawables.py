
'''
 * Date: 14-12-16
 * Desc: All Surface-holding objects
 * Author: H. Skjevling
'''
import pygame
from Utilities import Functions

s_orignalCardSize = (363, 513)
s_defaultCardSize = (int(363/2), int(513/2))
'''
class Drawable(pygame.sprite.Sprite): #Should we just use Surface?
  def __init__(self, imageFile):
    pygame.sprite.Sprite.__init__(self)
    display_surf = pygame.display.get_surface()
    self.originalImage, self.rect = Functions.loadImage(imageFile)
    self.image = pygame.Surface.copy(self.originalImage)
    self.area = display_surf.get_rect()
    self.sprite = pygame.sprite.RenderPlain(self)

    #More or less test-code
    self.rect.center = self.area.center

    print(imageFile + ": " + str(self.rect))

  def move(self, pos):
    self.rect.center = pos

  def draw(self, screen):
    self.sprite.draw(screen)

  def update(self):
    pygame.event.pump()

  def resetScale(self):
    self.image = pygame.Surface.copy(self.originalImage)
    self.rect.size = self.image.get_rect().size

  def rescale(self, size:tuple=None, scaleRatio:float=None):
    newSize = self.image.get_rect().size

    if size != None:
      newSize = size

    if scaleRatio != None:
      newSize = (int(newSize[0]*scaleRatio), int(newSize[1]*scaleRatio))

    self.image = pygame.transform.scale(self.image, newSize)
    self.rect.size = self.image.get_rect().size
'''
class Drawable(): #Should we just use Surface?
  def __init__(self, imageFile):
    self.imageFile = str(imageFile)
    self.originalImage, self.rect = Functions.loadImage(self.imageFile)
    self.image = pygame.Surface.copy(self.originalImage)
    self.rotation = 0.0
    self.highlit = False

  def move(self, pos):
    self.rect.center = pos

  def draw(self, screen):
    screen.blit(self.image, self.rect)

  def update(self):
    pygame.event.pump()

  def resetScale(self):
    self.rescale(size=self.originalImage.get_rect().size)

  #Size overrides ratio
  #Sets absolute size or multiplies current size by ratio
  def rescale(self, size:tuple=None, scaleRatio:float=None):

    if size != None:
      self.rect.size = size
    elif scaleRatio != None:
      print("Rescaling " + self.imageFile + " by a ratio of " + str(scaleRatio))
      self.rect.size = (self.rect.size[0]*scaleRatio, self.rect.size[1]*scaleRatio)
    else:
      self.resetScale()
      return
      #raise Exception("Drawable.rescale requires at least one argument")

    self.recalcDimensions()

  def rotate(self, angle):
    self.rotation += angle
    self.recalcDimensions()

  def recalcDimensions(self):
    self.image = pygame.transform.scale(self.originalImage, self.rect.size)
    self.rect.size = self.image.get_rect().size
    self.image = pygame.transform.rotate(self.image, self.rotation)
    print("Attributes of " + self.imageFile + ": " + str(self.rect.size) + ", " + str(self.rotation))

  def highlight(self, highlight_onOff):
    if self.highlit == highlight_onOff:
      highlight_onOff = False

    print("highlight_onOff=" + str(highlight_onOff))

    if highlight_onOff:
      self.rescale(scaleRatio=2.0)
    else:
      self.resetScale()
    self.highlit = highlight_onOff

#Consider using sprite.groups (maybe for stacks and decks?) (read up first!)
class Card(Drawable):
  def __init__(self, cardDict):
    self.cardDict = dict(cardDict)
    imageFile = self.cardDict["FileName"]
    print("Loading: " + imageFile)
    Drawable.__init__(self, imageFile)
    self.isTapped = False
    self.resetScale()

  def resetScale(self):
    Drawable.resetScale(self)
    self.rescale(size=s_defaultCardSize)

  def isTapped(self):
    return self.isTapped


  # Bug: When tapped, collision is still done on the original rect for some reason
  def tap(self):
    if not self.isTapped:
      center = self.rect.center
      self.rotate(-90)
      self.rect.center = center
      self.isTapped = True

  def untap(self):
    if self.isTapped:
      center = self.rect.center
      self.rotate(90)
      self.rect.center = center
      self.isTapped = False

  def toggleTap(self):
    if self.isTapped:
      self.untap()
    else:
      self.tap()

  def flip(self):
    pass    

class MousePointer(Drawable):
  def __init__(self):
    Drawable.__init__(self, "Resources/blooddrop.png")
    self.rotate(-135.0)
    self.rescale(scaleRatio=0.1)
    #self.image = pygame.transform.rotozoom(self.image, -135.0, 0.1)
    #self.rect = self.image.get_rect()
    self.grabbed = None
    self.highlit = None

  #TODO: grab() and drop() seriously fuck with images if they are rotated before picking up
  def grab(self, item):
    if type(item) == Card:
      self.grabbed = item
      if self.grabbed == self.highlit:
        self.highlight(None)
      print("Mousepointer grabbed: " + str(self.grabbed.cardDict["Name"]))
      item.rescale(scaleRatio=1.1)

  def drop(self):
    if self.grabbed != None:
      print("Mousepointer dropped: " + str(self.grabbed.cardDict["Name"]))

      if type(self.grabbed) == Card:
        self.grabbed.resetScale() #Should probably be moved to the Card class (drop())
      self.grabbed = None

  def move(self, pos):
    self.rect.topleft = (pos[0]-10, pos[1]-10)

    if not self.grabbed == None:
      self.grabbed.move(pos)

  def highlight(self, item):
    if self.highlit != None and item == None:
      self.highlit.highlight(False)

    self.highlit = item
    if item != None:
      item.highlight(True)

class InfoPanel(Drawable):
  def __init__(self, infoDict:dict):
    self.dict = infoDict

class CardPreview(InfoPanel):
  def __init__(self, card:Card):
    InfoPanel.__init__(self)