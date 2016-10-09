import datetime
import os
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
                    errorMesg = self.classErrorName + methodErrorName + "Unable to open file. "
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
                        errorMesg = self.classErrorName + methodErrorName + "Unable to open file. "
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
                text_file = open(self.logFile, "a")
                utc_datetime = datetime.datetime.utcnow()
                text_file.write("LOG " + utc_datetime.strftime("%Y-%m-%d %H:%M:%S") + "-6:00 "+ "Start of sighting file: " + str(sightingFile) + "\n")
                return True
            else:
                return False
        else:
            errmsg = self.classErrorName + methodErrorName + 'Improper file extension used'
            raise ValueError(errmsg)
        