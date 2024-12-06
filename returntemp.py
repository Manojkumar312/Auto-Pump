import MAX6675.MAX6675 as MAX6675



def qwerty():
    while True:
        sensor=MAX6675.MAX6675(25,24,18)
        Temp=sensor.readTempC()
        return(Temp)
        
