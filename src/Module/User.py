# -*- coding: UTF-8 -*-
class User(object):
    def __init__(self, name, password, email, phone):
        self.__name = name
        self.__password = password
        self.__email = email
        self.__phone = phone
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, name):
        self.__name = name
    @property
    def password(self):
        return self.__password
    @password.setter
    def password(self, password):
        self.__password = password
    @property
    def email(self):
        return self.__email
    @email.setter
    def email(self, email):
        self.__email = eamil
    @property
    def phone(self):
        return phone
    @phone.setter
    def phone(self, phone):
        self.__phone = phone
