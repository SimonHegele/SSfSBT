from argparse           import ArgumentParser
from matplotlib.pyplot  import savefig, subplots, violinplot
from numpy              import min, sum, average, std
from os                 import path
from pandas 	        import DataFrame

from file_services  import utils

class MyArgumentParser(ArgumentParser):

    prog        =   "lengths"

    description =   """
                    Basic read length distribution analysis.
                    """
    
    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)

        self.add_argument("file", help=".fasta or .fastq")
        self.add_argument("-s","--scale",
                          help="Setting y-axis scale for violin plot [default: linear]",
                          metavar="",
                          default="linear"
                          )

    def parse_args(self):

        self.args = super().parse_args()

        if not path.isfile(self.args.file):
            raise Exception("file does not exist")
        
        return self.args
    
def main():

    args  = MyArgumentParser().parse_args()
    file  = args.file
    scale = args.scale

    print("Reading ...")
    read_lengths = [read["length"] for read in utils.get_read_reader(file).read(file)]
    print("Done")

    print("Evaluating ...")
    metrics = ["# reads","# bases","Min length","Avg length","Max length","Std"]
    values  = [len(read_lengths), sum(read_lengths), min(read_lengths), average(read_lengths), max(read_lengths), std(read_lengths)]
    values  = [int(round(v,0)) for v in values]
    print("Done")

    print("Data outputting ...")
    data = {"Metric": metrics,
            "Value":  values  }
    
    DataFrame(data).to_csv(file+".rld.tsv", sep="\t")

    fig, axes = subplots(figsize=(5,5))
    
    axes.set_yscale(scale)
    
    violinplot([read_lengths], showmeans=True)
    
    savefig(file+".rld.png")

    print("Done")
    print("##############################################")
    print("#    Simon says: Thanks for using SSfSBT!    #")
    print("##############################################")
    
if __name__ == "__main__":
    main()
