import sys
from process import extractfile, gen_report
from pydantic_ai import Agent

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <pdf_filename>")
        sys.exit(1)

    filename = sys.argv[1]

    try:
        extraction = extractfile(filename)
        print(extraction)
        rpt = gen_report(extraction)

        # Generate HTML report
        from pydantic import BaseModel
        class htmloutput(BaseModel):
            html: str

        html_agent = Agent(
            model="openai:gpt-4o-mini",
            result_type=htmloutput
        )

        html = html_agent.run_sync(f"generate the html base on the input data: {rpt}")

        import codecs
        with codecs.open(f"{filename}.html", "w", "utf-8") as f:
            f.write(html.data.html)

    except FileNotFoundError:
        print(f"Error: File not found: {filename}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
