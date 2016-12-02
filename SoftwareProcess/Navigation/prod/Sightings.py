import math
import Angle
from _ast import Num
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
        SHA = starLongList[iterStar-1]

        GHA1 = ariesLongList[iterAries-1]
        GHA2 = ariesLongList[iterAries]

        minute =  int(sightingDic['time'][3:5])
        sec =  int(sightingDic['time'][6:8])
        interpolTime = sec + minute*60
        GHA = GHA1 + abs(GHA2-GHA1)*interpolTime/3600.0
        return GHA+SHA
    
    def calculateGeodedicLat(self,starLatList,iterStar):
        return str(starLatList[iterStar])
    
    def calculateAzimuthAdjustment(self,geoLng,geoLatUnvalid,assumeLng,assumeLat,adjustedAlt):
#         geoLat = self.checkgeoLat(geoLatUnvalid)
        deg2rad = 3.1415/180
        geoLat = self.checkgeoLat(geoLatUnvalid)
#         geoLng = 318.165


        LHA = Angle.Angle()
        LHA.setDegrees(geoLng + assumeLng)
        num = math.sin(geoLat*deg2rad)-(math.sin(assumeLat*deg2rad)*(math.sin(geoLat*deg2rad)*math.sin(assumeLat*deg2rad)+math.cos(geoLat*deg2rad)*math.cos(assumeLat*deg2rad)*math.cos(LHA.getDegrees()*deg2rad)))
        den = math.cos(assumeLat*deg2rad)*math.cos(math.asin(math.sin(geoLat*deg2rad)*math.sin(assumeLat*deg2rad)+math.cos(geoLat*deg2rad)*math.cos(assumeLat*deg2rad)*math.cos(LHA.getDegrees()*deg2rad)))
        try:
            azimuthAdjusted = math.acos(num/den)*180/3.1415
            return azimuthAdjusted

        except ValueError as e:
            raise ValueError(e) 
    
    def calculateDistanceAdjustment(self,geoLng,geoLatUnvalid,assumeLng,assumeLat,adjustedAlt):
#         print geoLng
        geoLat = self.checkgeoLat(geoLatUnvalid)
#         geoLng = 318.165
        deg2rad = 3.1415/180

        LHA = Angle.Angle()
        LHA.setDegrees(geoLng + assumeLng)
        correctedAlt = math.asin(math.sin(geoLat*deg2rad)*math.sin(assumeLat*deg2rad)+math.cos(geoLat*deg2rad)*math.cos(assumeLat*deg2rad)*math.cos(LHA.getDegrees()*deg2rad))*180/3.1415
        distanceAdjusted = round((correctedAlt-adjustedAlt)*60,0)
        return distanceAdjusted
    
    def checkgeoLat(self,geoLat):
        state = 0 # will be used determine if current character should be appended to minute or degree string
        degreeString = ''
        seperatorString = ''
        minuteString = ''

        #For loop to read input string
        #places input string into three different variables to be error checked later
        for i in geoLat:
            if i == 'd':
                state = 1
                seperatorString = i
                continue
            if state == 0:
                degreeString = degreeString + i
            else:
                minuteString = minuteString + i

        #error checking to make sure all required sections were provided       
        if seperatorString != 'd':
            errmsg ="'d' separator is missing from input string"
            raise ValueError(errmsg)
        if degreeString == '':
            errmsg ="degrees is missing from input string"
            raise ValueError(errmsg)
        if minuteString == '':
            errmsg = "minutes is missing from input string"
            raise ValueError(errmsg)
        
        #Now that all sections were validated to be provided, degrees and minutes must be validated 
        #to be the correct input type (i.e. a number not a character or being float and not an int, ect, ect
        try: #Verify that degrees is a number
            degrees = int(degreeString)
        except:
            errmsg = "degrees must be a numerical value (int)"
            raise ValueError(errmsg)
        if degrees != float(degreeString): #if input degrees is a decimal this should catch it 
            errmsg = "degrees must be type int"
            raise ValueError(errmsg)
    
        #now that degrees has been verified, grabbing the sign of degrees
        if degrees < 0:
            sign = -1
        else:
            sign = 1
            
        #Verifying minutes similar to how degrees was validated above
        try:
            minute = float(minuteString)
        except:
            errmsg = "minutes must be a numerical value (int or float)"
            raise ValueError(errmsg)
        if minute < 0:
            errmsg = "minutes must be a positive number"
            raise ValueError(errmsg)
        if minute*10 != int(minute*10):
            errmsg = "minutes must have only one decimal place"
            raise ValueError(errmsg)
        
        outputFloat = degrees + sign*float(minuteString)/60
        angle =  outputFloat
        return angle