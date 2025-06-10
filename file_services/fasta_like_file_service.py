from abc             import ABC, abstractmethod
from collections.abc import Iterable
from copy            import copy
from math            import inf
from random          import choice
from typing          import Union, Generator

class FastaLikeFileService(ABC):

    @classmethod
    @abstractmethod
    def parse_string(cls, string: str)->dict:
        pass

    @classmethod
    @abstractmethod
    def parse_dict(cls, data: dict)->str:
        pass

    @classmethod
    def read(cls, file_path:str, only=inf)->Generator:
         
        string = ""
        
        with open(file_path, "r") as f:

            for i, line in enumerate(f):

                if (line[0] == cls.separator) and (i > 0):
                    yield cls.parse_string(string)
                    if i == only:
                        return
                    string = ""
                string += line

            yield cls.parse_string(string)

    @classmethod
    def write(cls,
              file_path: str,
              data: Iterable[dict],
              mode="w",
              only=inf)->None:

        with open(file_path, mode) as file:
            for i, d in enumerate(data):
                if i < only:
                    file.writelines(cls.parse_dict(d))
                else:
                    return
                
    def unambigous_codes(cls,
                         data: Iterable[dict],
                         inplace = True) -> Generator:

        translate = {"R": ["A","G"],
                     "Y": ["C","T"],
                     "S": ["G","C"],
                     "W": ["A","T"],
                     "K": ["G","T"],
                     "M": ["A","C"],
                     "B": ["C","G","T"],
                     "D": ["A","G","T"],
                     "H": ["A","C","T"],
                     "V": ["A","C","G"],
                     "N": ["A","C","G","T"]}
        
        for i, d in enumerate(data):
            if not inplace:
                d = copy(d)
            for j, b in enumerate(d["sequence"]):
                if not b in "ACGT":
                    d["sequence"] = choice(translate[b])
            yield d
