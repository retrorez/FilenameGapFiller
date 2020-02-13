#! python3

# File Gap Filler - Scans a directory and searches for files that are in
# a sequence. If at least 3 files are found, the program will check if they
# are in proper sequence (i.e. 1,2,3, and not 1,3,6,9). If not, it will rename
# all of the files to make them sequential.

import os, re, shutil

#create empty list for files that pass regex
hasNumbersOnEnd = []

#list to hold prefixes that appear at least 3 times
prefixes = []
extensions = []
prefixDict = {}
longestTrail = {}

lastPrefix = ''
counter = 1

# Module to Correct Numbering and Fill Gaps
def fillGaps(listOfFilenames, prefix, numberTrails):
    listOfFilenames.sort()
    counter = 1
    print('Running FillGaps Module on: ' + prefix + '!')
    print('Filename List: ' )
    print(listOfFilenames)
    #print('Prefix to search for gaps on: ' + prefix)
    
    for filename in listOfFilenames:
        prefixLength = len(prefix)
        if filename[:prefixLength] == prefix:
            number = int(filename[prefixLength:])
            print('Current File Number: ' + str(number))
            print('Current File Counter: ' + str(counter))
            if number == counter:
                counter = counter + 1
                
            else:
                #create filler zeroes to match original numbering format
                length = len(str(filename[prefixLength:]))
                length2 = len(str(counter))
                lengthDifference = length - length2
                zeroes = '0' * (longestTrail[prefix] - 1)
                
                
                newFileName = str(os.getcwd()) + '\\' + prefix + zeroes + str(counter)+ prefixDict[filename]
                currentFileName = str(os.getcwd()) + '\\' + filename + prefixDict[filename]
                print('Current filename: ' + currentFileName)
                print('Rename to: ' + newFileName)
                shutil.move(currentFileName, newFileName)
                
                counter = counter + 1
                
                
            

# Welcome Banner
print('Welcome to the Filename Gap Filler Project!')
os.chdir('C:\\code\\python\\FGF')
print('Your current working directory is: ' + str(os.getcwd()))
print('')
print('Press enter to begin...')
input()

# Create regex to locate numbers at end of filename
numbersOnEnd = re.compile(r'[0-9]+$')


# Walk directory, removing extensions and adding to new list
for folderName, subfolders, filenames in os.walk(os.getcwd()):
    for filename in filenames:
        filenameChopped = filename[:-4]
        extension = filename[-4:]
        prefixDict[filenameChopped] = extension
        foundOne = numbersOnEnd.search(filenameChopped)
        try:
            if foundOne.group() : # if search succeeds, add to list
                trail = len(str(foundOne.group())) 
                               
                hasNumbersOnEnd.append(filenameChopped)
                hasNumbersOnEnd.sort()
                prefix = filenameChopped[:-1*(len(foundOne.group()))]
                                  
                #print('Found One>> Prefix: ' + prefix +' | ' + 'Number: ' + number)
                if prefix != lastPrefix:
                    if counter > 2:
                        if prefix not in prefixes:
                            prefixes.append(prefix)
                             
                    #print('New Prefix')
                    lastPrefix = prefix
                else:
                    #print('Same Prefix')
                    counter = counter + 1
                    if counter > 2:
                        if prefix not in prefixes:
                            prefixes.append(prefix)
                        if prefix not in longestTrail.keys():
                            longestTrail[prefix] = trail
                            
                        else:
                            if longestTrail[prefix] < trail:
                                longestTrail[prefix]  = trail
                            #print('The longest trail for ' + prefix + ' is ' + str(longestTrail[prefix]))
                       
        except Exception as err:
            #print(str(err))
            continue
    
#print('')
#print('List of filenames with numbers on the end:')
#print(hasNumbersOnEnd)
#print('')
#print('List of prefixes that occur 3 or more times')
#print(prefixes)


for prefix in prefixes:
    fillGaps(hasNumbersOnEnd, prefix, longestTrail)
        
print('All files resequenced!')
input()



