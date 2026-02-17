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
                          help="Alignment file in FASTA-format")
        
        self.add_argument("-p","--position",
                          help="Only print alignment at chosen position (positions start with 1)",
                          type=int)
        self.add_argument("-s","--sequence",
                          help="Refer to position of given sequence instead of alignment position",
                          type=str)
        
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
    
    if args.position is None:
        print(alignment)
    else:
        if args.sequence is None:
            print(alignment.iloc[[args.position]])
        else:
            print(alignment.loc[alignment[f"Pos {args.sequence}"]==args.position])

if __name__ == "__main__":
    main() 