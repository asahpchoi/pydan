from process import extractfile,  gen_report, gen_html, report_output

extraction = extractfile("pdfs/p1.pdf")
rpt = gen_report(extraction)
gen_html(rpt)
