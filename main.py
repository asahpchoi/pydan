import sys
from process import extractfile, gen_report
from pydantic_ai import Agent
import codecs
from pydantic import BaseModel


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <pdf_filename>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        extraction = extractfile(filename)
 
        
        rpt = gen_report(extraction, filename)



    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
