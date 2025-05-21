# SSfSBT
Small Scripts for Small Bioinformatics Tasks.

Collection of python scripts as a backup for me and hopefully a help for you!

**Table of contents**
1. Installation
2. Usage<br>
&emsp;2.1 Commandline-Tools<br>
&emsp;&emsp;2.1.1 fa2fq<br>
&emsp;&emsp;2.1.2 sample<br>
&emsp;&emsp;2.1.3 lengths<br>
&emsp;&emsp;2.1.4 kallisto2nanosim<br>
&emsp;&emsp;2.1.5 busco_merge<br>
&emsp;2.2 File services

## 1 Installation

Python >= 3.5 (I'm using type hints)

`git clone https://github.com/SimonHegele/SSfSBT`<br>
`cd SSfSBT`<br>
`pip install .`

## 2 Usage

### 2.1 Commandline-Tools:

**2.2.1 fa2fq**

Converting FASTA to FASTQ where lower and upper case denoted bases have different expected
error rates.

Examplary usecase:<br>
The hybrid long read error correction tool [LoRDEC]([https://example.com)](http://www.atgc-montpellier.fr/lordec/) outputs corrected
long reads in FASTA-format with upper case characters for corrected regions and lower case
characters for uncorrected regions. Long read transcriptome assembly tools such as 
[RATTLE](https://github.com/comprna/RATTLE) or [isON](https://github.com/aljpetri/isONform)
accept or expect long reads in FASTQ-format. Using long reads precorrected with LoRDEC
and their expected quality added with fa2fq can improve the accuracy of the resulting
assembly.

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
```

**2.2.2 sample**

Sampling sequences from FASTA/FASTQ-files.

```
usage: sample [-h] [-r] number in_file out_file

Sampling sequences from FASTA/FASTQ.

positional arguments:
  number        Number of sequences to sample
  in_file
  out_file

options:
  -h, --help    show this help message and exit
  -r, --random  Sample randomly instead of first n sequence (slower)
```

**2.2.3 lengths**

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

**2.2.4 kallisto2nanosim**

Converting transcript abundance files from [Kallisto](https://github.com/pachterlab/kallisto)
for [NanoSim](https://github.com/bcgsc/NanoSim).<br>
Why is this conversion required?<br>
1. NanoSim can only read TSV-files with exactly three columns but Kallisto outputs five
2. NanoSim has/had a bug where underscores in the target_id will cause it to fail 

Examplary usecase:<br>
For the evaluation of hybrid tools using short and long RNAseq reads you might want to simulate long reads with NanoSim that match the expression profile in your short read data.

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

**2.2.4 busco_merge**

Compiles the results of a folder with [BUSCO](https://github.com/metashot/busco)-results into a single dataframe and plot that are addes them to the folder.

### 2.2 File services

The folder file_services contains usefull file services that can read from and write to various files used in bioinformatics.<br>
Their read()-methods are generators, yielding dictionaries.<br>
Their write()-methods accept iterables of dictionaries.

| File type    | Can read     | Can write    | Additional info |
|--------------|--------------|--------------|-----------------|
| FASTA        | ✅ | ✅ | Sequences
| FASTQ | ✅ | ✅ | Sequences
| PAF | ✅ | ✅ | Pairwise sequence alignments from [Minimap2](https://github.com/lh3/minimap2)
| SAM | ✅ | ✅ | Pairwise sequence alignments from basically any other alignment tool
| BCALM (FASTA) | ✅ | ❌ | De Bruijn Graph from BCALM
| FASTG (FASTA) | ✅ | ❌ | De Bruijn Graph from SPAdes
