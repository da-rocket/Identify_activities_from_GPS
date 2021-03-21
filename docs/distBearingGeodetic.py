import math

def geodetic (llat1, llong1, llat2, llong2):
    try:
        """ Function returns geodetic distance and initial azimuth between two points.

            Arguments:
            llat1 - latitude for point 1
            llong1 - longitude for point 1
            llat2 - latitude for point 2
            llong2 - longitude for point 2

            Returns:
            Geodetic distance and initial azimuth
            
        """


        #pi - число pi, rad - радиус сферы (Земли)
        rad = 6372795

        #координаты двух точек
        #llat1 = 40
        #llong1 = -79

        #llat2 = 50
        #llong2 = -89

        #print type(llat1), type(llong1)
        

        #в радианах
        lat1 = float(llat1)*math.pi/180.
        long1 = float(llong1)*math.pi/180.        
        lat2 = float(llat2)*math.pi/180.
        long2 = float(llong2)*math.pi/180.
        

        #косинусы и синусы широт и разницы долгот
        cl1 = math.cos(lat1)
        cl2 = math.cos(lat2)
        sl1 = math.sin(lat1)
        sl2 = math.sin(lat2)
        delta = long2 - long1
        cdelta = math.cos(delta)
        sdelta = math.sin(delta)

        #вычисления длины большого круга
        y = math.sqrt(math.pow(cl2*sdelta,2)+math.pow(cl1*sl2-sl1*cl2*cdelta,2))
        x = sl1*sl2+cl1*cl2*cdelta
        ad = math.atan2(y,x)
        dist = ad*rad

        #вычисление начального азимута
        x = (cl1*sl2) - (sl1*cl2*cdelta)
        y = sdelta*cl2

        z = math.degrees(math.atan(-y/x))

        # для 3 и 4 четверти
        if (x < 0):
         z = z+180.

        z2 = (z+180.) % 360. - 180.
        z2 = - math.radians(z2)
        anglerad2 = z2 - ((2*math.pi)*math.floor((z2/(2*math.pi))) )
        angledeg = (anglerad2*180.)/math.pi

        #print 'Distance >> %.0f' % dist, ' [meters]'
        #print 'Initial bearing >> ', angledeg, '[degrees]'
        

        return dist, angledeg

    except Exception as e:
        return e
