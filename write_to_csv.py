import pandas as pd
import os
import csv

def write_to_csv(episode_dict, filename = "output/episode_data.csv", fieldnames=None):
    if fieldnames is None:
        fieldnames = ['title', 'summary', 'year_from', 'year_until', 'url']
    try:
        # Convert single dictionary to DataFrame
        df = pd.DataFrame([episode_dict])

        # If file exists, append without header
        if os.path.isfile(filename):
            df.to_csv(filename,
                      mode='a',
                      encoding='utf-8-sig',
                      index=False,
                      header=False,
                      sep=';',
                      quoting=csv.QUOTE_MINIMAL)
        else:
            # If file doesn't exist, write with header
            df.to_csv(filename,
                      mode='w',
                      encoding='utf-8-sig',
                      index=False,
                      header=fieldnames,
                      sep=';',
                      quoting=csv.QUOTE_MINIMAL)

    except Exception as e:
        print(f"Error writing to CSV: {str(e)}")