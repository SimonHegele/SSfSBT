from argparse           import ArgumentParser
from collections        import defaultdict
from logging            import basicConfig, INFO, info, StreamHandler
from itertools          import chain
from multiprocessing    import Pool
from numpy              import sum, ceil
from pandas             import DataFrame
from os.path            import isfile
from random             import choice
from sys                import stdout
from typing             import Iterable

from file_services.utils import get_read_reader

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
                          default=1)
        
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
    
def replace(sequences: Iterable[dict]):

    n_bases   = 0
    n_seqs    = 0
    replaced  = defaultdict(int)

    for i, sequence in enumerate(sequences):
        if i % 100_000 == 0 and i > 0:
            print(f"Processed: {i:>10}")
        n_bases += sequence["length"]
        n_seqs  += 1
        for i, base in enumerate(sequence["sequence"]):
            if not base in "ACGT":
                replaced[base] += 1
                sequence["sequence"]
        yield sequence

    def report():

        keys = sorted(map.keys(), key=lambda key: len(map[key]))

        codes = keys + ["Any"]
        bases = [map[key] for key in keys] + [["A","C","G","T"]]
        repla = [replaced[key] for key in keys] + [sum([replaced[key] for key in keys])]
        uncer = sum([replaced[key]/len(map[key]) for key in keys])/n_bases

        print(f"\n# Total sequences: {n_bases}")
        print(f"# Total bases: {n_bases}\n")

        print(DataFrame({"Ambigous code": codes,
                         "Bases":         bases,
                         "Replaced":      repla}))

        print(f"\nUncertainty: {uncer:.10f}\n")

    report()
       
def main():

    basicConfig(level = INFO,
                format   = "%(asctime)s %(levelname)s %(message)s",
                datefmt  = "%d-%m-%Y %H:%M:%S",
                handlers = [StreamHandler(stream=stdout)]
                )

    args = MyArgumentParser().parse_args()
    fs   = get_read_reader(args.in_file)
    t    = args.threads

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
    for bin in bins:
        fs.write(args.out_file, bin, mode="a")
    info("Done")

    keys           = sorted(map.keys(), key=lambda key: len(map[key]))
    total_replaced = defaultdict(int)

    for r in replaced:
        for key in r.keys():
            total_replaced[key] += r[key]

    total_replaced = [total_replaced[key] for key in keys]
    data           = {"Ambiguity code":   keys + ["All"],
                      "Bases":            [map[key] for key in keys] + [["A","C","G","T"]],
                      "Replaced":         total_replaced + [sum(total_replaced)]}
    
    print("\n",DataFrame(data),"\n")
    print(f"# Sequences: {n_sequences}")
    print(f"# Bases:     {n_bases}")
    print(f"Uncertainty: {sum([replaced[key]/len(map[key]) for key in keys])/n_bases:.10f}\n")
    
    info("##############################################")
    info("#    Simon says: Thanks for using SSfSBT!    #")
    info("##############################################")

if __name__ == "__main__":
    main()
