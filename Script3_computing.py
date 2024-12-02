import argparse
import GMI_ComputeEngine_ODPS as GMI_CE

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Computing in ODPS.')
    parser.add_argument('source_table', type=str, help='Source table name in ODPS.')
    parser.add_argument('results_table', type=str, help='Results table name in ODPS.')
    parser.add_argument('--method', type=str, nargs='?', default='mineral_indices', help='Computing method in ODPS, [merge,color_transfer,mineral_indices].')

    args = parser.parse_args()
    source_table = args.source_table
    results_table = args.results_table
    method = args.method

    if method == 'merge': # dn2radiance, atmospheric correction, merge
        job_status = GMI_CE.method.merge(source_table,results_table)
    elif method == 'color_transfer': # dn2radiance, atmospheric correction, merge, color(spectral) transfer
        job_status = GMI_CE.method.color_transfer(source_table,results_table)
    elif method == 'mineral_indices': # dn2radiance, atmospheric correction, merge, color(spectral) transfer, mineral indices calculation
        job_status = GMI_CE.method.mineral_indices(source_table,results_table)
    else:
        raise RuntimeError('Only method in list is allowed!')
    