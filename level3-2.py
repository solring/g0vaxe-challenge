import requests
import re
import io
import json

pat = "<tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>"
nextpat = "page=next"

ans = []

def parse(body):
    
    content = body.replace("\n", "").replace(" ", "")
    matches = re.findall(pat, content)
    
    if matches is None: return

    for m in matches[1:]:
        ans.append(
            {
                "town": m[0],    
                "village": m[1],    
                "name": m[2]
            }
        )

def hasNextPage(body):
    return nextpat in body

if __name__ == "__main__":
    
    url = "http://axe-level-1.herokuapp.com/lv3"
    url2 = url+"?page=next"

    fdout = io.open("result2.txt", mode="w", encoding="utf-8")
    #fdout = open("result2.txt","w")


    res = requests.get(url)
    res.encoding = "utf-8"
    clonecookie  = {"PHPSESSID": res.cookies["PHPSESSID"]}
    
    parse(res.text)

    while(hasNextPage(res.text)):
        res = requests.get(url2, cookies=clonecookie)
        res.encoding = "utf-8"
        parse(res.text)
        
    #json.dump(ans, fdout, ensure_ascii=False)
    result = json.dumps(ans, ensure_ascii=False)
    fdout.write(unicode(result))
