from argparse   import ArgumentParser
from itertools  import chain
from logging    import info, basicConfig, INFO, StreamHandler
from os         import mkdir, path
from pandas     import read_csv, DataFrame
from sys        import stdout
from typing     import Generator, Iterable

from file_services.fasta_file_service import FastaFileService

class MyArgumentParser(ArgumentParser):

    prog        =   "busco_transcripts"

    description =   """
                    Identifying BUSCOs in assembled transcripts
                    """
    
    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)
        
        self.add_argument("blast_m8",
                          help="BLAST m8 file with transcripts mapped to reference BUSCOs")
        self.add_argument("outdir",
                          help="Output directory")
        
        self.add_argument("-f","--fasta",
                          metavar="",
                          help="FASTA file with assembled transcripts")
        self.add_argument("-b","--best_only",
                          action="store_true",
                          help="For each BUSCO")
        self.add_argument("-e","--exclude",
                          metavar="",
                          help="File with lists of IDs ofBUSCOs to exclude")
        
blast_m8_columns = ["query",
                    "target",
                    "% id",
                    "alignment length",
                    "mismatches",
                    "gap openings",
                    "query_start",
                    "query start",
                    "query end",
                    "target start",
                    "target end",
                    "e-value",
                    "bit-score"]

def get_excluded_buscos(exclude_file: str | None) -> list:
    
    if not exclude_file is None:
        with open(exclude_file,"r") as file:
            return list(file.readlines())
    
    return []

def get_matches(blast_m8: DataFrame,
                exclude: list[str],
                best_only: bool) -> dict[str, list[str]]:
    
    buscos   = blast_m8["target"].unique()
    matches  = dict()
    
    for i, busco in enumerate(buscos):
        
        busco_blast_m8 = blast_m8.loc[blast_m8["target"]==busco]
        
        if not busco in exclude:
        
            if best_only is None:
                matches[busco] = list(busco_blast_m8["query"])
            else:
                best_score     = busco_blast_m8["e-value"].min()
                best_match     = busco_blast_m8.loc[busco_blast_m8["e-value"]==best_score]
                matches[busco] = list(best_match["query"])
        
        blast_m8.drop(busco_blast_m8.index)
        
    return matches

def write_matched_buscos(matches: dict[str, list[str]], outdir: str):
    
    with open(path.join(outdir, "matched_buscos.txt"),"w") as file:
        
        for busco in sorted(matches.keys()):
            
            file.write(busco+"\n")
        
def write_matches(matches: dict[str, list[str]], outdir: str):
    
    with open(path.join(outdir, "matches.txt"),"w") as file:
        
        for busco in matches.keys():
            
            file.write(busco + "\t" + ";".join(matches[busco]) + "\n")
        
def filter_transcripts(matches: dict[str, list[str]],
                      transcripts: Iterable[dict[str, str]]) -> Generator:
    
    filter_IDs  = list(chain.from_iterable(matches.values()))
    
    for transcript in transcripts:
        
        transcript_id = transcript["header"][1:].split(" ")[0]
        
        if transcript_id in filter_IDs:
            filter_IDs.remove(transcript_id)
            yield transcript
              
def main():
    
    basicConfig(level    = INFO,
                format   = "%(asctime)s %(levelname)s %(message)s",
                datefmt  = "%d-%m-%Y %H:%M:%S",
                handlers = [StreamHandler(stream=stdout)]
                )
    
    args = MyArgumentParser().parse_args()
    
    if not path.isdir(args.outdir):
        mkdir(args.outdir)
    
    exclude  = get_excluded_buscos(args.exclude)
    
    info("Reading blast_m8 ...") 
    blast_m8 = read_csv(args.blast_m8, sep="\t", names=blast_m8_columns)
    
    info("Extracting matches ...")
    matches  = get_matches(blast_m8, exclude, args.best_only)
    
    info("Writing matches ...")
    write_matches(matches, args.outdir)
    write_matched_buscos(matches, args.outdir)
    
    if not args.fasta is None:
        
        info("Filtering for BUSCO transcripts")
    
        fs = FastaFileService()
        
        fs.write(path.join(args.outdir, "busco_transcripts.fasta"),
                filter_transcripts(matches, fs.read(args.fasta)))
    
    info("##############################################")
    info("#    Simon says: Thanks for using SSfSBT!    #")
    info("##############################################")
    
if __name__ == "__main__":
    main()