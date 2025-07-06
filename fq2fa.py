from argparse import ArgumentParser

from file_services.fasta_file_service import FastaFileService
from file_services.fastq_file_service import FastqFileService

class MyArgumentParser(ArgumentParser):

    prog        =   "fa2fq"

    description =   """
                    FASTQ to FASTA conversion
                    """
    
    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)

        self.add_argument("FASTQ")

def main():

    args = MyArgumentParser().parse_args()

    FastaFileService().write(args.FASTQ[:-1]+"a", FastqFileService.read(args.FASTQ))

if __name__ == "__main__":
    main()