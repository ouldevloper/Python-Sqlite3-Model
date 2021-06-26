import sys
import os

class ModelException(Exception):
    def __init__(self,message):
        self.message=message
        super().__init__(self.message)

    def __str__(self):
        return f"Error at Model Class : {self.message}"
    
    def getMessage(self):
        return self.__str__()