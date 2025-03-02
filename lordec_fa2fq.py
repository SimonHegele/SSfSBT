from argparse   import ArgumentParser
from numpy      import log10
from os         import path

from file_services.fasta_file_service import FastaFileService
from file_services.fastq_file_service import FastqFileService

class MyArgumentParser(ArgumentParser):

    prog        =   "lordec_fa2fq"

    description =   """
                    ----------
                    Commandline tool that converts FASTA to FASTQ for LoRDEC output files
                    """
    
    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)

        self.add_argument("LoRDEC_fasta")
        self.add_argument("S",
                          type=float,
                          help="Expected error rate for bases denoted with upper case characters")
        self.add_argument("s",
                          type=float,
                          help="Expected error rate for bases denoted with lower case characters")
        self.add_argument("--offset",
                          type=int,
                          default=33,
                          help="Phred-quality offset (Default: 33)")

    def parse_args(self):

        self.args = super().parse_args()

        if not path.isfile(self.args.LoRDEC_fasta):
            raise Exception("LoRDEC FASTA does not exist")
        
        if self.args.LoRDEC_fasta.count(".") > 1:
            raise Exception("LoRDEC FASTA path contains multiple .")
        
        if self.args.S > self.args.s:
            raise Exception("S > s (Upper case characters represent higher quality bases)")
        
        return self.args
        
def phred(error_rate, o):

    return chr(int(-10*log10(error_rate))+o)

def fasta_2_fastq(read, P, p):

    read["file_type"]   = "fastq"
    read["info"]        = "+"
    read["quality"]     = "".join([P if b.isupper() else p for b in read["sequence"]])
    read["sequence"]    = read["sequence"].upper()
        
def main():

    args = MyArgumentParser().parse_args()

    P = phred(args.S, args.offset)
    p = phred(args.s, args.offset)

    print(f"P: {P}")
    print(f"p: {p}")

    print("Reading...")
    reads = list(FastaFileService().read(args.LoRDEC_fasta))
    print("Done")

    print("Conversion ...")
    for i, read in reads:
        if i % 100_000 == 0:
            print(f"Progress: {i} of {len(reads)}")
        fasta_2_fastq(read, P, p) 
    print("Done")

    print("Writing...")
    FastqFileService.write(args.LoRDEC_fasta.split(".")[0]+".fastq", reads)
    print("Done")

if __name__ == "__main__":
    main()