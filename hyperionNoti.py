import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import urllib2
import time
import MySQLdb


urlWatch_ = 'http://eahq-portalapps.rws.ad.ea.com/gadgetserver2/apofinance/test.html'
urlWatch = 'http://10.50.133.219/Buildplan/ActivityLogView.aspx'

copyRight = '(c) 2014 Hyperion Notification 2.0'
emailFooter = "\n\nDashboard: " + urlWatch + "\n"

emailList = ['amali@ea.com', 'steng@ea.com', 'mgallardo@ea.com', 'bbabakan@ea.com', 'akao@ea.com', 'rzhong@ea.com', 'cpeters@ea.com', 'vle@ea.com', 'ccarbonelli@ea.com', 'lentereso@ea.com', 'rajohn@ea.com', 'annale@ea.com', 'jtsao@ea.com', 'mwerbinski@contractor.ea.com']

pageDataOld = ""
spanCheck = ['<span>FPA', '<span>HPP', '<span>VAL', '<span>GAAP']
extraction = []
oldExtraction = spanCheck
endKey = "MainContent_Gladius_"
emailListdb = []



def urlChangeChecker(url, emailFooter):
    global pageDataOld, extraction, oldExtraction
    appendStr = ""
    try:
    	response = urllib2.urlopen(url)
    	html = response.read()
    except Exception:
	pass
    pageData = ""

    compCounter = 0

    pageData = str(html)
    pageData = pageData.replace(" ","") #remove whitespace

    extraction = []

    for i in range(len(spanCheck)):
	spanPos = pageData.find(spanCheck[i])
	endPos = pageData.find(endKey, spanPos) + len(endKey) + 6
	extraction.append(pageData[spanPos : endPos])


    if (extraction != oldExtraction) & (oldExtraction != spanCheck):
	for i in range(len(extraction)):
		if extraction[i][len(extraction[i]) - 6 : len(extraction[i])] == "first_":
		    appendStr += extraction[i][6:10].replace("<", "")+ " cube is up.\n"
		    compCounter += 1
		else:
		    appendStr += extraction[i][6:10].replace("<", "")+ " cube is down.\n"
        if compCounter == 4:
		emailHeader = "All servers up!\nGet back to it."
	elif compCounter == 0:
		emailHeader = "All servers down :(\nTime to go home."
	else:
		emailHeader = appendStr
	
	emailBody = emailHeader + emailFooter
	sendEmail(emailBody)
	
    oldExtraction = extraction
	
 
def sendEmail(emailBody):
    db = MySQLdb.connect(host="localhost", user="root", passwd="raspberry", db="myDatabase")
    cur = db.cursor()
    cur.execute("SELECT email FROM hyperionemails WHERE subsc = 0")
    emailListdb = cur.fetchall()
    
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    
    usr = 'notificationserv@gmail.com'
    password = 'notificationservice'
    
    smtpserver.login(usr,password)
    
    to = 'notificationserv@gmail.com'
    bcc = emailList
    frm = 'notificationserv@gmail.com'
    msg = MIMEText(emailBody)
    
    msg['From'] = frm
    msg['To'] = to
    msg['Bcc'] = ", ".join(bcc)
    msg['Subject'] = 'Hyperion Server Update'  

    #msg.attach(MIMEText(html, 'html')
    
    smtpserver.sendmail(msg['From'], msg['To'].split(",") + msg['Bcc'].split(","), msg.as_string())
    print("Email sent:\n" + emailBody)
    smtpserver.close()
    
    db.close()


while True:
    currTime = "Time: " + time.strftime("%c")
    currDay = time.strftime("%a")
    currHour = int(time.strftime("%H"))
    while (not currDay == "Sat") & (not currDay == "Sun") & (8 < currHour < 20):
	    currTime = "Time: " + time.strftime("%c")
    	    currDay = time.strftime("%a")
    	    currHour = int(time.strftime("%H"))
	    try:
	    	urlChangeChecker(urlWatch, emailFooter + currTime + '\n\n' + copyRight)
	    	print(currTime)
    	    	time.sleep(60)
	    except Exception:
		pass
