"simple bank management system"

#created by JSP BROTHERS

""""
    Primary functions include accepting deposits, withdrawl,new account entry,updating personal info 
    and checking available balance"""

import random,os,math,csv,time,datetime
import mysql.connector



def connect():###connection code

    global h
    h=input("\n\n\nEnter host name('localhost' in most cases) : ")
    global u 
    u=input("Enter user name(default user is 'root') : ")
    global pwd
    pwd=input("Enter your mysql password : ")

    c={"port":3306,"host":h,"user":u,"password":pwd}

    try:
        global con
        con=mysql.connector.connect(**c)#variable length keyword arguement
        if con.is_connected():
            print("\n\n\n")
            print("\\"*102)
            print("\t"*6,"(0) (0)")
            print("\t"*6,"  (_) ")
            print("/"*102)
    except:
        print("\nCouldn't connect to database!!!\n")
        print("Please re-enter your details carefully.\n\n")
        connect()



def database_creation():
    global myc
    myc=con.cursor()#cursor object created

    myc.execute("CREATE DATABASE IF NOT EXISTS JSP_BANKING")
    myc.execute("USE JSP_BANKING")

    s="CREATE TABLE IF NOT EXISTS bank(acno bigint(12) primary key,name varchar(40),age int(3),\
dob date,phno bigint(10),address varchar(50),savings decimal(15,2),created_on datetime)"

    myc.execute(s)#table created


def newac():#working#simple savings and withdrawl account
    
    lst=[]
    r=random.randint(100000000000,999999999999)    
    with open("acdetails.csv",'r',newline='') as f:
        fw=csv.reader(f,delimiter=',')
        temp_lst=[]#temporary storing of account no.
        for row in fw:
            if row!=[]:
                temp_lst.append(row[0])
        while(r in temp_lst):#new account no generator
            r=random.randint(100000000000,999999999999)
        lst.append(r)

    with open("acdetails.csv",'a',newline='') as f:
        fw=csv.writer(f,delimiter=',')
        print("\nEnter necessary details :- \n")
        
        lst.append(input("Enter your name : "))
        lst.append(0)#age to be filled later
        lst.append(input("Enter date of birth(yyyy-mm-dd) : "))
        lst.append(int(input("Enter 10-digit phone number : ")))
        lst.append(input("Enter address : "))
        print("\nA minimum of Rs. 2000.00 is to be deposited.\n")
        while (True):
            
            sa=int(input("Enter saving amount to be deposited in new account : Rs."))
            if sa>=2000.00:
                print("\nDeposit successful\n")
                break
            else:
                print("\nDeposit failed.Try again with an amount >=Rs.2000.00\n")
        lst.append(sa)
        lst.append(datetime.datetime.now())
        lst[2]=datetime.datetime.now().year-int(lst[3].split('-')[0])#always age gets updated with year

        fw.writerow(lst)#entering data into csv

    sqlentry="insert into bank values(%s,%s,%s,%s,%s,%s,%s,%s)"
    sqldata=tuple(lst)
    myc.execute(sqlentry,sqldata)
    con.commit()#data entered into database
                    
    print("\n\n","x"*20,"NEW ACCOUNT CREATED SUCESSFULLY!!!","x"*20,"\n\n")
    print("Please note down your account no. for future reference")
    display(r)#working




def search(acn):#ok working
    #some strange errors occur so everything recreated
    
    c={"password":pwd,"user":u,"host":h,"port":3306,"database":"JSP_BANKING"}
    con=mysql.connector.connect(**c)
    myc=con.cursor()
    
    s="select acno from bank"
    myc.execute(s)
    for i in myc:
        if i[0]==acn:
            return True
    return False



