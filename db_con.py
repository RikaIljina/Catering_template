import streamlit as st
from streamlit_gsheets import GSheetsConnection
import gspread
# from oauthlib.oauth2 import ServiceAccountCredentials
# scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

from gspread_formatting import CellFormat, Color, TextFormat, format_cell_range

class CatSheet():
    def __init__(self):
        # gc = gspread.service_account(filename="service_account.json")
        # sh = gc.open("Catering offert mall")
        #sh.append_row(["name"])
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def read(self, name, cols):
       # return self.conn.worksheet(name).col_values(cols)
        return self.conn.read(worksheet=name, usecols=list(range(cols)), ttl=10)

    def write(self, name, dff):
        df = self.conn.update(
            worksheet=name,
            data=[[dff]],
            
        )
        print(df)

    def write_result(self, df):
        dff = self.conn.update(
            worksheet="Resultat",
            data=df,
        )
        print("result:", dff)

class UpdSheet():
    def __init__(self):
        print("Connecting with gspread...")
        gc = gspread.service_account(filename="service_account.json")
        self.conn = gc.open("Catering offert mall")
    def write(self, name, data, pos):
        st.write(pos)
        print("Writing with gspread...")

        # self.conn.worksheet(name).update_cell(pos + 2, 1, data)
        if isinstance(data, str):
            self.conn.worksheet(name).update(f"A{pos + 2}", [[data]])
        else:
            self.conn.worksheet(name).update(f"A{pos + 2}", [data])

    def write_range(self, name, data):
        self.conn.worksheet(name).batch_update(data) # update(range, [data])

    def read(self):
        return self.conn.worksheet("Resultat").get_all_values()

    def merge_cells(self, range):
        # self.conn.worksheet("Resultat").merge_cells(range, merge_type=("MergeType.MERGE_COLUMNS"))
        self.conn.worksheet("Resultat").merge_cells(range)
        fmt = CellFormat(
        backgroundColor=Color(1, 0.9, 0.9),
        textFormat=TextFormat(bold=True, foregroundColor=Color(0, 0, 0)),
        horizontalAlignment='CENTER'
        )

        format_cell_range(self.conn.worksheet("Resultat"), 'A9', fmt)

    def center_text(self, range):
        fmt = CellFormat(
#        backgroundColor=Color(1, 0.9, 0.9),
        textFormat=TextFormat(bold=True, foregroundColor=Color(0, 0, 0)),
        horizontalAlignment='CENTER'
        )

        format_cell_range(self.conn.worksheet("Resultat"), range, fmt) # format_cell_ranges(worksheet, [('A1:J1', fmt), ('K1:K200', fmt2)]) !!!


        # self.conn.worksheet("Resultat").merge_cells(range, merge_type='MERGE_COLUMNS')

# To clear cache  and rerun app:
        # st.cache_data.clear()
        # st.rerun()

        # update connection class
 # 