import os
import sys
import pathlib
import asyncio

class Config(object):
    # does not work os.getcwd()
    def __init__(self,path=f'{os.getcwd()}/Model/',filename="config"):
        self.__path=path
        self.__filename=filename
        self.data = {}
        self.getValues()

    def __read(self)->list:
        fullpath = self.__path+"/"+self.__filename
        try:
            f = open(fullpath,'r+')
            data = f.readlines()
            f.close()
        except ConfigException as er: 
            raise ConfigException("Can not Open Config File")
        else:
            return data
        
    def getValues(self):
        tmp=self.__read()
        for line in tmp:
            splitedLine = line.strip("\n").split("=")
            if len(splitedLine)==2:
                self.data[splitedLine[0]]=splitedLine[1]
    
    def __getitem__(self, item):
        if item in self.data.keys():
            return self.data[item]
        else:
            raise ConfigException("Key Not Found")


class ConfigException(Exception):
    def __init__(self,message):
        self.message = message
        Exception.__init__(self,self.message)

    def __str__(self):
        return f"Config Error : {self.message}"

    def getMessage(self):
        return self.__str__()


