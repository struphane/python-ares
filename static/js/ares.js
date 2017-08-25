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
        tmpDict[data[i][cols[0]]] = getDict(tmpDict, data[i][cols[0]], 0)  + parseFloat(data[i][cols[1]]) ;
    }

    // Build the list of tuple that is expected by the graph
    var filterData = [];
    for (var key in tmpDict) {
        filterData.push([key, tmpDict[key]]);
    }
    return filterData;
};