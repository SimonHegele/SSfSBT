# SSfSBT
Small Scripts for Small Bioinformatics Tasks.

Whenever I have a small task that I or someone else might face again at hand I will upload a script for it here.

## Installation

Python >= 3.5 (I'm using type hints)

Dependencies:
- matplotlib
- numpy
- pandas
- polars

`git clone https://github.com/SimonHegele/SSfSBT`<br>
`cd SSfSBT`<br>
`pip install .` (installs missing dependencies)

## Usage

### Subsampling reads

`python3 sample_reads.py [-h] [-r RANDOM] number in_file out_file`

If -r is set a random sample is selected,<br>
else simply the first reads of the files are used.

Suggestion: -> Consider using Seqtk (https://github.com/lh3/seqtk) instead.

### Converting expression files for NanoSim

`python3 expression4nanosim.py [-h] [--remove_underscore] kallisto_file nanosim_file`

Expression profiles are usually stored in .tsv-files with three rows ("target_id","est_counts","tpm").<br>
Some tools like Kallisto (https://github.com/pachterlab/kallisto) produce files with additional columns,<br>
but NanoSim will not be able to read them.<br>
Also, NanoSim has/had a bug where underscores in the target_id will cause it to fail,<br>
so there is an option to remove them.

### Basic read length analysis

`python3 read_lengths.py [-h] file`

Will create a .tsv with the number of reads, number of bases, minimum read length, average read length, maximum read length and standart deviation of the reads.<br>
Will also create a violinplot for the read length distribution.

### Converting FASTA-files with LoRDEC-corrected long reads to FASTQ-files

`python3 lordec_fa2fq [-h] [--offset OFFSET] LoRDEC_fasta S s`

LoRDEC outputs sequences with upper case characters for corrected bases and lower case characters for uncorrected bases in FASTA-format.<br>
Some tools like RATTLE or isONform however, prefer or require long reads in FASTQ-format.<br>
This script will convert FASTA-files to FASTQ-files with Phred-scores according to the input quality-scores S for upper case bases and s for lower case bases<br>

Example:<br>
`lordec_fa2fq lordec.fasta 0.01 0.10`

## Bugs / Known issues