def update():#ok working

    acno=int(input("Dear customer,please enter your 12 digit account no. : "))
    
    if search(acno):
        display(acno)
        print()
        with open("acdetails.csv",'r',newline='') as f:
                fw=csv.reader(f,delimiter=',')
                mdlist=[]
                for row in fw:
                    mdlist.append(row)
                    if row[0]==str(acno):
                        k=mdlist.index(row)#stores index of that account which is to be changed
                        
                        
    
        ans='y'
        while(ans=='y'):
            ch=int(input("""\nPress to update:-
1. Your name
2. D.O.B.
3. Phone number
4. Address
Please enter your choice : """))

            #note all are string inputs
            #also note spacings in variable s wherein no space might cause error
            #printing s while coding is better(debugging purpose)
            
            if ch==1:
                mdlist[k][1]=input("Enter corrected name : ")
                s="UPDATE BANK SET NAME='"+mdlist[k][1]+"' WHERE ACNO="+str(mdlist[k][0])#ok
                myc.execute(s)
                con.commit()
            elif ch==2:
                mdlist[k][3]=input("Enter corrected date of birth in yyyy--mm-dd format : ")
                s="UPDATE BANK SET DOB='"+mdlist[k][3]+"' WHERE ACNO="+str(mdlist[k][0])#ok
                myc.execute(s)
                con.commit()
                
                age=datetime.datetime.now().year-int(mdlist[k][3].split('-')[0])
                mdlist[k][2]=age
                #age gets updated automatically when D.O.B. gets updated
                s="UPDATE BANK SET AGE="+str(age)+" WHERE ACNO="+str(mdlist[k][0])#ok
                myc.execute(s)
                con.commit()
            elif ch==3:
                mdlist[k][4]=input("Enter new phone number : ")
                s="UPDATE BANK SET PHNO="+mdlist[k][4]+" WHERE ACNO="+str(mdlist[k][0])#ok
                myc.execute(s)
                con.commit()
            elif ch==4:
                mdlist[k][5]=input("Enter new address : ")
                s="UPDATE BANK SET ADDRESS='"+mdlist[k][5]+"' WHERE ACNO="+str(mdlist[k][0])#ok
                myc.execute(s)
                con.commit()
            else:
                print("\nWrong choice!Try again.\n")
                
            ans=input("\nDo you want to update anything else?[y/n] : ")
        ###sql table updated
            
        with open("acdetails.csv",'w',newline='') as f:
            fw=csv.writer(f,delimiter=',')
            fw.writerows(mdlist)#overrides previous data with corrections
            print("\nData updated successfully!\n")
        ###csv file updated
            
    else:
        print("\nAccount number invalid!!!\n")



def display(acn):#ok working
    s="select * from bank where acno="+str(acn)
    myc.execute(s)
    for i in myc:
        print("\n","<"*100)
        print("DETAILS OF YOUR ACCOUNT HAVE BEEN APPENDED BELOW : -\n")
        print("\nName of customer : ",i[1])
        print("Account number : ",i[0])
        print("Age : ",i[2]," yrs.")
        print("D.O.B.(yyyy-mm-dd) : ",i[3])
        print("Phone no. : ",i[4])
        print("Address : ",i[5])
        print("Current balance : Rs.",i[6])
        print("Created on (yyyy-mm-dd hh:mm:ss format) : ",i[7])
        print(">"*100)
        time.sleep(6)
        

        
def transaction(trans):
    
    acno=int(input("Dear customer,please enter your 12 digit account no. : "))
    
    if search(acno):
        
        print()
        with open("acdetails.csv",'r',newline='') as f:
                fw=csv.reader(f,delimiter=',')
                mdlist=[]
                for row in fw:
                    mdlist.append(row)
                    if row[0]==str(acno):
                        k=mdlist.index(row)
        if trans=="deposit":
            dep=float(input("\nEnter the amount you want to deposit : Rs."))
            mdlist[k][6]=float(mdlist[k][6])+dep

        elif trans=="withdraw":#ok working
            while(True):
                print("\nNote :- To maintain your account an amount of at least Rs 2000.00\
 must be present.\nIn order to withdraw more or the entire ammount from our bank you must remove \
your account permanently from our system.\n")
                w=float(input("\nEnter the amount you want to withdraw : Rs."))
                
                if w<=(float(mdlist[k][6])-2000.00):
                    
                    from code import captcha
                    captcha.captcha()#working
                    print("\n\nVerified! Proceeding to withdraw",end="")
                    for i in range(10):
                        print(".",end='')
                        time.sleep(0.2)
                    print()
                    mdlist[k][6]=float(mdlist[k][6])-w
                    break
                else:
                    print("\nAvailable balance low!!!Unable to withdraw\n")
                    print("Total balance : Rs.",mdlist[k][6])
                    print("Account maintainence balance : Rs.2000.00(mandatory,cant be withdrawn)")
                    print("Available withdrawl balance : Rs.",float(mdlist[k][6])-2000.00)
                    ch=input("\nTo withdraw a lesser amount press 'y' or 'Y'\nTo cancel transaction \
press enter or any other key : ")
                    if ch in ['y','Y']:
                        continue
                    else:
                        print("\nTransaction cancelled!!!\n")
                        return
                        

        s="UPDATE BANK SET SAVINGS="+str(mdlist[k][6])+" WHERE ACNO="+str(mdlist[k][0])#ok
        myc.execute(s)
        con.commit()#database updated

        with open("acdetails.csv",'w',newline='') as f:
            fw=csv.writer(f,delimiter=',')
            fw.writerows(mdlist)#overrides previous data with corrections
            print("\nSavings account has been updated successfully!\n")
        ###csv file updated

    else:
        print("\nAccount number invalid!!!\n")


