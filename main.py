import threading
from process import extractfile,  gen_report, gen_html, report_output

 
def work(file):
    extraction = extractfile(file)
    rpt = gen_report(extraction)
    gen_html(rpt, file)

t1 = threading.Thread(target=work("pdfs/p1.pdf")) 
t2 = threading.Thread(target=work("pdfs/p2.pdf")) 

t1.start()
t2.start()