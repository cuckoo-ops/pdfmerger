import glob
import os
import logging
import PyPDF2
from PyPDF2.utils import PdfReadError
import click
from pdf_merger import __app_name__, __version__

logging.basicConfig(format='%(asctime)s:%(levelname)-7s: %(message)s', level=logging.INFO)


def list_pdf_directory(directory):
    pdf_directory = directory
    if not os.path.exists(os.path.dirname(pdf_directory)):
        raise NotADirectoryError(f'directory {os.path.dirname(pdf_directory)} does not exist')
    if os.path.splitext(pdf_directory)[1] != '.pdf':
        pdf_directory = os.path.join(pdf_directory, '*.pdf')
    return [file_path for file_path in glob.glob(pdf_directory)]


def merge_pdf(input_files: list, output_path: str, direct_merge: bool):
    '''
    :param direct_merge:
    :param input_files:
    :param output_path:
    :param header:
    :return:
    '''
    merged_ok = True
    open_files = []
    if direct_merge:
        merge_file = PyPDF2.PdfFileMerger()
        for one_pdf in input_files:
            try:
                # pdf_obj = PyPDF2.PdfFileReader(one_pdf, strict=False)
                merge_file.append(one_pdf)
            except Exception as e:
                logging.error('{} \'{}\''.format(one_pdf, e))
                merged_ok = False
                break

    else:
        merge_file = PyPDF2.PdfFileWriter()

        for one_file in input_files:
            file_path = one_file[0]
            extracted_page_index = one_file[1]
            one_pdf = open(one_file[0], 'rb')
            try:
                pdf_obj = PyPDF2.PdfFileReader(file_path, strict=False)
                page_number = pdf_obj.getNumPages()

                if page_number < len(extracted_page_index):
                    logging.error(
                        f'will extracted index {len(extracted_page_index)} greater than total pages {page_number}')
                    merged_ok = False
                    break
                for i in extracted_page_index:
                    p = pdf_obj.getPage(i)
                    merge_file.addPage(p)
                open_files.append(one_pdf)
            except Exception as e:
                logging.error(f' merge failed {e}')
                one_pdf.close()
                merged_ok = False
                break
    if merged_ok:
        with open(output_path, 'wb') as f:
            try:
                merge_file.write(f)
            except PdfReadError as e:
                logging.error(e)
                merged_ok = False
    for f in open_files:
        f.close()
    return merged_ok


def extract_page_index(input_files: list):
    for input_f in input_files:
        with open(input_f, 'rb') as f:
            pdf_obj = PyPDF2.PdfFileReader(f, strict=False)
            pages_count = pdf_obj.getNumPages()
            for page_index in range(pages_count):
                page = pdf_obj.getPage(page_index)
                page_contents = page.getContents()
                print(page_contents)


def sort_pdf_files(input_files):
    sorted_files = input_files
    return sorted_files


# def merge(input_files: list, output_path: str, header: list):
#
#    pass


@click.version_option(version=__version__, prog_name=__app_name__)
@click.help_option('-h', '--help')
@click.group()
def cli():
    pass


@cli.command('list', help='list pdf files in directory')
@click.help_option('-h', '--help')
@click.argument('directory', type=click.Path())
def list_pdf(directory):
    logging.info(f'PDF list in the {os.path.dirname(directory)}:')
    try:
        for index, f in enumerate(list_pdf_directory(directory), start=1):
            click.echo(f'[{index:<3}] {f}')
    except NotADirectoryError as  e:
        logging.warning(e)


@click.help_option('-h', '--help')
@cli.command('merge', help='merge pdf')
@click.option('-f', '--files', multiple=True, type=click.Path(exists=True), help='files to merge. e.g: 1.pdf 2.pdf...')
@click.option('-d', '--directory', type=click.Path(), help='input directory')
@click.option('-o', '--output', default=os.getcwd(), type=click.Path(writable=True), help='output path')
@click.option('-s', '--sort', is_flag=True, default=True, help='Specify whether to sort files, default is true')
@click.option('--headers', multiple=True, type=click.Path(exists=True), help='Specify file path to insert header')
def merge(files, directory, output, sort, headers):
    input_files = []
    if os.path.isdir(output):
        logging.error('output is invalid path')
        return False
    output_path = os.path.abspath(output)
    if os.path.splitext(output_path)[1] != '.pdf':
        output_path += '.pdf'
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if files:
        input_files = files
    elif directory:
        try:
            input_files = list_pdf_directory(directory)
        except NotADirectoryError as  e:
            logging.warning(e)
            return False
    if not input_files:
        logging.error('input files is empty')
        return False

    logging.info(f'{list(map(lambda x: os.path.basename(x), input_files))} \nwill be merged ...')
    sorted_files = sort_pdf_files(input_files) if sort else input_files
    direct_merge = True
    if merge_pdf(sorted_files, output_path, direct_merge):

        if headers:
            headers_content = headers[:]
            headers_content.extend(output_path)
            return merge_pdf(headers_content, output_path, True)
        return True
    return False


def command():
    cli(prog_name=__app_name__)


if __name__ == '__main__':
    command()