from pyhtml import *
import pdfkit
from wag.core.Page import Page
import datetime
from DOMParser import convertToStr

class Report():
    def __init__(self, siteName):
        self.projectName = siteName
        self.criticalErrors = 0
        self.normalErrors = 0
        self.evalDate = datetime.datetime.now()
        self.pages = []
    
    def formatPagesToReport(self, pages):
        reportPages = []
        for page in pages:
            reportPage = dict()
            resultMap = dict()
            for result in page.evaluationResults.results:
                if (int(result.ftrInfo['priority']) < 2):
                    self.criticalErrors = self.criticalErrors + 1
                else:
                    self.normalErrors = self.normalErrors + 1
                
                ftrTitle = result.ftrInfo['title']
                if ftrTitle in resultMap:
                    resultMap[ftrTitle] = resultMap[ftrTitle] + 1;
                else:
                    resultMap[ftrTitle] = 1; 
            reportPage['url'] = "Page URL:    " , page.url
            reportPage['violationMap'] = resultMap
            
            reportPages.append(reportPage)
        
        self.pages = reportPages    
        return reportPages    


def generateReport(siteName, pages):
    report = Report(siteName)
    report.formatPagesToReport(pages)
    generateHTMLReport(report)




def pagesGenerator(pageCollection):
    for reportPage in pageCollection:
        yield(div(
                  h4(reportPage['url']),"Violations: ", 
                  table(
                         errorsRowGenerator(reportPage['violationMap'])
                         )
                  ))
        
        
def errorsRowGenerator(resultMap):
    for key in resultMap.iterkeys():
        yield tr(
                   th("       "), 
                   th(align = "left")(key),
                   th(resultMap[key])
                   )

def generateHTMLReport(report):
   htmlPageResults = pagesGenerator(report.pages)
   
   print htmlPageResults
   t = html(
        head(
         title('WAG Report for '+ report.projectName),
         ),
        body(
             header(
                    h1("Web Accessibility Report")
                    ),
             div(
                 "Table of overview information",
                 table(
                       tr(
                          th(align = "left")("Project Name"),
                          th(report.projectName),
                          ),
                       tr(
                          th(align = "left")("Evaluated on"),
                          th(report.evalDate.date().isoformat()),
                          ),
                       tr(
                          th(align = "left")("Critical Violation"),
                          th(report.criticalErrors),
                          ),
                       tr(
                          th(align = "left")("Minor Violation"),
                          th(report.normalErrors),
                          )
                       )
                 ),
             br,
             br,
             div(pagesGenerator(report.pages)),
             footer(
                    hr, 
                    "Copyright 2013, 99x Technology"
                    )
         )
        )
   
   writeToHtml(str(t), report.projectName)
   generatePDF(report.projectName)
   
def writeToHtml(report, projectName):
    path = "wag/static/reports/WAG_report_" + projectName + ".html"
    f = open(path , 'w')
    f.write(report)
    f.close()

def generatePDF(projectName):
    projectName = convertToStr(projectName)
    htmlpath = "wag/static/reports/WAG_report_" + projectName + ".html"
    pdfpath = "wag/static/reports/WAG_report_" + projectName + ".pdf" 
    pdfkit.from_file(htmlpath,pdfpath)