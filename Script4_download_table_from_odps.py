import argparse
import GMI_ComputeEngine_ODPS as GMI_CE

# SET API KEY
GMI_CE.api_key = "*"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download table from ODPS to local.')
    parser.add_argument('csv_file', type=str, help='Path to the downloaded table.')
    parser.add_argument('results_table', type=str, help='Results table name in ODPS.')

    args = parser.parse_args()
    csv_path = args.csv_file
    results_table = args.results_table

    GMI_CE.Data.download(data_address=results_table, save_file=csv_path)
    