def removeac():
    acno=int(input("Dear customer,please enter your 12 digit account no. : "))
    
    if search(acno):
        
        print()
        with open("acdetails.csv",'r',newline='') as f:
                fw=csv.reader(f,delimiter=',')
                mdlist,delac=[],[]
                for row in fw:
                    if row[0]!=str(acno):
                        mdlist.append(row)
                    else:
                        delac=row
        ch=input("Are you sure to remove your account?\nOnce performed this cannot be reverted back!\
\nPress 'y' or 'Y' for yes or any other key or enter to cancel process : ")
        if ch in ['y','Y']:
            s="DELETE FROM BANK WHERE ACNO="+str(acno)
            myc.execute(s)
            con.commit()#row deleted from database
        else:
            print("\nTransaction cancelled!!!\n")
            return

        with open("acdetails.csv",'w',newline='') as f:
            fw=csv.writer(f,delimiter=',')
            fw.writerows(mdlist)#overrides previous data with corrections
            print("\nAccount has been removed successfully!\n")
        ###csv file updated row deleted    
        print("<"*100,"\nAccount holder(discontinued) : ",delac[1])
        print("Current balance : Rs.",delac[6])
        print("Received amount : Rs.",delac[6])
        print(">"*100,"\n\nThanks for being such a loyal customer.\nHope you enjoyed our services.\n")
    else:
        print("\nAccount number invalid!!!\n")


def refresh_data(path_csv):#under construction
    """this code basically focusses on machine independencency of account holders
so that their details are not lost on migrating to another system"""

    path_csv.replace(r"\\",r"\\\\")#raw path of acdetails.csv stored

    if os.path.isfile(path_csv):#already being checked in execute_me.py but done again to recheck
        print("\nRefreshing system.Please have patience",end="")
        for i in range(7):
            print(".",end="")
            time.sleep(0.3)
        print()
    s="SELECT * FROM BANK"
    myc.execute(s)
    lst=[]
    for i in myc:
        lst.append(i[0])#stores account no. (if any) present in bank table

    with open(path_csv,"r",newline='') as f:
        fw=csv.reader(f,delimiter=',')
        for i in fw:
            if  i[0]!="Ac. no." and int(i[0]) not in lst:#2nd condition prevents 1st row(heading) from execution
                s="insert into bank values(%s,%s,%s,%s,%s,%s,%s,%s)"
                myc.execute(s,i)
                con.commit()#missing data written from csv to bank table
                

def rating():#ok working
    ##review on our banking system

    ch=input("\nWould you mind to spare a minute to rate our services?\nyes->press 'y'\
 or 'Y'\nno->press any other key or enter :")
    if ch in ['Y',"y"]:

        path_rate=os.path.dirname(os.path.realpath(__file__))+r"\ratings.txt"
        path_rate.replace(r"\\",r"\\\\")#raw path of ratings.txt stored
        
        if os.path.isfile(path_rate):
            with open(path_rate,"r") as f:
                r=f.readline()
                
                print("\nRating history of other customer(s) :-\n(time shown below beside rating \
of individual customer follows year-month-day hour:minute:second.microsecond format)\n")
                while(r):
                    lst=r.split(',')
                    if lst[0]!="":
                        print(lst[0]," rated ",lst[1]," out of 5 stars on ",lst[2])
                    else:
                        print("A user has rated ",lst[1]," out of 5 stars on ",lst[2])
                    if lst[3]!="":
                        print("Comments : ",lst[3])
                    else:
                        print("No comments received.")
                    r=f.readline()
                    print("\n\n")
        else:
            with open(path_rate,"w") as f:
                print("\nBe the first one in the list to review our services!\n")
                
        with open(path_rate,"a") as f:
            lst=[]
            lst.append(input("Enter your name(or nicname)\nDont worry your identity will remain\
 hidden : "))
            while(True):
                rate=int(input("\nEnter your rating between 1 to 5(both inclusive)\n(any other number\
 will be considered invalid) : "))
                if rate in range(1,6):
                    break
                else:
                    print("\nInvalid input!\n")
            lst.append(rate)
            lst.append(datetime.datetime.now())
            lst.append(input("\nEnter your comments(if not any simply press enter) : "))
            
            f.write(lst[0]+','+str(lst[1])+','+str(lst[2])+','+lst[3]+','+"\n")
            

    else:
        return
            

    
def closeall():#ok working
    con.close()
    myc.close()
        
