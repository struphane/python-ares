"""

"""

NAME = 'User Account'

from flask import url_for, redirect
from Libs import AresUserAuthorization


DATASOURCES = [{'source': 'MRX', 'inputParams': ('Username', 'Password')}
               ]

def report(aresObj):
  # userRecordSet = getEnvData(aresObj)
  userdata = aresObj.http['USERDATA']
  title = aresObj.title('User Account Information')
  account_id = aresObj.http['USERNAME']
  title2 = aresObj.title2(account_id)
  aresObj.row([title, title2])

  aresObj.newline()
  aresObj.newline()

  title3 = aresObj.title2('Data Sources')
  editModal = aresObj.modal('Edit', btnCls=['btn btn-link'])
  editModal.modal_header = 'Add External System credentials'
  sourceDropDown = aresObj.select([rec['source'] for rec in DATASOURCES])
  sourceDropDown.setDefault('MRX')
  usernameInput = aresObj.input("Username", '')
  pwdInput = aresObj.pwd("Password", '')
  rowModal = aresObj.row([sourceDropDown, usernameInput, pwdInput])
  addSource = aresObj.button('Add')

  # Ajax call using a post message
  addSource.clickWithValidCloseModal('AresUserAddPass', editModal, {'source':sourceDropDown, 'username': usernameInput, 'pwd': pwdInput, 'app_id': account_id}, subPost=True)

  aresObj.addTo(editModal, rowModal)
  aresObj.addTo(editModal, addSource)


  aresObj.row([title3, editModal])
  if not userdata['sources']:
    text1 = aresObj.text('No Data Sources configured yet')
  else:
    aresObj.table(userdata['sources'], header=[{'key': 'src_nam', 'colName': 'Source Name'},
                                        {'key': 'src_username', 'colName': 'Username'},
                                        {'key': 'src_pwd', 'colName': 'Password'},])


  aresObj.newline()
  aresObj.newline()

  title4 = aresObj.title2(userdata['team'])
  editButton2 = aresObj.externalLink('Edit', '')
  aresObj.row([title4, editButton2])

  aresObj.newline()
  aresObj.newline()

  aresObj.title2('Authorized Environments')
  if not userdata['envs']:
    aresObj.text('No environments authorized yet')
  else:
    for envs in userdata['envs']:
      aresObj.text(envs.env_name)







