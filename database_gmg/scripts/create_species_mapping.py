#!/usr/bin/env python
"""
Annotates a file

Example usage:
"""

import argparse
import csv
from collections import defaultdict
from dojo.taxonomy import NCBITree
import sys


def make_arg_parser():
    parser = argparse.ArgumentParser(description='')
    # genomes_path = os.path.join('..', 'results', '170214-simulation', 'genomes')
    parser.add_argument('-r', '--headers', type=str, required=True)
    parser.add_argument('-c', '--refseq_catalog', type=str, required=True)
    # os.path.join('..', 'results', 'genome_lengths.json'), 'w'
    # parser.add_argument('-o', '--output', type=str, required=True)
    return parser


def main():
    parser = make_arg_parser()
    args = parser.parse_args()

    refseq_accession_to_taxid = defaultdict(str)
    ncbi_tree = NCBITree()

    with open(args.refseq_catalog) as inf:
        for line in inf:
            line = line.strip().split('\t')
            refseq_accession_to_taxid[line[1]] = line[0]

    no_mapping = 0
    taxids = set()
    species_taxids = set()

    print('rid\ttaxid\tspecies_taxid')

    with open(args.headers) as inf:
        for line in inf:
            line = line.strip()
            taxid = refseq_accession_to_taxid[line]
            taxids.add(taxid)
            if taxid:
                species_taxid = str(ncbi_tree.get_rank_with_taxon_id(int(taxid), 'species')[0])
                species_taxids.add(species_taxid)
            else:
                species_taxid = ''
                no_mapping += 1
            print('%s\t%s\t%s' % (line, refseq_accession_to_taxid[line], species_taxid))
    print(no_mapping, file=sys.stderr)
    print(len(taxids), file=sys.stderr)
    print(len(species_taxids), file=sys.stderr)

if __name__ == '__main__':
    main()