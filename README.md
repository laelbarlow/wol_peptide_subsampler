
# Web of Life project peptide sequence subsampling script

## Objective

Obtain peptide sequences for a manageable sampling of prokaryotic genomes for
small-scale comparative genomics and/or phylogenetics analyses. 

## Rationale

Inclusive databases such as the NCBI nr database contain data for so many
prokaryotic genomes, that obtaining sequences from a representative sampling of
bacteria or archaea via NCBI's Basic Local Alignment Search Tool (BLAST) or
other means becomes difficult. This is especially true for highly conserved
genes. 

Zhu *et al*. describe a systematic selection of representative prokaryotic
genomes in this article:

    Zhu, Q., Mai, U., Pfeiffer, W., Janssen, S., Asnicar, F., Sanders, J.G.,
    Belda-Ferre, P., Al-Ghalith, G.A., Kopylova, E., McDonald, D., Kosciolek,
    T., Yin, J.B., Huang, S., Salam, N., Jiao, J.-Y., Wu, Z., Xu, Z.Z.,
    Cantrell, K., Yang, Y., Sayyari, E., Rabiee, M., Morton, J.T., Podell, S.,
    Knights, D., Li, W.-J., Huttenhower, C., Segata, N., Smarr, L., Mirarab,
    S., Knight, R., 2019. Phylogenomics of 10,575 genomes reveals evolutionary
    proximity between domains Bacteria and Archaea. Nat Commun 10, 5477.
    https://doi.org/10.1038/s41467-019-13443-4

They provide a data sheet of information about each of the genomes they
selected, including taxonomic information and information on assembly quality,
etc. here:

    https://biocore.github.io/wol/data/genomes/metadata.tsv.bz2


They describe how to retrieve their genome and protein data here (you have to
use [Globus](https://docs.globus.org/how-to/get-started/)):

    https://biocore.github.io/wol/data/genomes/


For smaller-scale comparative genomics studies, it will be necessary to obtain
a subsampling of these 10,575 representative genomes in a systematic manner
according to measures of quality and taxonomic diversity. That is what this
script does.


## Software requirements

- Linux or MacOS operating system
- Python3
- The pandas python library
- Git
- bzip2


## Procedure

- Obtain the `per_genome.tar` file containing peptide sequence FASTA files from
  here via Globus:
    https://app.globus.org/file-manager?origin_id=31acbeb8-c62f-11ea-bef9-0e716405a293&origin_path=%2Fproteins%2F

- Unzip decompress the tar file.

- Clone this repository.
    ```
    git clone ...
    ```

- Change directories into the repository.
    ```
    cd ...
    ```

- Subsample the protein sequence files according to measures of quality and
  taxonomic diversity (as detailed in the TSV file).
    ```
    python3 subsample_wol_peptides.py <path to per_genome dir>
    ```

- Examine the CSV file with information for only the subsampled genomes here:
   ```
   ...
   ```

- Proceed with downstream analysis of the selected peptide FASTA file here:
    ```
    ...
    ```


## License

MIT License

Copyright (c) 2020 Lael D. Barlow

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

