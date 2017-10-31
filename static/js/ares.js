/*

 */

if ( typeof String.prototype.startsWith != 'function' ) {
  String.prototype.startsWith = function( str ) {
    return this.substring( 0, str.length ) === str;
  }
};

Number.prototype.formatMoney = function(decPlaces, thouSeparator, decSeparator) {
    var n = this,
        decPlaces = isNaN(decPlaces = Math.abs(decPlaces)) ? 2 : decPlaces,
        decSeparator = decSeparator == undefined ? "." : decSeparator,
        thouSeparator = thouSeparator == undefined ? "," : thouSeparator,
        sign = n < 0 ? "-" : "",
        i = parseInt(n = Math.abs(+n || 0).toFixed(decPlaces)) + "",
        j = (j = i.length) > 3 ? j % 3 : 0;
    return sign + (j ? i.substr(0, j) + thouSeparator : "") + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + thouSeparator) + (decPlaces ? decSeparator + Math.abs(n - i).toFixed(decPlaces).slice(2) : "");
};

function addInputforDeploy(divId){
            var newDiv = document.createElement('div');
            newDiv.innerHTML = "<br><input type='file' name='file' />";
            document.getElementById(divId).appendChild(newDiv);
}

function addInputForUpload(divId){
            var newDiv = document.createElement('div');
            newDiv.innerHTML = "<br><input type='file' name='file' />" +
             "<select name='File Type' required>" +
             "<option value='report'>report</option>" +
             "<option value='configuration'>configuration</option>" +
             "<option value='ajax'>ajax</option>" +
             "<option value='javascript'>javascript</option>" +
             "<option value='views'>views</option>" +
             "<option value='outputs'>outputs</option>" +
             "<option value='styles'>styles</option>" +
             "<option value='saved'>saved</option>" +
             "</select>";
             document.getElementById(divId).appendChild(newDiv);
}

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

        if (series.indexOf('default') != -1)
        {
            serie = 'Default';
        }
        else
        {
            if ( ( series.indexOf(data[i][seriesKey]) == -1 && series.indexOf('All') == -1))
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

function buildCountRecordSet(data, cursor){
    var result = {} ;
    for (var i = 0, len = data.length; i < len; i++) {
        var category = data[i][cursor];
        if (category in result){
            result[category] = result[category] + 1 ;}
        else {
            result[category] = 1;}
    } ;

    var recordSet = [];
    for (var key in result) {
        recordSet.push({text: key, size: result[key]});
    }
    return recordSet ;
}

function getSelectRadio(event, radios){
    /**
     * Return the selected value in a Radio component
     */
    var checked;
    radios.each(
        function() {
            if ($(this).hasClass('active')) {
                $(this).attr('class', 'btn btn-info');

            }
        }
    ) ;

    selectedItem = $(event.currentTarget) ;
    selectedItem.attr('class', 'btn btn-success');
    return selectedItem.text().trim() ;
}