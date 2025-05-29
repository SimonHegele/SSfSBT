# SSfSBT
Small Scripts for Small Bioinformatics Tasks.

Collection of python scripts as a backup for me and hopefully a help for you!

For details on installation, usage and examples, please refer to the [wiki](https://github.com/SimonHegele/SSfSBT/wiki).

## Contents

### Commandline-Tools

Tool              | Summary
------------------|--------
fa2fq             | FASTA to FASTQ conversion with different error rates for upper and lower case denoted nucleotides
sample            | Subsampling a fixed number of sequences from FASTA/FASTQ-files
lengths           | Basic sequence length distribution analysis for one or more FASTA/FASTQ-files
kallisto2nanosim  | Converting expression profiles from Kallisto for NanoSim
busco_merge       | Merging multiple reports from BUSCO
unambigous_codes  | Replacing ambiguity codes in FASTA/FASTQ-files

### File-Services

| File type     | Can read | Can write | Additional info |
|---------------|----------|-----------|-----------------|
| FASTA         | ✅       | ✅       | Sequences
| FASTQ         | ✅       | ✅       | Sequences
| PAF           | ✅       | ✅       | Pairwise sequence alignments from [Minimap2](https://github.com/lh3/minimap2)
| SAM           | ✅       | ✅       | Pairwise sequence alignments from basically any other alignment tool
| BCALM (FASTA) | ✅       | ❌       | De Bruijn Graph from BCALM
| FASTG (FASTA) | ✅       | ❌       | De Bruijn Graph from SPAdes
