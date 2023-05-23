
from abc import ABC, abstractmethod

class UploaderInterface(ABC):

    @abstractmethod
    def upload_file(self, file_path: str, object_name: str):
        pass