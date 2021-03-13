import argparse
import json
import os
from datetime import datetime

import PyPDF2


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
    ll = ll.replace("Ò", " ").replace("Õ", "'").replace(
        "Ñ", " ").replace("Ó", " ").replace("Þ", "fi").replace("ß", "fl")
    return ll


def clean_title(title):
    return title.replace("AM", "").replace("PM", "")


def getdata(ll, tag0):
    try:
        tag, date = get_tag(ll)
        ll[1] = clean_text(ll[1])
        text = ll[1]
        title = " ".join(ll[1].split("\n")[0].split()[:8])
        data = dict(created=getNowtime(), tags=tag0,
                    title=clean_title(title), text=text+"\n"+date)
    except Exception as ex:
        print(ex)
        text = " ".join(ll)
        text = clean_text(text)
        title = text[:30]
        data = dict(created=getNowtime(), tags=tag0,
                    title=clean_title(title), text=text)
        pass
        # print(data)
    return data


def getpage(i, pdf):
    ll = pdf.getPage(i).extractText().encode(
        "utf-8").decode("utf-8").split("#")
    return ll


def get_title_page(page, tag0=None, title=None):

    if title is None:
        ind = page[0].index(":")+3
        title = " ".join(page[0][ind:].split())

    if tag0 is None:
        tag0, _ = get_tag(page)

    tag = "TableOfContents"
    text = '<<list-links "[tag[{0}]sort[created]]">>'.format(tag0)
    data = dict(created=getNowtime(), tags=tag,
                title=clean_title(title), text=text)
    return data


def convert_file(fname, output="tt.json"):
    pdf_file = open(fname, "rb")
    pdf = PyPDF2.PdfFileReader(pdf_file)
    no = pdf.getNumPages()

    dd = []
    ll = getpage(0, pdf)
    data = get_title_page(ll)
    dd.append(data)
    tag0, _ = get_tag(getpage(0, pdf))
    for i in range(no):
        ll = getpage(i, pdf)
        data = getdata(ll, tag0)
        dd.append(data)

    pdf_file.close()
    write_json(output, dd)


def write_json(output, dd):
    with open(output, "w", encoding="utf") as f_out:
        json.dump(dd, f_out, ensure_ascii=False, indent=4)


def convert_markdown_file(fname, output="tt.json", tag="Not_provided"):
    findstr = "--------------------"

    rawdata = open(fname, "r", encoding='utf-8').read()
    pages = rawdata.split(findstr)

    dd = []
    data = get_title_page(pages[0], tag0=tag, title=tag)
    dd.append(data)
    for page in pages:
        if page:
            # page_as = page.encode("ascii", "ignore")
            page_as = page
            # title = " ".join(page_as.split()[:8])
            title = page_as[:50]
            text = page_as
            data = dict(created=getNowtime(), tags=tag, title=title, text=text)
            dd.append(data)

    write_json(output, dd)


def main():
    parser = argparse.ArgumentParser(
        "Convert PDF/Calibre highlights to Tidlers")
    parser.add_argument("fname", type=str, help="Journal.pdf")
    parser.add_argument("-o", "--out", type=str, default=None)
    parser.add_argument("-m", "--mark", action="store_true",
                        help="If provided, Calibre markdown is assumed")
    parser.add_argument("-t", "--tag", type=str, default=None)

    args = parser.parse_args()

    out_file = args.out
    fname = args.fname
    if out_file is None:
        name, ext = os.path.splitext(fname)
        out_file = "{0}_upd.json".format(name)

    if args.mark and args.tag is None:
        raise TypeError(
            "Please enter tag name using '-t tag' with markdown option")

    # print(args)
    # return
    if args.mark:
        convert_markdown_file(fname, out_file, args.tag)
    else:
        convert_file(fname, out_file)


if __name__ == "__main__":
    # fname=r"C:\Users\1002094\Downloads\Journal (1).pdf"
    main()
