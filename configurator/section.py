# Copyright (c) 2011 Simplistix Ltd
# See license.txt for license details.

_marker = object()

class Section(object):

    def __init__(self):
        self._api = SectionAPI()

    def __getitem__(self,name):
        return self._api.get(name)
    
    def __setitem__(self,name,value):
        self._api.set(name,value)

    def get(self,name,default=None):
        return self._api.get(name,default)
    
    def __getattr__(self,name):
        value = self._api.get(name,_marker)
        if value is _marker:
            raise AttributeError(name)
        return value

    def __setattr__(self,name,value):
        if name=='_api':
            self.__dict__[name]=value
        self._api.set(name,value)
