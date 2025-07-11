# SSfSBT
Small Scripts for Small Bioinformatics Tasks.

Collection of python scripts as a backup for me and hopefully a help for you!

For details on usage and examples, please refer to the [wiki](https://github.com/SimonHegele/SSfSBT/wiki).

## Installation

```
conda create -n ssfsbt # (optional but recommended)
conda activate ssfsbt  # (optional but recommended)

git clone https://github.com/SimonHegele/SSfSBT
cd SSfSBT
pip install .
```

## Contents

### Commandline-Tools

Tool              | Summary
------------------|--------
fa2fq             | FASTA to FASTQ conversion with different error rates for upper and lower case denoted nucleotides
sample            | Subsampling a fixed number of sequences from FASTA/FASTQ-files
lengths           | Basic sequence length distribution analysis for one or more FASTA/FASTQ-files
kallisto2nanosim  | Converting expression profiles from Kallisto for NanoSim
busco_merge       | Merging multiple reports from BUSCO and compiling a plot
unambiguous_codes | Replacing ambiguity codes in FASTA/FASTQ-files
rnaQUASTcompare   | Merging multiple reports from rnaQUAST and compiling a plot

### File-Services

SSfSBT provides a variety of file services that can read from and write to various files used in bioinformatics.
They are located in the file_services folder. Each file service is a class providing class methods.<br> 
Their read()-methods are generators, yielding dictionaries.<br>
Their write()-methods accept iterables of dictionaries.

| File type     | Can read | Can write | Additional info |
|---------------|----------|-----------|-----------------|
| FASTA         | ✅       | ✅       | Sequences
| FASTQ         | ✅       | ✅       | Sequences
| PAF           | ✅       | ✅       | Pairwise sequence alignments from [Minimap2](https://github.com/lh3/minimap2)
| SAM           | ✅       | ✅       | Pairwise sequence alignments from basically any other alignment tool
| BCALM (FASTA) | ✅       | ❌       | De Bruijn Graph from BCALM
| FASTG (FASTA) | ✅       | ❌       | De Bruijn Graph from SPAdes
