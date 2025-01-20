from argparse           import ArgumentParser
from matplotlib.pyplot  import savefig, subplots, violinplot
from numpy              import min, sum, average, std
from os                 import path
from pandas 	        import DataFrame

from file_services  import utils

class MyArgumentParser(ArgumentParser):

    prog        =   "read_lengths"

    description =   """
                    ----------
                    Commandline tool for basic read length distribution analysis
                    
                    """
    
    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)

        self.add_argument("file", help=".fasta or .fastq")

    def parse_args(self):

        self.args = super().parse_args()

        if not path.isfile(self.args.file):
            raise Exception("file does not exist")
        
        return self.args
    
def main():

    file = MyArgumentParser().parse_args().file

    read_lengths = [read["length"] for read in utils.get_read_reader(file).read(file)]

    metrics = ["# reads","# bases","Min length","Avg length","Max length","Std"]
    values  = [len(read_lengths), sum(read_lengths), min(read_lengths), average(read_lengths), max(read_lengths), std(read_lengths)]
    values  = [int(round(v,0)) for v in values]

    data = {"Metric": metrics,
            "Value":  values  }
    
    DataFrame(data).to_csv(file+".rld.tsv", sep="\t")

    fig, axes = subplots(figsize=(5,5))
    
    violinplot([read_lengths], showmeans=True)

    savefig(file+".rld.png")
    

if __name__ == "__main__":
    main()