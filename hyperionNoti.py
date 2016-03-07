import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import urllib2
import time
import MySQLdb


urlWatch = '' #enter URL to watch for changes

copyRight = '(c) 2014 Hyperion Notification 2.0'
emailFooter = "\n\nDashboard: " + urlWatch + "\n"

emailList = []

pageDataOld = ""
spanCheck = ['<span>foo', '<span>bar', '<span>baz'] #spans to check for changes
extraction = []
oldExtraction = spanCheck
endKey = "qux" #End value
emailListdb = [] #email list



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
		if extraction[i][len(extraction[i]) - 6 : len(extraction[i])] == "norf_": #Criteria for true
		    appendStr += extraction[i][6:10].replace("<", "")+ " True Statement.\n" #Modify to fit email message
		    compCounter += 1
		else:
		    appendStr += extraction[i][6:10].replace("<", "")+ " False Statement.\n" #Modify to fit email message
        if compCounter == 4:
		emailHeader = "All Spans True." #Modify to fit email message
	elif compCounter == 0:
		emailHeader = "All Spans False." #Modify to fit email message
	else:
		emailHeader = appendStr

	emailBody = emailHeader + emailFooter
	sendEmail(emailBody)

    oldExtraction = extraction


def sendEmail(emailBody):
    dbHost = ""
    dbUser = ""
    dbPassword = ""
    dbName = ""
    db = MySQLdb.connect(host=dbHost, user=dbUser, passwd=dbPassword, db=dbName)
    cur = db.cursor()
    cur.execute("SELECT email FROM hyperionemails WHERE subsc = 0")
    emailListdb = cur.fetchall()

    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo

    emailUser = ''
    emailPassword = ''

    smtpserver.login(emailUser,emailPassword)

    to = emailList
    bcc = ''
    frm = emailUser
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
    #Check while weekday from 8am to 8pm
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
