"""

"""

DOWNLOAD = None

def report(aresObj):
  """
  """
  aresObj.title("A new dimension for your reports")
  aresObj.paragraph("Simple way to write reports or implement algorithms based on a recordset. The recordSet should be"
                    " your data structure and it will be the one recognised in all the python data containers like "
                    "a table or the charts. The main data object will be stored only once in the page and all the data "
                    "transformations will be performed in the javascript layer automatically. No need for the Python layer "
                    "to adapt the data structure to the HTML components.")

  aresObj.paragraph("At this stage the recordSet is considered as the only possible data structure because some part of"
                    " the environment might require Jython so it is not possible in this context to use C type data structures"
                    " like the ones in Panda. Nevertheless in your reports you can use those as they are available in the server."
                    "For the time being in order to be fully generic for all the different Python flavour no external module has been"
                    " selected as the internal data structure.")

  div = aresObj.div('The target will be to use Pandas as the underlying data structure in a further release', cssCls=['alert alert-info'])
  div.addAttr('role', 'alert')

  content1 = aresObj.paragraph("Thus with few extra line of code and your recordSet object you can display your results both locally in "
                              " an HTML page or on the server in a dedicated environment.")
  img = aresObj.img('report_pie_chart.JPG')
  content2 = aresObj.paragraph("<br>The possibility to add more dimension in your report to make it more interactive easily."
                              "Based on the header definition and some special common keywords in the set up of your chart, it is"
                              " very easy to customize the display")
  code = aresObj.code('''
  pie.setKeys(['CCY', 'PTF'], 'CCY')
  pie.setVals(['VAL', 'VAL3'], 'VAL')
  ''')
  data = aresObj.img('report_data.JPG')
  aresObj.row([aresObj.col([content1, img, content2, code]), data])

  aresObj.newline()
  aresObj.paragraph("This will then display a chart to your HTML page with some buttons for the different axes")
  aresObj.img('report_display.JPG', cssAttr={'margin-left': '25%'})