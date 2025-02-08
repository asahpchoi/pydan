import threading
from process import extractfile,  gen_report, gen_html, report_output, summary, write_file, read_file
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from db import initUW
 
def work(file):
    extraction = extractfile(file)
    rpt = gen_report(extraction)
    summary(extraction)
    gen_html(rpt, file)


def getRef():
    extract = extractfile("./pdfs/p5.pdf")
    write_file(extract, "./pdfs/result") 

def indexer():
    class chunk_item(BaseModel):
        title: str
        content_in_markdown: str

    class chunks(BaseModel):
        chunk: list[chunk_item]
    
    

    ia = Agent("google-gla:gemini-2.0-flash-exp", 
                result_type=chunks,
                system_prompt="""you are an expert data injector, 
                you can base on the provided content to seperate it into different chunks for data indexing
                each chunk should have title and content and should be saved to database.
                remember to keep all the markdown in the content
                """)
    @ia.tool
    async def insertcontent(ctx: RunContext[int], title: str, content: str):
        """
            insert the extracted content into database
        """
        print(title, content.replace("\"", "'"))
        initUW(title, content.replace("\"", "'")) 

    context = read_file("pdfs/uw.txt")
    #print(context)
    result = ia.run_sync(
        f"context:{context}"
    )
    for item in result.data.chunk:
        print(item)
        

indexer()
