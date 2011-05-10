from south.modelsinspector import add_introspection_rules

add_introspection_rules([], ["^django_extensions\.db\.fields"])
add_introspection_rules([], ["^django_extensions\.db\.fields\.json"])

from django.core.files.storage import Storage
from django.core.files.storage import FileSystemStorage

def get_name_path(username):
    """
    The file system path to a user's directory consists of a tree of characters from
    the username followed by the username itself (e.g. for user='dwood', the path would
    be 'd/w/o/o/d/dwood').  This is done to ensure that the number of users is unlikely to
    exceed the maximum number of files allowed to be created in a given directory (which
    varies by OS, but is often 1024).
    """
    namepath = ''
    for letter in username:
        namepath += letter + "/"
    return namepath
    
def chunk_path(path):
    return get_name_path(path.split("/")[0]) 

class ExhibitStorage(FileSystemStorage):
    """
    Assume that incoming paths are of the form <username>/.../...
    """
    def __init__(self, *args, **kwargs): 
        self.__userdata_storage = FileSystemStorage(location=kwargs['location'], base_url=kwargs['base_url'])
        
    def _open(self, name, mode='rb'):
        return self.__userdata_storage._open(chunk_path(name) + name, mode)
        
    def _save(self, name, content):
        chunk = chunk_path(name)       
        fullname = chunk + name 
        if (self.__userdata_storage.exists(fullname)):
            self.__userdata_storage.delete(fullname)
        result = self.__userdata_storage._save(fullname, content)
        return result.partition(chunk)[2]
        
    def exists(self, name):
        return self.__userdata_storage.exists(chunk_path(name) + name)
    
    def path(self, name):
        return self.__userdata_storage.path(chunk_path(name) + name)
    
    def size(self, name):
        return self.__userdata_storage.size(chunk_path(name) + name)
    
    def delete(self, name):
        return self.__userdata_storage.delete(chunk_path(name) + name)
    
    def url(self, name):
        return self.__userdata_storage.url(name)
    def get_available_name(self, name):
        return self.__userdata_storage.get_available_n
