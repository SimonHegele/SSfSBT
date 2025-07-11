from typing import Generator
from math   import inf

from . import fasta_like_file_service

class FastqFileService(fasta_like_file_service.FastaLikeFileService):

    separator = "@"

    @classmethod
    def parse_string(cls, string: str)->dict:

        lines    = string.rstrip().split("\n")
        header   = lines[0]
        i        = [i for i, line in enumerate(lines) if line[0]=="+"][0]
        sequence = "".join(lines[1:i])
        info     = lines[i]
        quality  = "".join(lines[i+1:])

        return {"header": header,
                "sequence": sequence,
                "info": info,
                "quality": quality,
                "length": len(sequence),
                "file_type": "fastq"}

    @classmethod
    def parse_dict(cls, read: dict)->str:
        
        return "\n".join([read["header"],read["sequence"],read["info"],read["quality"]])+"\n"

    @classmethod
    def read(cls, file_path:str, only=inf)->Generator:

        # Overrides method read inherited from parent class fasta_like_file_service.FastaLikeFileService
        # -> In FASTQ-files, the character "@" at the start of a line either marks the beginning of a new
        #    entry or refer to a phred score of 31.

        string = ""
        
        with open(file_path, "r") as f:

            for i, line in enumerate(f):

                if (line[0] == cls.separator) and (i > 0):

                    read = cls.parse_string(string)

                    if len(read["sequence"]) == len(read["quality"]):
                        yield read
                        if i == only:
                            return
                        string = ""
                        
                string += line

            yield cls.parse_string(string)
    
