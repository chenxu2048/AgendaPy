# -*- coding: UTF-8 -*-
from .User import User
from datetime import datetime
class Meeting(object):
    def __init__(self, sponsor, participators, startDate, endDate, title):
        self.__sponsor = sponsor
        self.__participators = participators
        self.__startDate = startDate
        self.__endDate = endDate
        self.__title = title
    @property
    def sponsor(self):
        return self.__sponsor
    @sponsor.setter
    def sponsor(self, sponsor):
        self.__sponsor = sponsor
    @property
    def participators(self):
        return self.__participators
    @participators.setter
    def participators(self, participators):
        if isinstance(participators, list):
            self.__participators = participators
    @property
    def startDate(self):
        return self.__startDate
    @startDate.setter
    def startDate(self, startDate):
        if isinstance(startDate, datetime):
            self.__startDate = startDate
    @property
    def endDate(seld):
        return self.__endDate
    @endDate.setter
    def endDate(self, endDate):
        if isinstance(endDate, datetime):
            self.__endDate = endDate
    @property
    def title(self):
        return self.__title
    @title.setter
    def title(self, title):
        self.__title = title
    def isParticipator(self, user):
        if isinstance(user, User):
            return user in self.__participators
        else:
            return False
