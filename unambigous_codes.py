from argparse           import ArgumentParser
from collections        import defaultdict
from datetime           import datetime
from logging            import basicConfig, INFO, info, StreamHandler
from itertools          import chain
from multiprocessing    import Pool
from numpy              import sum, ceil
from pandas             import DataFrame
from os                 import mkdir
from os.path            import isfile, join
from random             import choice
from shutil             import rmtree
from subprocess         import run
from sys                import stdout
from typing             import Iterable

from file_services.utils import get_read_reader, get_read_writer

class MyArgumentParser(ArgumentParser):

    prog        =   "unambigous_codes"

    description =   """
                    Replacing ambigouity codes in FASTA/FASTQ with A,C,G or T.
                    """
    
    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)

        self.add_argument("in_file")
        self.add_argument("out_file")
        self.add_argument("-t","--threads",
                          help="Number of parallel threads [default: 1]",
                          type=int,
                          default=1,
                          metavar="")
        self.add_argument("-tmp","--tempdir",
                          default=f"tmp_{datetime.now().strftime("%dd%mm%Yy_%Hh%Mm%Ss")}")
        
    def parse_args(self):

        self.args = super().parse_args()

        if not isfile(self.args.in_file):
            raise Exception("Input file does not exist")
        
        if isfile(self.args.out_file):
            raise Exception("Output file exists")
        
        return self.args
    
map = {"R": ["A","G"],
       "Y": ["C","T"],
       "S": ["G","C"],
       "W": ["A","T"],
       "K": ["G","T"],
       "M": ["A","C"],
       "B": ["C","G","T"],
       "D": ["A","G","T"],
       "H": ["A","C","T"],
       "V": ["A","C","G"],
       "N": ["A","C","G","T"]}

def process(sequences: list[dict]) -> tuple[list[dict], dict[str, int]]:

    replaced = defaultdict(int)

    for sequence in sequences:

        for i, base in enumerate(sequence["sequence"]):

            if not base in "ACGT":

                seq             = sequence["sequence"]
                replaced[base] += 1
                seq             = seq[:i] + choice(map[base]) + seq[i+1:]

    return sequences, replaced

def threaded_writing(args) -> None:

    file_path, sequences = args[0], args[1]

    fs = get_read_writer(sequences[0])
    fs.write(file_path, sequences)
       
def main():

    basicConfig(level = INFO,
                format   = "%(asctime)s %(levelname)s %(message)s",
                datefmt  = "%d-%m-%Y %H:%M:%S",
                handlers = [StreamHandler(stream=stdout)]
                )

    args = MyArgumentParser().parse_args()
    fs   = get_read_reader(args.in_file)
    t    = args.threads

    mkdir(args.tempdir)

    info("Loading sequences ...")
    sequences   = list(fs.read(args.in_file))
    n_sequences = len(sequences)
    n_bases     = sum([s["length"] for s in sequences])
    info("Done")

    info("Processing ...")
    size = ceil(len(sequences)/args.threads)
    bins = [sequences[int(size*i):int(min(size*(i+1), len(sequences)))]
            for i in range(args.threads)]
    with Pool(args.threads) as pool:
        results  = pool.map(process, bins)
        bins, replaced = zip(*results)
    info("Done")

    info("Writing sequences ...")
    with Pool(args.threads) as pool:
        tmp_files = [join(args.tempdir,f"uc{i}") for i in range(len(bins))]
        results   = pool.map(threaded_writing, zip(tmp_files, bins))
    run(f"cat {' '.join(tmp_files)} > {args.out_file}",
        shell=True,
        check=True)
    rmtree(args.tempdir)
    info("Done")

    keys           = sorted(map.keys(), key=lambda key: len(map[key]))
    total_replaced = defaultdict(int)

    for r in replaced:
        for key in r.keys():
            total_replaced[key] += r[key]

    u = (sum([(total_replaced[key]*(1-(1/len(map[key])))) for key in keys]))/(n_bases)

    total_replaced = [total_replaced[key] for key in keys]
    data           = {"Ambiguity code":   keys + ["All"],
                      "Bases":            [map[key] for key in keys] + [["A","C","G","T"]],
                      "Replaced":         total_replaced + [sum(total_replaced)]}
    
    print("\n",DataFrame(data),"\n")
    print(f"# Sequences: {n_sequences}")
    print(f"# Bases:     {n_bases}")
    print(f"Uncertainty: {u:.10f}\n")
    
    info("##############################################")
    info("#    Simon says: Thanks for using SSfSBT!    #")
    info("##############################################")

if __name__ == "__main__":
    main()
