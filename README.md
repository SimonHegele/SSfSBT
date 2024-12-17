# SSfSBT
Small Scripts for Small Bioinformatics tasks

## Requirements

- python3
- polars

## Usage

### Converting expression files for NanoSim

Expression profiles are usually stored in -tsv-files with three rows ("target_id","est_counts","tpm").
Some tools like Kallisto produce additional columns, but NanoSim will not be able to read them.

