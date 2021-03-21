#-------------------------------------------------------------------------------
# Name:        homeRecognition.py
# Purpose:     Recovery of 'home-end' from tour data
#
# Author:      Vladimir Usyukov
#
# Created:     17/03/2015
# Copyright:   (c) Rocket 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import time, datetime
import csv
import distBearingGeodetic

#read *CSV files for processing
for root, dirs, files in os.walk("D:\gpsProject\projectData\OD_pairs"):
    for file in files:
        if file.endswith(".csv"):
            filepath = os.path.join(root, file)
            csvFile = open(filepath)
            #print "processing file ", csvFile

            #settings for OD pairs
            distThreshold = 150.
            sumLat, sumLong, count, flag = 0.,0.,0.,0

            #lists' definitions
            candidatesList = list()

            alldataList = list()
            alldataList.append(["Group", "Unit", "Date", "weekDate", "Time", "Seconds", "Lat", "Long", "Alt", "Speed", "Track", "tourEnd"])

            homeRecognitionList = list()
            homeRecognitionList.append(["Group", "Unit", "Date", "weekDate", "Time", "Seconds", "Lat", "Long", "Alt", "Speed", "Track", "tourEnd","Activity"])

            #find position of titles and strips of '\n' character from list
            headerLine = (csvFile.readline()).strip()
            valueList = headerLine.split(',')

            groupIndex = valueList.index("Group")
            unitIndex = valueList.index("Unit")
            dateIndex = valueList.index("Date")
            weekdateIndex = valueList.index("weekDate")
            timeIndex = valueList.index("Time")
            secondsIndex = valueList.index("Seconds")
            latValueIndex = valueList.index("Lat")
            longValueIndex = valueList.index("Long")
            altitudeIndex = valueList.index("Alt")
            speedIndex = valueList.index("Speed")
            trackIndex = valueList.index("Track")
            tourendIndex = valueList.index("tourEnd")

            #read first point
            tourStart = csvFile.readline()
            tourPoint = tourStart.split(',')

            pointGroup = int(tourPoint[groupIndex])
            pointUnit = int(tourPoint[unitIndex])
            pointDate = tourPoint[dateIndex]
            pointweekDate = tourPoint[weekdateIndex]
            pointTime = tourPoint[timeIndex]
            pointSeconds = tourPoint[secondsIndex]
            pointLat = float(tourPoint[latValueIndex])
            pointLong = float(tourPoint[longValueIndex])
            pointAltitude = float(tourPoint[altitudeIndex])
            pointSpeed = float(tourPoint[speedIndex])
            pointTrack = int(tourPoint[trackIndex])
            pointTour = int(tourPoint[tourendIndex])

            #save first point to alldata list
            alldataList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed, pointTrack, pointTour])

            #read first record
            rowList = csvFile.readlines()

            #insert csv points from data file and convert data to required format
            for row in rowList:
                row = row.split(',')

                nextpointGroup = int(row[groupIndex])
                nextpointUnit = int(row[unitIndex])
                nextpointDate = row[dateIndex]
                nextpointweekDate = row[weekdateIndex]
                nextpointTime = row[timeIndex]
                nextpointSeconds = row[secondsIndex]
                nextpointLat = float(row[latValueIndex])
                nextpointLong = float(row[longValueIndex])
                nextpointAltitude = float(row[altitudeIndex])
                nextpointSpeed = float(row[speedIndex])
                nextpointTrack = int(row[trackIndex])
                nextpointTour = int(row[tourendIndex])

                #save data to list
                alldataList.append([nextpointGroup, nextpointUnit, nextpointDate, nextpointweekDate, nextpointTime, nextpointSeconds, nextpointLat, nextpointLong,
                nextpointAltitude, nextpointSpeed, nextpointTrack, nextpointTour])

                #hypothesis 1: check trip ends of the same tour, same date
                if(pointDate==nextpointDate):

                    if(pointTour==nextpointTour) and (pointTour == 1):
                        geoValues = distBearingGeodetic.geodetic(pointLat,pointLong,nextpointLat,nextpointLong)
                        tourDistance = geoValues[0]

                        if(tourDistance < distThreshold):
                            candidatesList.append([pointLat, nextpointLat, pointLong, nextpointLong])
                        else:
                            pass #ignore unfinished tours
                    else:
                        pass #process only OD of a tour

                #new day data
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
                    pointTrack = nextpointTrack
                    pointTour = nextpointTour

            #find averageLat, averageLong for non-empty list
            try:
                for item in candidatesList:
                    sumLat = sumLat + item[0] + item[1]
                    sumLong = sumLong + item[2] + item[3]
                    count = count + 2.
                aveLat = sumLat/count
                aveLong = sumLong/count
                flag = 1

            except Exception:
                if not candidatesList:
                    print file, " - home-end can not be determined for this file"
                pass

            #last iteration to find home-end in all records
            if (flag):
                headerLine = alldataList[0]
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
                    elif nameValue == "Speed":
                        speedIndex = indexValue
                    elif nameValue == "Track":
                        trackIndex = indexValue
                    else:
                        #nameValue == "tourEnd":
                        tourendIndex = indexValue
                #print groupIndex, unitIndex, dateIndex,weekdateIndex, timeIndex,secondsIndex,latValueIndex,longValueIndex,altitudeIndex,speedIndex, trackIndex, tourendIndex

                for row in alldataList[1:]:

                    pointGroup = row[groupIndex]
                    pointUnit = row[unitIndex]
                    pointDate = row[dateIndex]
                    pointweekDate = row[weekdateIndex]
                    pointTime = row[timeIndex]
                    pointSeconds = row[secondsIndex]
                    pointLat = row[latValueIndex]
                    pointLong = row[longValueIndex]
                    pointAltitude = row[altitudeIndex]
                    pointSpeed = row[speedIndex]
                    pointTrack = row[trackIndex]
                    pointTrack = row[tourendIndex]

                    geoValues = distBearingGeodetic.geodetic(pointLat,pointLong,aveLat,aveLong)
                    tourDistance = geoValues[0]

                    if(tourDistance <distThreshold):
                        activityEnd = "Home"
                    else:
                        activityEnd = ""

                    homeRecognitionList.append([pointGroup, pointUnit, pointDate, pointweekDate, pointTime, pointSeconds, pointLat, pointLong, pointAltitude, pointSpeed, pointTrack, pointTour,activityEnd])

                #save home-acitivity end to file
                save_path = 'D:\gpsProject\projectData\Activity_End'
                fileName = file[:-4] + '_activity'
                completeName = os.path.join(save_path,fileName+".csv")

                with open(completeName, 'wb') as outcsv:
                    writer = csv.writer(outcsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
                    for item in homeRecognitionList:
                        #Write item to outcsv
                        writer.writerow([item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10], item[11], item[12]])
                outcsv.close()