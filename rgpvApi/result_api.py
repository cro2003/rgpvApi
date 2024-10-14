import io
import json
import aiohttp
import asyncio
import pandas as pd
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
        self.base_url = 'http://result.rgpv.ac.in'
        self.session = None

    async def __checkSem(self):
        semData = {1: 8, 24: 8, 5: 6, 2: 8, 43: 8, 11: 10, 7: 4, 6: 6, 8: 6, 10: 8, 20: 6, 21: 10, 23: 10,
                    3: 8, 44: 4, 51: 4, 22: 4, 53: 6, 4: 4, 42: 8, 71: 4}
        if self.sem > semData[self.courseId]:
            raise ValueError(f"Invalid Semester for {self.courseId}")
        await self.__prgSel()

    async def getMain(self, sem: int):
        self.sem = sem
        await self.__checkSem()
        async with self.session.post(f'{self.base_url}/Result/ProgramSelect.aspx',
                                      headers=self.__get_headers(),
                                      data=self.__get_main_data()) as response:
            await self.__handle_response(response)
            return await self.__parse_main_result()

    async def getReval(self, sem: int):
        self.sem = sem
        await self.__checkSem()
        async with self.session.post(f'{self.base_url}/Result/ProgramSelect.aspx',
                                      headers=self.__get_headers(),
                                      data=self.__get_reval_data()) as response:
            await self.__handle_response(response)
            return await self.__parse_reval_result()

    async def getChlng(self, sem: int):
        self.sem = sem
        await self.__checkSem()
        async with self.session.post(f'{self.base_url}/Result/ProgramSelect.aspx',
                                      headers=self.__get_headers(),
                                      data=self.__get_chlng_data()) as response:
            await self.__handle_response(response)
            return await self.__parse_chlng_result()

    async def __prgSel(self):
        async with self.session.get(f'{self.base_url}/result/programselect.aspx?id=$%') as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            self.VIEWSTATE = soup.find(id='__VIEWSTATE')['value']
            self.VIEWSTATEGENERATOR = soup.find(id='__VIEWSTATEGENERATOR')['value']
            self.EVENTVALIDATION = soup.find(id='__EVENTVALIDATION')['value']

    async def __handle_response(self, response):
        if response.status != 200:
            raise Exception("Failed to fetch data")

        self.soup = BeautifulSoup(await response.text(), 'html.parser')
        if 'Enrollment No not Found' in self.soup.text:
            raise ValueError("Enrollment No not Found")

    async def __parse_main_result(self):
        returnInfo = {
            "enrollId": self.enrollId,
            "name": " ".join(self.soup.find(id='ctl00_ContentPlaceHolder1_lblNameGrading').get_text().split()),
            "status": " ".join(self.soup.find(id='ctl00_ContentPlaceHolder1_lblResultNewGrading').get_text().split()),
            "sgpa": " ".join(self.soup.find(id='ctl00_ContentPlaceHolder1_lblSGPA').get_text().split()),
            "cgpa": " ".join(self.soup.find(id='ctl00_ContentPlaceHolder1_lblcgpa').get_text().split()),
            "subjects": []
        }
        table = self.soup.find(id='ctl00_ContentPlaceHolder1_pnlGrading').find_all('tr')[6].find_all('table')
        for x in table:
            element = x.find_all('td')
            if element:
                subjectInfo = {
                    'subject': " ".join(element[0].get_text().split()),
                    'grade': " ".join(element[3].get_text().split())
                }
                returnInfo['subjects'].append(subjectInfo)
        return json.dumps(returnInfo)

    async def __parse_reval_result(self):
        # Similar to __parse_main_result but for revaluation
        returnInfo = {
            "enrollId": self.enrollId,
            "name": " ".join(self.soup.find(id='ctl00_ContentPlaceHolder1_lblName').get_text().split()),
            "Subjects": []
        }
        table = self.soup.find(id='ctl00_ContentPlaceHolder1_gvRevalResult').find_all('tr')
        for x in table:
            element = x.find_all('td')
            if element:
                subjectInfo = {
                    'subjectCode': " ".join(element[1].get_text().split()),
                    'subjectName': " ".join(element[2].get_text().split()),
                    'status': " ".join(element[4].get_text().split()),
                    'newGrade': " ".join(element[3].get_text().split())
                }
                returnInfo['Subjects'].append(subjectInfo)
        return json.dumps(returnInfo)

    async def __parse_chlng_result(self):
        # Similar to __parse_reval_result but for challenge
        return await self.__parse_reval_result()

    def __get_headers(self):
        return {
            'Host': 'result.rgpv.ac.in',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://result.rgpv.ac.in/result/ProgramSelect.aspx'
        }

    def __get_main_data(self):
        return {
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.VIEWSTATE,
            '__VIEWSTATEGENERATOR': self.VIEWSTATEGENERATOR,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
            '__EVENTTARGET': 'radlstProgram$1',
            'radlstProgram': str(self.courseId)
        }

    def __get_reval_data(self):
        return {
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.VIEWSTATE,
            '__VIEWSTATEGENERATOR': self.VIEWSTATEGENERATOR,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
            '__EVENTTARGET': 'radlstRevalProg$1',
            'radlstRevalProg': str(self.courseId)
        }

    def __get_chlng_data(self):
        return {
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': self.VIEWSTATE,
            '__VIEWSTATEGENERATOR': self.VIEWSTATEGENERATOR,
            '__EVENTVALIDATION': self.EVENTVALIDATION,
            '__EVENTTARGET': 'ChallengeRbtnList$1',
            'ChallengeRbtnList': str(self.courseId)
        }

async def fetch_result(row, result_type: str, courseId: int, sem: int):
    enrolment_id = row['enrolment_id']
    if enrolment_id:
        stu_result = Result(enrolment_id, courseId)
        async with aiohttp.ClientSession() as session:
            stu_result.session = session
            if result_type == 'main':
                fetched_result = await stu_result.getMain(sem)
            elif result_type == 'revaluation':
                fetched_result = await stu_result.getReval(sem)
            elif result_type == 'challenge':
                fetched_result = await stu_result.getChlng(sem)
            else:
                raise ValueError("Invalid result_type. Choose from 'main', 'revaluation', or 'challenge'.")
            return enrolment_id, json.loads(fetched_result)
    return None

async def bulkresults(input_path, result_type: str, courseId: int, sem: int):
    results = {}

    if input_path.endswith("csv"):
        reader = pd.read_csv(input_path)
    elif input_path.endswith("xlsx"):
        reader = pd.read_excel(input_path)
    else:
        raise ValueError("Unsupported file format. Please provide a .csv or .xlsx file.")

    tasks = []
    for index, row in reader.iterrows():
        tasks.append(fetch_result(row, result_type, courseId, sem))

    results_data = await asyncio.gather(*tasks)

    for result in results_data:
        if result:
            results[result[0]] = result[1]

    return results
