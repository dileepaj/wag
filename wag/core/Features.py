from bs4 import BeautifulSoup
#xml =open("web_accessibility_spec.xml")
#soup = BeautifulSoup(xml, "xml")

class Feature:
    def __init__(self, title, disability,rank,priority,level,error,description,solution,rule):
        self.title = title
        self.disability = disability
        self.rank = rank
        self.priority = priority
        self.level = level
        self.error = error
        self.description = description
        self.solution = solution
        self.rule = rule 
        
    
class Features:      
    def makeFeatureCollection (self):
        features = [];
        for i in soup.findAll("FEATURE"):
            features.append(Feature(i.TITLE,i.DISABILITY,i.DISABILITY['rank'],i.PRIORITY,i.PRIORITY['level'],i.ERROR.get_text(),i.DESCRIPTION,i.SOLUTION,i['id']))
        return features