from bs4 import BeautifulSoup
#Refer BeautifulSoup http://www.crummy.com/software/BeautifulSoup/bs4/doc/#searching-the-tree 
#Please refer Rules_example.py for an example rule implementation 

class Rules:
    def __init__(self):        
        self.ruleCollection = {
         "1" : self.rule1,         
        }
 
    def getRule(self, id):
        return self.ruleCollection[id]
  
    def rule1(self,dom):
        #Enter Your code here
    


