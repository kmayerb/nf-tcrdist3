params.output_folder = "./outputs"

input_file_channel = Channel.fromPath('inputs/*.csv')
// input_file_channel.view()

process default_tcrdist {

    container 'quay.io/kmayerb/tcrdist3:0.1.2'

    publishDir params.output_folder

    input: 
        path(input_filename) from input_file_channel
    
    output: 
        path("${input_filename}.archive.tar.gz") into output_channel
    
    """
    #!/usr/bin/env python
    import pandas as pd
    import numpy as np
    from tcrdist.repertoire import TCRrep

    df = pd.read_csv('${input_filename}').head(100)
    tr = TCRrep(cell_df = df, 
            organism = 'mouse', 
            chains = ['alpha','beta'], 
            db_file = 'alphabeta_gammadelta_db.tsv',
            archive_result=True, 
            archive_name = '${input_filename}.archive')
    """
} 
