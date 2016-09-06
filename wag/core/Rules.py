from bs4 import BeautifulSoup
import re

class Rules:
    def __init__(self):
        self.ruleCollection = {
         "1" : self.rule1,
         "2" : self.rule2,
         "3" : self.rule3,
         "4" : self.rule4,
         "5" : self.rule5,
         "6" : self.rule6,
         "7" : self.rule7,
         "8" : self.rule8,
         "9" : self.rule9,
         "10" : self.rule10,
        }
        
    def getRule(self, id):
        return self.ruleCollection[id]
    # Image without text alternatives
    def rule1(self,dom):
        return dom.find_all(self._img_without_alt)
           
    # Embeded multimedia without noembed (text or audio)
    def rule2(self,dom):
       video_arr = []
       for embed in dom.find_all("embed"):
           if not embed.noembed:
               video_arr.append(embed)
       return video_arr
       
    #color cues
    #without the definitions in css
    #This rule needs to be improved
    def rule3(self,dom):
        clrcue_arr = []
        for fnt in dom.find_all('font'):
            if fnt.has_attr('color'):
                clrcue_arr.append(fnt)
        for spn in dom.find_all('span'):
            if spn.has_attr('style'):
                clrcue_arr.append(spn)
        return clrcue_arr
    
    #Table without summary
    def rule4(self,dom):
        return dom.find_all(self._tbl_without_summ)
    
    
    #Table without caption
    def rule5(self,dom):
        twcap_arr = [];
        for tb in dom.find_all("table"):
            if not tb.caption:
                twcap_arr.append(tb)
        return twcap_arr
    
    def rule6(self,dom):
        lbl_arr = [];
        inputElems =[]
        inputElems.extend(dom.find_all(["textarea", "select"]))
        inputElems.extend(dom.find_all(type=["text","password", "checkbox", "radio", "file"]))
        labels = dom.find_all('label')
        for input in inputElems:
            hasLabel = False
            if input.has_attr('id'):
                id = input['id']
                
                for lbl in labels:
                    if lbl.has_attr("for") and lbl['for'] == id:
                        hasLabel = True
                        break
                
            if not hasLabel:
                lbl_arr.append(input)

        return lbl_arr
    
    def rule7(self,dom):
        dblclk_arr = []
        dblclk_arr = dom.find_all(ondblclick = True, onkeypress = False)
        return dblclk_arr
    
    def rule8(self,dom):
        title_arr = []
        isTitle = dom.find('title')
        if isTitle is None:
            title_arr.append(dom.find('head'))
        return title_arr
    
    def rule9(self,dom):
        link_arr = []
        url_tags = ['http', 'https', '://www.' , 'www' ]
        for link in dom.find_all('a'):
            if not ('http' in link or 'https' in link or '://www.' in link or 'www' in link):
                link_arr.append(link)
        
        return link_arr
    
    def rule10(self,dom):
        tab_arr = []
        for tab in dom.find_all('a', 'input', ondblclick = True, onkeydown = True, onkeypress = True):
            if not tab.has_attr('tabindex'):
                tab_arr.append(tab)
        
        return tab_arr    
    
    def _img_without_alt(self,tag):
        return tag.name == "img" and not tag.has_attr("alt")
    
    def _tbl_without_summ(self,tag):
        return tag.name == "table" and not tag.has_attr("summary")
    
#for testing



