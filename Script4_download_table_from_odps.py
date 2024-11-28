import argparse
import GMI_ComputeEngine_ODPS as GMI_CE

# SET API KEY
GMI_CE.api_key = "NDUkMTczMjY5OTcwNyRqYXh5anBnbQ"
GMI_CE.api_baseurl = "http://221.228.10.51:18080/platform/"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process an ASTER HDF file.')
    parser.add_argument('csv_file', type=str, help='Path to the output table to be downloaded.')
    parser.add_argument('results_table', type=str, help='Results table name in ODPS.')

    args = parser.parse_args()
    csv_path = args.csv_file
    results_table = args.results_table

    GMI_CE.Data.download(data_address=results_table, save_file=csv_path)
    