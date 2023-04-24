from fpdf import FPDF
import time
import streamlit as st
import pandas as pd
# from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix
import datetime
# from fileup import kimiwa
import pandas as pd
import pandas as pd
import openai
st.title("Download your PDF here")
st.markdown('---')
openai.api_key = "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"

# uploaded_file = kimiwa()


# @st.cache_data
# def corridors():
#     df = pd.read_csv(uploaded_file)
#     return df


# if uploaded_file is not None:
#     corridors = corridors()
#     st.write(corridors)

df = pd.read_csv('data_csv.csv')
# Access df from session state
# if 'df' in st.session_state:
#     df = st.session_state['df']
# else:
#     st.write("Error in accessing df")
# datafr = st.session_state['dfr']
# df = pd.read_csv(datafr)
# app = Flask(__name__)

# df = pd.read_csv('data_csv.csv')

# continue with generating PDF report from the dataframe


class PDF(FPDF):
    # datafr = st.session_state['dfr']
    # df = pd.read_csv(datafr)
    def footer(self):
        # set position of footer
        self.set_y(-15)
        # text color
        # self.set_text_color(169, 169, 169)
        # Page number
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")
    # chap title

    def chapter_title(self, ch_title):
        # set font
        self.set_font('helvetica', '', 15)
        # background color
        self.set_fill_color(200, 220, 255)
        # Chapter title
        chapter_title = f'{ch_title}'
        # make a single cell in pdf with a line break
        self.cell(0, 7, chapter_title, ln=1, fill=1)
        # Adding line break
        self.ln()
    # chap body

    def chapter_body(self, name):
        # read the text file
        if 'txt' in name:
            with open(name, 'rb') as fh:
                txt = fh.read().decode('latin-1')
            # set font
                self.add_font(
                    'DejaVuSans', '', r'C:\Users\KIIT\AppData\Local\Microsoft\Windows\Fonts\DejaVuSans.ttf', uni=True)
                self.set_font('DejaVuSans', '', 12)
            # insert text
                self.multi_cell(0, 7, txt)
            # line break
                self.ln()
            # end each chapter
            # self.cell(0, 5, '')
        else:
            self.add_font(
                'DejaVuSans', '', r'C:\Users\KIIT\AppData\Local\Microsoft\Windows\Fonts\DejaVuSans.ttf', uni=True)
            self.set_font('DejaVuSans', '', 12)
            self.multi_cell(0, 7, name)
            self.ln()

    def cor(self, df):
        # df = pd.read_csv(st.session_state['dfr'])
        corr_matrix = df.corr()
        corr_list = corr_matrix.values.tolist()
        num_cols = len(corr_list[0])
        # self.add_page()
        # Define the table format
        self.set_font('Arial', 'B', 12)
        # pdf.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Correlation Matrix', 0, 1)

        self.set_font('Arial', '', 12)
        row_height = self.font_size * 2
        table_width = self.w - 2*self.l_margin
        num_cols = len(corr_list[0])
        col_width = table_width / num_cols
        # col_width = pdf.w / num_cols
        for row in corr_list:
            for item in row:
                self.cell(col_width, row_height, str(round(item, 2)), border=1)
            self.ln()
        self.ln(10)

    def print_chapter(self, ch_title, name):
        # self.add_page()
        self.chapter_title(ch_title)
        self.chapter_body(name)
    # title page

    def create_pdf(self, title, name, input, model_meth, model_ass):
        pdf = PDF('P', 'mm', 'Letter')
        today = datetime.date.today()
        date_string = today.strftime("%Y-%m-%d")
        a = "Model Risk Management Document"
        a = a.upper()
        # pdf = PDF()
        # self.add_page()
        # a = a.upper()
        # pdf = PDF()
        pdf.add_page()
        pdf.set_font('Arial', 'BU', 32)
        cell_width = 180
        cell_height = 20
        pdf.multi_cell(cell_width, cell_height, a, 0, 'C')
        pdf.cell(0, 10, "", 0, 1)
        pdf.set_font('Arial', '', 25)
        subtitle_width = 180
        subtitle_height = 30
        pdf.multi_cell(subtitle_width, subtitle_height, title, 0, 'C')
        pdf.cell(0, 10, "", 0, 1)
        pdf.set_font('Arial', '', 15)
        pdf.multi_cell(subtitle_width, subtitle_height,
                       f"Model created by : {name}\nDate created : {date_string}", 0, 'C')
        pdf.add_page()
        pdf.print_chapter('Model Risk', 'model-risk.txt')
        pdf.print_chapter('Overview', 'overview.txt')
        # input will be handled by the api
        completion_mod_over = openai.Completion.create(
            engine="text-davinci-003", prompt=f"Elaborate on this problem statement: {input}", max_tokens=500)
        txt_mod_overview = completion_mod_over.choices[0]['text']
        ans = input + " " + txt_mod_overview
        pdf.print_chapter('Model Overview', ans)
        # gpt api will elaborate on the methodology
        completion_mod_meth = openai.Completion.create(
            engine="text-davinci-003", prompt=f"Elaborate on this : {model_meth}", max_tokens=500)
        txt_mod_meth = completion_mod_meth.choices[0]['text']
        ans = model_meth + " " + txt_mod_meth
        pdf.print_chapter('Model Methodology', ans)
        pdf.print_chapter('Diagnostic and Statistic test',
                          'diagnostic-tests.txt')
        pdf.cor(df)
        # gpt api will explain the cause of assumption
        completion_mod_ass = openai.Completion.create(
            engine="text-davinci-003", prompt=f"Explain the assumption behind using this model : {model_ass}", max_tokens=500)
        txt_mod_ass = completion_mod_ass.choices[0]['text']
        ans = model_ass + " " + txt_mod_ass
        pdf.print_chapter('Model Assumptions', ans)

        pdf.print_chapter('Annual Model Review', 'annual-model-rev.txt')
        return pdf.output(dest='S')


def main():
    st.title("PDF Generator")
    title = st.text_input("Enter the title of your project:")
    # text = st.text_area("Enter the problem to be addressed:")
    name = st.text_input("Enter the name of the modeller:")
    # model_name = st.text_input("Enter the name of the model used:")
    model_method = st.text_area(
        "Enter the model methodology here:", height=200)
    model_overview = st.text_area("Enter the model overview here:", height=300)
    # model_name = st.text_input("Enter the name of the model used: ")
    model_assumption = st.text_area(
        "Enter the assumptions made behind your model:", height=100)
    if st.button("Download PDF"):
        pdf = PDF('P', 'mm', 'Letter')
        pdfi = pdf.create_pdf(title, name, model_overview,
                              model_method, model_assumption)

        st.download_button(
            label="Generate PDF",
            data=bytes(pdfi),
            file_name="mrm.pdf",
            mime="application/pdf",
        )


if __name__ == "__main__":
    main()
