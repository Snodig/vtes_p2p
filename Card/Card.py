'''
 * Date: 14-12-07
 * Desc: Card Generic Container
 * Author: H. Skjevling
'''

class Discipline:
  def __init__(self, name):
    self._name = name

class Auspex(Discipline):
  def __init__(self):
    Discipline.__init__(self, self.__class__.__name__)

class Card:
  def __init__(self, name):
  	self._name = "Unnamed card"
    self._filename = "CardName.png"
    #Attributes such as tapping or torpor, should be controlled by the board, not the cards

class LibraryCard(Card):
  def __init__(self, name):
    Card.__init__(self, name)
    self._cost = int()
    poolCost = False

class CryptCard(Card):
  def __init__(self, name):
    Card.__init__(self, name)
    self._capacity = int()
    self.blood = 0
    self._clan = str()
    self.__group = int()
    self._bleed = 1
    self._title = ""
    self.__set = ""

class Master(LibraryCard):
  def __init__(self, name):
    LibraryCard.__init__(self, name)
    self.__trifle = False

#Also counts as Gehenna
class Event(LibraryCard):
  def __init__(self, name):
    LibraryCard.__init__(self, name)

''''''
class Action(LibraryCard):
  def __init__(self, name):
    LibraryCard.__init__(self, name)

class Referendum(Action):
  def __init__(self, name):
    Action.__init__(self, name)

class Rush(Action):
  def __init__(self, name):
    Action.__init__(self, name)

class Bleed(Action):
  def __init__(self, name):
    Action.__init__(self, name)
    self.__bleedValue

class Equip(Action):
  def __init__(self, name):
    Action.__init__(self, name)
''''''

''''''
class Reaction(LibraryCard):
  def __init__(self, name):
    LibraryCard.__init__(self, name)

class Wake(Reaction):
  def __init__(self, name):
    Reaction.__init__(self, name)

class Bounce(Reaction):
  def __init__(self, name):
    Reaction.__init__(self, name)
''''''

class Combat(LibraryCard):
  def __init__(self, name):
    LibraryCard.__init__(self, name)

class Modifier(LibraryCard):
  def __init__(self, name):
    LibraryCard.__init__(self, name)

class Deck:
  def __init__(self):
    self.crypt = list()
    self.library = list()

  def count(self):
    return len(self.crypt) + len(self.library)