from argparse   import ArgumentParser
from os         import path
from random     import sample

from file_services.utils import get_read_reader, get_read_writer

class MyArgumentParser(ArgumentParser):

    prog        =   "SampleReads"

    description =   """
                    ----------
                    Commandline tool for sampling reads from fastq.
                    
                    """
    
    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)

        self.add_argument("number", help="Number of reads to sample")
        self.add_argument("in_file")
        self.add_argument("out_file")
        self.add_argument("-r", "--random", help="Use to sample randomly from the file instead of using the first n reads")

    def parse_args(self):

        self.args = super().parse_args()

        if not path.isfile(self.args.in_file):
            raise Exception("Input file does not exist")
        
        if path.isfile(self.args.out_file):
            raise Exception("Output file exists")
        
        return self.args
        

def sample_first_n_reads(in_file, n):

    return list(get_read_reader(in_file).read(in_file, only=n))
    #return [read for i, read in enumerate(get_read_reader(in_file).read(in_file)) if i<n]

def sample_random_reads(in_file, n): 

    reads          = list(get_read_reader(in_file).read(in_file))
    sample_indices = sample(range(len(reads)), n)

    return [read for i, read in enumerate(reads) if i in sample_indices]

def main():

    args = MyArgumentParser().parse_args()

    print("Sampling ...")

    if args.random == None:
        sampled_reads = sample_first_n_reads(args.in_file, int(args.number))
    else:
        sampled_reads =sample_random_reads(args.in_file, int(args.number))

    print("Writing ...")

    get_read_writer(sampled_reads[0]).write(args.out_file, sampled_reads)

    print("-----DONE-----")

if __name__ == "__main__":
    main()