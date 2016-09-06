
def enum(**enums):
    return type('Enum', () , enums)

States = enum(UNRESOLVED = u'Unresolved' , 
              IGNORE = u'Skipped',
              RESOLVED = u'Solved')  
       
class RuleEvalResult(object):
    
    id = 0;
    element = None
    line = 0;
    nodeLines = 0;
    status = ''       
    
    def __init__(self, id, type, elem):        
        self.id = id
        self.featureId = type
        self.element = elem
        self.nodeLines = elem.count('\\n')
        self.status = States.UNRESOLVED
        self.ftrInfo = None 

        
   