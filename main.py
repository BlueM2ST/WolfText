# WolfText
# Author: BlueMist
# Text input tool for the Wolf RPG Editor

from sys import exit, path
from json import load
from os import path, listdir, makedirs
from time import sleep
import re
import binascii


# default config file name, path
CONFIG_FILE = 'text.json'
# default output dir
OUTPUT_DIR = 'output/'


# make sure all the files are either present or are created
def main():
    # if the config file is not found, exit the program
    if not path.exists(CONFIG_FILE):
        print('Could not find {}. It must be in the same directory as the program.'.format(CONFIG_FILE))
        sleep(2)
        exit('Exiting.')

    # if the output directory doesn't exist, try to create it
    if not path.exists(OUTPUT_DIR):
        print('Output dir does not exist, attempting to create.')
        try:
            makedirs(OUTPUT_DIR)
            print('Successfully created output dir.')
        except:
            print('Could not create output dir.')
            sleep(2)
            exit('Exiting.')

    wolftext()


def wolftext():
    # open the config file
    config = load(open(CONFIG_FILE, encoding='utf_8'))
    try:
        fileDirectory = config['fileDirectory']

        # make sure the directory is valid
        if not path.exists(fileDirectory):
            if fileDirectory == '':
                fileDirectory = '.'
            else:
                print('Could not find the directory \"{}\", please check to make sure it is correct.'
                      .format(fileDirectory))
                sleep(2)
                exit('Exiting.')
    except:
        print('Could not find the file directory defined in {}'.format(CONFIG_FILE))
        fileDirectory = None
        sleep(2)
        exit('Exiting.')

    # load values from config.json
    try:
        maxCharactersHex = config['maxCharactersHex'].encode('utf-8')
        charMax = config['maxCharactersInt']
        breakCharacter = config['breakCharacter']
        textSet = config['textSet'].encode('utf-8').hex().encode('utf-8')
        version = config['_version']
    except:
        print('Some config values in {} can not be found or are entered incorrectly.'.format(CONFIG_FILE))
        # set them here before closing for referencing
        maxCharactersHex = None
        charMax = None
        breakCharacter = None
        version = None
        sleep(2)
        exit('Exiting')

    print('== WolfText Tool version {} =='.format(version))
    for file in listdir(fileDirectory):
        # open the file in binary
        openFile = open(path.join(fileDirectory, file), 'rb')
        openFileRead = openFile.read()
        openFile.close()
        # convert the entire file to hex
        openFileHex = binascii.hexlify(openFileRead)
        # split out, in order, the Display Message hex code
        displayMessage = re.findall(b'000001%s0000000001[0-9a-fA-F][0-9a-fA-F]000000%s%s'
                                    % (maxCharactersHex, textSet, textSet), openFileHex)
        # split the Text by the textSet value
        textMessage = re.split(b'%s%s' % (textSet, textSet), openFileHex)

        textCount = 1
        displayCount = 0
        # catch an error with count increasing by 2
        try:
            for text in textMessage:
                outputFile = open('{}{}'.format(OUTPUT_DIR, file), 'wb')
                # this is what is in the file
                thisValue = '$$' + str(binascii.unhexlify(textMessage[textCount]))[2:-1] + '$$'
                # this is the name of the current map file
                thisFile = file[:-4]
                # check if the keys match
                try:
                    keyValue = config['text'][thisFile][thisValue]
                    keyValue = linebreak(keyValue, charMax, breakCharacter)
                    lineCountHex = characterCountInHex(keyValue)

                    # replace the number of characters
                    thisDisplay = displayMessage[displayCount].replace(displayMessage[displayCount],
                                                                       b'000001%s0000000001%s000000%s%s' % (
                                                                       maxCharactersHex, lineCountHex, textSet,
                                                                       textSet))
                    openFileHex = openFileHex.replace(displayMessage[displayCount], thisDisplay, 1)

                    # replace the old placeholder text with the new text
                    replace = (b'%s%s' % (textSet, textSet) +textMessage[textCount] + b'%s%s' % (textSet, textSet))
                    newValue = keyValue.encode('utf-8').hex().encode('utf-8')
                    # replace the value in the file in memory, only replace the first occurrence in case of duplicates
                    # although if there were duplicate keys, that would be another problem
                    openFileHex = openFileHex.replace(replace, newValue, 1)

                except IndexError:
                    print('Key did not match for map file {}, this will likely cause errors with the game\'s script.'
                          .format(thisFile))
                    input('Press any key if you want to continue.')
                    textCount += 2
                    displayCount += 1
                    continue
                textCount += 2
                displayCount += 1

        # there will always be an IndexError
        except IndexError:
            outputFile.write(binascii.unhexlify(openFileHex))
            outputFile.close()
            continue

    print('Finished.')


def linebreak(line, charMax, breakCharacter):
    # split the string into a list of words
    wordList = line.split(' ')
    characterCount = 0
    finishedLine = ''
    for word in wordList:
        # count the characters in the word, add one for the space that was taken out
        characterCount += len(word) + 1
        # if the character count exceeds the maximum allowed
        if characterCount > charMax:
            finishedLine += breakCharacter
            characterCount = 0
            characterCount += len(word) + 1
            finishedLine += word
            continue
        finishedLine += ' ' + word
    # remove the space at the beginning of the string
    return finishedLine[1:]


# counts the number of characters + 1 and converts the output to type byte
def characterCountInHex(line):
    # \n will turn into a single hex value, not two
    extraBreak = line.count('\n')
    intCount = (len(line) + 1) -extraBreak
    return str(intCount.to_bytes((intCount.bit_length() + 7 // 8),"big").hex()[10:]).encode('utf-8')




main()
