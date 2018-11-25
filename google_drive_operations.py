import pandas as pd
import pygsheets

def write_to_google_spreadsheet(file_name):
    #open the google spreadsheet
    gc = pygsheets.authorize(service_file='') #json file
    sh = gc.open_by_url('') #link to workbook
    wks = sh.worksheet_by_title('raw')

    df = pd.read_csv('./{}'.format(file_name))
    #update the first sheet with df, starting at cell B2.
    wks.set_dataframe(df, 'A1',fit=True,nan='')