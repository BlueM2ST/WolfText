# WolfText
# Author: BlueMist

from json import dump
from os import path, listdir
from re import findall
from binascii import hexlify, unhexlify
from collections import OrderedDict


def extractTextFromExistingGame(OUTPUT_DIR, config, fileDirectory):
    dictionary = OrderedDict()
    dictionary, textSet, showMessageHex = addDefaultJSONValues(dictionary, config)
    outputjson = open('{}text.json'.format(OUTPUT_DIR), 'w', encoding='utf-8')

    # ======================== iterating over each file ====================================================
    for file in listdir(fileDirectory):
        # open the file in binary
        openFile = open(path.join(fileDirectory, file), 'rb')
        openFileRead = openFile.read()
        openFile.close()
        # convert the entire file to hex
        openFileHex = hexlify(openFileRead)

        displayMessageSetterList = findall(b'000001650000000[0-9]01[0-9a-fA-F][0-9a-fA-F]000000', openFileHex)

        for value in displayMessageSetterList:
            openFileHex = openFileHex.replace(value, value[:18] + b'07' + value[20:])

        outputMapFile = open('{}{}'.format(OUTPUT_DIR, file), 'wb')
        textMessageList = findall(b'01%s0000000[0-9]01[0-9a-fA-F][0-9a-fA-F]000000.+?(?=0000)'
                                  % showMessageHex, openFileHex)

        count = 0
        for value in textMessageList:
            value = value.split(b'000')

            try:
                if len(value) > 8:
                    comValue = value[-2] + value[-1]
                    textMessageList[count] = unhexlify(comValue)
                else:
                    textMessageList[count] = unhexlify(value[-1])
            except:
                comValue = value[-2] + value[-1]
                try:
                    textMessageList[count] = unhexlify(comValue)
                except:
                    textMessageList[count] = unhexlify(comValue[1:])
            count += 1

        # ================================== iterating over each piece of text =================================
        outputFile = open('{}{}'.format(OUTPUT_DIR, file), 'wb')
        # this is the name of the current map file
        fileName = file[:-4]
        count = 1
        for text in textMessageList:
            if fileName not in dictionary['text']:
                dictionary['text'][fileName] = {}

            dictionary['text'][fileName]['{}{:05d}'.format(str(textSet), count)] = str(text)[2:-1]

            setterTextToReplace = hexlify(text)
            textToReplaceWithSetter = '{}{:05d}'.format(str(textSet), count).encode('utf-8').hex().encode('utf-8')

            # actually replace the values in memory
            openFileHex = openFileHex.replace(setterTextToReplace, textToReplaceWithSetter, 1)
            count += 1
        outputMapFile.write(unhexlify(openFileHex))
        outputMapFile.close()
        # check to make sure there is text in the file at all
        try:
            dictionaryOrdered = OrderedDict({int(key.replace(textSet, '')): value for key, value in dictionary['text'][fileName].items()})
        except KeyError:
            print('File \'{}\' does not contain any text. This is not an error message.'.format(fileName))
            continue
        dictionary['text'][fileName] = dictionaryOrdered
        print('File \'{}.mps\' completed successfully.'.format(fileName))

    dump(dictionary, outputjson, indent=4)
    outputjson.close()

    forceCorrectFormat(OUTPUT_DIR, textSet)


def addDefaultJSONValues(dictionary, config):
    # adding default values to the json file
    dictionary['.comment'] = 'Config; don\'t change these values unless you have modified the Wolf RPG Editor in some way.'
    dictionary['_version'] = config['_version']
    dictionary['_isGenerated'] = 'True'
    dictionary['breakCharacter'] = config['breakCharacter']
    dictionary['showMessageHex'] = config['showMessageHex']
    showMessageHex = dictionary['showMessageHex'].encode('utf-8')
    dictionary['showChoiceHex'] = '66'
    dictionary['showCommentHex'] = '67'
    dictionary['maxCharactersInt'] = config['maxCharactersInt']
    dictionary['textSet'] = config['textSet']
    textSet = dictionary['textSet']
    dictionary['..comment'] = 'Change this directory if you are not running the program from the Wolf RPG Editor Data file.'
    dictionary['mapDirectory'] = config['mapDirectory']
    dictionary['...comment'] = "Set this to '1' if you want to extract the text from map files into a json file, otherwise set to '0'"
    dictionary['isExistingGame'] = '0'
    dictionary['....comment'] = 'Text; place all text below here.'
    dictionary['text'] = {}
    return dictionary, textSet, showMessageHex


def forceCorrectFormat(OUTPUT_DIR, textSet):
    outputjson = open('{}text.json'.format(OUTPUT_DIR), 'r', encoding='utf-8')
    outputjsonRead = outputjson.readlines()
    outputjson.close()
    string = ''
    for line in outputjsonRead:
        try:
            splitLine = line.split('": "')
            newLine = int(splitLine[0].replace(' ', '')[1:])
            newLine = '            "{}{:05d}": "{}'.format(textSet, newLine, splitLine[1])
            string += newLine
        except ValueError:
            string += line
            continue

    finalOutputjson = open('{}text.json'.format(OUTPUT_DIR), 'w', encoding='utf-8')
    finalOutputjson.write(string)
    finalOutputjson.close()