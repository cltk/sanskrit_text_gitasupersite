import urllib
import BeautifulSoup
import os
import sys

category = ''

def Parse(val0, val1):
   Url = 'http://www.gitasupersite.iitk.ac.in/minigita/' + category + '?language=dv&field_chapter_value='+str(val0)+'&field_nsutra_value='+str(val1)
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
   except IndexError:
      return None
   if(str(val1) in html):
      pass
   else:
      return None
   L = len(x)
   for i in x:
      first = str(i.encode('utf8'))
      san += first + ' '
   san = san.strip()
   san = san.strip(' ')
   san = san.strip('\n')
   return san

def get(chapter):
   Mem = []
   Fin = []
   Count = 0
   for i in xrange(1, 301):
      print i,
      sys.stdout.flush()
      san = Parse(chapter, i)
      if(san == None):
         Count += 1
         if(Count >= 20):
            break
      else:
         Count = 0
      if(san in Mem):
         continue
      else:
         Mem.append(san)
      if(len(Mem) >= 25):
         Mem = Mem[1:]
      if(san != None):
         if(san in Fin):
            break
         else:
            Fin.append(san)
         Count = 0
         f = open(category + '/' + str(chapter) + '_sanskrit.txt', 'a+')
         f.write(san + '\n')
         f.close()
      else:
         Count += 1
         if(Count >= 20):
            break

cat = [('ashtavakra', 20), ('avadhuta', 8), ('kapila', 3), ('sriram', 1), ('sruti', 2), ('uddhava', 24), ('vibhishana', 1)]
for i in cat:
   category, chapter = i[0], i[1]
   os.system('mkdir ' + category)
   print category, ":"
   for j in xrange(1, chapter + 1):
      print "  ", j, ":",
      get(j)
      sys.stdout.flush()
      print
   print
