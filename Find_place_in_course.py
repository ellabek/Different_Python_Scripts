import mechanize
import re
import time

####################################################functions
def get_number(my_str):
    ##do here a loop that finds the first ">" and after here adds all strings until "<"
    txt=my_str
    number = ( re.findall("[^<>]*" , txt )[3])
    return number

def make_some_noise():
    for x in range(0, 20):
        print '\a'
######################################################

print "Hi! you will now need to enter some details, please make sure you are entering a valid course and group numbers because otherwise the program will crash\n"
course_number = raw_input("Please enter the number of course: ")
Study_Group = int(input("Please enter the number of group you are interested to find available space in: "))
ID = raw_input("Please enter your ID number: ")
Password = raw_input("Please enter your password ")
web_str =  "http://techmvs.technion.ac.il/cics/wmn/wmnnut02?OP=VM&MK=" + course_number

while True:
    print "now checking for available place..."


    Identification = web_str
    page = mechanize.Browser()
    page.open(Identification)

    page.select_form(nr=0)
    page["UID"] = ID  #user_id
    page["PWD"] = Password    #password
    results = page.submit().read()


    Free_Spots =web_str 
    response = page.open(Free_Spots)


    r = response.get_data() #copy into text file
    f = open('c:/groups.txt', 'w')
    f.write(r) 
    f.close()

    location = 0 #copy from the text file to an array
    array = {}
    with open('c:/groups.txt', 'r') as inF:
        for line in inF:
            array[location] = line
            location = location + 1
    inF.close()


    for i in array:
        if  "Add to my basket" in array[i]: 
            available = get_number(array[i+1]) #string1 is num of available places
            group = get_number(array[i+2]) #study group
            if (int(group) == Study_Group) & (int(available) > 0):
                print "FOUND PLACE!" ##need to do here fun sounds
                make_some_noise()
            elif (int(group) == Study_Group) & (int(available) <= 0):
                print available, group
                print "BASSA, No space in the group you wanted"
    time.sleep(60) #wait for one minute

