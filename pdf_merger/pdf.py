import PyPDF2
from PyPDF2.utils import PdfReadError
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter, PDFTextExtractionNotAllowed
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.pdfdevice import TagExtractor
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter

# from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


class Pdf(object):
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def get_page_indexes(self):
        page_indexes = []
        with open(self.pdf_path, 'rb') as f:
            pdf_obj = PyPDF2.PdfFileReader(f, strict=False)
            pages_count = pdf_obj.getNumPages()
            is_encrypted = pdf_obj.getIsEncrypted()
            print(f'isEncrypted:{is_encrypted}')
            print(pages_count)

            for page_index in range(pages_count):
                page = pdf_obj.getPage(page_index)
                page_contents = page.extractText()
                print(page_contents.decode())
                break
    def to_text(self):
        with open(self.pdf_path, 'rb') as fp:
            rsrcmgr = PDFResourceManager(caching=False)
            laparams = LAParams()
            with open('test.txt', 'w') as outfp:
                device = TextConverter(rsrcmgr, outfp, laparams=laparams)
                process_pdf(rsrcmgr, device, fp, [0,1], maxpages=100, password=None,
                            caching=False, check_extractable=True)
    def get_text(self):
        with open(self.pdf_path, 'rb') as fp:
            # 用文件对象来创建一个pdf文档分析器
            parser = PDFParser(fp)
            # 创建一个PDF文档PDFDocument
            doc = PDFDocument()
            # 连接分析器 与文档对象
            parser.set_document(doc)
            doc.set_parser(parser)

            # 提供初始化密码,如果没有密码 就创建一个空的字符串
            doc.initialize()

            # 检测文档是否提供txt转换，不提供就忽略
            if not doc.is_extractable:
                raise PDFTextExtractionNotAllowed
            else:
                # 创建PDf 资源管理器 来管理共享资源PDFResourceManager
                rsrcmgr = PDFResourceManager()
                # 创建一个PDF设备对象LAParams
                laparams = LAParams()
                # 创建聚合器,用于读取文档的对象PDFPageAggregator
                device = PDFPageAggregator(rsrcmgr, laparams=laparams)
                # 创建一个PDF解释器对象,对文档编码，解释成Python能够识别的格式：PDFPageInterpreter
                interpreter = PDFPageInterpreter(rsrcmgr, device)

                # 循环遍历列表，每次处理一个page的内容
                for page in doc.get_pages():  # doc.get_pages() 获取page列表
                    # 利用解释器的process_page()方法解析读取单独页数
                    interpreter.process_page(page)
                    # 这里layout是一个LTPage对象,里面存放着这个page解析出的各种对象,一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal等等,想要获取文本就获得对象的text属性，
                    # 使用聚合器get_result()方法获取页面内容
                    layout = device.get_result()
                    for x in layout:
                        # if (isinstance(x, LTTextBoxHorizontal)):
                        try:
                            results = x.get_text()
                            print(results)

                        except AttributeError as  e:
                            pass
                    # break
