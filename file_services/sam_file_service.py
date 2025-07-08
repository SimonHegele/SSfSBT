from typing import Generator

class SamFileService():

    sorted_keys = [ "QNAME",
                    "FLAG",
                    "RNAME",
                    "POS",
                    "MAPQ",
                    "CIGAR",
                    "RNEXT",
                    "PNEXT",
                    "TLEN",
                    "SEQ",
                    "QUAL"]

    @classmethod
    def parse_string(cls, line)->dict:

        d = {cls.sorted_keys[i]: line for i, line in enumerate(line.split("\t"))}

        d["format"] = "sam"

        return d
    
    @classmethod
    def parse_dict(cls, mapping: dict)->str:

        return "\t".join([mapping[key] for key in cls.sorted_keys])+"\n"

    @classmethod
    def read(cls, file)->Generator:

        with open(file, "r") as sam:

            for line in sam:

                yield cls.parse_line(line)

    @classmethod
    def write(cls, mappings: list[dict], file: str)->None:

        with open(file, "w") as sam:

            for mapping in mappings:

                sam.write(cls.parse_dict(mapping))
