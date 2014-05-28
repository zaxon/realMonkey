import os
import re

class LogParser():

    def parser(self,logFile):

        file_object=open(logFile,'rb')
        line=file_object.readline()
        _str=''
        while line:
            line=file_object.readline()
            if re.search('crash',line):
                _str='crash'
        file_object.close()
        return _str

    
    
