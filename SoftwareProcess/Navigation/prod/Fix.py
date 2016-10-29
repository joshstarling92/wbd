#Written by: Joshua Starling
#Imports

import os
import Angle
import XML_handler
import Sightings

class Fix():
    def __init__(self,logFile = None):
        self.classErrorName = 'Fix.' #used for error handling
        methodErrorName = '__init__:  ' #defined for error handling

        self.sightingFile = 'Null' #init sighting file so code can know if a file has already been opened
        
        #InitLogFile takes the given file input and will open and write start of log file 
        #as well as validate the file input
        try:
            self.initLogFile(logFile) 
        except ValueError as e:
            errmsg = self.classErrorName + methodErrorName + str(e)
            raise ValueError(errmsg)

    def setSightingFile(self, sightingFile = None):
        methodErrorName = 'setSightingFile:  ' #defined for error handling
        
        if sightingFile == None: #verify sighting file given
            errmsg = self.classErrorName + methodErrorName + 'No .xml file given'
            raise ValueError(errmsg)
        suffix = ".xml";
        if str(sightingFile) == sightingFile:
            if sightingFile.endswith(suffix):     #verify that sighting file has correct extension   
                if len(sightingFile)  <= 4:
                    errmsg = self.classErrorName + methodErrorName + 'Improper file extension length'
                    raise ValueError(errmsg)
                else:  
                    if os.path.isfile(sightingFile): #file already exist
                        self.sightingFile = sightingFile
                        self.writeStartOfSightingFile() #Write start of sighting file to log file
                        return str(self.sightingFile)
                    else:
                        errmsg = self.classErrorName + methodErrorName + 'Sighting file does not exist'
                        raise ValueError(errmsg) 
            else:
                errmsg = self.classErrorName + methodErrorName + 'Improper file extension used'
                raise ValueError(errmsg)
        else:
            errmsg = self.classErrorName + methodErrorName + 'Sighting file is not a string'
            raise ValueError(errmsg) 

        
    def getSightings(self):
        methodErrorName = 'getSightings:  ' #defined for error handling
        if self.sightingFile == 'Null': #if no sighting file was set, raise error
            errmsg = self.classErrorName + methodErrorName + 'No sighting file set'
            raise ValueError(errmsg) 
        
        #Parse .xml file and print information to log file
        sightingXML = XML_handler.XML_handler()
        log_file = open(self.logFile, "a")
        try:
            sightingsDic = sightingXML.handleSightingLog(self.sightingFile)

        except ValueError as e:
            errmsg = self.classErrorName + methodErrorName + str(e)
            raise ValueError(errmsg)
        if sightingsDic['Message'] == 'No sightings found':
            print 'No sightings found'
        else:
            for key in sightingsDic:
                if key != 'Message':
                    sightingDic = sightingsDic[str(key)]
                    sighting = Sightings.Sightings() 
                    angle = Angle.Angle()
                    angle.setDegrees(sighting.calculateAngle(sightingDic))
                    self.WriteSightingData(log_file,sightingDic['body'],sightingDic['date'],sightingDic['time'],angle.getString())
              
        #Write end of sighting information to log file
        log_file.write("End of sighting file ")
        log_file.write(self.sightingFile)
        log_file.write("\n")
        #return a lat and long
        self.approxLat = Angle.Angle() #constructs class and sets to default values of 0d0.0
        self.approxLong = Angle.Angle() #constructs class and sets to default values of 0d0.0
        return (self.approxLat.getString(),self.approxLong.getString()) #return values as a touple
   
    ######################################
    #########Log File Functions###########
    ######################################
    
    def initLogFile(self,textFile):
        if textFile == None: #if no log file given, make default
            try: #try for if by some reason, program can't open file
                default_text_file = open("log.txt", "a")
                self.writeStartOfLog(default_text_file)
                self.logFile = "log.txt"
            except:
                errorMesg = "Unable to open file. "
                raise ValueError(errorMesg) 
        else: #if user supplies a log file name, first verify extension then write to it
            if str(textFile) == textFile:
                suffix = ".txt";
                if textFile.endswith(suffix): #file has correct extension
                    try:  #try for if by some reason, program can't open file
                        text_file = open(textFile, "a")  
                        self.writeStartOfLog(text_file)  
                        self.logFile = textFile
                    except:
                        errorMesg = "Unable to open file. "
                        raise ValueError(errorMesg)                    
                else: #if file does not have proper extension
                    errmsg = 'Improper file extension used'
                    raise ValueError(errmsg)
            else:
                errmsg = "Given Text File is not a string"
                raise ValueError(errmsg)
            
    def writeStartOfLog(self,logfile):
        #basic function that will log the start of of the log file
#         utc_datetime = datetime.datetime.utcnow()
#         logfile.write("LOG:\t")
#         logfile.write(utc_datetime.strftime("%Y-%m-%d %H:%M:%S"))
#         logfile.write("-6:00\t")
        logfile.write("Start of log\n")
    
    def writeStartOfSightingFile(self):
        #Basic function to log the start of a sighting file
        log_file = open(self.logFile, "a")
#         utc_datetime = datetime.datetime.utcnow()
#         log_file.write("LOG:\t")
#         log_file.write(utc_datetime.strftime("%Y-%m-%d %H:%M:%S"))
#         log_file.write("-6:00\t")
        log_file.write("Start of sighting file: ")
        log_file.write(str(self.sightingFile))
        log_file.write("\n")
        
    def WriteSightingData(self,log_file,body,date,time,angle):
        #basic function that will log data from sighting
#         utc_datetime = datetime.datetime.utcnow()
        log_file.write("LOG:\t")
#         log_file.write(utc_datetime.strftime("%Y-%m-%d %H:%M:%S"))
#         log_file.write("-6:00\t")
        log_file.write(str(body))
        log_file.write("\t")
        log_file.write(str(date))
        log_file.write("\t")
        log_file.write(str(time))
        log_file.write("\t")
        log_file.write(str(angle))
        log_file.write("\n")
        