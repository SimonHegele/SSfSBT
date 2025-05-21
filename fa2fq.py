from argparse   import ArgumentParser
from numpy      import log10
from os         import path
from typing     import Generator

import logging
import sys

from file_services.fasta_file_service import FastaFileService
from file_services.fastq_file_service import FastqFileService

class MyArgumentParser(ArgumentParser):

    prog        =   "fa2fq"

    description =   """
                    FASTA to FASTQ conversion
                    """
    
    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)

        self.add_argument("FASTA")
        self.add_argument("S",
                          type=float,
                          help="Expected error rate for bases denoted with upper case characters")
        self.add_argument("s",
                          type=float,
                          help="Expected error rate for bases denoted with lower case characters")
        self.add_argument("-o","--offset",
                          metavar="",
                          type=int,
                          default=33,
                          help="Phred-quality offset (Default: 33)")
        
    def check_params(self)->None:

        # Checking file paths
        if not path.isfile(self.args.FASTA):
            logging.error("File FASTA does not exist")
            exit(1)
        if path.isfile(".".join(self.args.FASTA.split(".")[:-1])+".fastq"):
            f_out = ".".join(self.args.FASTA.split(".")[:-1])+".fastq"
            logging.error(f"{f_out} exists")
            exit(1)

        # Checking error values
        if not ((0 < self.args.S) and (self.args.S < 1)):
            logging.error("S must be greater than 0 and smaller than 1")
            exit(1)
        if not ((0 < self.args.s) and (self.args.s < 1)):
            logging.error("s must be greater than 0 and smaller than 1")
            exit(1)
        if self.args.S > self.args.s:
            logging.error("S < s (Upper case character represent higher quality bases, therefore S should be smaller than s)")
            exit(1)

    def parse_args(self):

        self.args = super().parse_args()
        self.check_params()
   
        return self.args
        
def phred(error_rate: float, offset: int):

    return chr(int(-10*log10(error_rate))+offset)

def fasta_2_fastq(sequences: list[dict[str, str]], P: chr, p: chr) -> Generator:

    for i, sequence in enumerate(sequences):
        if i % 100_000 == 0:
            logging.info(f"{i:>10}")

        sequence["file_type"]   = "fastq"
        sequence["info"]        = "+"
        sequence["quality"]     = "".join([P if b.isupper() else p for b in sequence["sequence"]])
        sequence["sequence"]    = sequence["sequence"].upper()

        yield sequence
        
def main():

    args = MyArgumentParser().parse_args()

    logging.basicConfig(level    = "info",
                        format   = "%(asctime)s %(levelname)s %(message)s",
                        datefmt  = "%d-%m-%Y %H:%M:%S",
                        handlers=[logging.StreamHandler(stream=sys.stdout)]
                        )

    P = phred(args.S, args.offset)
    p = phred(args.s, args.offset)

    reader = FastaFileService()
    writer = FastqFileService()
    f_out  = ".".join(args.FASTA.split(".")[:-1])+".fastq"

    writer.write(f_out, fasta_2_fastq(reader.read(args.FASTA), P, p))

    logging.info("##############################################")
    logging.info("#    Simon says: Thanks for using SSfSBT!    #")
    logging.info("##############################################")

if __name__ == "__main__":
    main()
