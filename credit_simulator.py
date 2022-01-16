from logging import error
import pandas as pd
import numpy as np
import functions as f
import uuid as u
from datetime import datetime
import random as r
import time as t
#import mysql.connector
from mysql.connector import Error

########################################################


# creates given number of new users. 
# new_users_count = 10000
# for x in range(new_users_count):
#     nu = f.newUser()
#     f.insert_new_customer(nu)
#     nu = []


for far in range(3600):
########################################################################################################################
#a for loop creates a set of new REQUESTS
    for x in range(3):
        nreq = f.newRequest() # a new request is created
        f.insert_new_request(nreq[:4]) # data assosiated with the generated request is being recorded to a MySQL table
        if nreq[2] == 0: #if request_result is 0 then continue
            m = f.newScoringRequest(nreq[1]) # eligibility check is being performed
            f.insert_new_scorring_request(m) # scorring data is recorded to the MySQL table
            c = f.newCreditProvision(m[:5]) # a new loan issuance record is generated
            f.insert_new_creditprovisionrequest(c) # loan issuance data is recoded to the MySQL table
            if c[4] != 'rejected':
                f.insert_new_debt(c[0],c[1],c[3],c[4],c[5],c[6],c[5]+c[6],datetime.now())  # a new debt is being registered in LOANS table
                balance = f.getBalance(c[1])
                new_balance = balance + c[5]
                f.adjustBalance(c[1],new_balance) # updates a balance of a pseudo customer            
            nreq = []
    #t.sleep(1)
########################################################################################################################

# a for loop creates a set of top-ups which in their turn trigger collection

    for x in range(8):
        nt = f.newRecharge() #generates a new pseudo top-up
        f.insert_new_topup(nt[0],nt[1],nt[2])
        f.adjustBalance(nt[0],nt[2]) # customer balance is being adjusted after top-up
        balance = f.getBalance(nt[0]) #nt[0] = CUSTOMERID
        debts = f.getDebtInfo(nt[0]) #nt[0] = CUSTOMERID
        if len(debts) > 0: 
            for debt in debts:
                if balance >= debt[6]:         #DEBIT,COLLECTIONDATETIME,CUSTOMERID,MESSAGEID,LOANTYPE,LOANAMOUNT,SERVICFEE,BALANCE,AMOUNTTOCHARGE,CHARGEDAMOUNT,RESULTSUBCODE
                    f.insert_newloancollection(debt[0],datetime.now(),debt[1],f.get_topup_messageid(debt[1]),debt[3],debt[4],debt[5],balance,debt[6],debt[6],1)
                    new_balance = balance - debt[6] #deducts the debt amount from balance
                    f.adjustBalance(debt[1],new_balance) 
                    f.move_to_loansarchive(debt[0],debt[1],debt[2],debt[3],debt[4],debt[5],debt[6],debt[7],1,datetime.now())
                    f.deleteDebt(debt[0])
                elif balance < debt[6]:
                    f.insert_newloancollection(debt[0],datetime.now(),debt[1],f.get_topup_messageid(debt[1]),debt[3],debt[4],debt[5],balance,debt[6],0,2)
                    f.updateLastCollectionAttempt(datetime.now(),debt[0])  #update last charging attempt in loans table
t.sleep(1)






















