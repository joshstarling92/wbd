import unittest
import uuid
import os
import Navigation.prod.Fix as Fix

 
class TestFix(unittest.TestCase):
     
    def setUp(self):
        self.className = "Fix."
        self.logStartString = "Start of log"
        self.logSightingString = "Start of sighting file"
        self.absolutePath = '/Users/Josh/Downloads/wbd-CA02/SoftwareProcess/Navigation/test/' 
         
        # set default log file name
        self.DEFAULT_LOG_FILE = "log.txt"
        if(os.path.isfile(self.DEFAULT_LOG_FILE)):
            os.remove(self.DEFAULT_LOG_FILE)
             
        # generate random log file name
        self.RANDOM_LOG_FILE = "log" + str(uuid.uuid4())[-12:] + ".txt"
        
        
#     def test100_010_ShouldStartLogFileWithAbsPath(self):
# #         testFile = "CA02_300_ValidOneStarArtificialHorizon.xml"
#         theFix = Fix.Fix(self.RANDOM_LOG_FILE)
#         theFix.setSightingFile('CA02_300_GenericValidStarSightingFile.xml')
#         theFix.getSightings()
#         targetStringList = 'LOG: Log file:/Users/Josh/git/SoftwareProcess/SoftwareProcess/Navigation/test/'
#         theLogFile = open(self.RANDOM_LOG_FILE, "r")
#         logFileContents = theLogFile.readlines()
#         theLogFile.close()
# #         print logFileContent
#         for logEntryNumber in range(0, len(logFileContents)):
#             if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
#                     for target in targetStringList:
#                         self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
#                                              "Major:  Log entry of path is not correct for log file")
#         self.cleanup() 
#     def test100_020_ShouldSpecifySightingFileWithAbsPath(self):
#         theFix = Fix.Fix(self.RANDOM_LOG_FILE)
#         theFix.setSightingFile('CA02_300_GenericValidStarSightingFile.xml')
#         theFix.getSightings()
#         targetStringList = 'LOG:    Sighting file:/Users/Josh/git/SoftwareProcess/SoftwareProcess/Navigation/test/'+'CA02_300_GenericValidStarSightingFile.xml'
#         theLogFile = open(self.RANDOM_LOG_FILE, "r")
#         logFileContents = theLogFile.readlines()
#         theLogFile.close()
# #         print logFileContents
#         for logEntryNumber in range(0, len(logFileContents)):
#             if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
#                 for target in targetStringList:
# #                     print target
# #                     print logFileContents[logEntryNumber].find(target)
#                     self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
#                                              "Major:  Sighting entry of path is not correct for log file")
#         self.cleanup()
#         
#         setAriesFile
    def test100_030_ShouldWriteToLogPathToAries(self):
        testFile = "CA02_300_ValidMultipleStarSighting.xml"
        targetStringList = ['/Users/Josh/Downloads/wbd-CA02/SoftwareProcess/Navigation/aries.txt'] #"29d55.7"
        theFix = Fix.Fix(self.RANDOM_LOG_FILE)
        theFix.setAriesFile('aries.txt')
        theFix.setStarFile('stars.txt')
        theFix.setSightingFile(testFile)
        theFix.getSightings()
           
        theLogFile = open(self.RANDOM_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        theLogFile.close()
           
        sightingCount = 0
        for logEntryNumber in range(0, len(logFileContents)):
            if(logFileContents[logEntryNumber].find(targetStringList[0]) > -1):
                sightingCount += 1
                for target in targetStringList:
                    self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
                                         "Major:  Log entry is not correct for getSightings")
        self.assertEquals(1, sightingCount)
        self.cleanup() 
