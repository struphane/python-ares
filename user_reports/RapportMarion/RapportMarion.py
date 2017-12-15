""" [SCRIPT COMMENT]


"""
import random
TEAM = '' # Report's team
DSC = '' # Report Short description
NAME = 'Repo Bond Details' # The Report Name in the left menu
# The Shortcuts should be defined as below
# [(Cateogry Name, [List of the script in the root directory])]
# It is only possible to create new links for scripts in the root
SHORTCUTS = [] # All the possible link to other pages
FILE_CONFIGS = [] # All the static and output files configurationa
# The format in the above list should be as: {'filename': 'data.txt', 'folder': 'outputs', 'parser': InFilePricesConfig.InFilePices},

HTTP_PARAMS = [] # If you want to use the param method to set parameter before running hte report


#def params(modalObj):
#  """ Optional param method to be run before the report method to set parameter """


def report(aresObj):
  '''
  Write your function below
  '''
  aresObj.title("Repo Bond Details")

  maturity_map = {0: '0M', 1: '1M', 2: '3M', 3: '1Y'}
  bl_map = {0: 'GM', 1: 'ALM', 2: 'BP2S'}
  liquidity_map = {0: 'Level1', 1: 'Level2', 2: 'Non Liquid'}
  cpty_type_map = {0: 'Government', 1: 'Corporate', 2: 'Agency', 3: 'Fund', 4: 'Financial', 5: 'Others'}
  rtg_map = {1: 'AAA',2: 'AA+',3: 'AA',4: 'AA−',5: 'A+',6: 'A',7: 'A−',8: 'BBB+',9: 'BBB',10: 'BBB−',11: 'BB+',12: 'BB',
             13: 'BB−',14: 'B+',15: 'B',16: 'B−',17: 'CCC+',18: 'CCC',19: 'CCC−',20: 'CC',21: 'C',22: 'SD',23: 'D'}
  cty_map = {1: 'Afghanistan',2: 'Albania',3: 'Algeria',4: 'American Samoa',5: 'Andorra',6: 'Angola',7: 'Anguilla',8:
    'Antarctica',9: 'Antigua and Barbuda',10: 'Argentina',11: 'Armenia',12: 'Aruba',13: 'Australia',14: 'Austria',15:
    'Azerbaijan',16: 'Bahamas',17: 'Bahrain',18: 'Bangladesh',19: 'Barbados',20: 'Belarus',21: 'Belgium',22: 'Belize',
             23: 'Benin',24: 'Bermuda',25: 'Bhutan',26: 'Bolivia',27: 'Bosnia and Herzegovina',28: 'Botswana',29: 'Brazil',
             30: 'British Indian Ocean Territory',31: 'British Virgin Islands',32: 'Brunei',33: 'Bulgaria',34: 'Burkina Faso',
             35: 'Burundi',36: 'Cambodia',37: 'Cameroon',38: 'Canada',39: 'Cape Verde',40: 'Cayman Islands',41: 'Central African Republic',
             42: 'Chad',43: 'Chile',44: 'China',45: 'Christmas Island',46: 'Cocos Islands',47: 'Colombia',48: 'Comoros',49: 'Cook Islands',
             50: 'Costa Rica',51: 'Croatia',52: 'Cuba',53: 'Curacao',54: 'Cyprus',55: 'Czech Republic',56: 'Democratic Republic of the Congo',
             57: 'Denmark',58: 'Djibouti',59: 'Dominica',60: 'Dominican Republic',61: 'East Timor',62: 'Ecuador',63: 'Egypt',64: 'El Salvador',
             65: 'Equatorial Guinea',66: 'Eritrea',67: 'Estonia',68: 'Ethiopia',69: 'Falkland Islands',70: 'Faroe Islands',
             71: 'Fiji',72: 'Finland',73: 'France',74: 'French Polynesia',75: 'Gabon',76: 'Gambia',77: 'Georgia',78: 'Germany',
             79: 'Ghana',80: 'Gibraltar',81: 'Greece',82: 'Slovenia',83: 'Solomon Islands',84: 'Somalia',85: 'South Africa',
             86: 'South Korea',87: 'South Sudan',88: 'Spain',89: 'Sri Lanka',90: 'Sudan',91: 'Suriname',92: 'Svalbard and Jan Mayen',
             93: 'Swaziland',94: 'Sweden',95: 'Switzerland',96: 'Syria',97: 'Taiwan',98: 'Tajikistan',99: 'Tanzania',
             100: 'Thailand',101: 'Togo',102: 'Tokelau',103: 'Tonga',104: 'Trinidad and Tobago',105: 'Tunisia',106: 'Turkey',
             107: 'Turkmenistan',108: 'Turks and Caicos Islands',109: 'Tuvalu',110: 'U.S. Virgin Islands',111: 'Uganda',
             112: 'Ukraine',113: 'United Arab Emirates',114: 'United Kingdom',115: 'United States',116: 'Uruguay',117: 'Uzbekistan',
             118: 'Vanuatu',119: 'Vatican',120: 'Venezuela',121: 'Vietnam',122: 'Wallis and Futuna',123: 'Western Sahara',
             124: 'Yemen',125: 'Zambia',126: 'Zimbabwe'}

  dealRecordSet, cptyRecSet = [], []
  for i in range(50):
    cpty = chr(int(random.uniform(65, 90)))
    maturity = maturity_map.get(random.randint(0,3))
    for y in range(2000):
      if y * random.randint(0, 100) > 4000:
        break

      dealRecordSet.append({'cpty': cpty,
                        'deal': y,
                        'cash_in': random.randint(1000, 1000000),
                        'cash_out': -1 * random.randint(1000, 1000000),
                        'RNFB': random.randint(100, 5000000),
                        'maturity': maturity,
                        'business_line': bl_map.get(random.randint(0,2)),
                        'liquidity': liquidity_map.get(random.randint(0,2)),
                        'country': cty_map.get(random.randint(1, 124)),
                        'type': cpty_type_map.get(random.randint(0, 5)),
                        'rtg': i % 23})
    cptyRecSet.append({'cpty': cpty, 'maturity': maturity, 'rtg': i % 23})

  # xFilterDeal = aresObj.crossFilterData(dealRecordSet, [{'colName': 'cpty', 'key': 'cpty'},
  #                                     {'colName': 'deal', 'key': 'deal'},
  #                                     {'colName': 'cash_in', 'key': 'cash_in'},
  #                                     {'colName': 'cash_out', 'key': 'cash_out'},
  #                                     {'colName': 'RNFB', 'key': 'RNFB'},
  #                                     {'colName': 'maturity', 'key': 'maturity'},
  #                                     {'colName': 'business_line', 'key': 'business_line'},
  #                                     {'colName': 'liquidity', 'key': 'liquidity'},
  #                                     {'colName': 'country', 'key': 'country'},
  #                                     {'colName': 'type', 'key': 'type'},
  #                                     {'colName': 'rtg', 'key': 'rtg'},])


  xFilterCpty = aresObj.crossFilterData(cptyRecSet, [{'colName': 'cpty', 'key': 'cpty'},
                                      {'colName': 'maturity', 'key': 'maturity'},
                                      {'colName': 'rtg', 'key': 'rtg'},])
  import pprint
  pprint.pprint(cptyRecSet)
  scatterData = xFilterCpty.group('maturity', 'rtg')
  xFilterCpty.addFilter('cpty', 'Filter On Counterparty')
  xFilterCpty.display(scatterData)
  aresObj.newline()
  aresObj.select(['Cpty Type', 'Issuer', 'Country'], 'Select Criteria')
  aresObj.newline()
  aresObj.newline()

  aresObj.title('Top 50 Counterparties')

  aresObj.newline()

  scatter = aresObj.xscatter(scatterData)
  scatter.mapxAxes(list(maturity_map.values()))
