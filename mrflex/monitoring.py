from flask import Blueprint, render_template
from ares.Lib import Ares

monitoringBP = Blueprint("monitoring", __name__, url_prefix='/monitoring')

@monitoringBP.route("/")
def index():
    onload, content, js = index_report()
    return render_template("ares_template.html", onload=onload, content=content, js=js)

def index_report():
    aresObj = Ares.Report()
    aresObj.reportName = "Mrflex Monitoring"
    aresObj.title("Mrflex Monitoring")

    # Number of scripts per type
    aresObj.generatePdf()
    # Number of deployments / Number of commits / average change size per commit

    # Number of jobs per script

    # Average run time per script / Size of logs / Size of useful logs

    # Number of failures / number of success

    onload, content, js = aresObj.html()
    return onload, content, js


if __name__ == '__main__':
    onload, content, js = index_report()
    print(js)
