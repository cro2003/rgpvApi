import io
import time
import csv
import json
import aiohttp
import asyncio
import pytesseract
import urllib.parse
from bs4 import BeautifulSoup
from PIL import Image, ImageFilter, ImageOps

class Result:
    def __init__(self, enrollId: str, courseId: int):
        self.enrollId = enrollId
        self.courseId = courseId
        self.cookies = None
        if len(self.enrollId) != 12:
            raise ValueError("Invalid Enrollment Number")
        if self.courseId not in [1, 24, 5, 2, 43, 11, 7, 6, 8, 10, 20, 21, 23, 3, 44, 51, 22, 53, 4, 42, 71]:
            raise ValueError("Invalid CourseId, Check info.courseId")
        self.session = aiohttp.ClientSession()

    async def fetch(self, url, headers, data=None):
        async with self.session.post(url, headers=headers, data=data) as response:
            return await response.text()

    async def getMain(self, sem: int):
        self.sem = sem
        await self.__checkSem()
        headers = {
            'Host': 'result.rgpv.ac.in',
            'Cache-Control': 'max-age=0',
            'Origin': 'http://result.rgpv.ac.in',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Referer': 'http://result.rgpv.ac.in/result/ProgramSelect.aspx',
            'Accept-Language': 'en-GB,en;q=0.9'
        }
        data = {
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.VIEWSTATE,
            '__VIEWSTATEGENERATOR': self.VIEWSTATEGENERATOR,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
            '__EVENTTARGET': 'radlstProgram$1',
            'radlstProgram': str(self.courseId)
        }
        response_text = await self.fetch('http://result.rgpv.ac.in/Result/ProgramSelect.aspx', headers, data)
        self.cookies = response_text.headers['Set-Cookie'].split(';')[0] if self.cookies is None else self.cookies
        self.url = 'http://result.rgpv.ac.in/' + urllib.parse.unquote(BeautifulSoup(response_text, 'html.parser').find('a')['href'])
        await self.__checkResult()
        return await self.__parseMainResult()

    async def __checkSem(self):
        semData = {1: 8, 24: 8, 5: 6, 2: 8, 43: 8, 11: 10, 7: 4, 6: 6, 8: 6, 10: 8, 20: 6, 21: 10, 23: 10, 3: 8, 44: 4, 51: 4, 22: 4, 53: 6, 4: 4, 42: 8, 71: 4}
        if self.sem > semData[self.courseId]:
            raise ValueError(f"Invalid Semester for {self.courseId}")
        await self.__programSelect()

    async def __programSelect(self):
        async with self.session.get('http://result.rgpv.ac.in/result/programselect.aspx?id=$%') as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            self.VIEWSTATE = soup.find(id='__VIEWSTATE')['value']
            self.VIEWSTATEGENERATOR = soup.find(id='__VIEWSTATEGENERATOR')['value']
            self.EVENTVALIDATION = soup.find(id='__EVENTVALIDATION')['value']

    async def __checkResult(self):
        headers = {
            'Host': 'result.rgpv.ac.in',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'Referer': 'http://result.rgpv.ac.in/result/ProgramSelect.aspx',
            'Accept-Language': 'en-GB,en;q=0.9',
            'Cookie': self.cookies
        }
        response_text = await self.fetch(self.url, headers)
        soup = BeautifulSoup(response_text, 'html.parser')
        link = f"http://result.rgpv.ac.in/Result/{soup.find_all('img')[1]['src']}"
        self.VIEWSTATE = soup.find(id='__VIEWSTATE')['value']
        self.VIEWSTATEGENERATOR = soup.find(id='__VIEWSTATEGENERATOR')['value']
        self.EVENTVALIDATION = soup.find(id='__EVENTVALIDATION')['value']
        captcha_text = await self.__captchaSolver(link)
        data = {
            '__VIEWSTATE': self.VIEWSTATE,
            '__VIEWSTATEGENERATOR': self.VIEWSTATEGENERATOR,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            'ctl00$ContentPlaceHolder1$txtrollno': self.enrollId,
            'ctl00$ContentPlaceHolder1$drpSemester': self.sem,
            'ctl00$ContentPlaceHolder1$rbtnlstSType': 'G',
            'ctl00$ContentPlaceHolder1$TextBox1': captcha_text,
            'ctl00$ContentPlaceHolder1$btnviewresult': 'View+Result'
        }
        await asyncio.sleep(5)  # Simulate delay
        self.mainResponse = await self.fetch(self.url, headers, data)

    async def __captchaSolver(self, link):
        async with self.session.get(link) as response:
            img = Image.open(io.BytesIO(await response.read()))
            img = img.convert('L')
            img = ImageOps.invert(img)
            img = img.filter(ImageFilter.SHARPEN)
            text = pytesseract.image_to_string(img).strip().replace(' ', '').replace('\n', '').upper()
            if len(text) != 5 and self.courseId != 11:
                return await self.__captchaSolver(link)
            return text

    async def __parseMainResult(self):
        # Parsing logic for main result
        returnInfo = {"enrollId": self.enrollId}
        soup = BeautifulSoup(self.mainResponse, 'html.parser')
        if "Result for this Enrollment No. not Found" in self.mainResponse or 'Enrollment No not Found' in self.mainResponse:
            return json.dumps({"error": "Enrollment No not Found"})
        returnInfo['name'] = " ".join(soup.find(id='ctl00_ContentPlaceHolder1_lblNameGrading').get_text().split())
        returnInfo['status'] = " ".join(soup.find(id='ctl00_ContentPlaceHolder1_lblResultNewGrading').get_text().split())
        returnInfo['sgpa'] = " ".join(soup.find(id='ctl00_ContentPlaceHolder1_lblSGPA').get_text().split())
        returnInfo['cgpa'] = " ".join(soup.find(id='ctl00_ContentPlaceHolder1_lblcgpa').get_text().split())
        returnInfo['subjects'] = []
        table = soup.find(id='ctl00_ContentPlaceHolder1_pnlGrading').find_all('tr')[6].find_all('table')
        for x in table:
            element = x.find_all('td')
            if element:
                subjectInfo = {
                    'subject': " ".join(element[0].get_text().split()),
                    'grade': " ".join(element[3].get_text().split())
                }
                returnInfo['subjects'].append(subjectInfo)
        return json.dumps(returnInfo)

    async def close(self):
        await self.session.close()

async def csvresults(input_csv, result_type: str, courseId: int, sem: int):
    results = {}
    async with aiofiles.open(input_csv, mode='r') as file:
        reader = csv.DictReader(await file.readlines())
        for row in reader:
            enrollment_id = row.get('enrolment_id')
            if enrollment_id:
                stu_result = Result(enrollment_id, courseId)
                if result_type == 'main':
                    fetched_result = await stu_result.getMain(sem)
                # Handle other result types similarly...
                fetched_result = json.loads(fetched_result)
                results[enrollment_id] = fetched_result
    return json.dumps(results)

async def main():
    # Example call to csvresults
    results = await csvresults('input.csv', 'main', 1, 1)
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
