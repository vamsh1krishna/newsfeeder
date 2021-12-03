from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.multipart  import MIMEMultipart
from email.mime.text import MIMEText
import datetime

now = datetime.datetime.now()
content = ''

def extract_news(url):
    print('Extracting The wire News stories......')
    cnt = ''
    cnt += ('<font size='+'"5"'+'><strong>The wire Stories:</strong></font>\n'+'<br>'+'-'*50+'<br>')
    response= requests.get(url)
    content =response.content
    soup = BeautifulSoup(content,'html.parser')
    if (home_page := soup.find('div',class_="home-section-featured-highlights")):
        cnt += '<b>Home Page:</b>\n'+'<br>'
        news_title = home_page.find('a')['title']
        news_url = 'https://thewire.in'+home_page.find('a')['href']
        cnt += '<a href='+news_url+'>'+news_title+'</a>'+"\n"+'<br>'
        

    cnt += '<b>Cards</b>\n'+'<br>'
    for i, tag in enumerate(soup.find_all('div', attrs= {'class':'card horizontal card__header--rm-margin row-height'})):
        posttime = tag.find('div',class_='card__posted-on hide-on-small-only tag-inline')
        if posttime.text[3:8] == 'hours' or posttime.text[0:2] == str(now.day-1):
            ms =''
            newstitle = tag.find('a')['title']
            newsurl = 'https://thewire.in'+tag.find('a')['href']
            ms = '<a href='+newsurl+'>'+newstitle+'</a>'+"\n"+'<br>'
            cnt += ms
        else:
            continue
    print(cnt)
    return cnt

cnt = extract_news(('https://thewire.in/'))
content += cnt


content += ('<br>-------<br>')
content += ('<br><br>End of Message')
content += '</body></html>'
# with open("mint.html","w") as file:
#     file.write(content.encode)
print('Composing Email.....')
# print(content)

SERVER = 'smtp.gmail.com' #your smtp server
PORT = 587 # Your port number, for gmail it is 587
FROM = 'vasanram220@gmail.com'
TO = 'vasanram220@gmail.com,vamshi998shivam@gmail.com,pujasinha719@gmail.com,princeraja777@gmail.com,dileepcs07@gmail.com'
PASS = '102102102'

msg = MIMEMultipart()

#msg.add_header('content-Disposition','attachment',filename='empty.txt)
msg['Subject'] = 'Top News Stories from Wire [Automated Email]'  + ''+str(now.day)+'-'+str(now.month)+'-'+str(now.year)
msg['From'] = FROM
msg['To'] = TO
msg.attach(MIMEText(content,'html'))
#fp.close()

#Intialising the server

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(0)
server.ehlo()
server.starttls()

server.login(FROM,PASS)
server.sendmail(FROM, TO.split(','),msg.as_string())

print('Email Sent')

server.quit()