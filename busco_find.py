from argparse   import ArgumentParser
from numpy      import log10
from os         import mkdir, path
from pandas     import DataFrame, concat
from time       import time
from typing     import Iterable, Generator


from file_services.fasta_file_service import FastaFileService

class MyArgumentParser(ArgumentParser):

    prog        =   "busco_find"

    description =   """
                    Extracting BUSCOs sequences from transcriptome assemblies
                    """
    
    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)
        
        self.add_argument("transcriptome",
                          help="FASTA-file with transcripts")
        self.add_argument("buscotable",
                          help="Full table from corresponding BUSCO run")
        self.add_argument("outdir",
                          help="Output directory")
        
        self.add_argument("-l","--longest",
                          help="For duplicated BUSCOs choose the longest transcript only",
                          action="store_true")
        self.add_argument("-b","--best",
                          help="For duplicated BUSCOs choose the best scoring transcript only",
                          action="store_true")
        self.add_argument("-e", "--exclude",
                          help="File containing a list of IDs of BUSCOs to exclude",
                          metavar="")
        self.add_argument("-v","--verbosity",
                          help="Verbosity level. Report progress after each 10^v scanned transcripts [default: 5]",
                          metavar="",
                          type=int,
                          default=5)
        
    def parse_args(self):
        
        args = super().parse_args()
        
        if args.longest and args.best:
            print("Chose either best or longest")
            exit(1)
            
        return args
    
def read_excludedlist(file_path: str) -> list[str]:
    
    if file_path is None:
        return []
    else:
        with open(file_path, "r") as file:
            return [id.rstrip() for id in file.readlines()]
        
def read_buscotable(file_path: str) -> DataFrame:
    
    data = {"BUSCO_id":     [],
            "TRANS_id":     [],
            "Fragmented":   [],
            "Score":        [],
            "Length":       [],
            "Description":  []}
    
    with open(file_path,"r") as file:
        
        for line in file.readlines():
            
            if line.startswith("#") or not line.count("\t")==6:
                continue
            
            line = line.rstrip().split("\t")
            
            data["BUSCO_id"]    += [line[0]]
            data["TRANS_id"]    += [line[2].split(":")[0]]
            data["Fragmented"]  += [line[1]=="Fragmented"]
            data["Score"]       += [line[3]]
            data["Length"]      += [line[4]]
            data["Description"] += [line[6]]
            
    return DataFrame(data)

def filter_buscotable(busco_table: DataFrame,
                      best:        bool,
                      longest:     bool,
                      exclude:     str) -> DataFrame:
    
    busco_table = busco_table.loc[~busco_table["BUSCO_id"].isin(read_excludedlist(exclude))]
    
    if not (best or longest):
        return busco_table
    
    busco_subtables = [busco_table.loc[busco_table["BUSCO_id"]==id]
                       for id in busco_table["BUSCO_id"].unique()]
    
    if best:
        busco_subtables = [subtable.loc[subtable["Score"]==subtable["Score"].max()]
                           for subtable in busco_subtables]
    if longest:
        busco_subtables = [subtable.loc[subtable["Score"]==subtable["Score"].max()]
                           for subtable in busco_subtables]
    
    return concat(busco_subtables)

def filter_transcriptome(transcriptome: Iterable[dict[str, str]],
                         busco_table:   DataFrame,
                         verbosity:     int) -> Generator:
    
    found   = 0
    to_find = len(busco_table)
    start   = time()
    
    for i, transcript in enumerate(transcriptome):
        
        transcript_id = transcript["header"].split(" ")[0]
        
        if transcript_id in list(busco_table["TRANS_id"].unique()):
            
            row = busco_table.loc[busco_table["TRANS_id"]==transcript_id]
            idx = row.index[0]
            row = row.iloc[0]
            var = str(len(busco_table.loc[busco_table["BUSCO_id"]==row["BUSCO_id"]]))
            
            transcript["header"]  = ">" + row["BUSCO_id"] + "_" + var + "_" + row["TRANS_id"]  + " "
            transcript["header"] += "Fragmented:"   + str(row["Fragmented"])
            transcript["header"] += ";Score:"       + str(row["Score"])
            transcript["header"] += ";Length:"      + str(row["Length"])
            transcript["header"] += ";Description:" + str(row["Description"])
            
            found += 1        
            busco_table.drop(idx)
            
            yield transcript
            
        if i % 10**verbosity == 0 or len(busco_table) == 0:
            print(f"Scanned: {i:>6}, found {found:>4} of {to_find} ({int(time()-start)} seconds)")
    
    print(f"Scanned: {i:>6}, found {found:>4} of {to_find} ({int(time()-start):>3} seconds)")

def main():
    
    args          = MyArgumentParser().parse_args() 
    busco_table   = read_buscotable(args.buscotable)
    busco_table   = filter_buscotable(busco_table, args.best, args.longest, args.exclude)
    
    print(busco_table)
    
    if not path.isdir(args.outdir):
        mkdir(args.outdir)
    
    with open(path.join(args.outdir, "buscos.txt"),"w") as file:
        for busco_id in busco_table["BUSCO_id"].unique():
            file.write(busco_id+"\n")
    
    transcriptome = FastaFileService().read(args.transcriptome)
    buscos        = filter_transcriptome(transcriptome, busco_table, args.verbosity)

    FastaFileService().write(path.join(args.outdir, "buscos.fasta"), buscos)
    
    print("##############################################")
    print("#    Simon says: Thanks for using SSfSBT!    #")
    print("##############################################")
