"captcha coding"
#very simple one just adding some visualization to our code
import random


def captcha():
    r=random.randint(1000,9999)
    print("\nEnter the captcha carefully(for security reasons):-\n")
    #three unit space for each element in list(adjust space accordingly)
    dict={'1':['   ',' | ',' | '],'2':[' _ ',' _|','|__'],'3':['__ ','__|','__|'],\
         '4':['   ','|_|','  |'],'5':[' _ ','|_ ','__|'],'6':[' _ ','|_ ','|_|'],\
         '7':['__ ','  |','  |'],'8':[' _ ','|_|','|_|'],'9':[' _ ','|_|','  |'],\
         '0':[' _ ','| |','|_|']}
    for i in range(3):
        for j in str(r):
            print(dict[j][i],end=" ")
        print()
    
    

    entry(r)#calls the entry function
    
    return

def entry(num):
    while(True):
        ch=input("\nEnter captcha shown above\
(to refresh captcha press 'r' or 'R')\nAny other input will be considered invalid : ")
        if ch=='r' or ch=='R':
            
            captcha()
            break
        elif ch.isdigit():
            if int(ch)==num:
                break
##                return
            else:
                 print("\nPlease enter a valid input !\n ")
        else:
            print("\nPlease enter a valid input !\n ")
    
    

    
    
