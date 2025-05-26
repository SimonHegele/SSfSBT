from argparse           import ArgumentParser
from logging            import basicConfig, error, info, INFO, StreamHandler
from matplotlib.pyplot  import legend, savefig, subplots, subplots_adjust
from multiprocessing    import Pool
from numpy              import log10, min, max, sum, sqrt
from pandas 	        import DataFrame
from random             import randint
from seaborn            import kdeplot
from sys                import stdout
from time               import time

from file_services  import utils

class MyArgumentParser(ArgumentParser):

    prog        =   "lengths"

    description =   """
                    Basic read length distribution analysis.
                    """
    
    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)

        self.add_argument("files",
                          help="FASTA/FASTQ-file(s)",
                          nargs='+',
                          type=str)
        self.add_argument("-c","--colors",
                          help    = "Hexcodes for plotting",
                          type    = list,
                          default = [],
                          metavar="")
        self.add_argument("-s","--scale",
                          help="y-axis scale plots [default: linear]",
                          metavar="",
                          default="linear")
        self.add_argument("-p", "--prefix",
                          help="prefix for output-files [default: ssfsbt.lengths]",
                          default="ssfsbt.lengths",
                          metavar="")
        self.add_argument("-t","--threads",
                          help="number of parallel threads to use for counting [default: 1]",
                          type=int,
                          default=1,
                          metavar=""
                          )

class AutoList(list):

    def __init__(self, default_factory=lambda: None):
        super().__init__()
        self.default_factory = default_factory

    def __getitem__(self, index):
        if index >= len(self):
            self.extend(self.default_factory() for _ in range(index + 1 - len(self)))
        return super().__getitem__(index)

    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend(self.default_factory() for _ in range(index + 1 - len(self)))
        super().__setitem__(index, value)

def count_sequence_lengths(file: str) -> list[int]:

    start = time()

    reader = utils.get_read_reader(file)
    counts = AutoList(default_factory=lambda: 0)

    if reader is None:
        error(f"Cannot read {file}")
        return list(counts)
    
    for sequence in reader.read(file):
        counts[sequence["length"]] += 1

    info(f"Completed length counting for {file} in {round(time()-start,2)} seconds")

    return list(counts)

def compile_data(file: str,
                 length_count: list[int]) -> DataFrame:

    def get_min_len(length_count: list[int]) -> int:
        for i, c in enumerate(length_count):
            if c > 0:
                return i
            
    def get_n_reads(length_count: list[int]) -> int:       
        return sum(length_count)
    
    def get_n_bases(length_count: list[int]) -> int:
        return sum([c*i for i, c in enumerate(length_count)])
    
    def get_mean_len(length_count: list[int]) -> int:
        return int(get_n_bases(length_count)/get_n_reads(length_count))
    
    def get_std(length_count: list[int]) -> float:
        n = get_n_reads(length_count)
        m = get_mean_len(length_count)
        return sqrt(sum([((i-m)**2)*(c/n) for i, c in enumerate(length_count)]))
    
    return {"File": file,
            "# Sequences":  get_n_reads(length_count),
            "# Bases":      get_n_bases(length_count),
            "Min len":      get_min_len(length_count),
            "Mean len":     get_mean_len(length_count),
            "Max len":      len(length_count),
            "Std":          int(get_std(length_count))
            }

def compile_data_threaded(args):

    return compile_data(args[0], args[1])

def plot(length_counts: list[int],
         dataframe: DataFrame,
         colors: list[str],
         scale: str,
         prefix: str):

    fig, axes = subplots(2)

    def formatting():

        axes[0].set_xlabel("Length", fontweight="bold")
        axes[0].set_ylabel("Cummulative counts", fontweight="bold")
        axes[0].set_yscale(scale)
        axes[0].set_xlim(xmin=0,xmax=max_len)

        axes[1].set_xlabel("Length", fontweight="bold")
        axes[1].set_ylabel("Frequencies", fontweight="bold")

        legend(bbox_to_anchor=(0.25, -0.25, 0, 0))
        subplots_adjust(hspace=0.3)

    def cummulative(length_count: list[int]) -> list[int]:
        c = [0]
        for j in range(1,len(length_count)):
            c.append(c[-1]+length_count[j])
        return c
    
    def random_hex_color():
        return "#{:06x}".format(randint(0, 0xFFFFFF))

    max_len = max([len(length_count) for length_count in length_counts])

    for i, length_count in enumerate(length_counts):
        
        if len(colors) < len(length_counts):
            colors.append(random_hex_color())
        
        axes[0].plot(list(range(len(length_count))),
                     cummulative(length_count),
                     label = dataframe.iloc[i]["File"],
                     color = colors[i])
        
        axes[1].hist(length_count,
                     histtype="step",
                     bins=10*int(log10(max_len)),
                     label = dataframe.iloc[i]["File"],
                     color = colors[i])
        
    formatting()
    savefig(prefix+".png", bbox_inches = "tight")
    
def main():

    start = time()

    basicConfig(level = INFO,
                format   = "%(asctime)s %(levelname)s %(message)s",
                datefmt  = "%d-%m-%Y %H:%M:%S",
                handlers = [StreamHandler(stream=stdout)]
                )

    args  = MyArgumentParser().parse_args()

    with Pool(min([args.threads, len(args.files)])) as pool:
        length_counts = pool.map(count_sequence_lengths, args.files)

    with Pool(min([args.threads, len(args.files)])) as pool:
        data = pool.map(compile_data_threaded, zip(args.files, length_counts))

    dataframe = DataFrame(data,
                          columns=["File",
                                   "# Sequences",
                                   "# Bases",
                                   "Min len",
                                   "Mean len",
                                   "Max len",
                                   "Std"])

    print("\n",dataframe,"\n")
    dataframe.to_csv(args.prefix + ".tsv", sep="\t")

    plot(length_counts, dataframe, args.colors, args.scale, args.prefix)

    info(f"Completed in {round(time()-start,2)} seconds\n")

    info("##############################################")
    info("#    Simon says: Thanks for using SSfSBT!    #")
    info("##############################################")
    
if __name__ == "__main__":
    main()
