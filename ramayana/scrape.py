import urllib
import BeautifulSoup

def iseng(s):
   return all(ord(c) < 128 for c in s)

def Parse(val0, val1, val2):
   Url = 'http://www.valmiki.iitk.ac.in/content?language=dv&field_kanda_tid=' + str(val0)+'&field_sarga_value=' + str(val1)+'&field_sloka_value=' + str(val2)
   idy = str(val0) + '.' + str(val1) + '.' + str(val2)
   pidy = str(val0) + '.' + str(val1) + '.' + str(val2 - 1)
   nidy = str(val0) + '.' + str(val1) + '.' + str(val2 + 1)
   while(True):
       try:
           html = urllib.urlopen(Url).read()
           break
       except Exception:
           pass
   html = html.replace('\r','')
   soup = BeautifulSoup.BeautifulSoup(html)
   DIV = soup.findAll('div', {'class' : 'field-content'})
   san = ''
   try:
      x = DIV[0].findAll(text = True)
   except IndexError:
      return None, None
   if(idy not in html):
      return None, None
   L = len(x)
   for i in x:
      if(iseng(i)):
         continue
      first = str(i.encode('utf8'))
      for aa in xrange(-7, 8):
          for bb in xrange(-7, 8):
            first = first.replace(str(val0) + '.' + str(val1 + aa) + '.' + str(val2 + bb), '')
            first = first.replace(str(val0) + str(val1 + aa) + str(val2 + bb), '')
      first = first.replace('\xe0\xa5\xa4', '')
      if(i == x[-1]):
         first += '\xe0\xa5\xa4\xe0\xa5\xa4'
      else:
         first += '\xe0\xa5\xa4'
      san += first + ' '
   en = DIV[2].findAll(text = True)
   try:
      tmp = en
      en = ''
      for i in tmp:
         en += str(i.encode('utf8'))
   except Exception:
      return None, None
   san = san.strip()
   san = san.strip(' ')
   san = san.strip('\n')
   en = en.strip()
   en = en.strip('\n')
   
   if(en == ''):
      return None, None
   return san, en
   
def get(Filename, sarga, kandaid):
   Mem = []
   for i in xrange(1, sarga):
      Count = 0
      for j in xrange(1, 301):
         san, en = Parse(kandaid, i, j)
         if(san == None and en == None):
            Count += 1
            if(Count >= 20):
               break
         else:
            Count = 0
         if((san, en) in Mem):
            continue
         else:
            Mem.append((san, en))
         if(len(Mem) >= 25):
            Mem = Mem[1:]
         print i, j
         print "   san: <" + str(san) + '>'
         try:
            print "   en: <" + str(en) + '>'
         except UnicodeError:
            en = str(en.encode('utf8'))
         if(san != None and en != None):
            Count = 0
            f = open(Filename + '_sanskrit.txt', 'a+')
            f.write(san + '\n')
            f.close()
            f = open(Filename + '_english.txt', 'a+')
            f.write(en + '\n')
            f.close()
         else:
            Count += 1
            if(Count >= 20):
               break

Kandas = [('sundarakanda', 69, 5), ('aranyakanda', 76, 3), ('ayodhyakanda', 120, 2), ('balakanda', 78, 1), ('kishkindakanda', 68, 4)]
for kanda, sarga, kandaid in Kandas:
   get(kanda, sarga, kandaid)