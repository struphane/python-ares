''' [SCRIPT COMMENT] '''

AJAX_CALL = ['MyRepotTestAjax.py'] # Ajax call definition
CHILD_PAGES = {'test': 'MyRepotTestChild.py',} # Child pages call definition

def report(aresObj, localPath=None):

  outFile = aresObj.createFile('mygreatFile.dat', ['aaa', 'fdfgf', 'fdfdf'], checkFileExist=False)
  if outFile is not None:
    for i in range(10):
      outFile.write("%s\n" % i)
    outFile.close()

  inFile = aresObj.readFile('mygreatFile.dat', ['aaa', 'fdfgf', 'fdfdf'])
  for line in inFile:
    print(line)
  return aresObj