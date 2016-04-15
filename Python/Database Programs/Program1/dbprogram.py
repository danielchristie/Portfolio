import sqlite3, sys

# Connect to simpsons database
conn = sqlite3.connect('simpsons.db')

# Create the table
conn.execute("CREATE TABLE IF NOT EXISTS SIMPSON_INFO( \
     ID INTEGER PRIMARY KEY AUTOINCREMENT, \
     NAME           TEXT        NOT NULL,\
     GENDER         TEXT        NOT NULL,\
     AGE            INT         NOT NULL,\
     OCCUPATION     TEXT        NOT NULL \
     );")

# Save changes
conn.commit()

# Add Data to the table
conn.execute('''INSERT INTO SIMPSON_INFO (NAME, GENDER, AGE, OCCUPATION) VALUES ('Bart Simpson', 'Male', 10, 'Student')''')
conn.execute('''INSERT INTO SIMPSON_INFO (NAME, GENDER, AGE, OCCUPATION) VALUES ('Homer Simpson', 'Male', 42, 'Parent')''')
conn.execute('''INSERT INTO SIMPSON_INFO (NAME, GENDER, AGE, OCCUPATION) VALUES ('Lisa Simpson', 'Female', 8, 'Student')''')
conn.execute('''INSERT INTO SIMPSON_INFO (NAME, GENDER, AGE, OCCUPATION) VALUES ('Marge Simpson', 'Female', 40, 'Parent')''')

# Save changes
conn.commit()

def printCursor(cursor):
    for row in cursor:
        print "Id: " + str(row[0])
        print "Name: " + row[1]
        print "Gender: " + row[2]
        print "Age: " + str(row[3])
        print "Occupation: " + row[4] + "\n"

def cursorArray(cursor):
    cursor_array = []
    for row in cursor:
        cursor_array.append([row[0],row[1],row[2],\
                             row[3],row[4]])
    return cursor_array

def newCharacter():
    print '\nAdding a new character...'
    name = raw_input('Name: ')
    gender = raw_input('Gender: ')
    age = raw_input('Age: ')
    occupation = raw_input('Occupation: ')

    # key value strings
    key_str = 'NAME, GENDER, AGE, OCCUPATION'
    val_str = "'{}', '{}', {}, '{}'".format(\
        name, gender, age, occupation)
    
    sql_str = "INSERT INTO SIMPSON_INFO ({}) \
        VALUES ({});".format(key_str, val_str)
    
    conn.execute(sql_str)
    conn.commit()
    print "Number of changes: ", conn.total_changes
    
def updateCharacter():
    print "\nEditing a character"
    name = raw_input("Please enter the character's name: ")
    sql_str = "SELECT * from SIMPSON_INFO where NAME='{}'"\
              .format(name)
    
    cursor = conn.execute(sql_str)
    cursor_arr = cursorArray(cursor)
    printCursor(cursor_arr)
    
    length = 0
    change_id = 0
    for row in cursor_arr:
        length += 1
    if length == 0:
        print 'No matches found'
        return
    elif length == 1:
        print 'Match found...'
        for row in cursor_arr:
            change_id = row[0]
            print change_id
    else:
        print 'More than one match found.'
        change_id = raw_input('Type the ID of the character to update: ')
    
    print 'Please insert the updated data (leave blank to skip):'
    
    name = raw_input('Name: ')
    gender = raw_input('Gender: ')
    age = raw_input('Age: ')
    occupation = raw_input('Occupation: ')
    
    if not name == '':
        sql_str = "UPDATE SIMPSON_INFO set NAME='{}' where ID={}"\
        .format(name, change_id)
        conn.execute(sql_str)
    if not gender == '':
        sql_str = "UPDATE SIMPSON_INFO set GENDER='{}' where ID={}"\
        .format(gender, change_id)
        conn.execute(sql_str)
    if not age == '':
        sql_str = "UPDATE SIMPSON_INFO set AGE='{}' where ID={}"\
        .format(age, change_id)
        conn.execute(sql_str)
    if not occupation == '':
        sql_str = "UPDATE SIMPSON_INFO set OCCUPATION='{}' where ID={}"\
        .format(occupation, change_id)
        conn.execute(sql_str)
    
    conn.commit()
    print "Number of changes: ", conn.total_changes

def viewDetails():
    print "\nViewing character details"
    name = raw_input("Please enter the character's name: ")
    sql_str = "SELECT * from SIMPSON_INFO where NAME='{}'"\
              .format(name)
    
    cursor = conn.execute(sql_str)
    cursor_arr = cursorArray(cursor)
    
    if len(cursor_arr)>0:
        printCursor(cursor_arr)
    else:
        print 'No records found'
    
def options():
    print '\nWhat would you like to do?'
    print '1. Add a new character'
    print '2. Edit character information'
    print '3. View character details'
    print '4. Exit'
    response = raw_input('Enter number: ')
    try:
        response = int(response)
    except:
        print 'Invalid input. Terminating program'
        sys.exit()
    
    if response == 1:
        newCharacter()
    elif response == 2:
        updateCharacter()
    elif response == 3:
        viewDetails()
    else:
        print 'Exiting program'
        sys.exit()
        
    return response


def mainLoop():
    in_loop = 1
    while in_loop == 1:
        options()
        again = raw_input( \
        'Would you like to do something else? (y/n) ')
        if not again.lower() == 'y':
            in_loop = 0

def createTable():
    conn.execute("CREATE TABLE SIMPSON_INFO( \
        ID INTEGER PRIMARY KEY AUTOINCREMENT, \
        NAME TEXT, \
        GENDER TEXT, \
        AGE INT, \
        OCCUPATION TEXT \
        );")


mainLoop()
