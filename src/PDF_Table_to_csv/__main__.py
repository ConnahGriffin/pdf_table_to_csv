import getopt


def pdf_table_to_csv(filepath: str, pages: str = None):
    """
    Uses the camelot library to parse the pdf file.

    :param filepath: Location of pdf
    :param pages: Optional (default: '1').
        Comma-separated page numbers.
        Example: '1,3,4' or '1,4-end' or 'all'.
    :return: None
    """
    # install camelot from pip
    # command: python -m pip install camelot[base]
    import camelot
    if pages is None:
        abc = camelot.read_pdf(filepath)
    else:
        abc = camelot.read_pdf(filepath, pages=pages)
    abc.export('done.csv', f='csv')


def combine_csv(page_range: tuple, table_range: tuple, filepath: str):
    """
    Combines the multiple csv passed in

    :param page_range:
    :param table_range: Optional
    :param filepath: Location of the file you're gonna write to. Must be csv.
    :return:
    """
    import csv
    with open(filepath, "w") as main_csv:
        csv_write = csv.writer(main_csv, delimiter=',', quotechar='"')
        # this section loops through the files and appends each new row from the range
        # into the file above.
        # NOTE: The file name is done<camelot type format>.csv.
        # Where the prefix "done" was user assigned. Upon saving on camelot.
        # There will be multiple files
        page_start, page_end = page_range
        for i in range(page_start, page_end):
            with open(f"done-page-{i}-table-1.csv", "r") as input_csv:
                c_read = csv.reader(input_csv, delimiter=',', quotechar='"')
                for index, row in enumerate(c_read):
                    # Makes it so that only the first column name is stored
                    if index != 0:
                        csv_write.writerow(row)
                    elif i == page_start:
                        csv_write.writerow(row)


def print_help():
    """
    Prints the help text

    :return:
    """
    print("""
        table_flip <Options> <Argument> PATTERN PATTERN
        Options:
            -h: Help. Display this menu.
            -s: Single table mode. This only parses the first table on the first page and no more.
            -m: Multi table mode. Parses the entire table.
        Argument: 
            -i: The file you want to parse. Must be pdf.
            -o: The file you want to output it to.
            (If left empty. It will save all the tables inside the pdf into one file named table_flip.csv)
            -p: This is to make it so that the output are only from specific pages.
                Must be used in conjunction or without the -o flag
                Example: '1,3,4' or '1,4-end' or 'all' or you can leave it as is and it will default to 1.
        """)


import sys


def main(argv):
    pdf_path = ""  # Input file
    csv_file = ""  # Output file
    pages = ""

    try:
        opts, args = getopt.getopt(argv, "hms:i:o:p:", ["ifile=", "ofile=", "pages="])
    except getopt.GetoptError:
        print_help()
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-i", "--ifile"):
            pdf_path = arg
        elif opt in ("-o", "--ofile"):
            csv_file = arg

    # This part will be vital for the

    pdf_table_to_csv(
        filepath=pdf_path,
        pages=pages if pages == "" else None
    )
    # If there are more than one pdf file. Uncomment the code below and fill in the appropriate values
    combine_csv(
        # Remove the quotation. Must be int.
        page_range=("<star of page number>", "<end of page number>"),
        # Optional This parameter is only useful if there are more than one table in a page
        # Remove the quotation. Must be int.
        table_range=("<star of table number>", "<end of table number>"),
        # Path to csv where the data will be combined
        filepath="/path/to/file.csv"
    )


if __name__ == "__main__":
    main(sys.argv[1:])
