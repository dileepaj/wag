import datetime

def serializeDatetime(dt):
    data = {
            'year' : dt.year,
            'month' : dt.month,
            'day' : dt.day,
            'hour' : dt.hour,
            'minute' : dt.minute
            }
    return data    

def deserializeDatetime(time):
    dt = datetime.datetime(time['year'], time['month'], time['day'], time['hour'], time['minute'])
    return dt

def formatDatetime(dt):
    strFormat = dt.ctime()
    return strFormat

