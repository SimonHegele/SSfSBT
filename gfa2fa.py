from argparse   import ArgumentParser
from typing     import Generator

from file_services.fasta_file_service   import FastaFileService
from file_services.gfa_file_service     import GfaFileService, Segment

class MyArgumentParser(ArgumentParser):

    prog        =   "gfa2fa"

    description =   """
                    GFA to FASTA conversion
                    """
    
    def __init__(self) -> None:

        super().__init__(prog=self.prog, description=self.description)

        self.add_argument("GFA")
        self.add_argument("FASTA")
        
def gfa2fa(gfa: str) -> Generator:
    
    for gfa_element in GfaFileService.read(gfa):
        
        if isinstance(gfa_element, Segment):
            
            yield {"header":    gfa_element.name,
                   "sequence":  gfa_element.sequence}
        
def main():
    
    args = MyArgumentParser().parse_args()
    
    FastaFileService.write(args.FASTA, gfa2fa(args.GFA))
    
    print("##############################################")
    print("#    Simon says: Thanks for using SSfSBT!    #")
    print("##############################################")
    
if __name__ == "__main__":
    main()