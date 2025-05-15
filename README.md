# SSfSBT
Small Scripts for Small Bioinformatics Tasks.

Collection of python scripts as a backup for me and hopefully a help for you!

## Installation

Python >= 3.5 (I'm using type hints)

`git clone https://github.com/SimonHegele/SSfSBT`<br>
`cd SSfSBT`<br>
`pip install .`

## Usage

### Commandline Tools:

**fa2fq**

Converting FASTA to FASTQ where lower and upper case denoted bases have different expected
error rates.

Examplary usecase:
The hybrid long read error correction tool LoRDEC outputs corrected long reads in
FASTA-format with upper case characters for corrected regions and lower case characters
for uncorrected regions. Long read transcriptome assembly tools such as RATTLE or isON
accept or expect long reads in FASTQ-format. Using long reads precorrected with LoRDEC
and their expected quality added with fa2fq can benefit the resulting assembly.

```
usage: fa2fq [-h] [-o] [-v] FASTA S s

FASTA to FASTQ conversion

positional arguments:
  FASTA
  S               Expected error rate for bases denoted with upper case characters
  s               Expected error rate for bases denoted with lower case characters

options:
  -h, --help      show this help message and exit
  -o , --offset   Phred-quality offset (Default: 33)
  -v, --verbose   Show conversion progress
```

**sample**

Sampling sequences from FASTA/FASTQ-files.

```
usage: sample [-h] [-r] number in_file out_file

---------- Sampling sequences from FASTA/FASTQ.

positional arguments:
  number        Number of sequences to sample
  in_file
  out_file

options:
  -h, --help    show this help message and exit
  -r, --random  Sample randomly instead of first n sequence (slower)
```

**lengths**

Basic sequence length distribution analysis.
Outputs a TSV and a PNG.

```
usage: lengths [-h] [-s] file

Basic read length distribution analysis.

positional arguments:
  file           .fasta or .fastq

options:
  -h, --help     show this help message and exit
  -s , --scale   Setting y-axis scale for violin plot [default: linear]
```

**kallisto2nanosim**

Converting transcript abundance files from Kallisto for NanoSim.<br>
Why is this conversion required?<br>
1. NanoSim can only read TSV-files with exactly three columns but Kallisto outputs five
2. NanoSim has/had a bug where underscores in the target_id will cause it to fail 

Examplary usecase:
For the evaluation of tools using short and long RNAseq reads you might want to simulate long reads with NanoSim that match the expression profile in your short read data.

```
usage: kallisto2nanosim [-h] [--remove_underscore] kallisto_file nanosim_file

Converting Kallisto transcript abundance files for NanoSim.

positional arguments:
  kallisto_file
  nanosim_file

options:
  -h, --help           show this help message and exit
  --remove_underscore
```

### File services

The folder file_services contains usefull file services that can read from and write to various files used in bioinformatics. They accept / return dictionaries.

| File type    | Can read     | Can write    | Additional info |
|--------------|--------------|--------------|-----------------|
| FASTA        | ✅ | ✅ | Sequences
| FASTQ | ✅ | ✅ | Sequences
| PAF | ✅ | ✅ | Sequence alignments e.g. from Minimap2
| SAM | ✅ | ✅ | Sequence alignments 
| BCALM | ✅ | ❌ | De Bruijn Graph from BCALM
| FASTG | ✅ | ❌ | De Bruijn Graph from SPAdes

## Bugs / Known issues
