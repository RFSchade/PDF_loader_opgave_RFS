#===================================================#
#=============> PDF Downloader Script <=============#
#===================================================#

#=====> Import modules
# System tools
import os
import argparse

# Read xlsx
import openpyxl
from xlsx2csv import Xlsx2csv

# Data tools
import pandas as pd
import math

# HTML requests
from requests import get 

# Multithreading 
from multiprocessing.pool import ThreadPool

# Timer 
from timeit import default_timer as timer

#=====> Define functions
# > Load data 
def load_data(list_file):
    # Info
    print("[info] Loading Excel file...")
    
    # Get path of the file and where to save the csvfile
    filepath = os.path.join("input", list_file)
    csvpath = os.path.join("input", "pdf_list.csv")
    
    # Convert excel to csv
    Xlsx2csv(filepath, outputencoding="utf-8", sheet_name=0).convert(csvpath)
    # Load csv
    pdf_data = pd.read_csv(csvpath, usecols = ['BRnum','Pdf_URL','Report Html Address'])
    
    # Rename columns and add outpaths
    pdf_data.columns = ["BRnum", "url", "alt_url"]
    pdf_data["outpaths"] = [os.path.join("output", "pdfs", f"{filename}.pdf") for filename in pdf_data["BRnum"]]
    
    # Info
    print("[info] File loaded")
    
    return pdf_data

# > Clean data
def clean_data(df):
    ## > Deal with NaNs
    # Drop rows without links
    df_no_nan = df.dropna(subset=["url", "alt_url"], how='all')

    # Put the alternate url first if the first url is NaN
    df_one_url = df_no_nan.copy()
    df_one_url["url"] = df_no_nan["url"].fillna(df_no_nan["alt_url"])
    
    # If the first and second urls are the same, change alt_url to NaN 
    df_one_url.loc[df_one_url.url == df_one_url.alt_url, "alt_url"] = math.nan
    
    ## > Deal with files that are already downloaded 
    # Get path of directory
    dirpath = os.path.join("output", "pdfs")

    # Scan directory
    entries = os.scandir(dirpath)

    # Get filenames of files in directory
    filenames = [entry.name for entry in entries]

    # Remove .pdf to compare with BRnum
    filenames = " ".join(filenames).replace(".pdf","").split()

    # Remove files already in directory 
    df_clean = df_one_url[~df_one_url["BRnum"].isin(filenames)]

    # Return clean data 
    return df_clean

# > Download pdf to folder
def export_pdf(path, r):
    with open(path, 'wb') as f:
        f.write(r)
        f.close()
        
# > Check if response is a pdf and download it
def touch_pdf(pdf_url, pdf_path):
    # Define function dictionary for response content
    content_dict = {"application/pdf": export_pdf}
    
    # Get response from URI
    response = get(pdf_url, stream=True, timeout = 2)
    # What is the type of the response content
    content_type = response.headers.get('content-type')
    content_dict[content_type](pdf_path, response.content)

# > Try to download a pdf
def worker(url, alt_url, path):
    # Try to download pdf
    try:
        touch_pdf(url, path)
    # If it didn't work
    except Exception:
        # And if the second URL is not NaN
        test = (alt_url == alt_url)
        fndict = {"True": touch_pdf}
        # Try the alternate URL
        try: 
            fndict[str(test)](alt_url, path)
        # If that did not work, do nothing
        except Exception: 
            pass
    finally: 
        # Info
        id = path[-11:-4]
        print(f"Processed PDF file [ {id} ]", end = "\r")

# > Complete download function
def download(df):
    # Make lists of BRnum, url, alt_url, and outpath
    brnum_vec, url_vec, alt_url_vec, path_vec = [df[col].tolist() for col in df.columns]

    # Zip iterables together
    items = zip(url_vec, alt_url_vec, path_vec)

    # Info
    print("Downloading PDFs...")
    
    # Download 
    with ThreadPool() as pool:
        pool.starmap(worker, iterable = items)
        
    # Info
    print("\n[info] PDFs downloaded")
    
# > Create list
def count_list(outpath_list, BRnum_list):
    # Check if files are downloaded
    downloaded = ["Ja" if os.path.exists(path) else "Nej" for path in outpath_list]
    
    # Create dataframe with files and whether or not they are downloaded
    download_df = pd.DataFrame(list(zip(BRnum_list, downloaded)),
                                columns = ["BRnum", "Downloadet"])

    # Define Listpath 
    listpath = os.path.join("output", "Download_liste.xlsx")
    download_df.to_excel(listpath, index=False)
    
# > Parse arguments
def parse_args(): 
    # Initialize argparse
    ap = argparse.ArgumentParser()
    # Commandline parameters 
    ap.add_argument("-f", "--file", 
                    required=False, 
                    type=str,
                    default="GRI_2017_2020 (1).xlsx",
                    help="Name of the file containing a list of PDF-files and URLs. Default is 'GRI_2017_2020 (1).xlsx'")
    # Parse argument
    args = vars(ap.parse_args())
    # return list of argumnets 
    return args
    
#=====> Define main()
def main():
    # Start timer 
    start = timer()
    
    # Get arguments
    args = parse_args()
    
    # Loading data 
    pdf_df = load_data(args["file"])
    
    # Clean data 
    df_clean = clean_data(pdf_df)

    # Download PDFs 
    download(df_clean)    
    
    # Create new list
    count_list(pdf_df["outpaths"], pdf_df["BRnum"])
    
    # End timer
    end = timer()
    
    # Info
    print("[info] Program is finished")
    print(f"[info] Runtime: {end - start} (sec.)")
    
# Run main() function from terminal only
if __name__ == "__main__":
    main()