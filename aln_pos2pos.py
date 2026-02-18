from argparse       import ArgumentParser
from collections    import defaultdict
from pandas         import DataFrame

from file_services.fasta_file_service import FastaFileService

class MyArgumentParser(ArgumentParser):

    prog        =   "aln_pos2pos"

    description =   """
                    A simple script that helps to navigate (multiple) sequence alignments
                    """
    
    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)

        self.add_argument("alignment",
                          help="Alignment inputfile in FASTA-format")
        
        self.add_argument("output",
                          help="output directory for file in TSV-format")
        
def parse_alignment(fasta_entries: list[dict]) -> DataFrame:
    
    organisms = [fasta_entry["header"].split(" ")[0] for fasta_entry in fasta_entries]
    sequences = [fasta_entry["sequence"] for fasta_entry in fasta_entries]
    columns   = ["Pos alignment"]
    
    for organism in organisms:
        columns.append("Pos " + organism)
        columns.append("Res " + organism)
    
    data              = defaultdict(list)
    position_counters = [0 for i in range(len(fasta_entries))]
    
    for i in range(len(sequences[0])):
        data["Pos alignment"].append(i+1)
        for j, sequence in enumerate(sequences):
            if sequence[i] != "-":
                position_counters[j] += 1
                data[f"Pos {organisms[j]}"].append(position_counters[j])
            else:
                data[f"Pos {organisms[j]}"].append("-")
            data[f"Res {organisms[j]}"].append(sequence[i])
            
    return DataFrame(data, columns=columns).set_index("Pos alignment")
        
def main():
    
    args          = MyArgumentParser().parse_args()
    fasta_entries = list(FastaFileService().read(args.alignment))
    alignment     = parse_alignment(fasta_entries)
    
    alignment.to_csv(args.output + "ssfsbt_msa.tsv", sep="\t")


if __name__ == "__main__":
    main() 