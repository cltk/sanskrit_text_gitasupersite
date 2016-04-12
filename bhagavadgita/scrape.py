import urllib
import BeautifulSoup

def iseng(s):
   return all(ord(c) < 128 for c in s)

def Parse(val0, val1):
   Url = 'http://www.gitasupersite.iitk.ac.in/srimad?language=dv&field_chapter_value='+str(val0)+'&field_nsutra_value='+str(val1)+'&etsiva=1&choose=1'
   idy = str(val0) + '.' + str(val1)
   pidy = str(val0) + '.' + str(val1 - 1)
   nidy = str(val0) + '.' + str(val1 + 1)
   while(True):
       try:
           html = urllib.urlopen(Url).read()
           break
       except Exception:
           pass
   html = html.replace('\r','')
   soup = BeautifulSoup.BeautifulSoup(html)
   FONT = soup.findAll('font', {'size':'3px'})
   
   san = ''
   try:
      x = FONT[0].findAll(text = True)
      y = FONT[1].findAll(text = True)
   except IndexError:
      return None, None
   if(idy not in html):
      return None, None
   L = len(x)
   for i in x:
      if(iseng(i)):
         continue
      first = str(i.encode('utf8'))
      san += first + ' '
   en = ''
   try:
      for i in y:
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

#x = Parse(1, 1)
#print x[0]
#print "----------"
#print x[1]
#exit(0)
def get(chapter):
   Mem = []
   Count = 0
   for i in xrange(1, 301):
      san, en = Parse(chapter, i)
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
      print i
      print "   san: <" + str(san) + '>'
      try:
         print "   en: <" + str(en) + '>'
      except UnicodeError:
         en = str(en.encode('utf8'))
      if(san != None and en != None):
         Count = 0
         f = open(str(chapter) + '_sanskrit.txt', 'a+')
         f.write(san + '\n')
         f.close()
         f = open(str(chapter) + '_english.txt', 'a+')
         f.write(en + '\n')
         f.close()
      else:
         Count += 1
         if(Count >= 20):
            break

for chapters in xrange(1, 19):
   get(chapters)
