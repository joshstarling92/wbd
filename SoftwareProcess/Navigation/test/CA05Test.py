import unittest
import uuid
import os
import Navigation.prod.Fix as F
 
class TestFix(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.className = "Fix."
        cls.logStartString = "Log file:"
        cls.starSightingString = "Sighting file:"
        cls.starSightingErrorString = "Sighting errors:"
        cls.ariesFileString = "Aries file:"
        cls.starFileString = "Star file:"
        cls.DEFAULT_LOG_FILE = "log.txt"
        cls.ariesFileName = "CA03_Valid_Aries.txt"
        cls.starFileName = "CA03_Valid_Stars.txt"
        cls.testToFileMap = [
            ["validStarSightingFile", "CA02_200_ValidStarSightingFile.xml"],
            ["validAriesFile", "CA03_Valid_Aries.txt"],           
            ["validStarFile", "CA03_Valid_Stars.txt"], 
            ["genericValidStarSightingFile", "CA02_300_GenericValidStarSightingFile.xml"], 
            ["genericValidSightingFileWithMixedIndentation", "CA02_300_ValidWithMixedIndentation.xml"],
            ["validOneStarSighting", "CA02_300_ValidOneStarSighting.xml"],
            ["validMultipleStarSighting", "CA02_300_ValidMultipleStarSighting.xml"],
            ["validMultipleStarSightingSameDateTime", "CA02_300_ValidMultipleStarSightingSameDateTime.xml"],
            ["validWithNoSightings", "CA02_300_ValidWithNoSightings.xml"],
            ["validWithExtraneousTags", "CA02_300_ValidWithExtraneousTags.xml"],
            ["validOneStarNaturalHorizon","CA02_300_ValidOneStarNaturalHorizon.xml"],
            ["validOneStarArtificialHorizon", "CA02_300_ValidOneStarArtificialHorizon.xml"],
            ["validOneStarWithDefaultValues", "CA02_300_ValidOneStarWithDefaultValues.xml"],
            ["invalidWithMissingMandatoryTags","CA02_300_InvalidWithMissingMandatoryTags.xml"],
            ["invalidBodyTag","CA02_300_InvalidBody.xml"],
            ["invalidDateTag","CA02_300_InvalidDate.xml"],
            ["invalidTimeTag","CA02_300_InvalidTime.xml"],
            ["invalidObservationTag","CA02_300_InvalidObservation.xml"],
            ["invalidHeightTag","CA02_300_InvalidHeight.xml"],
            ["invalidTemperatureTag", "CA02_300_InvalidTemperature.xml"],
            ["invalidPressureTag","CA02_300_InvalidPressure.xml"],
            ["invalidHorizonTag","CA02_300_InvalidHorizon.xml"],
            ["validLatLon", "CA03_300_ValidStarLatLon.xml"],
            ["validLatLonInterpolated", "CA03_300_ValidStarLatLonInterpolationRequired.xml"]
            ]  

#----------          
    def setUp(self):
        if(os.path.isfile(self.DEFAULT_LOG_FILE)):
            os.remove(self.DEFAULT_LOG_FILE) 
        # generate random log file name
        self.RANDOM_LOG_FILE = "log" + str(uuid.uuid4())[-12:] + ".txt"
        self.deleteNamedLogFlag = False
    
    def tearDown(self):
        if(self.deleteNamedLogFlag):
            try:
                if(os.path.isfile(self.RANDOM_LOG_FILE)):
                    os.remove(self.RANDOM_LOG_FILE)  
            except:
                pass
         
    def test100_010_NoInputGivenShouldUseDefaults(self):
        'log geographical position'
        targetStringList = ["Acrux", None, None, None, "0d0.0", "0d0.0"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile('CA05_StarSighting.xml')
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings()
         
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
         
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    if(target != None):
                        self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major: Assume LL entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True  
         
    def test100_020_InputsGivenShouldWriteToTextFile(self):
        'log geographical position'
        targetStringList = ["Acrux", None, None, None, "S30d0.0", "23d30.0"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile('CA05_StarSighting.xml')
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings('S30d00.0','23d30.0')
          
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
          
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    if(target != None):
                        self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major: Assume LL entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True 
#     
    def test900_030_InputNotInAngleFormatShouldRaiseError(self):   
        expectedString = "Fix.getSightings:  Latitude not in correct format"
        with self.assertRaises(ValueError) as context:
            theFix = F.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile('CA05_StarSighting.xml')
            theFix.setAriesFile(self.ariesFileName)   
            theFix.setStarFile(self.starFileName)
            theFix.getSightings('Naldsfj','23d30.0')  
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
#         
    def test900_050_InputOutOfBoundsShouldRaiseError(self):   
        expectedString = "Fix.getSightings:  Latitude is not in correct range"
        with self.assertRaises(ValueError) as context:
            theFix = F.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile('CA05_StarSighting.xml')
            theFix.setAriesFile(self.ariesFileName)   
            theFix.setStarFile(self.starFileName)
            theFix.getSightings('N300d0.0','230d30.0')  
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])  
          
    def test900_060_InputOutOfBoundsShouldRaiseError(self):   
        expectedString = "Fix.getSightings:  Longitude is not in correct range"
        with self.assertRaises(ValueError) as context:
            theFix = F.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile('CA05_StarSighting.xml')
            theFix.setAriesFile(self.ariesFileName)   
            theFix.setStarFile(self.starFileName)
            theFix.getSightings('N30d0.0','2030d30.0')  
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
           
    def test900_070_GivenNonNSwithNonZeroLatitudeShouldRaiseError(self):
        expectedString = "Fix.getSightings:  Latitude must be zero to not have N or S"
        with self.assertRaises(ValueError) as context:
            theFix = F.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile('CA05_StarSighting.xml')
            theFix.setAriesFile(self.ariesFileName)   
            theFix.setStarFile(self.starFileName)
            theFix.getSightings('4d0.0','3d0.0')  
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
         
    def test900_070_GivenQinsteadofNorSShouldRaiseError(self):
        expectedString = "Fix.getSightings:  Latitude not in correct format"
        with self.assertRaises(ValueError) as context:
            theFix = F.Fix(self.RANDOM_LOG_FILE)
            theFix.setSightingFile('CA05_StarSighting.xml')
            theFix.setAriesFile(self.ariesFileName)   
            theFix.setStarFile(self.starFileName)
            theFix.getSightings('Q3d0.0','3d0.0')  
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])  
          
    def test100_070_ValidSightingsShouldWriteApproxLL(self):   
        'log geographical position'
        targetStringList = ["Approximate latitude", "S13d28.1", "Approximate longitude", "101d43.0"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile('CA05_StarSighting.xml')
        theFix.setAriesFile(self.ariesFileName)   
        theFix.setStarFile(self.starFileName)
        theFix.getSightings('S53d38.4','74d35.3')
 
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
         
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    if(target != None):
                        self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major: Approx LL entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True   
#  helper methods
    def indexInList(self, target, searchList):
        for index in range(len(searchList)):
            if(target in searchList[index]):
                return index
        return -1
     
    def cleanup(self):
        if(os.path.isfile(self.RANDOM_LOG_FILE)):
            os.remove(self.RANDOM_LOG_FILE)  
    
    def mapFileToTest(self, target):
        for item in self.testToFileMap:
            if(item[0] == target):
                return item[1]
        return None
            