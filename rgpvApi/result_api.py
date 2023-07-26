import io
import time
import requests
import pytesseract
import urllib.parse
from bs4 import BeautifulSoup
from PIL import Image, ImageFilter, ImageOps


class result():
    def __init__(self, enrollId, courseId):
        self.enrollId = enrollId
        self.courseId = courseId
        self.cookies = None
        if len(self.enrollId)!=12:
            raise ValueError("Invalid Enrollment Number")
        if self.courseId not in [1, 24, 5, 2, 43, 11, 7, 6, 8, 10, 20, 21, 23, 3, 44, 51, 22, 53, 4, 42, 71]:
            raise ValueError("Invalid CourseId, Check info.courseId")
        self.ReqSession = requests.Session()

    def checkSem(self):
        semData = {1: 8, 24: 8, 5: 6, 2: 8, 43: 8, 11: 10, 7: 4, 6: 6, 8: 6, 10: 8, 20: 6, 21: 10, 23: 10, 3: 8, 44: 4, 51: 4, 22: 4, 53: 6, 4: 4, 42: 8, 71: 4}
        if self.sem>semData[self.courseId]:
            raise ValueError(f"Invalid Semester for {self.courseId}")
        self.prgSel()

    def getMain(self, sem):
        self.sem = sem
        self.checkSem()
        headers = {'Host': 'result.rgpv.ac.in', 'Cache-Control': 'max-age=0', 'Origin': 'http://result.rgpv.ac.in', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Referer': 'http://result.rgpv.ac.in/result/ProgramSelect.aspx', 'Accept-Language': 'en-GB,en;q=0.9'}
        data = {'__EVENTARGUMENT': '', '__LASTFOCUS': '', '__VIEWSTATE': self.VIEWSTATE, '__VIEWSTATEGENERATOR': self.VIEWSTATEGENERATOR, '__EVENTVALIDATION': self.EVENTVALIDATION, '__EVENTTARGET': 'radlstProgram$1', 'radlstProgram': str(self.courseId)}
        response = self.ReqSession.post('http://result.rgpv.ac.in/Result/ProgramSelect.aspx', headers=headers, data=data, allow_redirects=False)
        if self.cookies == None:
            self.cookies = response.headers['Set-Cookie'].split(';')[0]
        self.url = 'http://result.rgpv.ac.in/' + urllib.parse.unquote(BeautifulSoup(response.text, 'html.parser').find('a')['href'])
        self.chkReslt()
        returnInfo = {"enrollId": self.enrollId}
        if self.mainResponse.text.find("Result for this Enrollment No. not Found") != -1 or self.mainResponse.text.find('Enrollment No not Found') != -1:
            return {"error":"Enrollment No not Found"}
        returnInfo['name'] = " ".join(self.soup.find(id='ctl00_ContentPlaceHolder1_lblNameGrading').get_text().split())
        returnInfo['status'] = " ".join(
            self.soup.find(id='ctl00_ContentPlaceHolder1_lblResultNewGrading').get_text().split())
        returnInfo['sgpa'] = " ".join(self.soup.find(id='ctl00_ContentPlaceHolder1_lblSGPA').get_text().split())
        returnInfo['cgpa'] = " ".join(self.soup.find(id='ctl00_ContentPlaceHolder1_lblcgpa').get_text().split())
        returnInfo['subjects'] = []
        table = self.soup.find(id='ctl00_ContentPlaceHolder1_pnlGrading').find_all('tr')[6].find_all('table')
        for x in table:
            element = x.find_all('td')
            subjectInfo = {}
            if element == []: continue
            subjectInfo['subject'] = " ".join(element[0].get_text().split())
            subjectInfo['grade'] = " ".join(element[3].get_text().split())
            returnInfo['subjects'].append(subjectInfo)
        return returnInfo

    def getReval(self, sem):
        self.sem = sem
        self.checkSem()
        headers = {'Host': 'result.rgpv.ac.in', 'Cache-Control': 'max-age=0', 'Origin': 'http://result.rgpv.ac.in', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Referer': 'http://result.rgpv.ac.in/result/ProgramSelect.aspx', 'Accept-Language': 'en-GB,en;q=0.9'}
        data = {'__EVENTARGUMENT': '', '__LASTFOCUS': '', '__VIEWSTATE': self.VIEWSTATE, '__VIEWSTATEGENERATOR': self.VIEWSTATEGENERATOR, '__EVENTVALIDATION': self.EVENTVALIDATION, '__EVENTTARGET': 'radlstRevalProg$1', 'radlstRevalProg': str(self.courseId)}
        response = self.ReqSession.post('http://result.rgpv.ac.in/Result/ProgramSelect.aspx', headers=headers, data=data, allow_redirects=False)
        if self.cookies==None:
            self.cookies = response.headers['Set-Cookie'].split(';')[0]
        self.url = 'http://result.rgpv.ac.in/' + urllib.parse.unquote(BeautifulSoup(response.text, 'html.parser').find('a')['href'])
        self.chkReslt()
        returnInfo = {"enrollId": self.enrollId}
        if self.mainResponse.text.find("Result for this Enrollment No. not Found") != -1 or self.mainResponse.text.find('Enrollment No not Found') != -1:
            return {"error":"Enrollment No not Found"}
        returnInfo['name'] = " ".join(self.soup.find(id='ctl00_ContentPlaceHolder1_lblName').get_text().split())
        returnInfo['Subjects'] = []
        table = self.soup.find(id='ctl00_ContentPlaceHolder1_gvRevalResult').find_all('tr')
        for x in table:
            element = x.find_all('td')
            subjectInfo = {}
            if element == []: continue
            subjectInfo['subjectCode'] = " ".join(element[1].get_text().split())
            subjectInfo['subjectName'] = " ".join(element[2].get_text().split())
            subjectInfo['newGrade'] = " ".join(element[3].get_text().split())
            returnInfo['Subjects'].append(subjectInfo)
        return returnInfo

    def getChlng(self, sem):
        self.sem = sem
        self.checkSem()
        headers = {'Host': 'result.rgpv.ac.in', 'Cache-Control': 'max-age=0', 'Origin': 'http://result.rgpv.ac.in', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Referer': 'http://result.rgpv.ac.in/result/ProgramSelect.aspx', 'Accept-Language': 'en-GB,en;q=0.9'}
        data = {'__EVENTARGUMENT': '', '__LASTFOCUS': '', '__VIEWSTATE': self.VIEWSTATE, '__VIEWSTATEGENERATOR': self.VIEWSTATEGENERATOR, '__EVENTVALIDATION': self.EVENTVALIDATION, '__EVENTTARGET': 'ChallengeRbtnList$1', 'ChallengeRbtnList': str(self.courseId)}
        response = self.ReqSession.post('http://result.rgpv.ac.in/Result/ProgramSelect.aspx', headers=headers, data=data, allow_redirects=False)
        if self.cookies == None:
            self.cookies = response.headers['Set-Cookie'].split(';')[0]
        self.url = 'http://result.rgpv.ac.in/' + urllib.parse.unquote(BeautifulSoup(response.text, 'html.parser').find('a')['href'])
        self.chkReslt()
        returnInfo = {"enrollId": self.enrollId}
        if self.mainResponse.text.find("Result for this Enrollment No. not Found") != -1 or self.mainResponse.text.find('Enrollment No not Found') != -1:
            return {"error":"Enrollment No not Found"}
        returnInfo['name'] = " ".join(self.soup.find(id='ctl00_ContentPlaceHolder1_lblName').get_text().split())
        returnInfo['Subjects'] = []
        table = self.soup.find(id='ctl00_ContentPlaceHolder1_gvRevalResult').find_all('tr')
        for x in table:
            element = x.find_all('td')
            subjectInfo = {}
            if element == []: continue
            subjectInfo['subjectCode'] = " ".join(element[1].get_text().split())
            subjectInfo['subjectName'] = " ".join(element[2].get_text().split())
            subjectInfo['newGrade'] = " ".join(element[3].get_text().split())
            returnInfo['Subjects'].append(subjectInfo)
        return returnInfo

    def prgSel(self):
        response = self.ReqSession.get('http://result.rgpv.ac.in/result/programselect.aspx?id=$%')
        soup = BeautifulSoup(response.text, 'html.parser')
        self.VIEWSTATE = soup.find(id='__VIEWSTATE')['value']
        self.VIEWSTATEGENERATOR = soup.find(id='__VIEWSTATEGENERATOR')['value']
        self.EVENTVALIDATION = soup.find(id='__EVENTVALIDATION')['value']

    def chkReslt(self):
        headers = {'Host': 'result.rgpv.ac.in', 'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Referer': 'http://result.rgpv.ac.in/result/ProgramSelect.aspx', 'Accept-Language': 'en-GB,en;q=0.9', 'Cookie': self.cookies}
        response = self.ReqSession.get(self.url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        link = f"http://result.rgpv.ac.in/Result/{soup.find_all('img')[1]['src']}"
        self.VIEWSTATE = soup.find(id='__VIEWSTATE')['value']
        self.VIEWSTATEGENERATOR = soup.find(id='__VIEWSTATEGENERATOR')['value']
        self.EVENTVALIDATION = soup.find(id='__EVENTVALIDATION')['value']
        headers = {'Host': 'result.rgpv.ac.in', 'Content-Length': '1018', 'Cache-Control': 'max-age=0', 'Origin': 'http://result.rgpv.ac.in', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Referer': self.url, 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-GB,en;q=0.9', 'Cookie': self.cookies, 'Connection': 'keep-alive'}
        data = {'__VIEWSTATE': self.VIEWSTATE, '__VIEWSTATEGENERATOR': self.VIEWSTATEGENERATOR, '__EVENTVALIDATION': self.EVENTVALIDATION, '__EVENTTARGET': '', '__EVENTARGUMENT': '', 'ctl00$ContentPlaceHolder1$txtrollno': self.enrollId, 'ctl00$ContentPlaceHolder1$drpSemester': self.sem, 'ctl00$ContentPlaceHolder1$rbtnlstSType': 'G', 'ctl00$ContentPlaceHolder1$TextBox1': self.captchaSolver(link), 'ctl00$ContentPlaceHolder1$btnviewresult': 'View+Result'}
        time.sleep(5)
        self.mainResponse = self.ReqSession.post(self.url, headers=headers, data=data)
        response = self.mainResponse
        self.soup = BeautifulSoup(response.text, 'html.parser')
        if self.soup.find(id='ctl00_ContentPlaceHolder1_btnviewresult') != None:
            self.chkReslt()

    def captchaSolver(self, link):
        response = self.ReqSession.get(link)
        img = Image.open(io.BytesIO(response.content))
        img = img.convert('L')
        img = ImageOps.invert(img)
        img = img.filter(ImageFilter.SHARPEN)
        text = pytesseract.image_to_string(img)
        text = str(text).replace(' ', '').replace('\n', '').upper()
        if len(text)!=5 and self.courseId!=11:
            self.captchaSolver(link)
        else:
            return text
