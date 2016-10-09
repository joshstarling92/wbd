import time
class Fix():
    def __init__(self,txtFile = None):
        self.classErrorName = 'Fix.'
        methodErrorName = '__init__:  ' #defined for error handling
        if txtFile == None:
            text_file = open("log.txt", "w")
        else:
            suffix = ".txt";
            if txtFile.endswith(suffix):
                text_file = open(txtFile, "w")
            else:
                errmsg = self.classErrorName + methodErrorName + 'Improper file extension used'
                raise ValueError(errmsg)
        text_file.write("LOG " + str(time.strftime("%Y/%m/%d")))    
        text_file.close()
        
        