#         
#     def test100_040_ShouldReturnAbsPathToAries(self):
#         testFile = "CA02_300_ValidOneStarArtificialHorizon.xml"
#         targetStringList = ['/Users/Josh/Downloads/wbd-CA02/SoftwareProcess/Navigation/aries.txt'] #"29d55.7"
#         theFix = Fix.Fix(self.RANDOM_LOG_FILE)
#         theFix.setSightingFile(testFile)
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
#                     self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
#                                          "Major:  Log entry is not correct for getSightings")
#         self.assertEquals(1, sightingCount)
#         self.cleanup() 
#         
#     def test900_100_ShouldRaiseErrorAriesFileYearIsMissingYMorD(self): 
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
#     def test900_110_ShouldRaiseErrorAriesFileYearIsMissingslashes(self):     
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
#     def test900_120_ShouldRaiseErrorAriesFileHourIsntNum(self):     
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
#     def test900_130_ShouldRaiseErrorAriesFileAngleIsntValid(self):        
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
#     def test900_140_ShouldRaiseErrorAriesFileYearNotInRange(self):
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
#     def test900_150_ShouldRaiseErrorAriesFileDayNotInRange(self):        
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
#     def test900_160_ShouldRaiseErrorAriesFileMonthNotInRange(self):   
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])      
#     def test900_170_ShouldRaiseErrorAriesFileHourNotInRange(self):     
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
#     def test900_180_ShouldRaiseErrorAriesFileNotLongEnough(self):
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
#     def test900_190_ShouldRaiseErrorAriesFileNotHaveCorrectExt(self):
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])     
# 
#     def test200_010_ShouldWriteToLogPathToStar(self):
#         testFile = "CA02_300_ValidOneStarArtificialHorizon.xml"
#         targetStringList = ['/Users/Josh/Downloads/wbd-CA02/SoftwareProcess/Navigation/star.txt'] #"29d55.7"
#         theFix = Fix.Fix(self.RANDOM_LOG_FILE)
#         theFix.setSightingFile(testFile)
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
#                     self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
#                                          "Major:  Log entry is not correct for getSightings")
#         self.assertEquals(1, sightingCount)
#         self.cleanup() 
# #     def test200_000_ShouldReturnAbsPathToStar(self):
#         
#     def test900_200_ShouldRaiseErrorStarFileYearIsMissingYMorD(self): 
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
#     def test900_210_ShouldRaiseErrorStarFileYearIsMissingslashes(self):  
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])       
#     def test900_220_ShouldRaiseErrorStarFileHourIsntNum(self): 
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])        
#     def test900_230_ShouldRaiseErrorStarFileAngleIsntValid(self):    
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
#     def test900_240_ShouldRaiseErrorStarFileYearNotInRange(self):    
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
#     def test900_250_ShouldRaiseErrorStarFileDayNotInRange(self):      
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
#     def test900_260_ShouldRaiseErrorStarFileMonthNotInRange(self): 
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])     
#     def test900_270_ShouldRaiseErrorStarFileHourNotInRange(self):
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])     
#     def test900_280_ShouldRaiseErrorStarFileLatNotInRange(self):  
#         expectedString = "Fix.setSightingFile:  Date is in incorrect format"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])    
#     def test900_290_ShouldRaiseErrorStarFileLonNotInRange(self):   
#         expectedString = "Fix.setSightingFile:  long is in range "
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])    
#     def test900_291_ShouldRaiseErrorStarFileNotLongEnough(self):
#         expectedString = "Fix.setSightingFile:  Star file not correct length"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
#     def test900_292_ShouldRaiseErrorStarFileNotHaveCorrectExt(self):
#         expectedString = "Fix.setSightingFile:  Star file is not correct extension"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
# 
# 
#     def test300_010_ShouldWriteToLogLat(self):
#     def test300_020_ShouldWriteToLogLon(self):
#     def test300_030_ShouldWriteToLogNumberSightingError(self):
#     def test300_040_ShouldWriteToLogNumberSightingAngDisplacment(self):
#     def test300_050_ShouldWriteToLogNumberSightingGWHA(self):
#     def test300_060_ShouldWriteToLogNumberSightingLon(self):
#                    
#     def test900_300_ShouldRaiseErrorIfSightingFileNotGiven(self):
#         expectedString = "Fix.setSightingFile:  No Sighting file set"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)]) 
#         
#     def test900_310_ShouldRaiseErrorIfStarFileNotGiven(self):
#         expectedString = "Fix.setSightingFile:  No Star file set"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])    
#         
#     def test900_320_ShouldRaiseErrorIfAriesFileNotGiven(self):
#         expectedString = "Fix.setSightingFile:  No Aries file set"
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sightingFile.xm')
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
#         
#         
#         testFile = "CA02_300_ValidOneStarArtificialHorizon.xml"
#         targetStringList = ["Hadar", "2016-03-01", "23:40:01", "29d55.7"] #"29d55.7"
#         theFix = Fix.Fix(self.RANDOM_LOG_FILE)
#         theFix.setSightingFile(testFile)
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
#                     self.assertNotEquals(-1, logFileContents[logEntryNumber].find(target), 
#                                          "Major:  Log entry is not correct for getSightings")
#         self.assertEquals(1, sightingCount)
#         self.cleanup() 
#         
#  helper methods
    def indexInList(self, target, searchList):
        for index in range(len(searchList)):
            if(target in searchList[index]):
                return index
        return -1
     
    def cleanup(self):
        if(os.path.isfile(self.RANDOM_LOG_FILE)):
            os.remove(self.RANDOM_LOG_FILE)  