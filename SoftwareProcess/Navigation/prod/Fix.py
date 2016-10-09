import datetime
import os
import Angle
import xml.dom.minidom
import math

class Fix():
    def __init__(self,textFile = None):
        self.classErrorName = 'Fix.'
        methodErrorName = '__init__:  ' #defined for error handling
        if textFile == None:
            if os.path.isfile("log.txt"):
                self.logFile = "log.txt"
                text_file = open("log.txt", "a")
            else:
                try:
                    text_file = open("log.txt", "w")
                except ValueError as e:
                    errorMesg = self.classErrorName + methodErrorName + "Unable to open file. " + e
                    raise ValueError(errorMesg) 
        else:
            suffix = ".txt";
            if textFile.endswith(suffix):
                if os.path.isfile(textFile):
                    text_file = open(textFile, "a")
                else:
                    try:
                        self.logFile = textFile
                        text_file = open(textFile, "w")    
                    except ValueError as e:
                        errorMesg = self.classErrorName + methodErrorName + "Unable to open file. " + e
                        raise ValueError(errorMesg)                    
            else:
                errmsg = self.classErrorName + methodErrorName + 'Improper file extension used'
                raise ValueError(errmsg)
        utc_datetime = datetime.datetime.utcnow()
        text_file.write("LOG " + utc_datetime.strftime("%Y-%m-%d %H:%M:%S") + "-6:00 "+ "Start of Log\n")    
        text_file.close()
        
    def setSightingFile(self, sightingFile = None):
        methodErrorName = 'setSightingFile:  ' #defined for error handling
        if sightingFile == None:
            errmsg = self.classErrorName + methodErrorName + 'No .xml file given'
            raise ValueError(errmsg)
        suffix = ".xml";
        if sightingFile.endswith(suffix):
            if os.path.isfile(sightingFile):
                self.sightingFile = sightingFile
                log_file = open(self.logFile, "a")
                utc_datetime = datetime.datetime.utcnow()
                log_file.write("LOG " + utc_datetime.strftime("%Y-%m-%d %H:%M:%S") + "-6:00 "+ "Start of sighting file: " + str(sightingFile) + "\n")
                return True
            else:
                return False
        else:
            errmsg = self.classErrorName + methodErrorName + 'Improper file extension used'
            raise ValueError(errmsg)
        
    def getSightings(self):
        self.approxLat = Angle.Angle()
        self.approxLong = Angle.Angle()
        document = """\
<fix>
<sighting>            
<body>Aldebaran</body>        
<date>2016-03-01</date>        
<time>23:40:01</time>        
<observation>015d04.9</observation>    
<height>6.0</height>        
<temperature>72</temperature>        
<pressure>1010</pressure>        
<horizon>Artificial</horizon>        
</sighting>            
<sighting>            
<body>Peacock</body>        
<date>2016-03-02</date>        
<time>00:05:05</time>        
<observation>045d15.2</observation>    
<height>6.0</height>        
<temperature>71</temperature>        
<pressure>1010</pressure>        
<horizon>Natural</horizon>        
</sighting>            
</fix>
        """
        dom = xml.dom.minidom.parseString(document)
        self.handleSightingLog(dom)
        return (self.approxLat.getString(),self.approxLong.getString())
        
        
    def handleSightingLog(self, slideshow):
#         self.handleSlideshowTitle(slideshow.getElementsByTagName("title")[0])
        sightings = slideshow.getElementsByTagName("sighting")
        for sighting in sightings:
            body = self.handleBody(sighting)
            date = self.handleDate(sighting)
            time = self.handleTime(sighting)
            obs = self.handleObservation(sighting)
            height = self.handleHeight(sighting)
            temp = self.handleTemperature(sighting)
            pressure = self.handlePressure(sighting)
            horz = self.handleHorizon(sighting)
            utc_datetime = datetime.datetime.utcnow()
            log_file = open(self.logFile, "a")
            angle = self.calculateAngle(height,temp,pressure,horz,obs)
            log_file.write("LOG\t")
            log_file.write(utc_datetime.strftime("%Y-%m-%d %H:%M:%S"))
            log_file.write("\t")
            log_file.write("-6:00 ")
            log_file.write(str(body))
            log_file.write("\t")
            log_file.write(str(date))
            log_file.write("\t")
            log_file.write(str(time))
            log_file.write("\t")
            log_file.write(str(angle))
            log_file.write("\n")

    def calculateAngle(self,height,temp,pressure,horz,obs):
        observation = Angle.Angle()
        observation.setDegreesAndMinutes(obs)
        observationAngle = observation.getDegrees()
        if horz == 'natural':
            dip = (-0.97 * math.sqrt(height))/60
        else:
            dip = 0
        refraction = (-0.00452*pressure)/(273+temp)/math.tan(height)
        adjustedAlt = round(observationAngle + dip + refraction,1)
        return adjustedAlt
        
    def handleBody(self,sighting):
        body = sighting.getElementsByTagName('body')[0]
        return self.getText(body.childNodes)
        
    def handleDate(self,sighting):
        date = sighting.getElementsByTagName('date')[0]
        return self.getText(date.childNodes)
        
    def handleTime(self,sighting):
        time = sighting.getElementsByTagName('time')[0]
        return self.getText(time.childNodes) 
            
    def handleObservation(self,sighting):
        obs = sighting.getElementsByTagName('observation')[0]
        return self.getText(obs.childNodes)
        
    def handleHeight(self,sighting):
        height = sighting.getElementsByTagName('height')[0]
        return self.getText(height.childNodes)  
                  
    def handleTemperature(self,sighting):
        temp = sighting.getElementsByTagName('temperature')[0]
        return self.getText(temp.childNodes)
        
    def handlePressure(self,sighting):
        pressure = sighting.getElementsByTagName('pressure')[0]
        return self.getText(pressure.childNodes)  
        
    def handleHorizon(self,sighting):
        horz = sighting.getElementsByTagName('horizon')[0]
        return self.getText(horz.childNodes)  
             
    def getText(self,nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)
