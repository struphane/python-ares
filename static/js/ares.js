
function getDict(dict, key, dflt){
    if (key in dict) return dict[key];
    else return dflt
}
function getDataFromRecordSet(data, cols) {
    var tmpDict = {};
    for (var i = 0, len = data.length; i < len; i++) {
        tmpDict[data[i][cols[0]]] = getDict(tmpDict, data[i][cols[0]], 0)  + parseFloat(data[i][cols[1]]) ;
    }

    var filterData = [];
    for (var key in tmpDict) {
        filterData.push([key, tmpDict[key]]);
    }
    return filterData;
};