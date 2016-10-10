class Angle():
#Written by: Joshua Starling

    def __init__(self):
        #init function that will set the starting value at zero and defines the 
        #name of the class for the function of error handling
        self.angle = 0
        self.classErrorName = 'Angle.'
    
    def setDegrees(self, degrees = None):
        #Function sets the value angle by taking a numerical input value
        methodErrorName = 'setDegrees:  ' #defined for error handling
        if degrees == None: #optional requirement to set angle at zero if null input is given
            self.angle = 0
            return self.angle
        try:
            #if input is not a numerical value, casting to float will error and message is passed back up
            floatDegrees = float(degrees)
            wholeNumDegree = int(floatDegrees)
            minute = round((floatDegrees-wholeNumDegree)*60.0,1)
            
            self.angle = self.moduloDegree(wholeNumDegree+minute/60.0)
            return self.angle
        except:
            errorMesg = self.classErrorName + methodErrorName + "'degrees' violates the parameter specifications. Enter degrees as int or float."
            raise ValueError(errorMesg)
        
    def setDegreesAndMinutes(self, angleString = None):
        #Function sets the variable angle with a string of degrees in minutes in format 'xdy.y'
        #Lot of error handling in this function to make sure the input string is in the correct format
        #Initialize Variables
        methodErrorName = 'setDegreesAndMinutes:  ' #used for error handling
        state = 0 # will be used determine if current character should be appended to minute or degree string
        degreeString = ''
        seperatorString = ''
        minuteString = ''
        
        #Catches incorrect null input
        if angleString == None:
            errmsg = self.classErrorName + methodErrorName + 'Null input is not allowed.'
            raise ValueError(errmsg)

        #For loop to read input string
        #places input string into three different variables to be error checked later
        for i in angleString:
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
            errmsg = self.classErrorName + methodErrorName + "'d' separator is missing from input string"
            raise ValueError(errmsg)
        if degreeString == '':
            errmsg = self.classErrorName + methodErrorName + "degrees is missing from input string"
            raise ValueError(errmsg)
        if minuteString == '':
            errmsg = self.classErrorName + methodErrorName + "minutes is missing from input string"
            raise ValueError(errmsg)
        
        #Now that all sections were validated to be provided, degrees and minutes must be validated 
        #to be the correct input type (i.e. a number not a character or being float and not an int, ect, ect
        try: #Verify that degrees is a number
            degrees = int(degreeString)
        except:
            errmsg = self.classErrorName + methodErrorName + "degrees must be a numerical value (int)"
            raise ValueError(errmsg)
        if degrees != float(degreeString): #if input degrees is a decimal this should catch it 
            errmsg = self.classErrorName + methodErrorName + "degrees must be type int"
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
            errmsg = self.classErrorName + methodErrorName + "minutes must be a numerical value (int or float)"
            raise ValueError(errmsg)
        if minute < 0:
            errmsg = self.classErrorName + methodErrorName + "minutes must be a positive number"
            raise ValueError(errmsg)
        if minute*10 != int(minute*10):
            errmsg = self.classErrorName + methodErrorName + "minutes must have only one decimal place"
            raise ValueError(errmsg)
        
        #modulate degrees and minutes to proper value
        moduloDegree = self.moduloDegree(degrees) 
        moduloMinute = self.moduloMinute(float(minuteString))
        outputFloat = moduloDegree + sign*moduloMinute
        self.angle =  outputFloat
        return self.angle

    def add(self, angle = None):
        #Function will take self.angle and add to it the value of the angle class provided
        methodErrorName = 'add: '#used for error handling
        
        if angle is None:
            errorMesg = self.classErrorName + methodErrorName + "Null input is not allowed" 
            raise ValueError(errorMesg)
        try:        
            angleValue = angle.getDegrees()
        except:
            errorMesg = self.classErrorName + methodErrorName + "'angle' was not a valid instance of Angle"
            raise ValueError(errorMesg)
        self.angle = self.angle + angleValue
        self.angle = self.moduloDegree(self.angle)
        return self.angle
    
    def subtract(self, angle = None):
        #Function will take self.angle and subtract from it the value of the angle class provided
        methodErrorName = 'subtract:  '#used for error handling
        
        if angle is None:
            errorMesg = self.classErrorName + methodErrorName + "Null input is not allowed"
            raise ValueError(errorMesg)
        try:        
            angleValue = angle.getDegrees()
        except:
            errorMesg = self.classErrorName + methodErrorName + "'angle' was not a valid instance of Angle"
            raise ValueError(errorMesg)
        self.angle = self.angle - angleValue
        self.angle = self.moduloDegree(self.angle)
        return self.angle
    
    def compare(self, angle = None):
        #Function compares self.angle against the value of the angle class provided
        #Returns:
        #-1 if the instance is less than the value passed as a parameter            
        #0 if the instance is equal to the value passed as a parameter            
        #1 if the instance is greater than the value passed as a parameter            
        methodErrorName = 'compare:  '#used for error handling
        if angle is None:
            errorMesg = self.classErrorName + methodErrorName + "Null input is not allowed" 
            raise ValueError(errorMesg)
        try:        
            compareAngle = angle.getDegrees()
        except:
            errorMesg = self.classErrorName + methodErrorName + "'angle' was not a valid instance of Angle"
            raise ValueError(errorMesg)
        if self.angle > compareAngle:
            return 1
        elif self.angle == compareAngle:
            return 0
        else:
            return -1
    
    def getString(self):
        #Function will convert self.angle of class into the xdy.y string format and return it
        if self.angle < 0:
            sign = -1
        else:
            sign = 1
        return str(int(self.angle)) + 'd' + str(round((self.angle-int(self.angle))*sign*60,1))
    
    def getDegrees(self):
        #Function will return the self.angle of class and return it as a float with on decimal place
        return round(self.angle,7)
    
    def moduloDegree(self,degrees):
        #Internal function that is used to modulo the degree value to be within 0 and 360 
        degreePositive = 0
        varOverMax = 0
        if degrees < 0:
            while (degreePositive == 0):
                if degrees < 0:
                    degrees = degrees + 360
                else: 
                    degreePositive = 1;
        elif degrees >= 360:
            while (varOverMax == 0):
                if degrees >= 360:
                    degrees = degrees - 360
                else: 
                    varOverMax = 1;
        return degrees
    
    def moduloMinute(self,minutes):
        #Internal function that is used to modulo the degree value to be within 0 and 60
        degrees = 0
        varOverMax = 0
        if minutes > 60:
            while (varOverMax == 0):
                if minutes > 60:
                    degrees = degrees + 1
                    minutes = minutes - 60
                else:
                    varOverMax = 1
        return degrees + minutes/60