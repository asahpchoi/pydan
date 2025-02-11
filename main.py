import threading
from process import extractfile,  gen_report, gen_html, report_output

 
filename = "pdfs/p1.pdf"
extraction = extractfile(filename)

#file = open(f"{filename}.txt", "r")
#extraction = file.read()
print(extraction)
 

rpt = gen_report(extraction)
gen_html(rpt,filename)


 