from xml.dom.minidom import parse
import Angle


class XML_handler():
    def __init__(self):
        self.classErrorName = 'XML_handler.'

    ######################################
    ########XML Parse Functions###########
    ######################################

    def handleSightingLog(self, sightingFile):
        #function that takes entire xml file and parses it and searches through
        #each sighting and get at least the mandatory data and any optional data
        sightingDOM = parse(sightingFile)
        sightings = sightingDOM.getElementsByTagName("sighting") #get range of all sightings in file
        sightingsDic = {}
        sightingsDic['SightingError'] = 0
        bodyList = []
        if sightings == []:
            sightingsDic['Message'] = 'No sightings found'
        else:
            sightingsDic['Message'] = 'Sightings found'
#             try:
            orderedSightings = self.getChronologicalOrder(sightings)
#             except:
#                 orderedSightings = sightings
            for sighting in orderedSightings:
                errorOccured = 0;
                try: #get all mandatory data, failure to do so will raise error
                    body = self.handleBody(sighting)
                    date = self.handleDate(sighting)
                    time = self.handleTime(sighting)
                    obs = self.handleObservation(sighting)
                    sightingsDic[str(body)] = {}
                    sightingsDic[str(body)]['Message'] = 'No error'
                    sightingsDic[str(body)]['body'] = str(body)
                    sightingsDic[str(body)]['date'] = str(date)
                    sightingsDic[str(body)]['time'] = str(time)
                    sightingsDic[str(body)]['observation'] = obs
#                 except ValueError as e:
#                     raise ValueError(e)
                except:
                    try:
                        body = self.handleBody(sighting)
                        sightingsDic[str(body)]['Message'] = 'There was an error'
                    except:
                        body = 'NullBody'
                        sightingsDic[str(body)] = {}
                    errorOccured = errorOccured + 1
                    if (errorOccured == 1):
                        currentSightingError = sightingsDic['SightingError']
                        currentSightingError = currentSightingError + 1
                        sightingsDic['SightingError'] = currentSightingError

                #Get all  non-mandatory data
                try:
                    height = float(self.handleHeight(sighting))
                    temp = float(self.handleTemperature(sighting))
                    if (height == 1234567):
                        height = 0
                    if (height == 7654321):
                        errorOccured = errorOccured + 1
                        if (errorOccured == 1):
                            currentSightingError = sightingsDic['SightingError']
                            currentSightingError = currentSightingError + 1
                            sightingsDic['SightingError'] = currentSightingError
                        height = 0.0   
                    sightingsDic[str(body)]['height'] = height
                    sightingsDic[str(body)]['temperature'] = temp
                except:
                    sightingsDic[str(body)]['Message'] = 'There was an error' 
                try:
                    pressure = float(self.handlePressure(sighting))
                    sightingsDic[str(body)]['pressure'] = pressure
#                 except ValueError as e:
#                     raise ValueError(e)
                except:
                    errorOccured = errorOccured + 1
                    if (errorOccured == 1):
                        currentSightingError = sightingsDic['SightingError']
                        currentSightingError = currentSightingError + 1
                        sightingsDic['SightingError'] = currentSightingError
                try:
                    horz = self.handleHorizon(sighting)
                    sightingsDic[str(body)]['horizon'] = str(horz)
