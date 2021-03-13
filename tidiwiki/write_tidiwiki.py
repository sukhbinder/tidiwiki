import PyPDF2
from datetime import datetime
import json
import os

import argparse

def getNowtime():
    return datetime.now().strftime("%Y%m%d%H%M%S")


# <<list-links "[tag[Fifty-Inventions-That-Shaped-the-Modern]sort[title]]">>
# tag for table of content  TableOfContents

def get_tag(ll):
    ind = ll[0].index(":")+6
    date = ll[0][:ind]
    tag = "-".join(ll[0][ind:].strip().split()[:6])
    return tag, date

def clean_text(ll):
    ll = ll.replace("Ò"," ").replace("Õ","'").replace("Ñ"," ").replace("Ó"," ").replace("Þ", "fi").replace("ß","fl")
    ll = ll.replace("Cromwell", "").replace("Road", "").replace("DE23 6TR","").replace("Derby"," ")
    return ll

def getdata(ll, tag0):
    try:
        tag, date = get_tag(ll)
        ll[1] = clean_text(ll[1])
        text = ll[1]
        title = " ".join(ll[1].split("\n")[0].split()[:8])
        data = dict(created=getNowtime(), tags=tag, title=title, text=text+"\n"+date)
    except Exception as ex:
        print(ex)
        text= " ".join(ll)
        text = clean_text(text)
        title = text[:30]
        data=dict(created=getNowtime(), tags=tag0, title=title, text=text)
        pass
        # print(data)
    return data

def getpage(i,pdf):
    ll = pdf.getPage(i).extractText().encode("utf-8").decode("utf-8").split("#")
    return ll

def get_title_page(i,pdf):
    ll = getpage(i,pdf)
    
    tag = "TableOfContents"

    ind = ll[0].index(":")+3
    title = " ".join(ll[0][ind:].split())
    tag0, _ = get_tag(ll)

    text='<<list-links "[tag[{0}]sort[created]]">>'.format(tag0)
    data=dict(created=getNowtime(), tags=tag, title=title, text=text)
    return data

def convert_file(fname, output="tt.json"):
    pdf_file= open(fname, "rb")
    pdf = PyPDF2.PdfFileReader(pdf_file)
    no = pdf.getNumPages()

    dd=[]
    data = get_title_page(0,pdf)
    dd.append(data)
    tag0 , _ = get_tag(getpage(0,pdf))
    for i in range(no):
        ll = getpage(i,pdf)
        data = getdata(ll, tag0)
        dd.append(data)

    with open(output, "w", encoding="utf") as f_out:
        json.dump(dd, f_out, ensure_ascii=False)


if __name__ == "__main__":
    # fname=r"C:\Users\1002094\Downloads\Journal (1).pdf"
    parser = argparse.ArgumentParser("Convert PDF to Tidlers")
    parser.add_argument("fname", type=str, help="Journal.pdf")
    parser.add_argument("-o", "--out", type=str, default=None)

    args = parser.parse_args()

    out_file = args.out
    fname = args.fname
    if out_file is None:
        name,ext = os.path.splitext(fname)
        out_file = "{0}_upd.json".format(name)


    convert_file(fname, out_file)
