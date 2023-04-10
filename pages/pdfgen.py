from fpdf import FPDF
import time
import streamlit as st
import pandas as pd
from pandas_profiling import ProfileReport
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix
import datetime

st.title("Download your PDF here")
st.markdown('---')


class PDF(FPDF):

    def footer(self):
        # set position of footer
        self.set_y(-15)
        # Page number
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")



def create_pdf(title,name):
    today = datetime.date.today()
    date_string = today.strftime("%Y-%m-%d")
    a = "Model Risk Management Document"
    a = a.upper()
    pdf = PDF()
    pdf.add_page()
    a = a.upper()
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial','BU', 32)
    cell_width = 180
    cell_height = 20
    pdf.multi_cell(cell_width,cell_height,a,0,'C')
    pdf.cell(0, 10, "", 0, 1)
    pdf.set_font('Arial', '', 25)
    subtitle_width = 180
    subtitle_height = 30
    pdf.multi_cell(subtitle_width, subtitle_height,title, 0, 'C')
    pdf.cell(0, 10, "", 0, 1)
    pdf.set_font('Arial', '', 15)
    pdf.multi_cell(subtitle_width, subtitle_height,f"Model created by : {name}\nDate created : {date_string}", 0, 'C')
    # pdf.output('test.pdf','F')
    return pdf.output(dest='S')


def main():
    st.title("PDF Generator")
    title = st.text_input("Enter the title of your project:")
    # text = st.text_area("Enter the problem to be addressed:")
    name = st.text_input("Enter the name of the modeller:")
    if st.button("Download PDF"):
        pdf = create_pdf(title,name)
        st.download_button(
            label="Generate PDF",
            data=bytes(pdf),
            file_name="document.pdf",
            mime="application/pdf",
        )


if __name__ == "__main__":
    main()
