#Written by: Joshua Starling
#Imports
import datetime
import os
import Angle
from xml.dom.minidom import parse
import math

class Fix():
    def __init__(self,textFile = None):
        self.classErrorName = 'Fix.' #used for error handling
        methodErrorName = '__init__:  ' #defined for error handling

        self.sightingFile = 'Null' #init sighting file so code can know if a file has already been opened
        
        #InitLogFile takes the given file input and will open and write start of log file 
        #as well as validate the file input
        try:
            self.initLogFile(textFile) 
        except ValueError as e:
            errmsg = self.classErrorName + methodErrorName + str(e)
            raise ValueError(errmsg)

    def setSightingFile(self, sightingFile = None):
        methodErrorName = 'setSightingFile:  ' #defined for error handling
        
        if sightingFile == None: #verify sighting file given
            errmsg = self.classErrorName + methodErrorName + 'No .xml file given'
            raise ValueError(errmsg)
        
        suffix = ".xml";
        if sightingFile.endswith(suffix):     #verify that sighting file has correct extension            
            self.sightingFile = sightingFile
            return str(self.sightingFile)
        else:
            errmsg = self.classErrorName + methodErrorName + 'Improper file extension used'
            raise ValueError(errmsg)
        
    def getSightings(self):
        methodErrorName = 'getSightings:  ' #defined for error handling
        if self.sightingFile == 'Null': #if no sighting file was set, raise error
            errmsg = self.classErrorName + methodErrorName + 'No sighting file set'
            raise ValueError(errmsg) 
        
        self.writeStartOfSightingFile() #Write start of sighting file to log file
        #Parse .xml file and print information to log file
        dom = parse(self.sightingFile)  # parse an open file
        try:
            self.handleSightingLog(dom)
        except ValueError as e:
            errmsg = self.classErrorName + methodErrorName + str(e)
            raise ValueError(errmsg)
        
        #return a lat and long
        self.approxLat = Angle.Angle() #constructs class and sets to default values of 0d0.0
        self.approxLong = Angle.Angle() #constructs class and sets to default values of 0d0.0
        return (self.approxLat.getString(),self.approxLong.getString()) #return values as a touple
        

    def calculateAngle(self,height,temp,pressure,horz,obs):
        #function that calculates corrected observation angle 
        observation = Angle.Angle()
        observation.setDegreesAndMinutes(obs) #using the functionality of Angle class, use the given string and convert to a number
        observationAngle = observation.getRadians()
