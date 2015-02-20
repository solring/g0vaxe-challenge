import requests
import re
import io

pat = "<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>"
out_pat = u"{\"town\":\"%s\",\"village\":\"%s\",\"name\":\"%s\"}"
nextpat = "page=next"

def parse(body, fd):
    
    content = body.replace("\n", "").replace(" ", "")
    matches = re.finditer(pat, content)
    
    if matches is None: return

    header = 1
    for m in matches:
        if m != None:
            if header==1: 
                header = 0
                fd.write(out_pat % ( m.group(1), m.group(2), m.group(3)) )
            else: 
                fd.write(u","+out_pat % ( m.group(1), m.group(2), m.group(3)) )

def hasNextPage(body):
    return nextpat in body

if __name__ == "__main__":
    
    url = "http://axe-level-1.herokuapp.com/lv3"
    url2 = url+"?page=next"

    fdout = io.open("result.txt", mode="w", encoding="utf-8")

    fdout.write(u"[")

    res = requests.get(url)
    res.encoding = "utf-8"
    mycookie = res.cookies
    clonecookie  = {"PHPSESSID": res.cookies["PHPSESSID"]}
    #for k, v in res.cookies.iteritems():
    #    print "%s:%s" %(k, v)
    
    parse(res.text, fdout)

    while(hasNextPage(res.text)):
        fdout.write(u",")
        res = requests.get(url2, cookies=clonecookie)
        res.encoding = "utf-8"
        mycookie = res.cookies
        parse(res.text, fdout)
        
    fdout.write(u"[")

