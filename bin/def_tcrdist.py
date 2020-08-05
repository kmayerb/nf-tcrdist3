#!/usr/bin/env python
import argparse
import sys
import pandas as pd
import numpy as np
from tcrdist.repertoire import TCRrep

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_file", type=str,
                    help="input seqs file e.g., dash.csv")
parser.add_argument("-o", "--organism", default='mouse', type=str,
                    help="specifies relevant organism for analysis: 'human' or 'mouse'")
parser.add_argument("-c", "--chains", default = 'alpha,beta', type=str,
                    help="specifies relevant chains for single or paried TCR analysis (use lowercase letters and commas to separate multiple chains)")
parser.add_argument("--db_file", default = 'alphabeta_gammadelta_db.tsv', type=str,
                    help="x")
parser.add_argument("--imgt_aligned", default = True, type=str2bool,
                    help="If True, by default, cdr1, cdr2,and pmhc are inferred aligned to fixed length with gaps. If False, cdr1, cdr2,and pmhc are returned as ungapped raw sequences.")
parser.add_argument("--infer_cdrs", default = True, type=str2bool,
                    help="If True, infer cdr1, cdr2,and pmhc from the v gene name")
parser.add_argument("--infer_index_cols", default = True, type=str2bool,
                    help="If True, infer index_cols used to deduplicate cell_df")
parser.add_argument("--deduplicate", default = True, type=str2bool,
                    help=" If True, then clone_df will be assigned cell_df grouped_by index columns")
parser.add_argument("--compute_distances",  default = True, type=str2bool,
                    help="If True, save all distance matrices for each CDR (e.g., pw_cdr3_b_aa. If False, only save pw_alpha and pw_beta")
parser.add_argument("--store_all_cdr",  default = True, type=str2bool,help="If True, automatically compute distances")
parser.add_argument("--cpus",  default = 1, type=int,
                    help="Number of cpus to use. In general 1 cpu is sufficient from default Numba metric with less than 10^7 pairwise compairsons. However, more cpus will result in a speedup for metrics like pw.metrics.nw_hamming_metric for more than 10^6 pairwise compairsons.")                                                            
args = parser.parse_args()

print(args)

df = pd.read_csv(args.input_file)
tr = TCRrep(cell_df = df, 
            organism = args.organism, 
            chains = args.chains.split(','),#['alpha','beta'], 
            db_file = args.db_file,
            imgt_aligned = args.imgt_aligned,
            infer_cdrs = args.infer_cdrs,
            infer_index_cols = args.infer_index_cols,
            deduplicate = args.deduplicate,
            store_all_cdr = args.store_all_cdr,
            compute_distances = args.compute_distances,
            cpus = args.cpus,
            archive_result = True,
            archive_name = f"{args.input_file}.archive")

#tr.pw_beta.tofile(f"{args.input_file}.pw_beta.npy")
#tr.pw_cdr3_b_aa.tofile(f"{args.input_file}.pw_cdr3_b_aa.npy")
print(tr.__dict__.keys())

#tr2 = TCRrep(cell_df = pd.DataFrame(), organism = 'mouse', infer_all_genes= True, infer_cdrs=False,infer_index_cols=False, use_defaults=False,deduplicate=False, compute_distances=False, chains = ['alpha','beta'])
#z = Zipdist2(name = "archive2", target = tr2)
#z._build(dest_tar = "archive2.tar.gz", target = tr2, verbose = True)