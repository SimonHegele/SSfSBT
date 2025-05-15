from argparse   import ArgumentParser
from os         import path
from random     import sample

from file_services.utils import get_read_reader

class MyArgumentParser(ArgumentParser):

    prog        =   "sample"

    description =   """
                    ----------
                    Sampling sequences from FASTA/FASTQ.
                    
                    """
    
    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)

        self.add_argument("number", help="Number of sequences to sample")
        self.add_argument("in_file")
        self.add_argument("out_file")
        self.add_argument("-r","--random",
                          action="store_true",
                          help="Sample randomly instead of first n sequence (slower)")

    def parse_args(self):

        self.args = super().parse_args()

        if not path.isfile(self.args.in_file):
            raise Exception("Input file does not exist")
        
        if path.isfile(self.args.out_file):
            raise Exception("Output file exists")
        
        return self.args

def main():

    args = MyArgumentParser().parse_args()

    file_service = get_read_reader(args.in_file)

    if args.random:
        all_sequences     = list(file_service.read(args.in_file))
        sampled_indices   = sample(range(len(all_sequences)), args.number)
        sampled_sequences = [read for i, read in enumerate(all_sequences)
                             if i in sampled_indices]
    else:
        sampled_sequences = file_service.read(args.in_file, only=args.number)

    file_service.write(args.out_file, sampled_sequences)
    
    print("##############################################")
    print("#    Simon says: Thanks for using SSfSBT!    #")
    print("##############################################")

if __name__ == "__main__":
    main()