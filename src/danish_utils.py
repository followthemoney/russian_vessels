import dask.dataframe as dd
import pyarrow.parquet as pq
import pyarrow as pa
from pathlib import Path
from tqdm import tqdm
from multiprocessing import Pool, cpu_count


def csv_to_parquet(path_raw:str, 
                   path_parquet:str, 
                   )-> None:

    '''
    Converts cleaned csv files
    to more manageable parquets
    PARAMETERS:
    path_raw: location of raw AIS files
    path_parquet: location of parquet files
    '''

    for file in tqdm(path_raw.glob('*.csv')):

        # Read selection of columns
        ddf = dd.read_csv(file,
                          usecols = ['# Timestamp', 'Type of mobile', 'MMSI', 'Latitude', 'Longitude',
                                     'Navigational status', 'ROT', 'SOG', 'COG', 'Heading', 'IMO',
                                     'Callsign', 'Name', 'Ship type', 'Draught', 
                                     'Destination', 'ETA'],
                          dtype= {'Callsign': 'object',
                                  'Destination': 'object',
                                  'ETA': 'object',
                                  'Name': 'object',
                                  'MMSI': 'object',
                                  'Heading': 'float64'},
                          low_memory=False
                         )
        
        # Filter out Class A AIS
        ddf = ddf[ddf['Type of mobile'] == 'Class A']

        # Clean it up a bit
        ddf.columns = ddf.columns.str.lower().str.replace('# ', '').str.replace(' ', '_')
        ddf = ddf.drop('type_of_mobile', axis=1)

        # Write to file
        ddf.to_parquet(path_parquet.joinpath(f'{file.stem}.parquet'))
    
    return None

def parse_ais(path_parquet: str,
              path_processed: str)-> None:

    '''
    Parses raw AIS data from Denmark
    and converts files of daily activity to
    separate files per MMSI.
    
    Parameters:
    ----------
    path_raw: path to AIS data
    path_processed: path to write AIS data
    '''
    
    
    def parse_file(args):   
        
        mmsi, ddf, path_processed = args
        tmp = ddf[ddf.mmsi== mmsi]
        filepath = path_processed.joinpath(f'{mmsi}.parquet')
        table = pa.Table.from_pandas(tmp.compute())
        pq.write_to_dataset(table , root_path=filepath)
    
        return None
    
    files = [file for file in path_parquet.glob('*.parquet')]
    
    for file in tqdm(files):

        ddf = dd.read_parquet(file)
        mmsis = set(ddf.mmsi)
        args = [(mmsi, ddf, path_processed) for mmsi in mmsis]
        pool = Pool(cpu_count() -1)
        pool.map(parse_file, args)
        pool.close()
        pool.join()


    return None


