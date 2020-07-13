import PyPDF2
import sys
import os

# python3 pdf.py watermark.pdf directory/

# sys.argv[1] - watermark it should be .pdf
# sys.argv[2] - directory where there are .pdf files

# if one .pdf file, watermark added
# if more then one .pdf file found, they are combined at first, then watermark added
# the .pdf with watermark is watermarked.pdf


def pdf_combiner(my_dir, pdf_list, output):
    merger = PyPDF2.PdfFileMerger()
    for pdf in pdf_list:
        merger.append(my_dir+pdf)
    merger.write(output)


def add_waterMark(water, inputFile):
    watermark = PyPDF2.PdfFileReader(water).getPage(0)
    reader = PyPDF2.PdfFileReader(inputFile)
    writer = PyPDF2.PdfFileWriter()
    for i in range(0, reader.getNumPages()):
        page = reader.getPage(i)
        page.mergePage(watermark)
        writer.addPage(page)
    with open('watermarked.pdf', 'wb') as output:
        writer.write(output)


if (len(sys.argv) < 2):
    print("You have not provided enough arguments")
else:
    if (os.path.splitext(sys.argv[1])[-1] == '.pdf') and (os.path.exists(sys.argv[1])):
        waterMark = sys.argv[1]
        if os.path.exists(sys.argv[2]):
            my_dir = sys.argv[2]
            if sys.argv[2][-1] != '/':
                my_dir += '/'
            inputs = []
            for pdfs in os.listdir(my_dir):
                if os.path.splitext(pdfs)[-1] == '.pdf':
                    inputs.append(pdfs)
            if len(inputs) == 0:
                print("No .pdf files found")
            elif len(inputs) == 1:
                print(
                    f"You have uploaded {waterMark} as watermark. It will be added to {inputs[0]} from folder {my_dir}")
                with open(waterMark, 'rb') as water:
                    with open(my_dir+inputs[0], 'rb') as file:
                        add_waterMark(water, file)
            else:
                with open(waterMark, 'rb') as water:
                    print(
                        f"You have uploaded {waterMark} as watermark.\n\nNext files from folder {my_dir} will be combined to one:")
                    for i in range(0, len(inputs)):
                        print(f"{i+1}. {inputs[i]}")
                    output = 'final.pdf'
                    pdf_combiner(my_dir, inputs, output)
                    print("\nFiles were combined. Start adding watermark.")
                    with open(output, 'rb') as file:
                        add_waterMark(water, file)
                    os.remove('final.pdf')
            print("Watermark is added, see watermarked.pdf")
        else:
            print("Directory does not exist")
    else:
        print(f"{sys.argv[1]} does not exist or not .pdf")

print("Thank you for using our app.\nBye.")
