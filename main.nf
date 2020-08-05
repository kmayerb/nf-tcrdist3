params.output_folder = "./outputs"
params.input_path = 'inputs/*.csv'
input_file_channel = Channel.fromPath('nextflow/inputs/dash.csv')

process default_tcrdist {

    container 'quay.io/kmayerb/tcrdist3:0.1.2'

    publishDir params.output_folder

    input: 
        path(input_filename) from input_file_channel
    
    output: 
        path("${input_filename}.archive.tar.gz") into output_channel
    
    """
    def_tcrdist.py -i ${input_filename} --store_all_cdr False --chains beta
    """
} 
