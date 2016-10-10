import Navigation.prod.Fix as Fix
import unittest
import os
# ---- Acceptance Tests
# 100 constructor
#    Desired level of confidence:    boundary value analysis
#    Input-output Analysis
#        inputs:      n ->    integer .GE. 2 and .LT. 30  mandatory, unvalidated
#        outputs:    instance of TCurve
#    Happy path analysis:    
#        n:      nominal value    n=4
#                low bound        n=2
#                high bound       n=29
#    Sad path analysis:
#        n:      non-int n          n="abc"
#                out-of-bounds n    n=1; n=30
#                missing n
class FixTest(unittest.TestCase):
# Happy path 
    def test100_010_ShouldConstruct(self):
        self.assertIsInstance(Fix.Fix(),Fix.Fix)
        
    def test100_020_ShouldMakeTextFileWithGivenName(self):
        Fix.Fix()
        self.assertEqual(1, os.path.isfile('log.txt'))
        
    def test100_030_ShouldMakeTextFileWithGivenName(self):
        Fix.Fix('log1.txt')
        self.assertEqual(1, os.path.isfile('log1.txt'))
#sad path
    def test100_910_ShouldRaiseExceptionBadTxtFileName(self):
        expectedString = "Fix.__init__:  Improper file extension used"
        with self.assertRaises(ValueError) as context:
            Fix.Fix('dsdd.tx')                           
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
          
    def test100_040_ShouldEditLogFile(self):
        Fix.Fix()
        self.assertEqual(1, os.path.isfile('log.txt'))
  
    def test100_050_ShouldReturnStringofFile(self):
        fixTest1 = Fix.Fix()
        self.assertEqual(fixTest1.setSightingFile('sighting.xml') , 'sighting.xml')
            
  
    def test100_070_ShouldWriteInLogFile(self):
        fixTest1 = Fix.Fix()
        self.assertEqual(fixTest1.setSightingFile('sighting.xml') , 'sighting.xml') 
  
    def test100_970_ShouldRaiseExceptionForNoFileGiven(self):
        expectedString = "Fix.setSightingFile:  No .xml file given"
        with self.assertRaises(ValueError) as context:
            fixTest1 = Fix.Fix()
            fixTest1.setSightingFile()
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
            
    def test100_980_ShouldRaiseExceptionForBadFileNameGiven(self):
        expectedString = "Fix.setSightingFile:  Improper file extension used"
        with self.assertRaises(ValueError) as context:
            fixTest1 = Fix.Fix()
            fixTest1.setSightingFile('sightingFile.xm')
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
          
    def test200_010_ShouldReturnDefaultLatAndLong(self):
        fixTest1 = Fix.Fix('testLog.txt')
        fixTest1.setSightingFile('sighting.xml')
        (approxLat, approxLong) = fixTest1.getSightings()
        self.assertEqual(approxLat, '0d0.0')
        self.assertEqual(approxLong, '0d0.0')
        
#     def test200_610_ShouldRaiseExceptionForLackingMandatoryTag(self):
#         expectedString = 'Fix.getSightings:  Mandatory Tag "Observation" missing'
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sighting.xml')
#             fixTest1.getSightings()
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])

#     def test200_620_ShouldRaiseExceptionForObsLessThanHalfMin(self):
#         expectedString = 'Fix.getSightings:  Angle.setDegreesAndMinutes:  minutes must have only one decimal place'
#         with self.assertRaises(ValueError) as context:
#             fixTest1 = Fix.Fix()
#             fixTest1.setSightingFile('sighting.xml')
#             fixTest1.getSightings()
#         self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])

    def test200_930_ShouldRaiseErrorForNoSightingFile(self):
        expectedString = 'Fix.getSightings:  No sighting file set'
        with self.assertRaises(ValueError) as context:
            fixTest1 = Fix.Fix('testLog.txt')
            (approxLat, approxLong) = fixTest1.getSightings()
        self.assertEquals(expectedString, context.exception.args[0][0:len(expectedString)])
        
    def test200_040_ShouldWriteLoginChronologicalOrder(self):
        fixTest1 = Fix.Fix('testLog.txt')
        fixTest1.setSightingFile('sighting.xml')
        (approxLat, approxLong) = fixTest1.getSightings()
        self.assertEqual(approxLat, '0d0.0')
        self.assertEqual(approxLong, '0d0.0')
        
    def test200_040_ShouldWriteLoginSameValuesAsHandCalculated(self):
        fixTest1 = Fix.Fix('testLog.txt')
        fixTest1.setSightingFile('sighting.xml')
        (approxLat, approxLong) = fixTest1.getSightings()
        self.assertEqual(approxLat, '0d0.0')
        self.assertEqual(approxLong, '0d0.0')