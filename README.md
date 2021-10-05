# PDF-Merger Getting Started
Merge multiple pdf files to one pdf
## Support Platform
+ Unix
+ Windows

## Build & Package
+ Python3.6+
```
pip install -r requirements-dev.txt
```
- linux
```bash
./package.sh
```
- windows
```batch
./package.bat
```
## How to use
- Installation 
    ```
    pip install  pdfmerger-0.2.1-py3-none-any.whl
    ```
- Help Information
    ```
     pdfmerger.exe -h
    Usage: pdfmerger [OPTIONS] COMMAND [ARGS]...
    
    Options:
      -h, --help  Show this message and exit.
      --version   Show the version and exit.
    
    Commands:
      list   List pdf files in directory
      merge  Sort and merge pdf with page number
      show   Display pdf content include page number with text
      test   Test whether pattern can correctly extract page numbers
    
    ```
- **List** command, list pdf files in input directory
    ```
    pdfmerger list
    ```

1. Example:
    ```
    $ pdfmerger list  /xx/xx/*.pdf
    >> 2021-05-27 20:29:07,397:INFO   : PDF list in the /xx/xx/:
    >> [1] /xx/xx/2.0 others.pdf
    >> [2] /xx/xx/2.others .pdf
    >> [3] /xx/xx/test+3.1.pdf
    >> [4] /xx/xx/test+3.2.pdf
    >> [5] /xx/xx/test+3.3.pdf
    >> [6] /xx/xx/test+3.4.pdf
    ```
2. Example with patten:
    ```
    $ pdfmerger list  /xx/xx/*+3.*.pdf
    >> [1] /xx/xx/test+3.1.pdf
    >> [2] /xx/xx/test+3.2.pdf
    >> [3] /xx/xx/test+3.3.pdf
    >> [4] /xx/xx/test+3.4.pdf
    ```
- Show command
    ```
    pdfmerger.exe show -h
    Usage: pdfmerger show [OPTIONS] PDF_FILE_PATH
    
      Display pdf content include page number with text
    
    Options:
      -p, --pages INTEGER RANGE  specify page count for showing,default=2
      -l, --lines INTEGER RANGE  specify line count for showing,default=5
      -h, --help                 Show this message and exit.
    ```
- Test command
    ```
     pdfmerger.exe test -h
    Usage: pdfmerger test [OPTIONS] PDF_FILE_PATH
    
      Test whether pattern can correctly extract page numbers
    
    Options:
      -p, --pages INTEGER RANGE  specify page count for showing,default=2
      --pattern TEXT             specify search regex pattern for extracting page
                                 index,default:(\d+)
    
      --line-number INTEGER      specify line number for extracting page
                                 index,default=-1
    
      -h, --help                 Show this message and exit.
    ```

- **merge** command, merge multiple pdf files order by input order
    ```
     pdfmerger.exe merge -h
     Usage: pdfmerger merge [OPTIONS]

     Sort and merge pdf with page number

    Options:
      -f, --files PATH       files to merge. e.g: 1.pdf 2.pdf...
      -d, --directory PATH   input directory
      -o, --output PATH      output path
      -s, --sort             Specify whether to sort files, default is true
      --pattern TEXT         specify search regex pattern for extracting page
                             index,default:(\d+)
    
      --line-number INTEGER  specify line number for extracting page
                             index,default=-1
    
      --headers PATH         Specify file path to insert header
      -h, --help             Show this message and exit.
    ```
1. Example:
    ```batch
     .\pdfmerger merge -f /xx/xx/test+3.4.pdf  -f /xx/xx/test+3.3.pdf -o output.pdf --line-number=0 --pattern="·(\d+)·"
    ```
1. Example:
     ```batch
     .\pdfmerger merge -d /xx/xx/*+3.*.pdf -o output.pdf --line-number=0 --pattern="·(\d+)·"
    ```
Note: replace with pdfmerger to pdfmerger.exe on windows
