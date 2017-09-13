from flask import Blueprint, render_template
from click import echo

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

    aresObj.table('Table Example', {"header": ["Node Code", "Ptf Code", "IR Delta"], "body": [["GBCSA", 31415, 24683], ["IRLPAS", 31415, 24683]]})
    aresObj.table('Table Example', { "header": [[("Calc Date", "rowspan='2'"), ("Node Code", "rowspan='2'"), ("Position", "colspan='2'")], ["FX Expo PV", "IR Delta"]]
                                   , "body": [["2017-08-24", "GBCSA", 24683, 31514], ["2017-08-25", "IRLPAS", 24683, 31514]]})


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
    echo(js)
