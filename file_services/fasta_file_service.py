from . import fasta_like_file_service

class FastaFileService(fasta_like_file_service.FastaLikeFileService):

    separator = ">"

    @classmethod
    def parse_string(cls, string: str)->dict:

        lines    = string.split("\n")
        header   = lines[0][1:]
        sequence = "".join(lines[1:])

        return {"header": header,
                "sequence": sequence,
                "length": len(sequence),
                "file_type": "fasta"}

    @classmethod
    def parse_dict(cls, read: dict)->str:
        
        return cls.separator+read["header"]+"\n"+read["sequence"]+"\n"

