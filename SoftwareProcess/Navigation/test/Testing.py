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
    
#==================== Fix.__init__ ====================
# 100 Constructor
#    Analysis
#        inputs:
#            logFile: string, optional, unvalidated, len >= 1        regression
#        outputs:
#            returns:  instance of Fix                               regression
#|           also:    writes "Log file: " + filepath of log file     new to CA03
#
#    Happy tests:
#        logFile:  
#            test 010:    omit parm
#            test 020:    construct with default file name        CA03
#            test 030:    construct with named parm                
#            test 040:    construct with specific file name        CA03
#            test 050:    construct and append to existing file
#            existing logfile  -> Fix("myLog.txt") (assuming myLog.txt exits)
#    Sad tests:
#        logFile:
#            test 910:    length error -> Fix("")
#            test 920:    test nonstring -> Fix(42)
#    
#+++++++++++++++++++ Happy Path Tests ++++++++++++++++++++  
#----------      



#==================== Fix.setStarFile ===================              
# 500 setStarFile
#    Analysis
#        inputs:
#            starFile: string, mandatory, unvalidated, format = f.txt (len(f) >= 1)
#        outputs:
#            returns:  string with absolute filepath                
#            also:    writes "Star file\tf.txt" to log file
#
#    Happy tests:
#        ariesFile:
#            test 010:    legitimate file, no parm name
#            test 020:    legitimate file, named parm  -> verify correct return value                          
#            test 030:    legitimate file name  -> verify correct log 
#    Sad tests:
#        ariesFile:
#            test 910:    nonstring file name
#            test 920:    missing file prefix
#            test 930:    missing .txt file extension
#            test 940:    missing .txt file extension, but presence of "txt" in name
#            test 950:    missing parm
#            test 960:    missing file
#
#+++++++++++++++++++ Happy Path Tests ++++++++++++++++++++  
#-
#----------
#==================== Fix.getSightings ===================         
# 300 getSightings
#    Analysis
#        inputs:
#            via parm:  none
#            via file:  xml description of sighting
#        outputs:
#            returns:    ("0d0.0", "0d0.0")
#|            via file:    writes body/tdate/ttime/tadjustedAltitude/tlongitude/tlatitude
#                        sorted by date, time, body
#        entry criterion:
#            setSightingsFile must be called first
#
#    Happy tests:
#        sighting file 
#            test 010:     file with valid sightings -> should return ("0d0.0", "0d0.0")
#            valid file with mixed indentation -> should not indicate any errors
#            valid file with one sighting  -> should log one star body
#            valid file with multiple sightings -> should log star bodies in sorted order
#            valid file with multiple sightings at same date/time -> should log star bodies in order sorted by body 
#            valid file with zero sightings -> should not log any star bodies
#            valid file with extraneous tag -> should log star(s) without problem
#        sighting file contents
#            valid body with natural horizon -> should calculate altitude with dip
#            valid body with artificial horizon -> should calculate altitude without dip
#            valid body with default values -> should calculate altitude with height=0, temperature=72, pressure=1010, horizon-natural
#            sighting file with invalid mandatory tag (one of each:  fix, body, date, time, observation)
#            sighting file with invalid tag value (one of each:  date, time, observation, height, temperature, pressure, horizon)
#    Sad tests:
#        sightingFile:
#            sighting file not previously set
#            star file not previously set
#            aries file not previously set
#+++++++++++++++++++ Happy Path Tests ++++++++++++++++++++  
    def test300_110_ShouldLogStarLatLonWithInterpolation(self):
        'log geographical position'
        testFile = self.mapFileToTest("validLatLonInterpolated")
        targetStringList = ["Betelgeuse", None, None, None, "7d24.3", "75d54.3"]
        theFix = F.Fix(self.RANDOM_LOG_FILE)
        theFix.setSightingFile(testFile)
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
                                         "Major:  Lat/Lon entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
        self.assertEquals(1, sightingCount)
        self.deleteNamedLogFlag = True  
        
         
#-----------        
#     def test300_110_ShouldLogStarLatLonWithInterpolation(self):
#         'log geographical position'
#         testFile = self.mapFileToTest("validLatLonInterpolated")
#         targetStringList = ["Betelgeuse", None, None, None, "7d24.3", "75d54.3"]
#         theFix = F.Fix(self.RANDOM_LOG_FILE)
#         theFix.setSightingFile(testFile)
#         theFix.setAriesFile(self.ariesFileName)   
#         theFix.setStarFile(self.starFileName)
#         theFix.getSightings()
#         
#         theLogFile = open(self.RANDOM_LOG_FILE, "r")
#         logFileContents = theLogFile.readlines()
#         theLogFile.close()
#         
#         sightingCount = 0
#         for logEntryNumber in range(0, len(logFileContents)):
#             if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
#                 sightingCount += 1
#                 for target in targetStringList:
#                     if(target != None):
#                         self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
#                                          "Major:  Lat/Lon entry is not correct for getSightings " + self.RANDOM_LOG_FILE)
#         self.assertEquals(1, sightingCount)
#         self.deleteNamedLogFlag = True     


#  helper methods
    def indexInList(self, target, searchList):
        for index in range(len(searchList)):
            if(target in searchList[index]):
                return index
        return -1
    
    def mapFileToTest(self, target):
        for item in self.testToFileMap:
            if(item[0] == target):
                return item[1]
        return None