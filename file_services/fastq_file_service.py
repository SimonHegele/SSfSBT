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
    