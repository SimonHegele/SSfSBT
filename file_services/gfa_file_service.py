from json   import loads
from typing import Callable, Generator

class IllegalOptionalTypeError(Exception):
    
    def __init__(self, optional_type_char: str) -> None:
        
        super().__init__(optional_type_char)
        
class IllegalOptionalError(Exception):
    
    def __init__(self, optional: str) -> None:
        
        super().__init__(optional)

class GFA_element():
    
    allowed_optionals = []
    required_fields   = 0
    
    def __init__(self, line: str):
        
        self.line       = line
        
    def __repr__(self) -> str:
        
        return self.line
    
    @staticmethod
    def get_optional_type(optional_type_char: str) -> Callable:
                
        match optional_type_char:
            case "A":
                return chr
            case "i":
                return int
            case "f":
                return float
            case "Z":
                return str
            case "J":
                return loads
            case "H":
                return bytearray.fromhex
            case "B":
                return lambda number_array: [float(n) for n in number_array]
            
        raise IllegalOptionalTypeError(optional_type_char)

    def get_optionals_dict(self) -> dict:
        
        optionals_dict = {o: None for o in self.allowed_optionals}
        
        for o in self.line.rstrip().split("\t")[self.required_fields:]:
            
            o = o.split(":")
            
            optionals_dict[o[0]] = self.get_optional_type(o[1])(o[2])
        
        return optionals_dict

class Segment(GFA_element):
    
    allowed_optionals = ["LN", "RC", "FC", "KC", "SH", "UR"]
    required_fields   = 3
    
    def __init__(self, line: str):
        
        super().__init__(line)
        
        line_split = line.rstrip().split("\t")
        
        self.name       = line_split[1]
        self.sequence   = line_split[2]
        self.optionals  = self.get_optionals_dict()
        
class GfaFileService():
    
    @staticmethod
    def read(file_path: str) -> Generator:
        
        with open(file_path, "r") as gfa:
            
            for line in gfa:
                
                match line[0]:
                    case "S":
                        yield Segment(line)