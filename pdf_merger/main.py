import glob
import os
import click
import logging
import PyPDF2
from PyPDF2.utils import PdfReadError
from pdf_merger import __app_name__, __version__, ExtractPageIndexError
from pdf_merger.pdf import Pdf, Pages

logging.basicConfig(format='%(asctime)s:%(levelname)-7s:%(filename)s [line:%(lineno)d] %(message)s',
                    level=logging.WARNING)


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
    open_files = {}
    if direct_merge:
        merge_file = PyPDF2.PdfFileMerger(strict=False)
        for one_pdf in input_files:
            file_path = one_pdf
            if isinstance(one_pdf, tuple):
                file_path = one_pdf[0]
            try:
                # pdf_obj = PyPDF2.PdfFileReader(one_pdf, strict=False)
                merge_file.append(file_path)
            except Exception as e:
                logging.error('{} \'{}\''.format(one_pdf, e))
                merged_ok = False
                break

    else:
        merge_file = PyPDF2.PdfFileWriter()
        for one_file in input_files:
            file_path = one_file[0]
            extracted_page_index = one_file[1]
            if file_path in open_files.keys():
                one_pdf = open_files.get(file_path)
            else:
                one_pdf = open(file_path, 'rb')

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
                open_files[file_path] = one_pdf
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
    for f in open_files.values():
        f.close()
    return merged_ok


def sort_pdf_files(input_files: list):
    pages_index = Pages()
    with click.progressbar(length=len(input_files),
                           label='Extract page number...'.format(len(input_files))) as bar:
        for input_f in input_files:
            pages_index.extend(Pdf(input_f).extract_pages_index())
            bar.update(1)
        pages_index.sort()
    return pages_index.get_path_indexes(), pages_index.has_duplicate()


@click.version_option(version=__version__, prog_name=__app_name__)
@click.help_option('-h', '--help')
@click.group()
def cli():
    pass


@cli.command('list', help='list pdf files in directory')
@click.help_option('-h', '--help')
@click.argument('directory', type=click.Path())
def list_pdf(directory):
    click.echo(f'PDF list in the {os.path.dirname(directory)}:')
    try:
        for index, f in enumerate(list_pdf_directory(directory), start=1):
            click.echo(f'[{index:<3}] {f}')
    except NotADirectoryError as  e:
        logging.warning(e)


@click.help_option('-h', '--help')
@cli.command('show', help='merge pdf')
@click.option('-d', '--directory', type=click.Path(), help='input directory')
def show(directory):
    # try:
    #     input_files = list_pdf_directory(directory)
    #     Pdf(input_files[0]).display_page_text()
    pass

@click.help_option('-h', '--help')
@cli.command('merge', help='merge pdf')
@click.option('-f', '--files', multiple=True, type=click.Path(exists=True), help='files to merge. e.g: 1.pdf 2.pdf...')
@click.option('-d', '--directory', type=click.Path(), help='input directory')
@click.option('-o', '--output', default=os.getcwd(), type=click.Path(writable=True), help='output path')
@click.option('-s', '--sort', is_flag=True, default=True, help='Specify whether to sort files, default is true')
@click.option('--headers', multiple=True, type=click.Path(exists=True), help='Specify file path to insert header')
@click.option('-l', '--line', default=-1, type=click.INT, help='Specify the page index is which line')
def merge(files, directory, output, sort, headers, line):
    Pdf.index_on_line = line
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

    click.echo(f'{list(map(lambda x: os.path.basename(x), input_files))} will be merged ...')
    try:
        sorted_files, has_duplicate = sort_pdf_files(input_files) if sort else (input_files, False)
    except ExtractPageIndexError as e:
        logging.error(f'merge failed {e}')
        return False
    click.echo(sorted_files)
    click.echo('Start to merge....')
    if merge_pdf(sorted_files, output_path, not has_duplicate):
        if headers:
            headers_content = headers[:]
            headers_content.extend(output_path)
            return merge_pdf(headers_content, output_path, True)
        click.echo(f'Merged file save to \'{output_path}\'')
        return True
    return False


def command():
    cli(prog_name=__app_name__)


if __name__ == '__main__':
    command()
