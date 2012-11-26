#-------------------------------------------------------------------------------
# Name:        Primes
# Purpose:     Compute prime mubers and store them in a database.
#
# Author:      Flagoul
#
# Created:     22.11.2012
#-------------------------------------------------------------------------------
import math
import sqlite3

primes = []

conn = sqlite3.connect("primes.db")
c = conn.cursor()


def isPrime(a):
    """Function used to know if a number is prime or not by different means."""

    prime = True
    n = 2
    nMaxReg = primes[len(primes)-1]
    aFloorSqrt = math.floor(math.sqrt(a))


    # if a is smaller or equal to the maximum prime registered, we check if a is in the list
    if(a<= nMaxReg):
        prime = False
        for i in range(0,len(primes)):
            if(a == primes[i]):
                prime = True

    # if the square root of a is equal or smaller than the max prime registered, we compute
    elif(aFloorSqrt <= nMaxReg):

        indexAFloorSqrt = 0

        for i in range(0,len(primes)): # finds the index of the prime <= aFloorSqrt in primes
            if(primes[i] <= aFloorSqrt):
                indexAFloorSqrt = i

        for i in range(0,indexAFloorSqrt+1):
            if(a%primes[i] == 0):
                prime = False


    #else we compute the primes to the square root of a. Usually not used if isPrime() is used
    # within storePrimeNumbersTo().
    else:
        while(n<=aFloorSqrt and a!= 2):
            if(aFloorSqrt >= n):
            	if(a%n == 0):
            		prime = False;
            		break

            	else: n+=1

    return prime


def storePrimeNumbersTo(a):
    """Function used to compute prime number to a number a and store them into list 'primes'."""

    loadNumbers()
    global primes

    n = primes[len(primes)-1] # allows to store only the prime numbers which aren't already stored
    indicator = 0
    percentage = math.floor((a-n)/100)
    percentageEval = 1

    for i in range(n,a): # the numbers to test
        if(isPrime(n)):
            primes.append(n)
        n+=1
        indicator+=1
        if(percentage != 0):
            if(indicator%percentage == 0):
                print("Done computing for ",n," : ",percentageEval,"%")
                percentageEval+=1


    print("Done computing.")


def printPrimes():
    """A simple function to print the content of list 'primes'."""
    for i in range(0,len(primes)):
        print(primes[i])


def loadNumbers():
    """The function used to load all the primes in the database to store it in list 'primes'."""

    global primes
    primes = []

    c.execute("""SELECT * FROM primes""")
    for line in c.fetchall():
        primes.append(line[1])


def saveNumbers():
    """Function used to store the numbers contianed in primes in the database."""

    start = 0
    max_id = 0
    startId = 1

    c.execute("""SELECT MAX(id) FROM primes""")
    max_id = c.fetchone()[0]
    c.execute("""SELECT MAX(prime) FROM primes""")
    start = c.fetchone()[0]

    for i in range(0,len(primes)):
        if(primes[i]>start):
            c.execute("""INSERT INTO primes VALUES (?,?)""",((max_id+startId),primes[i]))
            startId +=1
        if(i%100 == 0): # commit all 100 tuples written not to slow too much
            conn.commit()

    conn.commit()
    print("Done inserting primes in database.")


def loadDatabase():
    """Function used to load the database and make it ready to be used."""

    c.execute("""CREATE TABLE IF NOT EXISTS primes(id INTEGER PRIMARY KEY, prime BIGINTEGER)""")
    c.execute("""SELECT MAX(id) FROM primes""")
    max_id = c.fetchone()[0]

    if(max_id == None): # if the database is empty, we put 2 in it
        c.execute("""INSERT INTO primes VALUES (?,?)""",(0,2))


def printAllPrimes():
    """Function used to see what is currently registered in the database."""

    c.execute("""SELECT * FROM primes""")
    for line in c.fetchall():
        print(line)
    print("Done reading primes from database.")


def printPrimesFromTo(a,b):
    """Function used to get the prime numbers between number a and number b registered in the database.
    b must be at least 2."""

    global primes
    loadNumbers()

    if(b<2):
        print("b must be at least 2.")
    else:
        for i in range(0,len(primes)):
            if(a>primes[i]):
                a = primes[i]
                break
        for i in range(0,len(primes)):
            if(b<primes[i]):
                b = primes[i-1]
                break


    c.execute("""SELECT prime FROM primes WHERE prime BETWEEN """ +str(a)+""" AND """+str(b))
    for line in c.fetchall():
        print(line[0])
    print("Done reading primes in the interval from database.")


def exportToFile():
    """Exports the primes registered in database to the file 'primes.txt'."""
    loadNumbers()
    f = open("primes.txt", "w")

    for i in range (0,len(primes)-1):
        f.write(str(primes[i])+"\n")
    f.close()

    print("Done exporting prime numbers to text file.")


if __name__ == "__main__":

    # Examples: how to use the functions

    loadDatabase() # required to make the database ready to be used
    storePrimeNumbersTo(10000) # choose any number you want the script to calculate to. The numbers are stored in list 'primes'.
    saveNumbers() # required to save in the database the primes computed.
    #printAllPrimes() # show which numbers are registered in the database.
    printPrimesFromTo(2,97) # show the interval of primes you want from the database.
    exportToFile() # you can export with this the content of your database to a textfile.

    conn.close()

