from bs4 import BeautifulSoup
from Features import Feature
from Rules import Rules
from Settings import PROJECT_ROOT
from wag.utils.Constants import *
import os.path


class RuleInterpreter:
    
    def __init__(self):
        self.soup = self._initKnowledgeBase()
        self.features = []
        self.rules = Rules()
        self.makeFeatureCollection()
    
    def _initKnowledgeBase(self):
   #     dir = os.path.dirname(__file__)
        print KNOWLEDGE_BASE_URL
        filename = os.path.join(PROJECT_ROOT, KNOWLEDGE_BASE_URL)
        print filename
        xml = open(filename)
        return BeautifulSoup(xml, "xml")

    def getFeature(self, index):
        return features[index]
    
    def getFeatureDict(self, index):
        ftrDict = {'title' : self.features[index].title,
                    'disability' : self.features[index].disability,
                    'error' : self.features[index].error,
                    'description' : self.features[index].description,
                    'solution' : self.features[index].solution,
					'priority' : self.features[index].level,
					'rank' : self.features[index].rank
					}
        return ftrDict
    
    def makeFeatureCollection (self):
        for i in self.soup.findAll("FEATURE"):
            self.features.append(Feature(i.TITLE.get_text(),i.DISABILITY.get_text(),i.DISABILITY['rank'],i.PRIORITY,i.PRIORITY['level'],i.ERROR.get_text(),i.DESCRIPTION.get_text(),i.SOLUTION.get_text(),self.rules.getRule(i['id']))) 
        return self.features
    
