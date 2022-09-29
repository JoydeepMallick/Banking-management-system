#main code


from code import banking_func as bf
import os,time,csv

bf.connect()#database connection
bf.database_creation()#database creation with table (if new)

##the belowgiven code's if part is executed if never the program was executed earlier

if not(os.path.isfile("acdetails.csv")):#checks if file present otherwise creates new file
    with open("acdetails.csv","w",newline='') as f:
        fw=csv.writer(f,delimiter=',')
        fw.writerow(["Ac. no.","Name","Age","DOB","phno","address","savings"])
else:
    c=os.path.dirname(os.path.realpath(__file__))+r"\acdetails.csv"
    bf.refresh_data(c)

while (True):
    time.sleep(2)
    print("\n\n\n")
    print("-"*16,"*"*16,"JSP BROTHERS AND CO. SAVINGS BANK","*"*16,"-"*16)
    print("="*102)
    print("\n\t\t\t\tWe provide security because we care.\n\n")
    print("\nNote :- A minimum of Rs. 2000.00 is mandatory to be deposited on opening new account.")
    print("Think before opening a new one.\n")
    ch=int(input("\n1. Create new account\n2. Withdraw\n3. Deposit\n4. Update personal info\
\n5. Check available balance\n6. Remove account\n7. Exit : "))
    if ch==1:
        bf.newac()
    elif ch==2:
        bf.transaction("withdraw")
    elif ch==3:
        bf.transaction("deposit")
    elif ch==4:
        bf.update()
    elif ch==5:
        acno=int(input("Dear customer,please enter your 12 digit account no. : "))
        if bf.search(acno):
            bf.display(acno)

        else:
            print("\nAccount number invalid!!!\n")
        
    elif ch==6:
        bf.removeac()
        
    elif ch==7:
        bf.rating()
        print("\nThanks for using our services.\nHave a nice day!\n")
        print("\\"*102)
        print("\n")
        print("/"*102,"\n\n")
        bf.closeall()
        break
    else:
        print("\nWrong choice!try again.\n ")
    
