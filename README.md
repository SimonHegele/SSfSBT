# SSfSBT
Small Scripts for Small Bioinformatics tasks

## Requirements

- python3
- polars

## Usage

### Converting expression files for NanoSim

`python3 expression4nanosim.py --remove_underscore kallisto_file nanosim_file`

Expression profiles are usually stored in -tsv-files with three rows ("target_id","est_counts","tpm").
Some tools like Kallisto produce additional columns, but NanoSim will not be able to read them.
Also, NanoSim has/had a bug where underscores in the target_id will cause it to fail, 
so there is an option to remove them.
