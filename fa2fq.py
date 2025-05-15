from argparse   import ArgumentParser
from logging    import error, info
from numpy      import log10
from os         import path

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
        self.add_argument("-v","--verbose",
                          help="Show conversion progress",
                          action='store_true')
        
    def check_params(self)->None:

        # Checking file paths
        if not path.isfile(self.args.FASTA):
            error("File FASTA does not exist")
            exit(1)
        if path.isfile(".".join(self.args.FASTA.split(".")[:-1])+".fastq"):
            outfile = ".".join(self.args.FASTA.split(".")[:-1])+".fastq"
            error(f"{outfile} exists")
            exit(1)

        # Checking error values
        if not ((0 < self.args.S) and (self.args.S < 1)):
            error("S must be greater than 0 and smaller than 1")
            exit(1)
        if not ((0 < self.args.s) and (self.args.s < 1)):
            error("s must be greater than 0 and smaller than 1")
            exit(1)
        if self.args.S > self.args.s:
            error("S < s (Upper case character represent higher quality bases, therefore S should be smaller than s)")
            exit(1)

    def parse_args(self):

        self.args = super().parse_args()
        self.check_params()
   
        return self.args
        
def phred(error_rate: float, offset: int):

    return chr(int(-10*log10(error_rate))+offset)

def fasta_2_fastq(read: dict[str, str], P: chr, p: chr) -> None:

    read["file_type"]   = "fastq"
    read["info"]        = "+"
    read["quality"]     = "".join([P if b.isupper() else p for b in read["sequence"]])
    read["sequence"]    = read["sequence"].upper()
        
def main():

    args = MyArgumentParser().parse_args()

    P = phred(args.S, args.offset)
    p = phred(args.s, args.offset)

    info("Reading...")
    reads = list(FastaFileService().read(args.LoRDEC_fasta))
    info("Done")

    info("Conversion ...")
    for i, read in reads:
        if i % 100_000 == 0 and args.verbose:
            info(f"Progress: {i} of {len(reads)}")
        fasta_2_fastq(read, P, p) 
    info("Done")

    info("Writing...")
    FastqFileService.write(".".join(args.FASTA.split(".")[:-1])+".fastq", reads)
    info("Done")

    info("##############################################")
    info("#    Simon says: Thanks for using SSfSBT!    #")
    info("##############################################")

if __name__ == "__main__":
    main()
