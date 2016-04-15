import urllib
import BeautifulSoup
import os
import sys

category = ''
def content(con):
   x = con.findAll(text = True)
   res = ''
   for i in x:
      first = str(i.encode('utf8'))
      res += first + ' '
   res = res.strip()
   res = res.strip(' ')
   res = res.strip('\n')
   return res

def Parse(val0, val1):
   Url = 'http://www.gitasupersite.iitk.ac.in/yogasutra_content?language=dv&field_chapter_value=' + str(val0) + '&field_nsutra_value=' + str(val1) + '&enable_sutra=1&enable_bhaysa=1&enable_vritti=1'
   while(True):
       try:
           html = urllib.urlopen(Url).read()
           break
       except Exception:
           pass
   html = html.replace('\r','')
   soup = BeautifulSoup.BeautifulSoup(html)
   FONT = soup.findAll('font', {'size':'3px'})
   if(len(FONT) != 3):
      print
      print val0, val1
      exit(1)
   return san1, san2, san3

def get(chapter, sutras):
   Mem = []
   Fin = []
   Count = 0
   f = open('./chapter_' + str(chapter) + '/sutra.txt', 'w')
   g = open('./chapter_' + str(chapter) + '/bhashya.txt', 'w')
   h = open('./chapter_' + str(chapter) + '/bhojavruthi.txt', 'w')
   print "   ",
   for i in xrange(1, sutras + 1):
      print i,
      sys.stdout.flush()
      san1, san2, san3 = Parse(chapter, i)
      f.write(san1 + '\n')
      g.write(san2 + '\n')
      h.write(san3 + '\n')
   f.close()
   g.close()
   h.close()
   print

sutras = [51, 55, 55, 34]
for i in xrange(4):
   os.system('mkdir chapter_' + str(i + 1))
   print "chapter :", i + 1
   get(i + 1, sutras[i])