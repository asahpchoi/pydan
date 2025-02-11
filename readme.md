# Medical Report Extraction Project

This project extracts information from medical PDF files and generates HTML reports.

## Overview

The project consists of three main Python files:

*   `main.py`: Orchestrates the extraction and report generation process.
*   `process.py`: Contains functions for extracting data from PDF files, mapping diagnoses, and generating medical reports.
*   `tools/tools.py`: Contains helper functions for OCR, PDF extraction, and user information retrieval.

## File Descriptions

### `main.py`

This file is the entry point of the application. It takes the PDF filename as a command-line argument, calls the `extractfile` function from `process.py` to extract data from the PDF, and then calls the `gen_report` function to generate a medical report. Finally, it generates an HTML report using the extracted data.

### `process.py`

This file contains the core logic for processing medical reports. It includes the following functions:

*   `extractfile(pdf_file: str) -> str`: Extracts information from a PDF file using an agent and several tools for image extraction, diagnosis mapping, and underwriting assessment.
*   `gen_report(context: str) -> report_output`: Generates a medical report from a given context.

### `tools/tools.py`

This file contains helper functions used by `process.py`:

*   `getOCR(path: str) -> str`: Extracts text from an image using OCR.
*   `extractpdf(path: str) -> list[str]`: Extracts images from a PDF file.
*   `getUserInfo(userID: str) -> str`: Retrieves user information (currently hardcoded).

## Dependencies

*   pydantic\_ai
*   crawl4ai
*   pdf2image
*   PIL
*   colorama
*   python-dotenv

## Usage

To run the program, use the following command:

```
python main.py <pdf_filename>
```

Replace `<pdf_filename>` with the path to the medical PDF file you want to process. The program will generate an HTML report with the same name as the PDF file (e.g., `pdfs/p1.pdf.html`).
