import urllib
import BeautifulSoup
import os
import sys

def Parse(chapter, quarter, sutra, name):
   Url = 'http://www.gitasupersite.iitk.ac.in/brahmasutra_content?language=dv&field_chapter_value=' + str(chapter) + '&field_quarter_value=' + str(quarter) + '&field_nsutra_value=' + str(sutra)
   while(True):
       try:
           html = urllib.urlopen(Url).read()
           break
       except Exception:
           pass
   html = html.replace('\r','')
   soup = BeautifulSoup.BeautifulSoup(html)
   content = soup.findAll('p', {'name' : name})
   san = ''
   try:
      x = content[0].findAll(text = True)
   except Exception:
      print
      print chapter, quarter, sutra, name
      print "-----------"
      print content
      exit(1)
   for i in x:
      tmp = str(i.encode('utf8'))
      tmp += '\n'
      san += tmp
   return san

def get():
   chapters = []
   chapters.append([31, 32, 43, 28])
   chapters.append([37, 45, 53, 22])
   chapters.append([27, 41, 66, 52])
   chapters.append([19, 21, 16, 22])
   for _chapter in xrange(1, 5):
      os.system('mkdir chapter_' + str(_chapter))
      print "chapter :", _chapter
      for quarter in xrange(1, 5):
         os.system('mkdir chapter_' + str(_chapter) + '/quarter_' + str(quarter))
         print "   quarter :", quarter, ", sutra : ",
         for sutra in xrange(chapters[_chapter - 1][quarter - 1] + 1):
            f = open('./chapter_' + str(_chapter) + '/quarter_' + str(quarter) + '/sutra_' + str(sutra) + '.txt', 'w')
            print sutra, 
            if(sutra == 0):
               san = Parse(_chapter, quarter, sutra, 'bs_intro')
            else:
               san = Parse(_chapter, quarter, sutra, 'bs_comm')
            f.write(san)
            f.close()
            sys.stdout.flush()
         print
get()
