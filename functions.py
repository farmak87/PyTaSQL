import uuid as u
import random as r
from datetime import datetime
import datetime as d
import mysql.connector
import pandas as pn

username = 'pytasql'
pswrd = 'PyTaSQL@'

################################################################## 

def newUser():
#returns a new pseudo users
    id = u.uuid4()
    aDate = randomDate()
    daysOnNetwork = (datetime.date(datetime.now()) - aDate).days
    c30days = r.randrange(0,100,2)
    if daysOnNetwork <=30: #checks whether a customer age is less than 30 
        c90days = c30days 
    else:
        c90days = r.randrange(0,500,2) + c30days
    lastTopUp = randomTopUpDate()
    balance = r.randrange(0,100,1)
    nu = [str(id),aDate,daysOnNetwork,c30days,c90days,lastTopUp,balance]
    return nu

#################################################################

def newRecharge():
#returns a new recharge 
    customerid = get_rand_customerid()
    recharge_datetime = datetime.now()
    recharge_amount = r.randrange(1,20,1)
    nr = [str(customerid), recharge_datetime,recharge_amount]
    return nr

#################################################################

def newRequest():
#returns a new request which then is being recorded to the requestservice table
#request_datetime,str(customerid),request_result,request_content
    request_datetime = datetime.now()
    customerid = get_rand_customerid()
    request_result = r.randrange(0,2,1)
    request_content = 'request' # ideally there shall be a request content, but for now it remains 'request'
    new_request = [request_datetime,str(customerid),request_result,request_content]
    return new_request
  
#################################################################
    
#generates a new scoring request

def newScoringRequest(CUSTOMERID):
#messageID, custID, loantype, loanamount, resultcode, scorringdatetime    
    messageID = get_messageid(CUSTOMERID)
    custID = CUSTOMERID
    scorringdata = get_scoring_data(CUSTOMERID)
    loandata = scoring(scorringdata[0],scorringdata[1],scorringdata[2])
    if loandata[1] == 0:
        loantype = loandata[0]
    else:
        loantype = 'rejected'
    loanamount = loandata[2]
    resultcode = loandata[1]
    scorringdatetime = datetime.now()
    ns = [messageID, custID, loantype, loanamount, resultcode, scorringdatetime]
    return ns

#################################################################

#generates new loan provision request
def newCreditProvision(cred_prov):
    #MESSAGEID, CUSTOMERID, LOANTYPE, LOANAMOUNT, RESULTCODE
    mesID = cred_prov[0]
    custID = cred_prov[1]
    debtid = get_debtid(custID, mesID)
    debtdatetime = datetime.now()
    ltype = cred_prov[2]
    lamount = cred_prov[3]
    sfee = lamount*0.2
    rcode = cred_prov[4]
    cp = [debtid,custID,mesID,debtdatetime,ltype,lamount,sfee,rcode]
    return cp

#################################################################

# returns a random date between given boundaries
def randomDate():
    startDate = d.date(2018,1,1)
    endDate = d.date(2021,12,20)
    timeBetweenDates = endDate - startDate
    daysBetweenDates = timeBetweenDates.days
    randomNumberOfDays = r.randrange(daysBetweenDates)
    return startDate + d.timedelta(days = randomNumberOfDays)

# returns a random pseudo recharge date between given boundaries
def randomTopUpDate():
    startDate = d.date(2021,6,1)
    endDate = d.date(d.datetime.now().year,d.datetime.now().month,d.datetime.now().day)
    timeBetweenDates = endDate - startDate
    daysBetweenDates = timeBetweenDates.days
    randomNumberOfDays = r.randrange(daysBetweenDates)
    return startDate + d.timedelta(days = randomNumberOfDays)

########################################################

