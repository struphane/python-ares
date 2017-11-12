/**
 * https://www.html5rocks.com/en/tutorials/file/filesystem-sync/
 * @param event
 */

onmessage = function(event) {
  console.log("message received in the worker" + event.data);

  var rawFile = new XMLHttpRequest();
  console.log(rawFile);
  //requestFileSystemSync = self.webkitRequestFileSystemSync || self.requestFileSystemSync;
  var fs = self.requestFileSystemSync(self.TEMPORARY, 1024*1024 /*1MB*/);
  var fileEntry = fs.root.getFile('log.txt', {create: true});

  console.log(rawFile);
  rawFile.open("GET", "file:///D:/GitHub/python-ares-master/user_reports/PivotTable/PivotTable.py", false);
  rawFile.onreadystatechange = function ()
  {
    console.log(rawFile.readyState);
      if(rawFile.readyState === 4)
      {
          if(rawFile.status === 200 || rawFile.status == 0)
          {
              var allText = rawFile.responseText;
              postMessage(allText);
          }
      }
  }
  //postMessage("rrr");
}