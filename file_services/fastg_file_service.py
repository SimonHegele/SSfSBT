from re import compile

from . import fasta_file_service

class FastgFileService(fasta_file_service.FastaFileService):

    r = compile(r"EDGE_(?P<ID>[a-zA-Z\d]+)_length_(?P<LENGTH>\d+)_cov_(?P<COVERAGE>[\d\.]+)")

    @classmethod
    def parse_string(cls, string: str)->dict:

        lines    = string.split(";")
        header   = lines[0][1:]
        id       = cls.r.search(header.split(":")[0]).group("ID")
        length   = cls.r.search(header.split(":")[0]).group("LENGTH")
        coverage = cls.r.search(header.split(":")[0]).group("COVERAGE")
        rc       = True if id.endswith("'") else False
        if len(header.split(":")) == 1 :
            neighbors = []
        else:
            neighbors = [cls.r.search(e).group("ID") for e in header.split(":")]
        sequence = lines[1].replace("\n","")

        for n in neighbors:
            if not n.isdigit():
                raise Exception(f"Neighbors {neighbors}")
        if not id.isdigit():
            raise Exception(f"ID {id}")
        for c in sequence:
            if not c in "ACGT":
                raise Exception(f"Sequence {sequence}")

        return {"header": header,
                "id": id,
                "length": length,
                "sequence": sequence,
                "coverage": coverage,
                "rc": rc,
                "neighbors": neighbors,
                "file_type": "fasta"}

