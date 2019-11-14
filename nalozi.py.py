import re
import orodja

def zajemi_knjige():
    for i in range(1,35):
         spletna_stran = 'http://www.bookdepository.com/bestsellers?format=1,2&searchLang=123'
         parametri = '&page={}'.format(i)
         naslov = spletna_stran + parametri
         ime_datoteke = 'Knjigehtml/Stran{:02}.html'.format(i)
         orodja.shrani(naslov, ime_datoteke)


zajemi_knjige()

regex_knjige = re.compile(
     r'''<div class="number">'''
     r'''.*?'''
     r'''(?P<uvrstitev>\d{1,4})'''
     r'''.*?'''
     r'''content="\d*" />'''
     r'''.*?'''
     r'''content="(?P<naslov>.*?)" \/>'''
     r'''.*?'''
     r'''content="(?P<avtor>.*?)" \/>'''
     r'''.*?'''
     r'''itemprop="datePublished">\d\d (?P<mesec_izdaje>\D\D\D) (?P<leto_izdaje>\d\d\d\d)<\/p>'''
     r'''.*?'''
     r'''<p class="format">(?P<format>.*?)<\/p>'''
     ,flags=re.DOTALL)


def izloci_podatke_knjig(imenik):
     knjige = []
     for html_datoteka in orodja.datoteke(imenik):
          for knjiga in re.finditer(regex_knjige, orodja.vsebina_datoteke(html_datoteka)):
               knjige.append(pocisti_knjige(knjiga))
     return knjige


def pocisti_knjige(knjiga):
     podatki = knjiga.groupdict()
     podatki['uvrstitev'] = int(podatki['uvrstitev'])
     podatki['naslov'] = str(podatki['naslov'])
     podatki['avtor'] = str(podatki['avtor'])
     podatki['mesec_izdaje'] = str(podatki['mesec_izdaje'])
     podatki['leto_izdaje'] = int(podatki['leto_izdaje'])
     podatki['format'] = str(podatki['format'])
     return podatki

def zamenjaj(niz):
    niz = niz.replace('&#039',"'")
    return niz

podatki = izloci_podatke_knjig('knjigehtml/')
orodja.zapisi_tabelo(podatki, ['uvrstitev', 'avtor', 'naslov', 'mesec_izdaje', 'leto_izdaje', 'format'], 'KnjigeCSV/podatki.csv')
