#Written by: Joshua Starling
#Imports
import Angle
import XML_handler
import Sightings

#default imports
import os
import re
import datetime


class Fix():
    def __init__(self,logFile = None):
        self.classErrorName = 'Fix.' #used for error handling
        methodErrorName = '__init__:  ' #defined for error handling

        self.sightingFile = 'Null' #init sighting file so code can know if a file has already been opened
        self.ariesFile = 'Null'#init Aries file so code can know if a file has already been opened
        self.starFile = 'Null'#init Star file so code can know if a file has already been opened
        #InitLogFile takes the given file input and will open and write start of log file 
        #as well as validate the file input
        
        self.ErrorsFound = 0
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
                        utc_datetime = datetime.datetime.utcnow()
                        logfile = open(self.logFile, "a")  
                        logfile.write("LOG:\t")
                        logfile.write(utc_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                        logfile.write("-6:00:\t")
                        logfile.write("Sighting file:\t")
                        logfile.write(str(os.path.abspath(self.sightingFile)))
                        logfile.write("\n")
                        logfile.close()
                        return str(os.path.abspath(self.sightingFile))
                    else:
                        errmsg = self.classErrorName + methodErrorName + 'Sighting file does not exist'
                        raise ValueError(errmsg) 
            else:
                errmsg = self.classErrorName + methodErrorName + 'Improper file extension used'
                raise ValueError(errmsg)
        else:
            errmsg = self.classErrorName + methodErrorName + 'Sighting file is not a string'
            raise ValueError(errmsg) 

    def setAriesFile(self, ariesFile = None):
        methodErrorName = 'setAriesFile:  ' #defined for error handling
        
        if ariesFile == None: #verify sighting file given
            errmsg = self.classErrorName + methodErrorName + 'No Aries file given'
            raise ValueError(errmsg)
        suffix = ".txt";
        if str(ariesFile) == ariesFile:
            if ariesFile.endswith(suffix):     #verify that sighting file has correct extension   
                if len(ariesFile)  <= 4:
                    errmsg = self.classErrorName + methodErrorName + 'Improper file extension length'
                    raise ValueError(errmsg)
                else:  
                    if os.path.isfile(ariesFile): #file already exist
                        self.ariesFile = ariesFile
                        logfile = open(self.logFile, "a")  
                        utc_datetime = datetime.datetime.utcnow()
                        logfile.write("LOG:\t")
                        logfile.write(utc_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                        logfile.write("-6:00:\t")
                        logfile.write("Aries file:\t")
                        logfile.write(str(os.path.abspath(self.ariesFile)))
                        logfile.write("\n")
                        logfile.close()
                        try:
                            self.parseAriesFile()
                            return str(os.path.abspath(self.ariesFile))
                        except ValueError as e:
                            errmessg = self.classErrorName + methodErrorName + str(e)
                            raise ValueError(errmessg)
                    else:
                        errmsg = self.classErrorName + methodErrorName + 'Aries file does not exist'
                        raise ValueError(errmsg) 
            else:
                errmsg = self.classErrorName + methodErrorName + 'Improper file extension used'
                raise ValueError(errmsg)
        else:
            errmsg = self.classErrorName + methodErrorName + 'Aries file is not a string'
            raise ValueError(errmsg) 
         
    def setStarFile(self, starFile = None):
        methodErrorName = 'setStarFile:  ' #defined for error handling
        
        if starFile == None: #verify sighting file given
            errmsg = self.classErrorName + methodErrorName + 'No star file given'
            raise ValueError(errmsg)
        suffix = ".txt";
        if str(starFile) == starFile:
            if starFile.endswith(suffix):     #verify that sighting file has correct extension   
                if len(starFile)  <= 4:
                    errmsg = self.classErrorName + methodErrorName + 'Improper file extension length'
                    raise ValueError(errmsg)
                else:  
                    if os.path.isfile(starFile): #file already exist
                        self.starFile = starFile
                        logfile = open(self.logFile, "a")  
                        utc_datetime = datetime.datetime.utcnow()
                        logfile.write("LOG:\t")
                        logfile.write(utc_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                        logfile.write("-6:00:\t")
                        logfile.write("Star file:\t")
                        logfile.write(str(os.path.abspath(self.starFile)))
                        logfile.write("\n")
                        logfile.close()
                        try:
                            self.parseStarFile()
                            return str(os.path.abspath(self.starFile))
                        except ValueError as e:
                            errmessg = self.classErrorName + methodErrorName + str(e)
                            raise ValueError(errmessg)


                    else:
                        errmsg = self.classErrorName + methodErrorName + 'Star file does not exist'
                        raise ValueError(errmsg) 
            else:
                errmsg = self.classErrorName + methodErrorName + 'Improper file extension used'
                raise ValueError(errmsg)
        else:
            errmsg = self.classErrorName + methodErrorName + 'Star file is not a string'
            raise ValueError(errmsg)  
              
    def getSightings(self):
        methodErrorName = 'getSightings:  ' #defined for error handling
        if self.sightingFile == 'Null' or self.ariesFile == 'Null' or self.starFile == 'Null': 
            #if no sighting star or Aries file was set, raise error
            errmsg = self.classErrorName + methodErrorName + 'Sighting, Star, and Aries file must all be set before getSighting can be called'
            raise ValueError(errmsg) 
        
        #Parse .xml file and print information to log file
        sightingXML = XML_handler.XML_handler()
        try:
            sightingsDic = sightingXML.handleSightingLog(self.sightingFile)
        except ValueError as e:
            errmsg = self.classErrorName + methodErrorName + str(e)
            raise ValueError(errmsg)
        
        if sightingsDic['Message'] == 'No sightings found':
            print 'No sightings found'
        else:
            self.writeStartOfSightingFile() #Write start of sighting file to log file
            self.ErrorsFound =  sightingsDic['SightingError']
            for chronologicalBody in sightingsDic['bodyList']:
                sightingDic = sightingsDic[str(chronologicalBody)]
                doesStarExist = 0
                for i in range(0,len(self.starDayList)):
                    if self.starNameList[i] ==  sightingDic['body']:
                        doesStarExist = 1
                if sightingDic['Message'] == 'No error' and doesStarExist == 1:
                    sighting = Sightings.Sightings() 
                    obsAngle = Angle.Angle()
                    obsAngle.setDegrees(sighting.calculateAngle(sightingDic))
                    iterStar = self.findClosestStarTime(sightingDic['body'],sightingDic['date'],sightingDic['time'])
                    iterAries = self.findClosestAriesTime(sightingDic['date'],sightingDic['time'])
                    
                    geoLatPos = Angle.Angle()
                    geoLonPos = Angle.Angle()
                    geoLatLongPos = Sightings.Sightings()
                    geoLatPos.setDegrees(geoLatLongPos.calculateGeodedicLat(self.starLatList,iterStar))
                    geoLonPos.setDegrees(geoLatLongPos.calculateGeodedicLon(sightingDic,self.starLongList,self.ariesLongList,iterStar,iterAries))
                    self.WriteSightingData(sightingDic['body'],sightingDic['date'],sightingDic['time'],obsAngle.getString(),geoLonPos.getString(),geoLatPos.getString())

                else:
                    self.ErrorsFound = self.ErrorsFound + 1
                    sightingsDic['SightingError'] = self.ErrorsFound
                    
        utc_datetime = datetime.datetime.utcnow()
        log_file = open(self.logFile, "a")
        log_file.write("LOG:\tSightings Errors: ")
        log_file.write(utc_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        log_file.write("-6:00:\t")
        log_file.write(str(sightingsDic['SightingError']))
        log_file.write("\n")
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
                default_text_file.close()
                self.logFile = "log.txt"
                self.writeStartOfLog()
            except:
                errorMesg = "Unable to open file. "
                raise ValueError(errorMesg) 
        else: #if user supplies a log file name, first verify extension then write to it
            if str(textFile) == textFile:
                suffix = ".txt";
                if textFile.endswith(suffix): #file has correct extension
                    try:  #try for if by some reason, program can't open file
                        self.logFile = textFile
                        self.writeStartOfLog()  
                    except:
                        errorMesg = "Unable to open file. "
                        raise ValueError(errorMesg)                    
                else: #if file does not have proper extension
                    errmsg = 'Improper file extension used'
                    raise ValueError(errmsg)
            else:
                errmsg = "Given Text File is not a string"
                raise ValueError(errmsg)
            
    def writeStartOfLog(self):
        #basic function that will log the start of of the log file
        logfile = open(self.logFile, "a")  
        logfile.write("Start of log\n")
        utc_datetime = datetime.datetime.utcnow()
        logfile.write("LOG:\t")
        logfile.write(utc_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        logfile.write("-6:00:\t")
        logfile.write("Log file:\t")
        logfile.write(str(os.path.abspath(self.logFile)))
        logfile.write("\n")
        logfile.close()
        
    def writeStartOfSightingFile(self):
        #Basic function to log the start of a sighting file
        log_file = open(self.logFile, "a")
        utc_datetime = datetime.datetime.utcnow()
        log_file.write("LOG:\t")
        log_file.write(utc_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        log_file.write("-6:00\t")
        log_file.write("Start of sighting file: ")
        log_file.write(str(os.path.abspath(self.sightingFile)))
        log_file.write("\n")
        
    def WriteSightingData(self,body,date,time,obsAngle,lon,lat):
        #basic function that will log data from sighting
        utc_datetime = datetime.datetime.utcnow()
        log_file = open(self.logFile, "a")        
        log_file.write("LOG:\t")
        log_file.write(utc_datetime.strftime("%Y-%m-%d %H:%M:%S"))
        log_file.write("-6:00:\t")
        log_file.write(str(body))
        log_file.write("\t")
        log_file.write(str(date))
        log_file.write("\t")
        log_file.write(str(time))
        log_file.write("\t")
        log_file.write(str(obsAngle))
        log_file.write("\t")
        log_file.write(str(lon))
        log_file.write("\t")
        log_file.write(str(lat))
        log_file.write("\n")
        
        
    def parseAriesFile(self):
        theAriesFile = open(self.ariesFile, "r")
        ariesFileContents = theAriesFile.readlines()
        theAriesFile.close()
        self.ariesMonthList = [] 
        self.ariesDayList = []
        self.ariesYearList = []
        self.ariesHourList = []
        self.ariesLongList = []
        for AriesEntryNumber in range(0, len(ariesFileContents)):
            singleLine = str(ariesFileContents[AriesEntryNumber])
            singleLineEntry = re.split(r'\t+', singleLine)
            date = singleLineEntry[0]
            hourLineEntry = singleLineEntry[1]
            ariesLongLineEntry = singleLineEntry[2]
            try:
                month =  int(date[0:2])
                if month > 12 or month < 1:
                    errmsg = 'Month of an entry in Aries log is not correct'
                    raise ValueError(errmsg)
            except:
                errmsg = 'Month of an entry in Aries log is an integer or entry is not in the correct format'
                raise ValueError(errmsg)  
            self.ariesMonthList.append(month)
            
            try:
                day = int(date[3:5])
                if day > 31 or day < 1:
                    errmsg = 'Day of an entry in Aries log is not correct'
                    raise ValueError(errmsg)
            except:
                errmsg = 'Day of an entry in Aries log is an integer or entry is not in the correct format'
                raise ValueError(errmsg) 
            self.ariesDayList.append(day)
            
            try:
                year = int(date[6:8])
                if year > 99 or year < 0:
                    errmsg = 'Year of an entry in Aries log is not correct'
                    raise ValueError(errmsg)
            except:
                errmsg = 'Year of an entry in Aries log is an integer or entry is not in the correct format'
                raise ValueError(errmsg) 
            self.ariesYearList.append(year)
            
            try:
                hour = int(hourLineEntry)
                if hour > 23 or hour < 0:
                    errmsg = 'Hour of an entry in Aries log is not correct'
                    raise ValueError(errmsg)
            except:
                errmsg = 'Hour of an entry in Aries log is an integer or entry is not in the correct format'
                raise ValueError(errmsg) 
            self.ariesHourList.append(hour)
            
            try:
                ariesLong = ariesLongLineEntry
                ariesAngle = Angle.Angle()
                ariesAngle.setDegreesAndMinutes(ariesLong)
            except:
                errmsg = 'Longitude of first point of Aries of an entry in Aries log is not correct'
                raise ValueError(errmsg)      
            self.ariesLongList.append(ariesAngle.getDegrees())

    def parseStarFile(self):
        theStarFile = open(self.starFile, "r")
        starFileContents = theStarFile.readlines()
        theStarFile.close()
        self.starNameList = [] 
        self.starDayList = []
        self.starMonthList = []
        self.starYearList = []
        self.starLatList = []
        self.starLongList = []
        
        for StarEntryNumber in range(0, len(starFileContents)):
            singleLine = str(starFileContents[StarEntryNumber])
            singleLineEntry = re.split(r'\t+', singleLine)
            name = singleLineEntry[0]
            date = singleLineEntry[1]
            starLong = singleLineEntry[2]
            starLat = singleLineEntry[3]

            self.starNameList.append(name)
            try:
                month =  int(date[0:2])
                if month > 12 or month < 1:
                    errmsg = 'Month of an entry in star log is not correct'
                    raise ValueError(errmsg)
            except:
                errmsg = 'Month of an entry in star log is an integer or entry is not in the correct format'
                raise ValueError(errmsg)  
            self.starMonthList.append(month)
            
            try:
                day = int(date[3:5])
                if day > 31 or day < 1:
                    errmsg = 'Day of an entry in star log is not correct'
                    raise ValueError(errmsg)
            except:
                errmsg = 'Day of an entry in star log is an integer or entry is not in the correct format'
                raise ValueError(errmsg) 
            self.starDayList.append(day)
            
            try:
                year = int(date[6:8])
                if year > 99 or year < 0:
                    errmsg = 'Year of an entry in star log is not correct'
                    raise ValueError(errmsg)
            except:
                errmsg = 'Year of an entry in star log is an integer or entry is not in the correct format'
                raise ValueError(errmsg) 
            self.starYearList.append(year)
            
            try:
                angleStarLat = Angle.Angle()
                angleStarLat.setDegreesAndMinutes(starLat)
            except:
                errmsg = 'Latitude of first point of Aries of an entry in star log is not correct'
                raise ValueError(errmsg)      
            self.starLatList.append(angleStarLat.getDegrees())
            
            try:
                angleStarLon = Angle.Angle()
                angleStarLon.setDegreesAndMinutes(starLong)
            except:
                errmsg = 'Longitude of first point of Aries of an entry in star log is not correct'
                raise ValueError(errmsg)      
            self.starLongList.append(angleStarLon.getDegrees())
            

    def findClosestAriesTime(self,date,time):
        month =  int(date[5:7])
        day =  int(date[8:10])
        hour =  int(time[0:2])
        minute =  int(time[3:5])
        sec =  int(time[6:8])
        sightingTime = (sec + minute*60 + hour*60**2 + day*24*60**2 + ((float(month)/12.0))*365*24*60**2)
        minVal = 10000
        minLoc = 10000000000
        for i in range(0,len(self.ariesDayList)):
            ariesListTime = (self.ariesHourList[i]*60**2 + self.ariesDayList[i]*24*60**2 + ((float(self.ariesMonthList[i])/12.0))*365*24*60**2)
            difference = abs(ariesListTime - sightingTime)
            if difference < minVal:
                minVal = difference
                minLoc = i
        return minLoc
    
    
    def findClosestStarTime(self,body,date,time):
        month =  int(date[5:7])
        day =  int(date[8:10])
        sightingTime = (day*24*60**2 + (float(month)/12.0)*365*24*60**2)
        minVal = 100000000
        minLoc = len(self.starDayList)
        for i in range(0,len(self.starDayList)):
            starListTime = (self.starDayList[i]*24*60**2 + (float(self.starMonthList[i])/12.0)*365*24*60**2)
            difference = abs(starListTime - sightingTime)
            if difference < minVal and body == self.starNameList[i]:
                minVal = difference
                minLoc = i
        if minVal == 0:
            return minLoc
        else:
            return minLoc - 1
            

            
        
            
            
            