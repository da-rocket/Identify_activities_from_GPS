#This program is used to filter gross blunders from gps data of a certain format
#and export processed data in a *.CSV fofrmat
#Initiated by Vladimir Usyukov
#Date of start March 1, 2015

import os
import time, datetime
import csv



#read *CSV files for processing
for root, dirs, files in os.walk("D:\gpsProject\projectData\Waterloo GPS data"):
    for file in files:
        if file.endswith(".csv"):
            filepath = os.path.join(root, file)
            csvFile = open(filepath)
            print "processing file ", csvFile

            #find position of titles and strips of '\n' character from list
            headerLine = (csvFile.readline()).strip()
            valueList = headerLine.split(',')

            groupIndex = valueList.index("Group")
            unitIndex = valueList.index("Unit")
            dateIndex = valueList.index("Date")
            timeIndex = valueList.index("StartTime")
            latValueIndex = valueList.index("Lat")
            longValueIndex = valueList.index("Long")
            altitudeIndex = valueList.index("Alt")
            speedIndex = valueList.index("Speed")

            #settings to filter altitude data and instanteneous speed (Doppler)
            altMin = 200.0
            altMax = 600.
            speedMin = 0.
            speedMax = 40.

            #definition of lists
            cleanpointList = list()
            cleanpointList.append(["Group", "Unit", "Date", "weekDate", "Time", "Seconds", "Lat", "Long", "Alt", "Speed"])

            cleansegmentList = list()
            cleansegmentList.append(["Group", "Unit", "Date", "weekDate", "Time", "Seconds", "Lat", "Long", "Alt", "Speed"])
            #print cleansegmentList

            gpstrackList = list()
            gpstrackList.append(["Group", "Unit", "Date", "weekDate", "Time", "Seconds", "Lat", "Long", "Alt", "Speed", "Track"])

            ODtrackList = list()
            ODtrackList.append(["Group", "Unit", "Date", "weekDate", "Time", "Seconds", "Lat", "Long", "Alt", "Speed", "Track"])

            tourIdList = list()
            tourIdList.append(["Group", "Unit", "Date", "weekDate", "Time", "Seconds", "Lat", "Long", "Alt", "Speed", "Track", "tourEnd"])

            errordataList = list()

            #reading file starting from the first point
            rowList = csvFile.readlines()

            #insert csv points from data file and convert data to required format
            for row in rowList:
                row = row.split(',')

                pointGroup = int(row[groupIndex])
                pointUnit = int(row[unitIndex])
                pointDate = row[dateIndex]
                pointTime = row[timeIndex]
                pointLat = float(row[latValueIndex])
                pointLong = float(row[longValueIndex])
                pointAltitude = float(row[altitudeIndex])
                pointSpeed = float(row[speedIndex])

                #convert aggregate time to seconds
                timeFormat = time.strptime(pointTime, "%H:%M:%S")
                pointSeconds = datetime.timedelta(hours=timeFormat.tm_hour, minutes=timeFormat.tm_min, seconds=timeFormat.tm_sec).seconds

                #convert date to time of the week format
                day, month, year = (int(x) for x in pointDate.split('/'))
                ans = datetime.date(year, month, day)
                pointweekDate = ans.strftime("%A")

                #filter point altitude, instanteneous speed and weekend data
                if ((pointAltitude > altMin) and (pointAltitude < altMax))and ((pointSpeed > speedMin) and (pointSpeed < speedMax)):
                    cleanpointList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed])

                else:
                    errordataList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed])

            #find new indexes in array
            headerLine = cleanpointList[0]

            for indexValue, nameValue in enumerate (headerLine):
                if nameValue == "Group":
                    groupIndex = indexValue
                elif nameValue == "Unit":
                    unitIndex = indexValue
                elif nameValue == "Date":
                    dateIndex = indexValue
                elif nameValue == "weekDate":
                    weekdateIndex = indexValue
                elif nameValue == "Time":
                    timeIndex = indexValue
                elif nameValue == "Seconds":
                    secondsIndex = indexValue
                elif nameValue == "Lat":
                    latValueIndex = indexValue
                elif nameValue == "Long":
                    longValueIndex = indexValue
                elif nameValue == "Alt":
                    altitudeIndex = indexValue
                else:
                    speedIndex = indexValue

            #print groupIndex, unitIndex, dateIndex, weekdateIndex, timeIndex, secondsIndex, latValueIndex, longValueIndex, altitudeIndex, speedIndex
            #save first point from the list
            firstPoint = cleanpointList[1]

            pointGroup = firstPoint[groupIndex]
            pointUnit = firstPoint[unitIndex]
            pointDate = firstPoint[dateIndex]
            pointweekDate = firstPoint[weekdateIndex]
            pointTime = firstPoint[timeIndex]
            pointSeconds = firstPoint[secondsIndex]
            pointLat = firstPoint[latValueIndex]
            pointLong = firstPoint[longValueIndex]
            pointAltitude = firstPoint[altitudeIndex]
            pointSpeed = firstPoint[speedIndex]

            cleansegmentList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed])

            for row in cleanpointList [2:]: #1sr - row are titles; 2nd - is first point

                nextpointGroup = row[groupIndex]
                nextpointUnit = row[unitIndex]
                nextpointDate = row[dateIndex]
                nextpointweekDate = row[weekdateIndex]
                nextpointTime = row[timeIndex]
                nextpointSeconds = row[secondsIndex]
                nextpointLat = row[latValueIndex]
                nextpointLong = row[longValueIndex]
                nextpointAltitude = row[altitudeIndex]
                nextpointSpeed = row[speedIndex]

                if(pointweekDate == nextpointweekDate):
                    altDifference = abs(pointAltitude - nextpointAltitude)

                    if(altDifference < 20.):
                        pointGroup = nextpointGroup
                        pointUnit = nextpointUnit
                        pointDate = nextpointDate
                        pointweekDate = nextpointweekDate
                        pointTime = nextpointTime
                        pointSeconds = nextpointSeconds
                        pointLat = nextpointLat
                        pointLong = nextpointLong
                        pointAltitude = nextpointAltitude
                        pointSpeed = nextpointSpeed

                        cleansegmentList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed])
                    else:
                        pointGroup = nextpointGroup
                        pointUnit = nextpointUnit
                        pointDate = nextpointDate
                        pointweekDate = nextpointweekDate
                        pointTime = nextpointTime
                        pointSeconds = nextpointSeconds
                        pointLat = nextpointLat
                        pointLong = nextpointLong
                        pointAltitude = nextpointAltitude
                        pointSpeed = nextpointSpeed

                else:
                    #reset to a new start
                    pointGroup = nextpointGroup
                    pointUnit = nextpointUnit
                    pointDate = nextpointDate
                    pointweekDate = nextpointweekDate
                    pointTime = nextpointTime
                    pointSeconds = nextpointSeconds
                    pointLat = nextpointLat
                    pointLong = nextpointLong
                    pointAltitude = nextpointAltitude
                    pointSpeed = nextpointSpeed

                    cleansegmentList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed])

            #add additional column 'tracks' to the list
            #gpstrackList = cleansegmentList

            headerLine = cleansegmentList[0]

            #headerTrack = headerLine + ['Track']
            #print headerTrack, type(headerTrack)

            for indexValue, nameValue in enumerate (headerLine):
                if nameValue == "Group":
                    groupIndex = indexValue
                elif nameValue == "Unit":
                    unitIndex = indexValue
                elif nameValue == "Date":
                    dateIndex = indexValue
                elif nameValue == "weekDate":
                    weekdateIndex = indexValue
                elif nameValue == "Time":
                    timeIndex = indexValue
                elif nameValue == "Seconds":
                    secondsIndex = indexValue
                elif nameValue == "Lat":
                    latValueIndex = indexValue
                elif nameValue == "Long":
                    longValueIndex = indexValue
                elif nameValue == "Alt":
                    altitudeIndex = indexValue
                else:
                    #nameValue == "Speed":
                    speedIndex = indexValue
