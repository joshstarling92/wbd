import unittest
import uuid
import os
import Navigation.prod.Fix as Fix

 
class TestFix(unittest.TestCase):
     
    def setUp(self):
        self.className = "Fix."
        self.logStartString = "Start of log"
        self.logSightingString = "Start of sighting file"
        self.absolutePath =  '/Users/Josh/git/SoftwareProcess/SoftwareProcess/Navigation/test/'
         
        # set default log file name
        self.DEFAULT_LOG_FILE = '/Users/Josh/git/SoftwareProcess/SoftwareProcess/Navigation/test'+"log.txt"
        if(os.path.isfile(self.DEFAULT_LOG_FILE)):
            os.remove(self.DEFAULT_LOG_FILE)
             
        # generate random log file name
        self.RANDOM_LOG_FILE = "log" + str(uuid.uuid4())[-12:] + ".txt"
         
         
    def test100_010_ShouldWriteLogFileWithAbsPathAndReturnFile(self):
#         testFile = "CA02_300_ValidOneStarArtificialHorizon.xml"
        theFix = Fix.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile('CA02_300_GenericValidStarSightingFile.xml')
        targetStringList = '/Users/Josh/git/SoftwareProcess/SoftwareProcess/Navigation/test/'+str(self.RANDOM_LOG_FILE)
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        theLogFile.close()
        self.assertEquals(targetStringList, targetStringList) 
        self.cleanup() 
        
    def test100_020_ShouldWriteSightingFileWithAbsPathAndReturnFile(self):
        theFix = Fix.Fix(self.RANDOM_LOG_FILE)
        returnValue = theFix.setSightingFile('CA02_300_GenericValidStarSightingFile.xml')
        targetStringList = '/Users/Josh/git/SoftwareProcess/SoftwareProcess/Navigation/test/CA02_300_GenericValidStarSightingFile.xml'
        self.assertEquals(returnValue, targetStringList) 
        self.cleanup()
         
         
    def test100_030_ShouldWriteStarFileWithAbsPathAndReturnFile(self):
        testFile = "exampleXML.xml"
        targetStringList = '/Users/Josh/git/SoftwareProcess/SoftwareProcess/Navigation/test/'+'stars.txt'
        theFix = Fix.Fix(self.RANDOM_LOG_FILE)
        returnValue = theFix.setStarFile('stars.txt')
        theFix.setSightingFile(testFile)

        self.assertEquals(returnValue, targetStringList) 

        self.cleanup() 
         
         
    def test100_040_ShouldWriteAriesFileWithAbsPathAndReturnFile(self):
        testFile = "exampleXML.xml"
        targetStringList = '/Users/Josh/git/SoftwareProcess/SoftwareProcess/Navigation/test/'+'aries.txt'
        theFix = Fix.Fix(self.RANDOM_LOG_FILE)
        theFix.setStarFile('stars.txt')
        returnValue = theFix.setAriesFile('aries.txt')
        theFix.setSightingFile(testFile)

        self.assertEquals(returnValue, targetStringList) 

        self.cleanup() 
        
        
    def test900_100_ShouldRaiseErrorAriesFileYearIsMissingYMorD(self): 
        expectedString = "Fix.setAriesFile:  Month of an entry in Aries log is an integer or entry is not in the correct format"
        with self.assertRaises(ValueError) as context:
            theFix = Fix.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile('exampleXML.xml')
            theFix.setStarFile('stars.txt')
            theFix.setAriesFile('ariesInvalidDate.txt')        
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
    def test900_110_ShouldRaiseErrorAriesFileYearIsMissingslashes(self):     
        expectedString = "Fix.setAriesFile:  Year of an entry in Aries log is an integer or entry is not in the correct format"
        with self.assertRaises(ValueError) as context:
            theFix = Fix.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile('exampleXML.xml')
            theFix.setStarFile('stars.txt')
            theFix.setAriesFile('AriesNoSlashses.txt')   
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
    def test900_120_ShouldRaiseErrorAriesFileHourIsntNum(self):     
        expectedString = "Fix.setAriesFile:  Hour of an entry in Aries log is an integer or entry is not in the correct format"
        with self.assertRaises(ValueError) as context:
            theFix = Fix.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile('exampleXML.xml')
            theFix.setStarFile('stars.txt')
            theFix.setAriesFile('ariesBadHour.txt')   
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
    def test900_130_ShouldRaiseErrorAriesFileAngleIsntValid(self):        
        expectedString = "Fix.setAriesFile:  Longitude of first point of Aries of an entry in Aries log is not correct"
        with self.assertRaises(ValueError) as context:
            theFix = Fix.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile('exampleXML.xml')
            theFix.setStarFile('stars.txt')
            theFix.setAriesFile('ariesBadAngle.txt')   
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        


    def test900_140_ShouldRaiseErrorAriesFileMonthNotInRange(self):   
        expectedString = "Fix.setAriesFile:  Day of an entry in Aries log is an integer or entry is not in the correct"
        with self.assertRaises(ValueError) as context:
            theFix = Fix.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile('exampleXML.xml')
            theFix.setStarFile('stars.txt')
            theFix.setAriesFile('ariesBadDayRange.txt')   
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
         

    def test900_180_ShouldRaiseErrorAriesFileNotLongEnough(self):
        expectedString = "Fix.setAriesFile:  Improper file extension length"
        with self.assertRaises(ValueError) as context:
            theFix = Fix.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile('exampleXML.xml')
            theFix.setStarFile('stars.txt')
            theFix.setAriesFile('.txt')   
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 

    def test900_190_ShouldRaiseErrorAriesFileNotHaveCorrectExt(self):
        expectedString = "Fix.setAriesFile:  Improper file extension used"
        with self.assertRaises(ValueError) as context:
            theFix = Fix.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile('exampleXML.xml')
            theFix.setStarFile('stars.txt')
            theFix.setAriesFile('aries.tx')   
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])     
# 
    def test200_010_ShouldWriteToLogPathToStarVisuallyChecked(self):
        testFile = "CA02_300_ValidOneStarArtificialHorizon.xml"
        with self.assertRaises(ValueError):
            theFix = Fix.Fix(self.RANDOM_LOG_FILE)
            theFix.setStarFile('stars.txt')
            theFix.setAriesFile('aries.tx') 
            theFix.setSightingFile(testFile)
            theFix.getSightings()
           
        self.assertEquals(1, 1)
        self.cleanup() 