#         if observationAngle < 1.0/60/180*3.14:
#             errmsg = 'Observed altitude less than 0.1 arc-minute'
#             raise ValueError(errmsg)
        
        #calculate correction
        if horz == 'natural':
            dip = (-0.97 * math.sqrt(height))/60
        else:
            dip = 0
        refraction = ((-0.00452*pressure)/(273+(temp-32)*5.0/9.0))/math.tan(observationAngle)
        adjustedAlt = round((observationAngle + dip + refraction)*180/3.14,1)
        return adjustedAlt
    
    ######################################
    ########XML Parse Functions###########
    ######################################

    def handleSightingLog(self, sightingDOM):
        #function that takes entire xml file and parses it and searches through
        #each sighting and get at least the mandatory data and any optional data
        log_file = open(self.logFile, "a") 
        sightings = sightingDOM.getElementsByTagName("sighting") #get range of all sightings in file
        orderedSightings = self.getChronologicalOrder(sightings)
        for sighting in orderedSightings:
            
            try: #get all mandatory data, failure to do so will raise error
                body = self.handleBody(sighting)
                date = self.handleDate(sighting)
                time = self.handleTime(sighting)
                obs = self.handleObservation(sighting)
            except ValueError as e:
                raise ValueError(e)
    
            #Get all  non-mandatory data
            height = float(self.handleHeight(sighting))
            temp = float(self.handleTemperature(sighting))
            pressure = float(self.handlePressure(sighting))
            horz = self.handleHorizon(sighting)
            
            try:#Calculate corrected angle
                angle = self.calculateAngle(height,temp,pressure,horz,obs)
            except ValueError as e:
                raise ValueError(e)
            
            #Write data to log file
            self.WriteSightingData(log_file,body,date,time,angle)
            
        #Write end of sighting information to log file
        log_file.write("End of sighting file ")
        log_file.write(self.sightingFile)
        log_file.write("\n")
    
    def getChronologicalOrder(self,sightingsList):
        timeInSecOfSighting = [] #make empty list
        for sighting in sightingsList:
            try: #get time and data tags, failure to do so will raise error
                date = self.handleDate(sighting)
                time = self.handleTime(sighting)
            except ValueError as e:
                raise ValueError(e)
            #convert both strings into their individual components
            year = int(date[0:4])
            month =  int(date[5:7])
            day =  int(date[8:10])
            hour =  int(time[0:2])
            minute =  int(time[3:5])
            sec =  int(time[6:8])
            
            #take components and converts to a single numerical value that can be used to sort
            timeInSecOfSighting.append(sec + minute*60 + hour*60**2 + day*24*60**2 + (year+(month/12.0))*365*24*60**2)
        #takes sightings dom list and timeInSecOfSighting list and places each element into tuples respectivly, using zip
        #the list of touples are then sorted by timeInSecOfSighting and uncoupled back to their respective lists
        TupleListOfTimeAndSightings = zip(timeInSecOfSighting, sightingsList) #combines into on list
        sortedTupleList = sorted(TupleListOfTimeAndSightings) #sorts list
        sortedTimeList, sortedSightings = (list(t) for t in zip(*sortedTupleList)) #unsorts list and saves as individual list again
        return sortedSightings
            
            
    ###########Mandatory Tags###########
    #######Raises error if not given
    def handleBody(self,sighting):
        try:
            body = sighting.getElementsByTagName('body')[0]
            return self.getText(body.childNodes)
        except:
            errmsg = 'Mandatory Tag "Body" missing'
            raise ValueError(errmsg) 
           
    def handleDate(self,sighting):
        try:
            date = sighting.getElementsByTagName('date')[0]
            return self.getText(date.childNodes)
        except:
            errmsg = 'Mandatory Tag "Date" missing'
            raise ValueError(errmsg)    
        
    def handleTime(self,sighting):
        try:
            time = sighting.getElementsByTagName('time')[0]
            return self.getText(time.childNodes) 
        except:
            errmsg = 'Mandatory Tag "Time" missing'
            raise ValueError(errmsg)           
            
    def handleObservation(self,sighting):
        try:
            obs = sighting.getElementsByTagName('observation')[0]
            return self.getText(obs.childNodes)
        except:
            errmsg = 'Mandatory Tag "Observation" missing'
            raise ValueError(errmsg)
    ###########Non-mandatory Tags###########
    #######Uses default values if not given
    def handleHeight(self,sighting):
        try:
            heightStr = sighting.getElementsByTagName('height')[0]
            height =  self.getText(heightStr.childNodes)
            if height == '':
                return 0
            else:
                return height    
        except:
            return 0
                  
    def handleTemperature(self,sighting):
        try:
            tempStr = sighting.getElementsByTagName('temperature')[0]
            temp = self.getText(tempStr.childNodes)
            if temp == '':
                return 72
            else:
                return temp   
        except:
            return 72
        
    def handlePressure(self,sighting):
        try:
            pressureStr = sighting.getElementsByTagName('pressure')[0]
            pressure = self.getText(pressureStr.childNodes)
            if pressure == '':
                return 1010
            else:
                return pressure  
        except:
            return 1010
        
    def handleHorizon(self,sighting):
        try:
            horzStr = sighting.getElementsByTagName('horizon')[0]
            horz  = self.getText(horzStr.childNodes)  
            if horz == '':
                return 'natural'
            else:
                return horz  
        except:
            return 'natural' 

    #Function to read lowest level tag
    def getText(self,nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)
    
    ######################################
    #########Log File Functions###########
    ######################################
    
    def initLogFile(self,textFile):
        if textFile == None: #if no log file given, make default
            if os.path.isfile("log.txt"): #file already exist
                self.logFile = "log.txt"
                text_file = open("log.txt", "a")
            else: #file doesn't already exist
                try: #try for if by some reason, program can't open file
                    text_file = open("log.txt", "w")
                    self.writeStartOfLog(text_file)
                except:
                    errorMesg = "Unable to open file. "
                    raise ValueError(errorMesg) 
        else: #if user supplies a log file name, first verify extension then write to it
            suffix = ".txt";
            if textFile.endswith(suffix): #file has correct extension
                if os.path.isfile(textFile):
                    self.logFile = textFile
                    text_file = open(textFile, "a")
                else:
                    try:  #try for if by some reason, program can't open file
                        self.logFile = textFile
                        text_file = open(textFile, "w")  
                        self.writeStartOfLog(text_file)  
                    except:
                        errorMesg = "Unable to open file. "
                        raise ValueError(errorMesg)                    
            else: #if file does not have proper extension
                errmsg = 'Improper file extension used'
                raise ValueError(errmsg)
            
    def writeStartOfLog(self,logfile):
        #basic function that will log the start of of the log file
        utc_datetime = datetime.datetime.utcnow()
        logfile.write("LOG:\t")
        logfile.write(utc_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        logfile.write("-6:00\t")
        logfile.write("Start of Log\n")
    
    def writeStartOfSightingFile(self):
        #Basic function to log the start of a sighting file
        log_file = open(self.logFile, "a")
        utc_datetime = datetime.datetime.utcnow()
        log_file.write("LOG:\t")
        log_file.write(utc_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        log_file.write("-6:00\t")
        log_file.write("Start of sighting file: ")
        log_file.write(str(self.sightingFile))
        log_file.write("\n")
        
    def WriteSightingData(self,log_file,body,date,time,angle):
        #basic function that will log data from sighting
        utc_datetime = datetime.datetime.utcnow()
        log_file.write("LOG:\t")
        log_file.write(utc_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        log_file.write("-6:00\t")
        log_file.write(str(body))
        log_file.write("\t")
        log_file.write(str(date))
        log_file.write("\t")
        log_file.write(str(time))
        log_file.write("\t")
        log_file.write(str(angle))
        log_file.write("\n")
        