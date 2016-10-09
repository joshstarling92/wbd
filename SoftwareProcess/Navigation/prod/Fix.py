import datetime
import os
class Fix():
    def __init__(self,textFile = None):
        self.classErrorName = 'Fix.'
        methodErrorName = '__init__:  ' #defined for error handling
        if textFile == None:
            if os.path.isfile("log.txt"):
                text_file = open("log.txt", "a")
            else:
                text_file = open("log.txt", "w")
        else:
            suffix = ".txt";
            if textFile.endswith(suffix):
                if os.path.isfile(textFile):
                    text_file = open(textFile, "a")
                else:
                    text_file = open(textFile, "w")            
            else:
                errmsg = self.classErrorName + methodErrorName + 'Improper file extension used'
                raise ValueError(errmsg)
        utc_datetime = datetime.datetime.utcnow()
        text_file.write("LOG " + utc_datetime.strftime("%Y-%m-%d %H:%M:%S") + "-6:00 "+ "Start of Log\n")    
        text_file.close()
        
        