def scoring(aon,c30,c90):
    response = ''
    resultcode = 0
    amount = 0
    if aon <= 30:
        response = 'Network age is less than 30'
        resultcode = 1
        amount = 0
    elif aon <= 60 and c30 < 4 and c90 < 20:
        response = 'Needs more top-up and network age'
        resultcode = 2
        amount = 0
    elif aon <= 90 and c30 < 2 and c90 < 20:
        response = 'Needs more top-up and network age'
        resultcode = 2
        amount = 0
    elif aon > 90 and c30 <= 15:
        response = 'Needs more top-up'
        resultcode = 3
        amount = 0
    elif aon > 180 and c30 > 100 and c90 > 200:
        response = 'C15'
        resultcode = 0
        amount = 15
    elif aon > 150 and c30 > 90 and c90 > 150:
        response = 'C10'
        resultcode = 0
        amount = 10
    elif aon > 100 and c30 > 50 and c90 > 100:
        response = 'C5'
        resultcode = 0
        amount = 5
    elif aon > 90 and c30 > 30 and c90 > 60:
        response = 'C2'
        resultcode = 0
        amount = 2
    elif aon > 90 and c30 > 15 and c90 > 30:
        response = 'C1'
        resultcode = 0
        amount = 1
    else:
        response = 'needs investingation'
        resultcode = 4
        amount = 0

    sresult = [response, resultcode, amount]
    return sresult  
        

###################################################################
# the below function was not written by us, taken from the internet
# it establishes connection to MYSQL, inserts the values to the table and then closes the connection 
def insert_new_customer(CUSTOMERID, ACTIVATIONDATE, DAYSONNETWORK, CUMULATIVE30DAYS, CUMULATIVE90DAYS, LASTRECHARGEDATETIME,BALANCE):
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_insert_query = """INSERT INTO customers (CUSTOMERID, ACTIVATIONDATE, DAYSONNETWORK, CUMULATIVE30DAYS, CUMULATIVE90DAYS, LASTRECHARGEDATETIME, BALANCE) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s) """

        record = (CUSTOMERID, ACTIVATIONDATE, DAYSONNETWORK, CUMULATIVE30DAYS, CUMULATIVE90DAYS, LASTRECHARGEDATETIME, BALANCE)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record inserted successfully into CUSTOMERS table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")

######################################################### 

def get_rand_customerid():
# returns a random customerid 
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_insert_query = """SELECT CUSTOMERID FROM customers ORDER BY RAND() LIMIT 1 """

        cursor.execute(mySql_insert_query)
        record = cursor.fetchone()
        rand_customer_id = record[0]

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")

    return rand_customer_id

############################################################### 

def insert_new_topup(CUSTOMERID, RECHARGEDATETIME, RECHARGEAMOUNT):
# adds a new recharge to the table and then closes the connection
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_insert_query = """INSERT INTO recharges (CUSTOMERID, RECHARGEDATETIME, RECHARGEAMOUNT) 
                                VALUES (%s, %s, %s) """

        record = (CUSTOMERID, RECHARGEDATETIME, RECHARGEAMOUNT)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record inserted successfully into RECHARGES table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")


# def insert_new_request(REQUESTDATETIME, CUSTOMERID, REQUESTRESULT, REQUESTCONTENT):
# # adds a new request to the table and then closes the connection
#     try:
#         connection = mysql.connector.connect(host='127.0.0.1',
#                                             database='pytasql',
#                                             user=username,
#                                             password=pswrd)
#         cursor = connection.cursor()    
#         mySql_insert_query = """INSERT INTO requestservice (REQUESTDATETIME, CUSTOMERID, REQUESTRESULT, REQUESTCONTENT) 
#                                 VALUES (%s, %s, %s, %s) """

#         record = (REQUESTDATETIME, CUSTOMERID, REQUESTRESULT, REQUESTCONTENT)
#         cursor.execute(mySql_insert_query, record)
#         connection.commit()
#         print("Record inserted successfully into REQUESTS table")

#     except mysql.connector.Error as error:
#         print("Failed to insert into MySQL table {}".format(error))

#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()
#             #print("MySQL connection is closed")

####################################################################################################

def insert_new_request(request): # adds a new request to the table and then closes the connection
#[REQUESTDATETIME, CUSTOMERID, REQUESTRESULT, REQUESTCONTENT]

    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_insert_query = """INSERT INTO requestservice (REQUESTDATETIME, CUSTOMERID, REQUESTRESULT, REQUESTCONTENT) 
                                VALUES (%s, %s, %s, %s) """

        record = (request[0], request[1], request[2], request[3])
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record inserted successfully into REQUESTS table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")

####################################################################################################

