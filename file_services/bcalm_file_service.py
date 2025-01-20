from re import compile, finditer

from src.io.file_services import fasta_file_service

class BcalmFileService(fasta_file_service.FastaFileService):

    r = {
            "id":              compile(r"^>(?P<ID>\d+)"),
            "length":          compile(r"LN:i:(?P<LENGTH>\d+)"),
            "total abundance": compile(r"KC:i:(?P<TOTAL_ABUNDANCE>\d+)"),
            "avg. abundance":  compile(r"km:f:(?P<AVG_ABUNDANCE>\d+\.\d)"),
            "edges":           compile(r"(?P<EDGE>L:[-+]:\d:[-+])"),
            "neighbors":       compile(r"L:[-+]:(?P<NEIGHBOR>\d):[-+]")
            }

    @classmethod
    def parse_string(cls, string: str)->dict:

        lines = string.split("\n")

        return {
            "id":              cls.r["id"].search(lines[0]).group("ID"),
            "header":          lines[0],
            "length":          cls.r["length"].search(lines[0]).group("LENGTH"),
            "total abundance": int(cls.r["total abundance"].search(lines[0]["header"]).group("TOTAL_ABUNDANCE")),
            "avg. abundance":  float(cls.r["avg. abundance"].search(lines[0]["header"]).group("AVG_ABUNDANCE")),
            "sequence":        "".join(lines[1:]),
            "edges":           [match.group("EDGE") for match in finditer(cls.r["edges"], lines[0])],
            "neighbors":       [match.group("NEIGHBOR") for match in finditer(cls.r["neighbors"], lines[0])]}