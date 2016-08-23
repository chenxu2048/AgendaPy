from re import findall
class Date(object):
    def __init__(self, year = 0, month = 0, day = 0, hour = 0, minute = 0):
        self.__year = year
        self.__month = month
        self.__day = day
        self.__hour = hour
        self.__minute = minute
    @property
    def year(self):
        return self.__year
    @property
    def month(self):
        return self.__month
    @property
    def day(self):
        return self.__day
    @property
    def hour(self):
        return self.__hour
    @property
    def minute(self):
        return self.__minute
    @year.setter
    def year(self, year):
        self.__year = year
    @month.setter
    def month(self, month):
        self.__month = month
    @day.setter
    def day(self, day):
        self.__day = day
    @hour.setter
    def hour(self, hour):
        self.__hour = hour
    @minute.setter
    def minute(self, minute):
        self.__minute = minute
    def __str__(date):
        if isinstance(date, Date):
            return '%04d-%02d-%02d/%02d:%02d' % (date.__year, date.__month, date.__day, date.__hour, date.__minute)
    def stringToDate(str):
        date = Date()
        date_dict = findall(pattern="([\\d]{4})-([\\d]{2})-([\\d]{2})/([\\d]{2}):([\\d]{2})", string = str)
        if date_dict:
            date_dict = date_dict[0]
            date.year = date_dict[0]
            date.month = date_dict[1]
            date.day = date_dict[2]
            date.hour = date_dict[3]
            date.minute = data_dict[4]
        return date
    def __lt__(self, date):
        if isinstance(date, Date):
            return [self.year, self.month, self.day, self.hour, self.minute] < [date.year, date.month, date.day, date.hour, date.minute]
        else:
            return False;
    def __eq__(self, date):
        if isinstance(date, Date):
            return self.year == date.year and self.month == date.month and self.day == date.day and self.minute == date.minute and self.huor == date.hour
        else:
            return False
    def __ne__(self, date):
        if isinstance(date, Date):
            return not self == date
        else:
            return False
    def __le__(self, date):
        if isinstance(date, Date):
            return self == date and self < date
        else:
            return False
    def __gt__(self, date):
        if isinstance(date, Date):
            return self != date and (not self < date)
        else:
            return False
    def __ge__(self, date):
        if isinstance(date, Date):
            return self == date and self > date
        else:
            return False
    def isVaild(date):
        if isinstance(date, Date):
            if date.year % 400 == 0 or (date.year % 100 != 0 and date.year % 4 == 0):
                Date.__leapDict[date.month] = 29
            else:
                Date.__leapDict[date.month] = 28
            return date.year >= 1000 and date.year <= 9999 and date.month >= 1 and date.month <= 12 and date.day >= 1 and date.day <= Date.__leapDict[date.month] and date.hour >= 0 and date.hour <= 23 and date.minute >= 0 and date.minute <= 59
        else:
            return False
    __leapDict = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
