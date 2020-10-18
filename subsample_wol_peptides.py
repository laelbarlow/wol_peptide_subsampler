#!/usr/bin/env python3
"""Script for parsing TSV file from
https://biocore.github.io/wol/data/genomes/metadata.tsv.bz2 and selecting a
subset of rows for a manageable number of representatives.

"""

import os
import sys
import subprocess
import glob
import shutil
import pandas as pd



def remove_rows_with_redundant_taxa(df):
    """Take a dataframe and return a new dataframe with rows removed if they
    contain info for taxonomically redundant genomes.
    """
    # Iterate over rows and compile a list of indices to exclude.
    indices_for_removal = []
    phyla_sampled = []
    for index, row in df.iterrows():
        if row['phylum'] == '':
            indices_for_removal.append(index)
        else:
            # Assign a taxon object to the row.
            taxon = None
            if row['superkingdom'] == 'Bacteria':
                # Only one genome per phylum for bacteria.
                taxon = row['phylum'].replace('Candidatus ', '')
            elif row['superkingdom'] == 'Archaea':
                # One genome per class for archaea.
                taxon = (row['phylum'].replace('Candidatus ', ''),
                         row['class'].replace('Candidatus ', ''))
                #row['order'].replace('Candidatus ', ''))
            assert taxon is not None

            if taxon not in phyla_sampled:
                phyla_sampled.append(taxon)
            else:
                indices_for_removal.append(index)
    
    # Exclude rows with identified indices.
    df = df.drop(indices_for_removal)

    # Return dataframe with rows removed.
    return df



if __name__ == '__main__':

    # Parse command line arguments.
    cmdln = sys.argv
    peptide_zip_file_dir = cmdln[1]

    # Make output directories (overwrite if already exists).
    outdir = 'results'
    if os.path.isdir(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)

    # Download TSV file.
    location = 'https://biocore.github.io/wol/data/genomes/metadata.tsv.bz2'
    destination = os.path.join('results', location.rsplit('/', 1)[1])
    subprocess.call(['curl', location, '--output', destination])

    # Unzip TSV file.
    tsv_file = destination.rsplit('.', 1)[0]
    subprocess.call(['bzip2', '-d', destination])
    
    # Parse TSV file.
    df = pd.read_csv(tsv_file, sep='\t', keep_default_na=False)
    
    # Exclude unclassified genomes.
    df = df[df.classified != False]
    

    #################################################################
    # Select bacteria.
    
    df_bact = df[df.superkingdom == 'Bacteria']
    
    # Exclude low draft_quality genomes.
    df_bact = df_bact[df_bact.draft_quality != 'low']
    
    # Exclude genomes of medium draft_quality.
    df_bact = df_bact[df_bact.draft_quality != 'medium']
    
    # Exclude genomes with completeness below 90%.
    df_bact = df_bact[df_bact.completeness >= 90.00]
    
    # Sort genomes by descending completeness.
    #df_bact = df_bact.sort_values(by = ['draft_quality']) 
    df_bact = df_bact.sort_values(by = ['contamination']) 
    df_bact = df_bact.sort_values(by = ['completeness'], ascending=False) 
    
    # Remove taxonomically redundant genomes.
    df_bact = remove_rows_with_redundant_taxa(df_bact)
    

    #################################################################
    
    # Select archaea.
    
    df_arch = df[df.superkingdom == 'Archaea']
    
    # Sort genomes by descending completeness, etc.
    df_arch = df_arch.sort_values(by = ['draft_quality']) 
    df_arch = df_arch.sort_values(by = ['contamination']) 
    df_arch = df_arch.sort_values(by = ['completeness'], ascending=False) 
    
    # Remove taxonomically redundant genomes.
    df_arch = remove_rows_with_redundant_taxa(df_arch)
    

    #################################################################
    
    # Combine dataframes.
    combined_df = pd.concat([df_bact, df_arch])
    
    # Write combined dataframe.
    out_file =  os.path.join(outdir, \
            os.path.basename(tsv_file).rsplit('.', 1)[0] + '_subsample.csv')
    combined_df.to_csv(out_file, index=False)


    #################################################################

    # Collect relevant predicted peptide FASTA files.

    # Define list of relevant genome IDs.
    genome_ids = list(combined_df['#genome'])

    # Define unique names corresponding to each genome ID.
    genome_names = {}
    for index, row in combined_df.iterrows():
        genome_names[row['#genome']] = row['unique_name']

    # define FASTA output subdir.
    faa_output_subdir = os.path.join(outdir, 'peptide_seqs_subsample')

    # Initiate list of genome IDs not found.
    gids_not_found = genome_ids

    # Iterate over compressed FASTA files in input directory.
    for f in glob.glob(os.path.join(peptide_zip_file_dir, '*.bz2')):
        gid = os.path.basename(f).split('.')[0]
        if gid in genome_ids:
            # Remove from not found list.
            gids_not_found.remove(gid)
            # Define name of new file.
            f2_bn = gid + '_' + genome_names[gid] + '.faa.bz2' 
            f2 = os.path.join(faa_output_subdir, f2_bn) 
            # Copy file to new path. 
            shutil.copyfile(f, f2)
            # Unzip file copy.
            #subprocess.call(['bzip2', '-d', f2])

    # Check that all the relevant files were found.
    assert len(gids_not_found) == 0, """Could not identify files with the
    following genome numbers:
%s""" % '\n'.join(gids_not_found)
         

