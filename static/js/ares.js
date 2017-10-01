/*

 */

function getDict(dict, key, dflt){
    // Return a default value in a dictionary
    if (key in dict) return dict[key];
    else return dflt
}

function getDataFromRecordSet(data, cols) {
    // Return the list of tuples as expected in a graph
    // It will use a temporary dictionary for the aggregation
    var tmpDict = {};
    for (var i = 0, len = data.length; i < len; i++) {
        tmpDict[data[i][cols[0]]] = getDict(tmpDict, data[i][cols[0]], 0) + parseFloat(data[i][cols[1]]) ;
    }

    // Build the list of tuple that is expected by the graph
    var filterData = [];
    for (var key in tmpDict) {
        filterData.push([key, tmpDict[key]]);
    }

    return filterData;
};

function wrapperSimpleCharts(data, categories, selectedVals) {
    var key ;
    var val ;
    categories.each(function() {
        key = $(this).val();
    });

    selectedVals.each(function() {
        val = $(this).val();
    });
    return getDataFromRecordSet(data, [key, val]);
}


function buildMultiSeriesRecordSet(data, seriesKey, category, selectedVals, selectedSeries)
{
    var tmpDict = {};
    var recSet = [];
    var series = [];
    var selCat = category.val();
    var selVal = selectedVals.val();

    selectedSeries.each(function() {
        series.push($(this).val());
        })

    //build tmpDict to aggregate the series together

    for (var i = 0, len = data.length; i < len; i++)
    {
        category = data[i][selCat];
        values = data[i][selVal];

        if (series.includes('default') )
        {
            serie = 'Default';
        }
        else
        {
            if (!(series.includes(data[i][seriesKey]) || series.includes('All')))
            {
                continue;
            }
            else
            {
                serie = data[i][seriesKey];
            }
        }
        if (serie in tmpDict)
        {
            tmpDict[serie].push([category, values]);
        }
        else
        {
            tmpDict[serie] = [[category, values]];
        }
    }

    for (var key in tmpDict)
    {

        recSet.push({"key": key, "values": tmpDict[key]});
    }

    return recSet;


}

function buildJsRecordSet(data, categories, selectedVals) {
    // new function to allow for multiple series to be passed to the graph
    series = [];
    values = [];
    categories.each(function() {
        series.push($(this).val());
    });

    selectedVals.each(function() {
        values.push($(this).val());
    });
    seriesLen = series.length;

    recSet = [];
    for (i = 0; i < seriesLen; i++)
    {
        var seriesDict = {"key": series[i], "values": getDataFromRecordSet(data, [series[i], values[i]])};
        recSet.push(seriesDict);
    }

    return recSet;
}


function getRecordSetFromTable(htmlTableId){
    // Return a list of dictionaries from a DataTable object
    // The recordSet will be based on the selected (displayed) data and the portfolio
    var nRow = $('#' + htmlTableId + ' thead tr')[0] ;
    headers = [] ;
    for (var i = 0, len = nRow.cells.length; i < len; i++) {
      headers.push(nRow.cells[i].innerText) ;
    };
    recordSet = [] ;
    $('#' + htmlTableId + '').dataTable().$('tr', {"filter": "applied"}).each( function () {
      var row = $(this).text().split("\n");
      rec = {};
      for (var i = 0, len = headers.length; i < len; i++) {
        rec[headers[i]] = row[i+1] ;
      }
      recordSet.push(rec) ;
    } );
    return recordSet ;
} ;

function buildCountRecordSet(){

    return [{text: 'Remi', size: 20}, {text: 'Alfredo', size: 120}, {text: 'Olivier', size: 40}, {text: 'Nelson', size: 200}]
}