#                 except ValueError as e:
#                     raise ValueError(e)
                except:
                    errorOccured = errorOccured + 1
                    if (errorOccured == 1):
                        currentSightingError = sightingsDic['SightingError']
                        currentSightingError = currentSightingError + 1
                        sightingsDic['SightingError'] = currentSightingError
                if (errorOccured == 0):
                    bodyList.append(str(body))
        sightingsDic['bodyList'] = bodyList
        return sightingsDic
            
    
    def getChronologicalOrder(self,sightingsList):
        timeInSecOfSighting = [] #make empty list
        validSightings = []
        incorrectSightings = []
        returnSightings = []

        for sighting in sightingsList:
            try: #get time and data tags, failure to do so will raise error
                date = self.handleDate(sighting)
                time = self.handleTime(sighting)
                #convert both strings into their individual components
                year = int(date[0:4])
                month =  int(date[5:7])
                day =  int(date[8:10])
                hour =  int(time[0:2])
                minute =  int(time[3:5])
                sec =  int(time[6:8])
                timeInSecOfSighting.append(sec + minute*60 + hour*60**2 + day*24*60**2 + (year+(float(month)/12.0))*365*24*60**2)
                validSightings.append(sighting)
            except:
                incorrectSightings.append(sighting)

            
            #take components and converts to a single numerical value that can be used to sort
        #takes sightings dom list and timeInSecOfSighting list and places each element into tuples respectivly, using zip
        #the list of touples are then sorted by timeInSecOfSighting and uncoupled back to their respective lists
        TupleListOfTimeAndSightings = zip(timeInSecOfSighting, validSightings) #combines into on list
        if validSightings != []:
            sortedTupleList = sorted(TupleListOfTimeAndSightings) #sorts list
            sortedTimeList, sortedSightings = (list(t) for t in zip(*sortedTupleList)) #unsorts list and saves as individual list again
        
            for sighting in sortedSightings:
                returnSightings.append(sighting)
        if incorrectSightings != []:
            for sighting in incorrectSightings:
                returnSightings.append(sighting)  
        return returnSightings
    
    ###########Mandatory Tags###########
    #######Raises error if not given
    def handleBody(self,sighting):
        try:
            body = sighting.getElementsByTagName('body')[0]
            bodyString =  self.getText(body.childNodes)
        except:
            errmsg = 'Mandatory Tag "Body" missing'
            raise ValueError(errmsg) 
        if bodyString == '':
            errmsg = 'Mandatory Tag "Body" missing'
            raise ValueError(errmsg)
        return bodyString
           
    def handleDate(self,sighting):
        try:
            date = sighting.getElementsByTagName('date')[0]
            stringDate =  self.getText(date.childNodes)
        except:
            errmsg = 'Mandatory Tag "Date" missing'
            raise ValueError(errmsg)
        cnt = 0
        for i in stringDate:
            if cnt == 4 or cnt == 7:
                if i != '-':
                    errmsg = 'Date is not in the correct format'
                    raise ValueError(errmsg)
            cnt = cnt + 1

        if int(stringDate[0:4]) < 0:
            errmsg = 'Date is not in the correct format'
            raise ValueError(errmsg)
        if int(stringDate[5:7]) > 12:
            errmsg = 'Date is not in the correct format'
            raise ValueError(errmsg)
        if int(stringDate[8:10]) > 31:
            errmsg = 'Date is not in the correct format'
            raise ValueError(errmsg)
        return stringDate
    
    def handleTime(self,sighting):
        try:
            time = sighting.getElementsByTagName('time')[0]
            stringTime = self.getText(time.childNodes) 
        except:
            errmsg = 'Mandatory Tag "Time" missing'
            raise ValueError(errmsg)  
        cnt = 0
        for i in stringTime:
            if cnt == 2 or cnt == 5 or cnt == 8:
                if i != ':':
                    errmsg = 'Time is not in the correct format'
                    raise ValueError(errmsg)
            cnt = cnt + 1
        return stringTime
         
            
    def handleObservation(self,sighting):
        try:
            obs = sighting.getElementsByTagName('observation')[0]
            parsedObs =  self.getText(obs.childNodes)
            obsAngle = Angle.Angle();
            try:
                obsAngle.setDegreesAndMinutes(parsedObs)
            except ValueError as e:
                raise ValueError(e)
            obsValue = obsAngle.getDegrees()
            if obsValue < 0 or obsValue > 90:
                errmsg = 'Observation must be greater than 0 deg and less than 90 deg'
                raise ValueError(errmsg)    
            else:
                return obsAngle.getRadians()
        except:
            errmsg = 'Mandatory Tag "Observation" missing'
            raise ValueError(errmsg)
    ###########Non-mandatory Tags###########
    #######Uses default values if not given
    def handleHeight(self,sighting):
        try:
            heightStr = sighting.getElementsByTagName('height')[0]
            height =  self.getText(heightStr.childNodes)
        except:
            return 1234567
        try:
            height = float(height)
        except:
            return 7654321
        if float(height) >= 0:
            return float(height)
        else:   
            errmsg = 'Height must be greater than or equal to 0'
            raise ValueError(errmsg) 

                  
    def handleTemperature(self,sighting):
        try:
            tempStr = sighting.getElementsByTagName('temperature')[0]
            temp = self.getText(tempStr.childNodes)
            temp = float(temp)
        except:
            return 72
        if float(temp) == int(temp):
            if int(temp) > 120 or int(temp) < -20:
                errmsg = 'Temperature must be between -20 and 120 in degrees F'
                raise ValueError(errmsg) 
            else:
                return int(temp)
        else:
            errmsg = 'Temperature must be an integer'
            raise ValueError(errmsg) 


        
    def handlePressure(self,sighting):
        try:
            pressureStr = sighting.getElementsByTagName('pressure')[0]
            pressure = self.getText(pressureStr.childNodes)
            pressure = float(pressure)
        except:
            pressure = 1010

        if float(pressure) == int(pressure):
            return int(pressure)
        else:
            errmsg = 'Invalid pressure value used'
            raise ValueError(errmsg) 
        
    def handleHorizon(self,sighting):
        try:
            horzStr = sighting.getElementsByTagName('horizon')[0]
            horz  = self.getText(horzStr.childNodes)
        except:
            horz =  'natural' 
        if horz.lower() != 'natural' and horz.lower() != 'artificial':
            errmsg = 'Invalid horizon used'
            raise ValueError(errmsg) 
        else:
            return horz  

    #Function to read lowest level tag
    def getText(self,nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)