#         
    def test900_200_ShouldRaiseErrorStarFileYearIsMissingYMorD(self): 
        expectedString = "Fix.setStarFile:  Day of an entry in star log is an integer or entry is not in the correct format"
        with self.assertRaises(ValueError) as context:
            theFix = Fix.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile('exampleXML.xml')
            theFix.setStarFile('starMissingDateValue.txt')
            theFix.setAriesFile('aries.txt')   
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
        
    def test900_210_ShouldRaiseErrorStarFileYearIsMissingslashes(self):  
        expectedString = "Fix.setStarFile:  Day of an entry in star log is an integer or entry is not in the correct format"
        with self.assertRaises(ValueError) as context:
            theFix = Fix.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile('exampleXML.xml')
            theFix.setStarFile('starMissingMissingSlashes.txt')
            theFix.setAriesFile('aries.txt')   
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])    
        
    def test900_220_ShouldRaiseErrorStarFileHourIsntNum(self): 
        expectedString = "Fix.setStarFile:  Day of an entry in star log is an integer or entry is not in the correct format"
        with self.assertRaises(ValueError) as context:
            theFix = Fix.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile('exampleXML.xml')
            theFix.setStarFile('starHourIsntNumber.txt')
            theFix.setAriesFile('aries.txt')   
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])     


    def test900_292_ShouldRaiseErrorStarFileNotHaveCorrectExt(self):
        expectedString = "Fix.setStarFile:  Improper file extension used"
        with self.assertRaises(ValueError) as context:
            theFix = Fix.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile('exampleXML.xml')
            theFix.setStarFile('starHourIsntNumber.tx')
            theFix.setAriesFile('aries.txt')   
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])   
 
 
    def test300_010_ShouldWriteToLogLatVisuallyChecked(self):
        testFile = "CA02_300_ValidOneStarArtificialHorizon.xml"
        with self.assertRaises(ValueError):
            theFix = Fix.Fix(self.RANDOM_LOG_FILE)
            theFix.setStarFile('stars.txt')
            theFix.setAriesFile('aries.tx') 
            theFix.setSightingFile(testFile)
            theFix.getSightings()
           
        self.assertEquals(1, 1)
        self.cleanup()    
        
    def test300_020_ShouldWriteToLogLonVisuallyChecked(self):
        testFile = "CA02_300_ValidOneStarArtificialHorizon.xml"
        with self.assertRaises(ValueError):
            theFix = Fix.Fix(self.RANDOM_LOG_FILE)
            theFix.setStarFile('stars.txt')
            theFix.setAriesFile('aries.tx') 
            theFix.setSightingFile(testFile)
            theFix.getSightings()
           
        self.assertEquals(1, 1)
        self.cleanup() 
                    
    def test900_300_ShouldRaiseErrorIfSightingFileNotGiven(self):
        expectedString = "Fix.getSightings:  Sighting, Star, and Aries file must all be set before getSighting can be called"
        with self.assertRaises(ValueError) as context:
            theFix = Fix.Fix(self.RANDOM_LOG_FILE)
            theFix.setStarFile('stars.txt')
            theFix.setAriesFile('aries.txt') 

            theFix.getSightings()
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
         
    def test900_310_ShouldRaiseErrorIfStarFileNotGiven(self):
        expectedString = "Fix.getSightings:  Sighting, Star, and Aries file must all be set before getSighting can be called"
        with self.assertRaises(ValueError) as context:
            theFix = Fix.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile('CA02_300_GenericValidStarSightingFile.xml')
            theFix.setAriesFile('aries.txt') 

            theFix.getSightings()
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])    
        
    def test900_320_ShouldRaiseErrorIfAriesFileNotGiven(self):
        expectedString = "Fix.getSightings:  Sighting, Star, and Aries file must all be set before getSighting can be called"
        with self.assertRaises(ValueError) as context:
            theFix = Fix.Fix()
            theFix.setSightingFile('CA02_300_GenericValidStarSightingFile.xml')
            theFix.setStarFile('stars.txt')

            theFix.getSightings()
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])  
        
    def test900_400_ShouldPrintAllDataInLog_FinalCheck(self):
        with self.assertRaises(ValueError):
            theFix = Fix.Fix('FinalLog.txt')
            theFix.setSightingFile('example.xml')
            theFix.setStarFile('stars.txt')
            theFix.setAriesFile('aries.txt') 
            theFix.getSightings()
            
        self.assertEquals(1,1)  
           
        
#  helper methods
    def indexInList(self, target, searchList):
        for index in range(len(searchList)):
            if(target in searchList[index]):
                return index
        return -1
     
    def cleanup(self):
        if(os.path.isfile(self.RANDOM_LOG_FILE)):
            os.remove(self.RANDOM_LOG_FILE)  