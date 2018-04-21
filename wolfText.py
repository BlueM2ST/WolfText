# WolfText
# Author: BlueMist
# Text input and extraction tool for the Wolf RPG Editor v2.10D ( ⑨ en)

from sys import exit, path
from json import load
from os import path, makedirs
from time import sleep
from lib import extraction, insertion


# default config file name, path
CONFIG_FILE = 'text.json'
# default output dir
OUTPUT_DIR = 'output/'


def wolfText():
    # open the config file
    checkIfFilesExist()
    config = load(open(CONFIG_FILE, encoding='utf_8'))
    checkJSON(config)

    # make sure fileDirectory exists, since it will have the map files inside
    try:
        fileDirectory = config['mapDirectory']

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
        errorFinish()

    print('== WolfText Tool version {} =='.format(config['_version']))

    # check to extract or insert
    if config['isExistingGame'] == '1':
        extraction.extractTextFromExistingGame(OUTPUT_DIR, config, fileDirectory)
        finished()
    else:
        insertion.insertTextIntoExistingMap(OUTPUT_DIR, config, fileDirectory)
        finished()


def checkIfFilesExist():
    # if the config file is not found, exit the program
    if not path.exists(CONFIG_FILE):
        print('Could not find {}. It must be in the same directory as the program.'.format(CONFIG_FILE))
        errorFinish()

    # if the output directory doesn't exist, try to create it
    if not path.exists(OUTPUT_DIR):
        print('Output dir does not exist, attempting to create.')
        try:
            makedirs(OUTPUT_DIR)
            print('Successfully created output dir.')
        except:
            print('Could not create output dir.')
            errorFinish()


def checkJSON(config):
    # check if these values exist
    try:
        config.get('_version', Exception)
        config.get('breakCharacter', Exception)
        config.get('showMessageHex', Exception)
        config.get('maxCharactersInt', Exception)
        config.get('textSet', Exception)
        config.get('mapDirectory', Exception)
        config.get('isExistingGame', Exception)
    except Exception:
        print('Some config values in {} could not be found or are entered incorrectly.'.format(CONFIG_FILE))
        errorFinish()


def finished():
    print('Finished.')
    sleep(2)
    exit('Exiting.')


def errorFinish():
    print('Error.')
    sleep(2)
    exit('Exiting.')

wolfText()