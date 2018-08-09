import urllib.request
import re
baseUrl = "https://tabelog.com"
pattern = r'<span class="rdheader-rating__score-val-dtl">(\d.\d*)<\/span>'
repatter = re.compile(pattern)

with urllib.request.urlopen(baseUrl + "/osaka/A2701/A270202/27082281/") as res:
    html = res.read().decode("utf-8")
    point = repatter.findall(html)[0]
    print(point)
