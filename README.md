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
- **merge** command, merge multiple pdf files order by input order
    ```
    Usage: pdfmerger merge [OPTIONS]
    
      merge pdf
    
    Options:
      -f, --files PATH      files to merge. e.g: 1.pdf 2.pdf...
      -d, --directory PATH  input directory
      -o, --output PATH     output path
      -s, --sort            Specify whether to sort files, default is true
      --headers PATH        Specify file path to insert header
      -h, --help            Show this message and exit.
    ```
1. Example:
    ```batch
     .\pdfmerger merge -f /xx/xx/test+3.4.pdf  -f /xx/xx/test+3.3.pdf -o output.pdf
    ```
1. Example:
     ```batch
     .\pdfmerger merge -d /xx/xx/*+3.*.pdf -o output.pdf
    ```
Note: replace with pdfmerger to pdfmerger.exe on windows
