from argparse   import ArgumentParser
from os.path    import isfile

from file_services.utils import get_read_reader

class MyArgumentParser(ArgumentParser):

    prog        =   "unambigous_codes"

    description =   """
                    Replacing ambigouity codes in FASTA/FASTQ with A,C,G or T
                    """
    
    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)

        self.add_argument("in_file")
        self.add_argument("out_file")
        
    def parse_args(self):

        self.args = super().parse_args()

        if not isfile(self.args.in_file):
            raise Exception("Input file does not exist")
        
        if isfile(self.args.out_file):
            raise Exception("Output file exists")
        
        return self.args
    
def main():

    args = MyArgumentParser().parse_args()

    fs = get_read_reader(args.in_file)

    fs.write(args.out_file,
             fs.unambigous_codes(fs.read(args.in_file)))
    
    print("##############################################")
    print("#    Simon says: Thanks for using SSfSBT!    #")
    print("##############################################")

if __name__ == "__main__":
    main()