def get_scoring_data(CUSTOMERID):
# returns inputs for scoring for indicated customerid 
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_insert_query = """SELECT DAYSONNETWORK, CUMULATIVE30DAYS,CUMULATIVE90DAYS FROM customers WHERE CUSTOMERID = %s """
        cID = CUSTOMERID    

        cursor.execute(mySql_insert_query,(cID,))
        record = cursor.fetchone()
        aon = record[0]
        c30 = record[1]
        c90 = record[2]

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")

    return aon,c30,c90

###############################################################

def get_messageid(CUSTOMERID):
# returns a messageid from requestservice for scorringservice 
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_insert_query = """SELECT max(messageid) FROM requestservice WHERE CUSTOMERID = %s """
        cID = CUSTOMERID    

        cursor.execute(mySql_insert_query,(cID,))
        record = cursor.fetchone()
        messageid = record[0]
        
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")

    return messageid

###################################################################

def insert_new_scorring_request(scorring_req):
# adds a new request to the table and then closes the connection
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_insert_query = """INSERT INTO scorringservice (MESSAGEID, CUSTOMERID, LOANTYPE, LOANAMOUNT, RESULTCODE, SCORRINGDATETIME) 
                                VALUES (%s, %s, %s, %s, %s, %s) """
                #MESSAGEID, CUSTOMERID, LOANTYPE, LOANAMOUNT, RESULTCODE, SCORRINGDATETIME
        record = (scorring_req[0], scorring_req[1], scorring_req[2], scorring_req[3], scorring_req[4], scorring_req[5])
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record inserted successfully into SCORRINGSERVICE table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")

################################################################

def get_debtid(CUSTOMERID, MESSAGEID):
# returns a debtid from scorringservice for creditprovisionservice 
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_insert_query = """SELECT debtid FROM scorringservice WHERE CUSTOMERID = %s AND MESSAGEID = %s """
        cID = CUSTOMERID
        mID = MESSAGEID    

        cursor.execute(mySql_insert_query,(cID,mID,))
        record = cursor.fetchone()
        debtid = record[0]
        
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")

    return debtid

###################################################################

def insert_new_creditprovisionrequest(cprequest):
# adds a new request to the table and then closes the connection
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_insert_query = """INSERT INTO loanprovisionservice (DEBTID,CUSTOMERID,MESSAGEID, LOANDATETIME, LOANTYPE, LOANAMOUNT, SERVICEFEE, RESULTCODE) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """
        #DEBTID,CUSTOMERID,MESSAGEID, LOANDATETIME, LOANTYPE, LOANAMOUNT, SERVICEFEE, RESULTCODE
        #
        record = (cprequest[0],cprequest[1],cprequest[2], cprequest[3], cprequest[4], cprequest[5], cprequest[6], cprequest[7])
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record inserted successfully into LOANPROVISIONSERVICE table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")


###################################################################
def insert_new_debt(DEBTID,CUSTOMERID, LOANDATETIME, LOANTYPE, LOANAMOUNT, SERVICEFEE, PRESENTAMOUNT,LASTCOLLECTIONATTEMPT):
# adds a new request to the table and then closes the connection
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_insert_query = """INSERT INTO loans (DEBTID,CUSTOMERID, LOANDATETIME, LOANTYPE, LOANAMOUNT, SERVICEFEE, PRESENTAMOUNT,LASTCHARGINGATTEMPT) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """

        record = (DEBTID,CUSTOMERID, LOANDATETIME, LOANTYPE, LOANAMOUNT, SERVICEFEE, PRESENTAMOUNT,LASTCOLLECTIONATTEMPT)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record inserted successfully into LOANS table")

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")


def getBalance(CUSTOMERID):
#returns customer balance
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_insert_query = """SELECT BALANCE FROM customers WHERE CUSTOMERID = %s """
        cID = CUSTOMERID
            

        cursor.execute(mySql_insert_query,(cID,))
        record = cursor.fetchone()
        balance = record[0]
        
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")

    return balance


def adjustBalance(CUSTOMERID,ADJAMOUNT):
#adjusts customer balance either negative or positive        
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_insert_query = """UPDATE customers SET BALANCE = %s WHERE CUSTOMERID = %s"""

        record = (ADJAMOUNT, CUSTOMERID)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Balance sucessfully adjusted")

    except mysql.connector.Error as error:
        print("Failed to updated customer balance {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")


