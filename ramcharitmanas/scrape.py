import urllib
import BeautifulSoup
import os
import sys

def clean(x):
  x = x.strip('\n')
  x = x.strip(' ')
  x = x.strip()
  x = x[::-1]
  x = x.strip('\n')
  x = x.strip(' ')
  x = x.strip()
  x = x[::-1]
  return x

def Parse(val0, val1):
   Url = 'http://www.ramcharitmanas.iitk.ac.in/ramcharitmanas?tid=' + str(val0) + '&tid_2=8&tid_1=11&page=0%2C' + str(val1)
   while(True):
       try:
           html = urllib.urlopen(Url).read()
           break
       except Exception:
           pass
   html = html.replace('\r','')
   soup = BeautifulSoup.BeautifulSoup(html)
   content = soup.findAll('p')
   chopayi = ''
   doha = ''
   for j in xrange(3):
    try:
      x = content[j].findAll(text = True)
    except IndexError:
      break
    f = 3
    for i in x:
      if(i.encode('utf8') == '\xe0\xa4\x9a\xe0\xa5\x8c\xe0\xa4\xaa\xe0\xa4\xbe\xe0\xa4\x88'):
        f = 1
      elif(i.encode('utf8') == '\xe0\xa4\xa6\xe0\xa5\x8b\xe0\xa4\xb9\xe0\xa4\xbe/\xe0\xa4\xb8\xe0\xa5\x8b\xe0\xa4\xb0\xe0\xa4\xa0\xe0\xa4\xbe'):
        f = 0
      elif(i.encode('utf8') == '\xe0\xa4\x9b\xe0\xa4\x82\xe0\xa4\xa6'):
        f = 2
      else:
        tmp = clean(str(i.encode('utf8')))
        if(f == 1):
          chopayi += tmp
          chopayi += '\n'
        elif(f == 0):
          doha += tmp
          doha += '\n'
   return chopayi, doha

def get():
   chapters = []
   chapters.append(('baal_kaanda', 360))
   chapters.append(('ayodhya_kaanda', 325))
   chapters.append(('aranya_kaanda', 45))
   chapters.append(('kishkindha_kaanda', 29))
   chapters.append(('sundara_kaanda', 59))
   chapters.append(('lanka_kaanda', 120))
   chapters.append(('uttara_kaanda', 129))
   for _chapter in xrange(7):
      os.system('mkdir ' + chapters[_chapter][0])
      print "chapter :", chapters[_chapter][0]
      f = open('./' + chapters[_chapter][0] + '/chopayi.txt', 'w')
      g = open('./' + chapters[_chapter][0] + '/doha.txt', 'w')
      print "     ",
      for i in xrange(chapters[_chapter][1] + 1):
        print i,
        sys.stdout.flush()
        chopayi, doha = Parse(_chapter + 1, i)
        f.write(chopayi)
        f.write('--x--\n')
        f.flush()
        g.write(doha)
        g.write('--x--\n')
        g.flush()
      f.close()
      g.close()
      print
get()
