import abc


class DBInterface(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self):
        self.openConnection()
    
    @abc.abstractmethod
    def openConnection(self):
        return
    
    #@abc.abstractmethod
    def closeConnection(self):
        return
    
    def createPage(self, obj):
        return
    
    #@abc.abstractmethod
    def update(self, recordId):
        return
    
    #@abc.abstractmethod
    def delete(self, recordId):
        return
    
    #@abc.abstractmethod
    def remove(self, recordId):
        return
    
    