def getDebtInfo(CUSTOMERID):
#returns customer's debt info
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_query = """SELECT * FROM pytasql.loans WHERE CUSTOMERID =%s ORDER BY LOANDATETIME desc"""
        cID = CUSTOMERID
            
        cursor.execute(mySql_query,(cID,))
        record = cursor.fetchall()
                 
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")

    return record



def deleteDebt(DEBTID):
   #deletes debt from loans table        
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_insert_query = """DELETE FROM loans WHERE DEBTID = %s"""

        record = (DEBTID)
        cursor.execute(mySql_insert_query, (record,))
        connection.commit()
        print("Debt sucessfully deleted")

    except mysql.connector.Error as error:
        print("Failed to delete debt {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed") 


def move_to_loansarchive(DEBTID,CUSTOMERID, LOANDATETIME, LOANTYPE, LOANAMOUNT, SERVICEFEE, PRESENTAMOUNT,LASTCOLLECTIONATTEMPT,ARCHIVEREASON,ARCHIVEDATETIME):
# adds a new record to the loancollection table
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_insert_query = """INSERT INTO loansarchive (DEBTID,CUSTOMERID, LOANDATETIME, LOANTYPE, LOANAMOUNT, SERVICEFEE, PRESENTAMOUNT,LASTCHARGINGATTEMPT,ARCHIVEREASON,ARCHIVEDATE) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

        record = (DEBTID,CUSTOMERID, LOANDATETIME, LOANTYPE, LOANAMOUNT, SERVICEFEE, PRESENTAMOUNT,LASTCOLLECTIONATTEMPT,ARCHIVEREASON,ARCHIVEDATETIME)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record inserted successfully into LOANSARCHIVE table")

    except mysql.connector.Error as error:
        print("Failed to insert into LOANSARCHIVE table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")
   

def insert_newloancollection(DEBTID,COLLECTIONDATETIME,CUSTOMERID, MESSAGEID, LOANTYPE, LOANAMOUNT, SERVICEFEE, BALANCE,AMOUNTTOCHARGE,CHARGEDAMOUNT,RESULTCODE):
# adds a new record to the loancollection table
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_insert_query = """INSERT INTO loancollectionservice (DEBTID,COLLECTIONDATETIME,CUSTOMERID, MESSAGEID, LOANTYPE, LOANAMOUNT, SERVICEFEE, BALANCE,AMOUNTTOCHARGE,CHARGEDAMOUNT,RESULTCODE) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """

        record = (DEBTID,COLLECTIONDATETIME,CUSTOMERID, MESSAGEID, LOANTYPE, LOANAMOUNT, SERVICEFEE, BALANCE,AMOUNTTOCHARGE,CHARGEDAMOUNT,RESULTCODE)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Record inserted successfully into LOANCOLLECTIONSERVICE table")

    except mysql.connector.Error as error:
        print("Failed to insert into LOANCOLLECTIONSERVICE table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")


def get_topup_messageid(CUSTOMERID):
# returns a messageid from recharges table for loancollectionservice 
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_insert_query = """SELECT max(messageid) FROM recharges WHERE CUSTOMERID = %s """
        cID = CUSTOMERID    

        cursor.execute(mySql_insert_query,(cID,))
        record = cursor.fetchone()
        messageid = record[0]
        
    except mysql.connector.Error as error:
        print("Failed to get MESSAGEID from RECHARGES table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")

    return messageid

#######################################################################################

def updateLastCollectionAttempt(DATETIME, DEBTID):
#updates last charging attempt datetime in loans table for failed collection cases        
    try:
        connection = mysql.connector.connect(host='127.0.0.1',
                                            database='pytasql',
                                            user=username,
                                            password=pswrd)
        cursor = connection.cursor()    
        mySql_insert_query = """UPDATE loans SET LASTCHARGINGATTEMPT = %s WHERE DEBTID = %s"""

        record = (DATETIME, DEBTID)
        cursor.execute(mySql_insert_query, record)
        connection.commit()
        print("Last collection attempt sucessfully updated")

    except mysql.connector.Error as error:
        print("Failed to update last collection attempt {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            #print("MySQL connection is closed")