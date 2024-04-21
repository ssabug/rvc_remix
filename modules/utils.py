import datetime
import mutagen
import traceback
import os
from math import floor

def log(msg,source='NONE',severity='INFO',sameline=False):  
    
    log_to_file=False;
    log_file="log.txt";
    debug=True;

    if not isinstance(msg,str):
        msg=str(msg);

    if isinstance(msg,list) or isinstance(msg,tuple):
        message= str(datetime.datetime.now() ) + ' [ ' + source + ' ] ' + str(msg)
    else:   
        message= str(datetime.datetime.now() ) + ' [ ' + source + ' ] ' + msg
    #if len(message) > 2000:
    #    message = str(datetime.datetime.now() ) + ' [ ' + source + ' ] ' +'Message too long '
    if debug :
        if sameline:
            print (message,end = '')
        else:
            print (message)

    if log_to_file :
            f = open(log_file, "a")  # append mode
            f.write(message + "\n")
            f.close()


def handleErrors(error,module="RNDR"):
    log("EXCEPTION " + str(type(error).__name__) + " " + str(error) ,module);
    stack = traceback.extract_stack()[:-3] + traceback.extract_tb(error.__traceback__);  # add limit=?? 
    for i,l in enumerate(stack):
        log(str(stack[len(stack)-1-i]),module) # An error occurred: NameError – name 'x' is not defined

def getAudioLength(path):
    if os.path.exists(path):     
        return floor(mutagen.File(path).info.length);
    else:
        log('file not found : ' +path);
    return -1;