##                else:
##                    trackIndex = indexValue

            ##print groupIndex, unitIndex, dateIndex,weekdateIndex, timeIndex,secondsIndex,latValueIndex,longValueIndex,altitudeIndex,speedIndex #, trackIndex
            #read point one
            firstPoint = cleanpointList[1]

            pointGroup = firstPoint[groupIndex]
            pointUnit = firstPoint[unitIndex]
            pointDate = firstPoint[dateIndex]
            pointweekDate = firstPoint[weekdateIndex]
            pointTime = firstPoint[timeIndex]
            pointSeconds = firstPoint[secondsIndex]
            pointLat = firstPoint[latValueIndex]
            pointLong = firstPoint[longValueIndex]
            pointAltitude = firstPoint[altitudeIndex]
            pointSpeed = firstPoint[speedIndex]
            #introduce index '10' as track
            pointTrack = 1
            #print pointTrack

            gpstrackList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed, pointTrack])

            ODtrackList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed, pointTrack])
            ##print pointDate, pointTrack
            ##print len(cleanpointList)

            for row in cleanpointList [2:]: #1sr - row are titles; 2nd - is first point

                nextpointGroup = row[groupIndex]
                nextpointUnit = row[unitIndex]
                nextpointDate = row[dateIndex]
                nextpointweekDate = row[weekdateIndex]
                nextpointTime = row[timeIndex]
                nextpointSeconds = row[secondsIndex]
                nextpointLat = row[latValueIndex]
                nextpointLong = row[longValueIndex]
                nextpointAltitude = row[altitudeIndex]
                nextpointSpeed = row[speedIndex]

                timeDifference = (nextpointSeconds - pointSeconds)/ 60.
                #print nextpointSeconds, pointSeconds, timeDifference

                if(pointDate == nextpointDate):

                    if(timeDifference < 10.0):
                        pointGroup = nextpointGroup
                        pointUnit = nextpointUnit
                        pointDate = nextpointDate
                        pointweekDate = nextpointweekDate
                        pointTime = nextpointTime
                        pointSeconds = nextpointSeconds
                        pointLat = nextpointLat
                        pointLong = nextpointLong
                        pointAltitude = nextpointAltitude
                        pointSpeed = nextpointSpeed

                        #print pointDate, pointweekDate, pointTime, pointLat, pointLong, pointAltitude, pointSpeed, pointTrack
                        gpstrackList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed, pointTrack])
                    else:
                        #save Destination of a track
                        ##print pointDate, pointweekDate, pointTime, pointLat, pointLong, pointAltitude, pointSpeed, pointTrack
                        ODtrackList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed, pointTrack])

                        pointGroup = nextpointGroup
                        pointUnit = nextpointUnit
                        pointDate = nextpointDate
                        pointweekDate = nextpointweekDate
                        pointTime = nextpointTime
                        pointSeconds = nextpointSeconds
                        pointLat = nextpointLat
                        pointLong = nextpointLong
                        pointAltitude = nextpointAltitude
                        pointSpeed = nextpointSpeed
                        pointTrack += 1

                        #print pointDate, pointTrack
                        ODtrackList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed, pointTrack])
                        gpstrackList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed, pointTrack])
                else:
                    #save Destination of a track
                    ##print pointDate, pointweekDate, pointTime, pointLat, pointLong, pointAltitude, pointSpeed, pointTrack
                    ODtrackList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed, pointTrack])

                    pointGroup = nextpointGroup
                    pointUnit = nextpointUnit
                    pointDate = nextpointDate
                    pointweekDate = nextpointweekDate
                    pointTime = nextpointTime
                    pointSeconds = nextpointSeconds
                    pointLat = nextpointLat
                    pointLong = nextpointLong
                    pointAltitude = nextpointAltitude
                    pointSpeed = nextpointSpeed
                    pointTrack = 1

                    gpstrackList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed, pointTrack])
                    ODtrackList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed, pointTrack])
                    #print pointDate, pointweekDate, pointTime, pointLat, pointLong, pointAltitude, pointSpeed, pointTrack
                    #print pointDate, pointTrack

            #add last 'destination' of last day, of last track
            destinationException = gpstrackList [-1]
            ODtrackList.append(destinationException)

