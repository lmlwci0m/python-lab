__author__ = 'roberto'


import urllib.request
import urllib.parse


url = 'http://10.215.20.22/underground/elencoSempliceQualificheValide'
url = 'http://10.215.20.22/underground/creazioneProfiloConNG'

qs=urllib.parse.urlencode({
    'codiceFiscale': 'FCTFNC83H16G039M',
    'codiceNaturaGiuridica': 'NG011'})

response = urllib.request.urlopen(url, qs.encode()).read()

print(str(response, 'Windows-1252'))

