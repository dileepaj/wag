from bs4 import BeautifulSoup

class Rules:
    def __init__(self):        
        self.ruleCollection = {
         "1" : self.rule1,         
        }
 
    def getRule(self, id):
        return self.ruleCollection[id]
    # Image without text alternatives
    def rule1(self,dom):
        return dom.find_all(self._img_without_alt)
        
    def _img_without_alt(self,tag):
        return tag.name == "img" and not tag.has_attr("alt")




