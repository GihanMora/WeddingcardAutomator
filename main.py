from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor


def write_card(prefix,name_of_invitee, out_dir):

    #Concatenate the name and prefix
    name = prefix +" "+ name_of_invitee

    # Use your choice of font
    pdfmetrics.registerFont(TTFont('Hancock', 'hancock.ttf'))

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    #set the font and size
    can.setFont('Hancock', 14)
    #set the color
    can.setFillColor(HexColor(0x645120))

    #wedding card length in pixels(standard letter width)
    width = 417

    #centering the invitee name
    x = (width-can.stringWidth(name,'Hancock',13))/2
    can.drawString(x, 360, name)
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)

    # create a new PDF with Reportlab
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("original.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    # finally, write "output" to a real file
    out_name = os.path.join(out_dir,name+".pdf")

    output_stream = open(out_name, "wb")
    output.write(output_stream)
    output_stream.close()


# write_card("Mr.", "FirstName LastName")

#iterate through the list
import pandas as pd

i_list = pd.read_csv(r"list.csv")
for i, row in i_list.iterrows():
    write_card(row['prefix'], row['name'], "set_1")