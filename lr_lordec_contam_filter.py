from argparse import ArgumentParser
from typing   import Iterable, Generator

from file_services.utils import get_read_reader

class MyArgumentParser(ArgumentParser):

    prog        =   "lr_lordec_contam_filter"

    description =   """
                    A simple script facilitating the filtering contaminations from
                    long reads corrected with LoRDEC using Kraken2-filtered short reads.
                    
                    (It removes long reads that were not corrected by LoRDEC)
                    """
    
    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)

        self.add_argument("longreads")
        self.add_argument("-m",
                          metavar="",
                          help="Minimum number of corrected bases in a long reads to accept [default: 21]",
                          default=21)
        self.add_argument("-v",
                          metavar="",
                          help="Report progress every v processed long reads [default: 100,000]",
                          default=100_000)

def main():

    args     = MyArgumentParser().parse_args()
    fs       = get_read_reader(args.longreads)
    accepted = []
    rejected = []
    
    bases_total                     = 0
    bases_accepted                  = 0
    bases_accepted_corrected        = 0
    bases_accepted_uncorrected      = 0
    bases_rejected                  = 0
    
    print("Reading and processing ...")

    for i, longread in enumerate(fs.read(args.longreads)):
        
        if i % args.v == 0:
            print(f"{i:>8}")
        
        bases_total += longread["length"]
        
        bases_corrected = len([c for c in longread["sequence"] if c.isupper()])
        
        if bases_corrected > args.m:
            accepted.append(longread)
            
            bases_accepted              += longread["length"]
            bases_accepted_corrected    += bases_corrected
            bases_accepted_uncorrected  += longread["length"] - bases_corrected
        else:
            rejected.append(longread)
            
            bases_rejected += longread["length"]
    
    print(f"{i:>8}")
    print("Writing ...")
    fs.write(args.longreads+".accepted", accepted)
    fs.write(args.longreads+".rejected", rejected)
    
    reads_accepted = len(accepted)
    reads_rejected = len(rejected)
    reads_total    = reads_accepted + reads_rejected

    print("##################################################################################")
    print(f"Reads accepted:     {reads_accepted:>10} ({(reads_accepted/reads_total)*100:.3f}%)")
    print(f"Reads rejected:     {reads_rejected:>10} ({(reads_rejected/reads_total)*100:.3f}%)")
    print()
    print(f"Bases accepted:     {bases_accepted:>10} ({(bases_accepted/bases_total)*100:.3f}%)")
    print(f"Bases rejected:     {bases_rejected:>10} ({(bases_rejected/bases_total)*100:.3f}%)")
    print()
    print("In accepted reads:")
    print(f"Bases corrected:    {bases_accepted_corrected:>10} ({(bases_accepted_corrected/bases_accepted)*100:.3f}%)")
    print(f"Bases uncorrected:  {bases_accepted_uncorrected:>10} ({(bases_accepted_uncorrected/bases_accepted)*100:.3f}%)")
    print()
    print("##############################################")
    print("#    Simon says: Thanks for using SSfSBT!    #")
    print("##############################################")

if __name__ == "__mai_":

    main()
