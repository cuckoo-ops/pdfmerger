import glob
import os
import logging
import PyPDF2
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
            click.echo(f'[{index}] {f}')
    except NotADirectoryError as  e:
        logging.warning(e)


@click.help_option('-h', '--help')
@cli.command('merge', help='merge pdf')
@click.option('-f', '--files', multiple=True, type=click.Path(exists=True), help='files to merge. e.g: 1.pdf 2.pdf...')
@click.option('-d', '--directory', type=click.Path(), help='input directory')
@click.option('-o', '--output', default=os.getcwd(), type=click.Path(writable=True), help='output path')
def merge(files, directory, output, ):
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
    merge_file = PyPDF2.PdfFileMerger()
    for one_pdf in input_files:
        try:
            # pdf_obj = PyPDF2.PdfFileReader(one_pdf, strict=False)
            merge_file.append(one_pdf)
        except Exception as e:
            logging.error('{} \'{}\''.format(one_pdf, e))
            return False
    with open(output_path, 'wb') as f:
        merge_file.write(f)
        logging.info(f'merged pdf:\'{output_path}\'')

    return True


if __name__ == '__main__':
    cli(prog_name=__app_name__)
