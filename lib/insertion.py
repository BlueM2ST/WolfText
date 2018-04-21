# WolfText
# Author: BlueMist

from os import path, listdir
from re import findall
from binascii import hexlify, unhexlify


def insertTextIntoExistingMap(OUTPUT_DIR, config, fileDirectory):
    breakCharacter, showMessageHex, charMax, textSet = getValuesFromConfig(config)
    showMessageHex = showMessageHex.encode('utf-8')
    textSetHex = textSet.encode('utf-8').hex().encode('utf-8')

    for file in listdir(fileDirectory):
        # open the file in binary
        openFile = open(path.join(fileDirectory, file), 'rb')
        openFileRead = openFile.read()
        openFile.close()
        fileName = file[:-4]
        # convert the entire file to hex
        openFileHex = hexlify(openFileRead)

        displayMessageSetterList = findall(b'000001%s0000000[0-9]01[0-9a-fA-F][0-9a-fA-F]000000%s'
                                    % (showMessageHex, textSetHex), openFileHex)

        textMessageList = []
        # catch if the map is not defined in the json file
        try:
            # find the key:value pairs and append them to a list
            for key, value in config['text'].items():
                for x in config['text'][fileName].items():
                    textMessageList.append(x)
        except KeyError:
            continue

        # ================================== iterating over each piece of text =================================
        outputFile = open('{}{}'.format(OUTPUT_DIR, file), 'wb')
        for valuePair in textMessageList:
            valueText = linebreak(valuePair[1], charMax, breakCharacter)
            lineCountHex = characterCountInHex(valueText)

            # replace the old placeholder text with the new text
            setterTextToReplace = hexlify(valuePair[0].encode('utf-8'))
            textToReplaceWithSetter = hexlify(valueText.encode('utf-8'))

            # at least it works...
            for value in displayMessageSetterList:
                fullHexToReplace = value[:-2] + setterTextToReplace
                fullHexToReplaceWithSetter = value[:18] + lineCountHex + value[20:-2] + textToReplaceWithSetter

                openFileHex = openFileHex.replace(fullHexToReplace, fullHexToReplaceWithSetter)

        outputFile.write(unhexlify(openFileHex))
        outputFile.close()


def getValuesFromConfig(config):
    breakCharacter = config['breakCharacter']
    showMessageHex = config['showMessageHex']
    maxCharactersInt = config['maxCharactersInt']
    textSet = config['textSet']
    return breakCharacter, showMessageHex, maxCharactersInt, textSet


# linebreak
def linebreak(line, charMax, breakCharacter):
    # remove existing linebreaks
    line = line.replace('\n', ' ')
    isSet = False
    # if the line starts with an @, then it is referencing a character image and needs a linebreak after
    if line.startswith('@'):
        line = line[:2] + '{}'.format(breakCharacter) + line[2:]
        charMax -= 12
        isSet = True
    # this would specify that it is a character name, it should have a linebreak after it
    if '  \"' in line:
        line = line.replace('  \"', '{}  \"'.format(breakCharacter))
        if not isSet: charMax -= 12
    # remove any double spaces this may cause
    line = line.replace('  ', ' ')
    # split the string into a list of words
    d = '{}'.format(breakCharacter)
    toSplitLine = [e+d for e in line.split(d) if e]
    wordList = toSplitLine[-1].split(' ')
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
    toSplitLine[-1] = finishedLine[1:]
    toSplitLine = ''.join(toSplitLine)
    if breakCharacter == '\n':
        toSplitLine = toSplitLine.replace('\\n', '').replace('\\\'', '\'')
        if toSplitLine.endswith('\n'):
            toSplitLine = toSplitLine[:-1]
    else:
        toSplitLine = toSplitLine.replace('{}'.format(breakCharacter), '').replace('\\\'', '\'')
    # print(toSplitLine)
    return toSplitLine


# counts the number of characters + 1 and converts the output to type byte
def characterCountInHex(line):
    intCount = (len(line) + 1)
    return str(intCount.to_bytes((intCount.bit_length() + 7 // 8),"big").hex()[-2:]).encode('utf-8')