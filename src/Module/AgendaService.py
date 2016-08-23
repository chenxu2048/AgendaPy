# -*- coding: UTF-8 -*-
from datetime import datetime
import torndb
import MySQLdb

class AgendaService(object):
    def __init__(self, db):
        if isinstance(db, torndb.Connection):
            self.__db = db
    @property
    def database(self):
        return self.__db
    @database.setter
    def database(self, db):
        if isinstance(db, torndb.Connection):
            self.__db = db
    def logIn(self, **userinfo):
        #userinfo 是一个字典，键值为
        #'username' => 用户名(str)
        #'password' => 密码(str)
        store = self.__db.query('SELECT * FROM user WHERE username = %s AND password = %s', userinfo['username'], userinfo['password'])
        if store:
            return True
        else:
            return False
    def deleteUser(self, **userinfo):
        #需要提供用户密码才能删除
        db = self.__db
        db.execute('LOCK TABLE user READ, meeting READ, meetingMember READ')
        store = db.query('SELECT userId AS id FROM user WHERE username = %s AND password = %s', userinfo['username'], userinfo['password'])
        if store:
            delMeeting = db.query('SELECT meetingId AS id FROM meetingMember WHERE userId = %s', store[0]['id'])
            db.execute('LOCK TABLE user WRITE, meeting WRITE, meetingMember WRITE')
            for row in delMeeting:
                db.execute('DELETE FROM meeting WHERE meetingId = %s', row['id'])
            db.execute('DELETE FROM user WHERE userId = %s', store[0]['id'])
            status = True
        else:
            status = False
        db.execute('UNLOCK TABLE')
        return status
    def userRegister(self, **userinfo):
        #userinfo 是注册用户信息表
        #'username' => 用户名
        #'password' => 密码md5
        #'email' => 邮箱
        #'phone' => 电话
        db = self.__db
        try:
            db.execute('INSERT user(username, password, email, phone) VALUE(%s, %s, %s, %s)', userinfo['username'], userinfo['password'], userinfo['email'], userinfo['phone'])
        except MySQLdb.IntegrityError, error:
            return False
        except:
            return False
        return True
    def listAllUsers(self):
        store = self.__db.query('SELECT username AS username, email AS email, phone AS phone FROM user')
        return store
    def listAllMeetings(self, username):
        store = self.__db.query('SELECT startDate, endDate, title, userMeeting.role FROM meeting INNER JOIN (SELECT meetingMember.role AS role, meetingMember.meetingId AS meetingId FROM user INNER JOIN meetingMember ON user.userId = meetingMember.userId WHERE username=%s) AS userMeeting ON meeting.meetingId = userMeeting.meetingId', username)
        for meet in store:
            meet['startDate'] = str(meet['startDate'])
            meet['endDate'] = str(meet['endDate'])
        return store
    def listAllSponsorMeetings(self, username):
        store = self.__db.query("SELECT startDate, endDate, title FROM meeting INNER JOIN (SELECT meetingMember.meetingId AS meetingId FROM user INNER JOIN meetingMember ON user.userId = meetingMember.userId WHERE username=%s AND role='sponsor') AS userMeeting ON meeting.meetingId = userMeeting.meetingId ORDER BY startDate", username)
        for meet in store:
            meet['startDate'] = str(meet['startDate'])
            meet['endDate'] = str(meet['endDate'])
        return store
    def listAllParticipateMeetings(self, username):
        store = self.__db.query("SELECT startDate, endDate, title FROM meeting INNER JOIN (SELECT meetingMember.meetingId AS meetingId FROM user INNER JOIN meetingMember ON user.userId = meetingMember.userId WHERE username=%s AND role='participator') AS userMeeting ON meeting.meetingId = userMeeting.meetingId ORDER BY startDate", username)
        for meet in store:
            meet['startDate'] = str(meet['startDate'])
            meet['endDate'] = str(meet['endDate'])
        return store
    def getMeetingInfo(self, meetingTitle):
        store = self.__db.query('SELECT meetingId, startDate, endDate, title FROM meeting WHERE title = %s', meetingTitle)
        if store:
            store = store[0]
        else:
            return {}
        allPeople = self.__db.query('SELECT username, role FROM user INNER JOIN meetingMember ON user.userId = meetingMember.userId WHERE meetingMember.meetingId = %s', store.pop('meetingId'))
        participators = []
        for person in allPeople:
            if person['role'] == 'participator':
                participators.append(person['username'])
            else:
                store['sponsor'] = person['username']
        store['participators'] = participators
        store['startDate'] = str(store['startDate'])
        store['endDate'] = str(store['endDate'])
        return store

    def deleteMeeting(self, username, meetingList):
        status = False
        for meet in meetingList:
            if self.__db.query("SELECT meeting.meetingId AS meetingId FROM meeting INNER JOIN (SELECT meetingMember.meetingId AS meetingId, username FROM user INNER JOIN meetingMember ON user.userId = meetingMember.userId WHERE username=%s AND role='sponsor') AS userMeeting ON meeting.meetingId = userMeeting.meetingId AND meeting.title = %s", username, meet):
                self.__db.execute('DELETE FROM meeting WHERE title = %s', meet)
                status = True
        return status
    def deleteAllMeeting(self, username):
        meeting = self.__db.query("SELECT meetingMember.meetingId FROM meetingMember INNER JOIN user ON meetingMember.userId = user.userId WHERE user.username = %s AND meetingMember.role = 'sponsor'", username)
        for meet in meeting:
            self.__db.execute("DELETE FROM meeting WHERE meetingId = %s", meet['meetingId'])

    def updateUser(self, prevUsername, prevPassword, **kwparam):
        store = self.__db.query('SELECT userId FROM user WHERE username = %s AND password = %s', prevUsername, prevPassword)
        if store and kwparam:
            count = 0
            sql = 'UPDATE user SET '
            for item in kwparam.items():
                if item[1]:
                    count += 1
                    sql += item[0] + "='" + item[1].replace("'", "\\'") + "', "
            sql = sql[0:len(sql)-2] + 'WHERE username = %s'
            #print sql
            if count:
                self.__db.execute(sql, prevUsername)
                return True
        return False
    def queryMeeting(self, username, **kwparam):
        store = self.__db.query('SELECT userId FROM user WHERE username = %s', username)
        if not store:
            return []
        userId = store[0]['userId']
        if 'title' in kwparam:
            store = self.__db.query("SELECT startDate, endDate, title FROM meeting INNER JOIN meetingMember ON meeting.meetingId = meetingMember.meetingId WHERE title = %s and meetingMember.userId = %s", kwparam['title'], userId)
        elif 'startDate' in kwparam and 'endDate' in kwparam:
            store = self.__db.query("SELECT startDate, endDate, title FROM meeting INNER JOIN meetingMember ON meeting.meetingId = meetingMember.meetingId WHERE meeting.startDate <= %s AND meeting.endDate >= %s AND meetingMember.userId = %s", kwparam['endDate'], kwparam['startDate'], userId)
        else:
            return []
        for meet in store:
            meet['startDate'] = str(meet['startDate'])
            meet['endDate'] = str(meet['endDate'])
        return store
    def createMeeting(self, **kwparam):
        if self.__db.query('SELECT meetingId FROM meeting WHERE title = %s', kwparam['title']):
            #print 'a'
            return False
        if kwparam['startDate'] >= kwparam['endDate'] or not kwparam['participators'] or len(kwparam['participators']) != len(set(kwparam['participators'])) or kwparam['sponsor'] in kwparam['participators']:
            #print 'b'
            return False
        self.__db.execute("LOCK TABLE user READ, meeting READ, meetingMember READ")
        allConflictMeeting = self.__db.query('SELECT meetingMember.userId as userId FROM meeting INNER JOIN meetingMember ON meeting.meetingId = meetingMember.meetingId WHERE startDate < %s and endDate > %s', kwparam['endDate'], kwparam['startDate'])
        userId = self.__db.query('SELECT userId FROM user WHERE username = %s', kwparam['sponsor'])
        if (not userId) or userId[0] in allConflictMeeting:
            #print allConflictMeeting
            self.__db.execute("UNLOCK TABLE")
            #print 'c', userId
            return False
        participatorsId = []
        for part in kwparam['participators']:
            partId = self.__db.query('SELECT userId FROM user WHERE username = %s', part)
            if not partId:
                self.__db.execute("UNLOCK TABLE")
                #print 'd'
                return False
            else:
                participatorsId.append(partId[0])
        for i in participatorsId:
            if i in allConflictMeeting:
                self.__db.execute('UNLOCK TABLE')
                #print 'e'
                return False
        self.__db.execute('LOCK TABLE user WRITE, meeting WRITE, meetingMember WRITE')
        self.__db.insert('INSERT meeting(title, startDate, endDate) VALUE(%s, %s, %s)', kwparam['title'], kwparam['startDate'], kwparam['endDate'])
        meetingId = self.__db.query('SELECT meetingId FROM meeting WHERE title = %s', kwparam['title'])[0]['meetingId']
        #print userId, meetingId
        self.__db.insert('INSERT meetingMember(userId, meetingId, role) VALUE(%s, %s, "sponsor")', userId[0]['userId'], meetingId)
        for i in participatorsId:
            #print participatorsId
            self.__db.insert('INSERT meetingMember(userId, meetingId) VALUE(%s, %s)', i['userId'], meetingId)
        self.__db.execute('UNLOCK TABLE')
        return True
    def queryUser(self, **userinfo):
        count = 0
        sql = 'SELECT username, email, phone FROM user WHERE '
        for item in userinfo.items():
            if item[1]:
                count += 1
                sql += item[0] + "='" + item[1].replace("'", "\\\'") + "' AND "
        if count:
            sql = sql[0:len(sql) - 4]
            #print sql
            return self.__db.query(sql)
        else:
            return []
