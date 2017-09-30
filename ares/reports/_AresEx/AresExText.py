

NAME = 'Text link'

def report(aresObj):
  # Write your report here
  title2 = aresObj.title2("")
  input = aresObj.input()
  input.js('change', '')
  input.jsLinkTo([title2])
  return aresObj
