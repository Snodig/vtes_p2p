'''
 * Date: 14-12-14
 * Desc: Parser for csv card-lists
 * Author: H. Skjevling
'''

import csv
from Utilities import Functions
    
import threading

class CardListCsvParser:

  def __init__(self):
    self.cryptDict = dict()
    self.libraryDict = dict()
    self.setsDict = dict()
    self.initialized = False

  def parseCrypt(self):
    try:
      with open("Resources/vtescrypt.csv", newline="", encoding="utf-8-sig") as csvFile:
        reader = csv.DictReader(csvFile, delimiter=",", quotechar="\"")
        for row in reader:
          row["FileName"] = Functions.getImageFileName(row)
          self.cryptDict[row["Name"]] = row
    except:
      print("\nParsing crypt failed at row " + str(len(self.cryptDict)+1) + ": \n" + str(row))
      raise
    finally:
      pass

  def parseLibrary(self):
    try:
      with open("Resources/vteslib.csv", newline="", encoding="utf-8-sig") as csvFile:
        reader = csv.DictReader(csvFile, delimiter=",", quotechar="\"", lineterminator="\n")
        for row in reader:
          row["FileName"] = Functions.getImageFileName(row)
          self.libraryDict[row["Name"]] = row
    except:
      print("\nParsing library failed at row " + str(len(self.libraryDict)+1) + ": \n" + str(row))
      raise
    finally:
      pass

  def parseSets(self):
    try:
      with open("Resources/vtessets.csv", newline="", encoding="utf-8-sig") as csvFile:
        reader = csv.DictReader(csvFile, delimiter=",", quotechar="\"")
        for row in reader:
          self.setsDict[row["Abbrev"]] = row
    except:
      print("\nParsing sets failed at row " + str(len(self.setsDict)+1) + ": \n" + str(row))
      raise
    finally:
      pass

  def initialize(self):
    print("Initializing Parser")
    self.parseCrypt()
    self.parseLibrary()
    self.parseSets()
    self.initialized = True

  def getCard(self, cardName):
    if self.initialized == False:
      print("Parser not initialized!")

    tmpCardName = cardName
    if tmpCardName.endswith("*"):
      tmpCardName = cardName.replace("*", "").lower()
    for k in self.cryptDict.keys():
      if k.lower().startswith(tmpCardName):
        return self.cryptDict[k]
    for k in self.libraryDict.keys():
      if k.lower().startswith(tmpCardName):
        return self.libraryDict[k]
    for k in self.setsDict.keys():
      if k.lower().startswith(tmpCardName):
        print("Found set by name: " + k)
        return self.setsDict[k]
    '''
    else:
      if cardName in self.cryptDict:
        return self.cryptDict[cardName]
      elif cardName in self.libraryDict:
        return self.libraryDict[cardName]
      elif cardName in self.setsDict:
        return self.setsDict[cardName]
     '''

    print("Could not find card by name: " + cardName)
    return None