##            #rewrite values from OD list to tour list, by adding a flag value of '1' to to tour start and end
##            headerLine = ODtrackList[0]
##            for indexValue, nameValue in enumerate (headerLine):
##                if nameValue == "Group":
##                    groupIndex = indexValue
##                elif nameValue == "Unit":
##                    unitIndex = indexValue
##                elif nameValue == "Date":
##                    dateIndex = indexValue
##                elif nameValue == "weekDate":
##                    weekdateIndex = indexValue
##                elif nameValue == "Time":
##                    timeIndex = indexValue
##                elif nameValue == "Seconds":
##                    secondsIndex = indexValue
##                elif nameValue == "Lat":
##                    latValueIndex = indexValue
##                elif nameValue == "Long":
##                    longValueIndex = indexValue
##                elif nameValue == "Alt":
##                    altitudeIndex = indexValue
##                elif nameValue == "Speed":
##                    speedIndex = indexValue
##                else:
####                  nameValue == "Track"
##                    trackIndex = indexValue
####                else:
####                    #nameValue == "tourEnd":
####                    tourendIndex = indexValue
##            ##print groupIndex, unitIndex, dateIndex,weekdateIndex, timeIndex,secondsIndex,latValueIndex,longValueIndex,altitudeIndex,speedIndex, trackIndex
##
##            firstPoint = ODtrackList[1]
##
##            pointGroup = firstPoint[groupIndex]
##            pointUnit = firstPoint[unitIndex]
##            pointDate = firstPoint[dateIndex]
##            pointweekDate = firstPoint[weekdateIndex]
##            pointTime = firstPoint[timeIndex]
##            pointSeconds = firstPoint[secondsIndex]
##            pointLat = firstPoint[latValueIndex]
##            pointLong = firstPoint[longValueIndex]
##            pointAltitude = firstPoint[altitudeIndex]
##            pointSpeed = firstPoint[speedIndex]
##            pointTrack = firstPoint[trackIndex]
##            pointTour = 1
##
##            tourIdList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed, pointTrack,pointTour])
##
##            for row in ODtrackList[2:]:
##
##                nextpointGroup = row[groupIndex]
##                nextpointUnit = row[unitIndex]
##                nextpointDate = row[dateIndex]
##                nextpointweekDate = row[weekdateIndex]
##                nextpointTime = row[timeIndex]
##                nextpointSeconds = row[secondsIndex]
##                nextpointLat = row[latValueIndex]
##                nextpointLong = row[longValueIndex]
##                nextpointAltitude = row[altitudeIndex]
##                nextpointSpeed = row[speedIndex]
##                nextpointTrack = row[pointTrack]
##                nextpointTour = 0
##
##                if(pointDate==nextpointDate):
##                    pointGroup = nextpointGroup
##                    pointUnit = nextpointUnit
##                    pointDate = nextpointDate
##                    pointweekDate = nextpointweekDate
##                    pointTime = nextpointTime
##                    pointSeconds = nextpointSeconds
##                    pointLat = nextpointLat
##                    pointLong = nextpointLong
##                    pointAltitude = nextpointAltitude
##                    pointSpeed = nextpointSpeed
##                    pointTrack = nextpointTrack
##                    pointTour = 0
##
##                else:
##                    tourIdList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed, pointTrack,pointTour])


            #send output tracks to file
            save_path = 'D:\gpsProject\projectData\Clean_tracks'
            fileName = file[:-4] + '_clean'
            completeName = os.path.join(save_path,fileName+".csv")

            with open(completeName, 'wb') as outcsv:
                writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
                for item in gpstrackList:
                    #Write item to outcsv
                    writer.writerow([item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10]])
            outcsv.close()

            #send output OD pairs to file
            save_path = 'D:\gpsProject\projectData\OD_pairs'
            fileName = file[:-4] + '_OD'
            completeName = os.path.join(save_path,fileName+".csv")

            with open(completeName, 'wb') as outcsv:
                writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
                for item in ODtrackList:
                    #Write item to outcsv
                    writer.writerow([item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10]])
            outcsv.close()

            print completeName + " is processed"






