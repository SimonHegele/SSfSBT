# SSfSBT
Small Scripts for Small Bioinformatics Tasks

## Requirements

- python3

- matplotlib
- numpy
- pandas
- polars
  
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
