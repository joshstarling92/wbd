import math
class Sightings():
    def __init__(self):
        self.classErrorName = 'Sightings.'
        
    def calculateAngle(self,sightingDic):
        #function that calculates corrected observation angle 
        height = float(sightingDic['height'])
#         print height
        temp = sightingDic['temperature']
        pressure = sightingDic['pressure']
        horz = sightingDic['horizon']
        obs = sightingDic['observation']
        
        #calculate correction
        if horz == 'natural':
            dip = (-0.97 * math.sqrt(height))/60
        else:
            dip = 0
        refraction = (-0.00452*pressure)/(273+(temp-32)*5.0/9.0)/math.tan(obs)
        adjustedAlt = (obs*180/3.141592654 + dip + refraction)
        adjustedAltDeg = math.floor(adjustedAlt)
        adjustedAltMin = round((adjustedAlt-adjustedAltDeg)*60,1)
        return adjustedAltDeg+adjustedAltMin/60
    
    def calculateGeodedicLon(self,sightingDic,starLongList,ariesLongList,iterStar,iterAries):
        SHA = starLongList[iterStar]
        GHA1 = ariesLongList[iterAries]
        GHA2 = ariesLongList[iterAries+1]

        minute =  int(sightingDic['time'][3:5])
        sec =  int(sightingDic['time'][6:8])
        interpolTime = sec + minute*60
        GHA = GHA1 + abs(GHA2-GHA1)*interpolTime/3600.0
        return GHA+SHA
    
    def calculateGeodedicLat(self,starLatList,iterStar):
        return starLatList[iterStar]
