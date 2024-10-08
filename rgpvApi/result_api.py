import io
import time
import csv
import json
import requests
import pytesseract
import urllib.parse
from bs4 import BeautifulSoup
from PIL import Image, ImageFilter, ImageOps
import pandas as pd
from concurrent.futures import *
from datetime import datetime, timedelta


class result():
    """
        This Class Contains Three Important Functions for fetching different Examination Results.

        Args:
            enrollId (string): 12 Character Enrollment Number of Student
            courseId (int): Course Id of the Course in which Student admitted to, which can be fetched by `rgpvApi.info_api.info.courseId()`
    """
    def __init__(self, enrollId: str, courseId: int):
        self.enrollId = enrollId
        self.courseId = courseId
        self.cookies = None
        if len(self.enrollId)!=12:
            raise ValueError("Invalid Enrollment Number")
        if self.courseId not in [1, 24, 5, 2, 43, 11, 7, 6, 8, 10, 20, 21, 23, 3, 44, 51, 22, 53, 4, 42, 71]:
            raise ValueError("Invalid CourseId, Check info.courseId")
        self.ReqSession = requests.Session()

    def __checkSem(self):
        semData = {1: 8, 24: 8, 5: 6, 2: 8, 43: 8, 11: 10, 7: 4, 6: 6, 8: 6, 10: 8, 20: 6, 21: 10, 23: 10, 3: 8, 44: 4, 51: 4, 22: 4, 53: 6, 4: 4, 42: 8, 71: 4}
        if self.sem>semData[self.courseId]:
            raise ValueError(f"Invalid Semester for {self.courseId}")
        self.__prgSel()

    def getMain(self, sem: int):
        """This Function Fetches the Main Semester Examination Result.

        :Args:
            sem (int): Semester for which Examination Result needed

        :Returns:
            json: Returns the Examination Result in following format
                  {
                    "enrollId": ENROLLMENT_NUMBER,
                    "name": NAME_OF_STUDENT,
                    "status": STATUS_OF_RESULT_(PASS/FAIL/PASS_WITH_GRACE),
                    "sgpa": SGPA,
                    "cgpa": CGPA,
                    "resType": RESULT_TYPE(REGULAR/EX),
                    "subjects": [{
                        "subject": "CS304- [T]",
                        "grade": "B"
                    }, {
                        "subject": "CS304- [P]",
                        "grade": "B+"
                    }]
                  }
        """
        self.sem = sem
        self.__checkSem()
        headers = {'Host': 'result.rgpv.ac.in', 'Cache-Control': 'max-age=0', 'Origin': 'http://result.rgpv.ac.in', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Referer': 'http://result.rgpv.ac.in/result/ProgramSelect.aspx', 'Accept-Language': 'en-GB,en;q=0.9'}
        data = {'__EVENTARGUMENT': '', '__LASTFOCUS': '', '__VIEWSTATE': self.VIEWSTATE, '__VIEWSTATEGENERATOR': self.VIEWSTATEGENERATOR, '__EVENTVALIDATION': self.EVENTVALIDATION, '__EVENTTARGET': 'radlstProgram$1', 'radlstProgram': str(self.courseId)}
        response = self.ReqSession.post('http://result.rgpv.ac.in/Result/ProgramSelect.aspx', headers=headers, data=data, allow_redirects=False)
        if self.cookies == None:
            self.cookies = response.headers['Set-Cookie'].split(';')[0]
        self.url = 'http://result.rgpv.ac.in/' + urllib.parse.unquote(BeautifulSoup(response.text, 'html.parser').find('a')['href'])
        self.__chkReslt()
        returnInfo = {"enrollId": self.enrollId}
        if self.mainResponse.text.find("Result for this Enrollment No. not Found") != -1 or self.mainResponse.text.find('Enrollment No not Found') != -1:
            return json.dumps({"error":"Enrollment No not Found"})
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
        return json.dumps(returnInfo)

    def getReval(self, sem: int):
        """This Function Fetches the Revaluation Examination Result.


            Args:
                sem (int): Semester for which Examination Result needed

            :Returns:
                json: Returns the Examination Result in following format
                      {
                            "enrollId": ENROLLMENT_NUMBER,
                            "name": NAME_OF_STUDENT,
                            "subjects": [{
                                "subjectCode": SUBJECT_CODE,
                                "subjectName": SUBJECT_NAME,
                                "status": PASSING_STATUS_(NO_CHANGE/CHANGE),
                                "newGrade": NEW_GRADE_(IF_CHANGE)
                            }, {
                                "subjectCode": SUBJECT_CODE,
                                "subjectName": SUBJECT_NAME,
                                "status": PASSING_STATUS_(NO_CHANGE/CHANGE),
                                "newGrade": NEW_GRADE_(IF_CHANGE)
                            }]
                      }
        """
        self.sem = sem
        self.__checkSem()
        headers = {'Host': 'result.rgpv.ac.in', 'Cache-Control': 'max-age=0', 'Origin': 'http://result.rgpv.ac.in', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Referer': 'http://result.rgpv.ac.in/result/ProgramSelect.aspx', 'Accept-Language': 'en-GB,en;q=0.9'}
        data = {'__EVENTARGUMENT': '', '__LASTFOCUS': '', '__VIEWSTATE': self.VIEWSTATE, '__VIEWSTATEGENERATOR': self.VIEWSTATEGENERATOR, '__EVENTVALIDATION': self.EVENTVALIDATION, '__EVENTTARGET': 'radlstRevalProg$1', 'radlstRevalProg': str(self.courseId)}
        response = self.ReqSession.post('http://result.rgpv.ac.in/Result/ProgramSelect.aspx', headers=headers, data=data, allow_redirects=False)
        if self.cookies==None:
            self.cookies = response.headers['Set-Cookie'].split(';')[0]
        self.url = 'http://result.rgpv.ac.in/' + urllib.parse.unquote(BeautifulSoup(response.text, 'html.parser').find('a')['href'])
        self.__chkReslt()
        returnInfo = {"enrollId": self.enrollId}
        if self.mainResponse.text.find("Result for this Enrollment No. not Found") != -1 or self.mainResponse.text.find('Enrollment No not Found') != -1:
            return json.dumps({"error":"Enrollment No not Found"})
        returnInfo['name'] = " ".join(self.soup.find(id='ctl00_ContentPlaceHolder1_lblName').get_text().split())
        returnInfo['Subjects'] = []
        table = self.soup.find(id='ctl00_ContentPlaceHolder1_gvRevalResult').find_all('tr')
        for x in table:
            element = x.find_all('td')
            subjectInfo = {}
            if element == []: continue
            subjectInfo['subjectCode'] = " ".join(element[1].get_text().split())
            subjectInfo['subjectName'] = " ".join(element[2].get_text().split())
            subjectInfo['status'] = " ".join(element[4].get_text().split())
            subjectInfo['newGrade'] = " ".join(element[3].get_text().split())
            returnInfo['Subjects'].append(subjectInfo)
        return json.dumps(returnInfo)

    def getChlng(self, sem: int):
        """This Function Fetches the Challenge Examination Result.


            Args:
                sem (int): Semester for which Examination Result needed

            :Returns:
                json: Returns the Examination Result in following format
                      {
                            "enrollId": ENROLLMENT_NUMBER,
                            "name": NAME_OF_STUDENT,
                            "subjects": [{
                                "subjectCode": SUBJECT_CODE,
                                "subjectName": SUBJECT_NAME,
                                "status": PASSING_STATUS_(NO_CHANGE/CHANGE),
                                "newGrade": NEW_GRADE_(IF_CHANGE)
                            }, {
                                "subjectCode": SUBJECT_CODE,
                                "subjectName": SUBJECT_NAME,
                                "status": PASSING_STATUS_(NO_CHANGE/CHANGE),
                                "newGrade": NEW_GRADE_(IF_CHANGE)
                            }]
                      }
        """
        self.sem = sem
        self.__checkSem()
        headers = {'Host': 'result.rgpv.ac.in', 'Cache-Control': 'max-age=0', 'Origin': 'http://result.rgpv.ac.in', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Referer': 'http://result.rgpv.ac.in/result/ProgramSelect.aspx', 'Accept-Language': 'en-GB,en;q=0.9'}
        data = {'__EVENTARGUMENT': '', '__LASTFOCUS': '', '__VIEWSTATE': self.VIEWSTATE, '__VIEWSTATEGENERATOR': self.VIEWSTATEGENERATOR, '__EVENTVALIDATION': self.EVENTVALIDATION, '__EVENTTARGET': 'ChallengeRbtnList$1', 'ChallengeRbtnList': str(self.courseId)}
        response = self.ReqSession.post('http://result.rgpv.ac.in/Result/ProgramSelect.aspx', headers=headers, data=data, allow_redirects=False)
        if self.cookies == None:
            self.cookies = response.headers['Set-Cookie'].split(';')[0]
        self.url = 'http://result.rgpv.ac.in/' + urllib.parse.unquote(BeautifulSoup(response.text, 'html.parser').find('a')['href'])
        self.__chkReslt()
        returnInfo = {"enrollId": self.enrollId}
        if self.mainResponse.text.find("Result for this Enrollment No. not Found") != -1 or self.mainResponse.text.find('Enrollment No not Found') != -1:
            return json.dumps({"error":"Enrollment No not Found"})
        returnInfo['name'] = " ".join(self.soup.find(id='ctl00_ContentPlaceHolder1_lblName').get_text().split())
        returnInfo['Subjects'] = []
        table = self.soup.find(id='ctl00_ContentPlaceHolder1_gvRevalResult').find_all('tr')
        for x in table:
            element = x.find_all('td')
            subjectInfo = {}
            if element == []: continue
            subjectInfo['subjectCode'] = " ".join(element[1].get_text().split())
            subjectInfo['subjectName'] = " ".join(element[2].get_text().split())
            subjectInfo['status'] = " ".join(element[4].get_text().split())
            subjectInfo['newGrade'] = " ".join(element[3].get_text().split())
            returnInfo['Subjects'].append(subjectInfo)
        return json.dumps(returnInfo)

    def __prgSel(self):
        response = self.ReqSession.get('http://result.rgpv.ac.in/result/programselect.aspx?id=$%')
        soup = BeautifulSoup(response.text, 'html.parser')
        self.VIEWSTATE = soup.find(id='__VIEWSTATE')['value']
        self.VIEWSTATEGENERATOR = soup.find(id='__VIEWSTATEGENERATOR')['value']
        self.EVENTVALIDATION = soup.find(id='__EVENTVALIDATION')['value']

    def __chkReslt(self):
        headers = {'Host': 'result.rgpv.ac.in', 'Cache-Control': 'max-age=0', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Referer': 'http://result.rgpv.ac.in/result/ProgramSelect.aspx', 'Accept-Language': 'en-GB,en;q=0.9', 'Cookie': self.cookies}
        response = self.ReqSession.get(self.url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        link = f"http://result.rgpv.ac.in/Result/{soup.find_all('img')[1]['src']}"
        self.VIEWSTATE = soup.find(id='__VIEWSTATE')['value']
        self.VIEWSTATEGENERATOR = soup.find(id='__VIEWSTATEGENERATOR')['value']
        self.EVENTVALIDATION = soup.find(id='__EVENTVALIDATION')['value']
        headers = {'Host': 'result.rgpv.ac.in', 'Content-Length': '1018', 'Cache-Control': 'max-age=0', 'Origin': 'http://result.rgpv.ac.in', 'DNT': '1', 'Upgrade-Insecure-Requests': '1', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Referer': self.url, 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-GB,en;q=0.9', 'Cookie': self.cookies, 'Connection': 'keep-alive'}
        data = {'__VIEWSTATE': self.VIEWSTATE, '__VIEWSTATEGENERATOR': self.VIEWSTATEGENERATOR, '__EVENTVALIDATION': self.EVENTVALIDATION, '__EVENTTARGET': '', '__EVENTARGUMENT': '', 'ctl00$ContentPlaceHolder1$txtrollno': self.enrollId, 'ctl00$ContentPlaceHolder1$drpSemester': self.sem, 'ctl00$ContentPlaceHolder1$rbtnlstSType': 'G', 'ctl00$ContentPlaceHolder1$TextBox1': self.__captchaSolver(link), 'ctl00$ContentPlaceHolder1$btnviewresult': 'View+Result'}
        time.sleep(5)
        self.mainResponse = self.ReqSession.post(self.url, headers=headers, data=data)
        response = self.mainResponse
        self.soup = BeautifulSoup(response.text, 'html.parser')
        if self.soup.find(id='ctl00_ContentPlaceHolder1_btnviewresult') != None:
            self.__chkReslt()

    def __captchaSolver(self, link):
        response = self.ReqSession.get(link)
        img = Image.open(io.BytesIO(response.content))
        img = img.convert('L')
        img = ImageOps.invert(img)
        img = img.filter(ImageFilter.SHARPEN)
        text = pytesseract.image_to_string(img)
        text = str(text).strip().replace(' ', '').replace('\n', '').upper()
        if len(text)!=5 and self.courseId!=11:
            self.__captchaSolver(link)
        else:
            return text



def get_notifications(_from=None, _to=None):
    """
    Fetch notifications from RGPV based on specified date filters.

    Parameters:
    _from (str): The start date in 'dd-mm-yyyy' format. Fetch notifications from this date onward.
    _to (str): The end date in 'dd-mm-yyyy' format. Fetch notifications between this and the _from date.

    Returns:
    str: JSON formatted string of notifications, with date formatted as 'dd/mm/yy'.
    If no dates are provided, returns notifications from the last 30 days.

        {
            'date': '2023-08-05T00:00:00.000',
            'title': 'Advertisement for Guest Faculty - School of Applied Management '
                '(MBA)'
        },
        {
            'date': '2023-08-05T00:00:00.000',
            'title': 'Urgent notice about sports grants 2021-2022'
        },
        {
            'date': '2023-02-05T00:00:00.000',
            'title': 'Notification regarding Cancellation of Registration and Extension '
                'Re-Registration'
        }
    """
    # Read data from the specified URL
    data = pd.read_html("https://www.rgpv.ac.in/Uni/ImpNoticeArchive.aspx")[1][[1, 2]]
    
    # Rename columns to "date" and "title"
    data.columns = ['date', 'title']
    
    # Convert the date column to datetime, coercing errors to NaT
    data['date'] = pd.to_datetime(data['date'], errors='coerce', format='%d/%m/%Y')  # Adjusting for dd/mm/yyyy format

    # Initialize an empty list for parsed dates
    dates = []

    # Process _from and _to if provided
    if _from and _to:
        for date in [_from, _to]:
            # Convert to datetime, coercing errors to NaT
            parsed_date = pd.to_datetime(date, errors='coerce', format='%d-%m-%Y')  # Adjust format if needed
            dates.append(parsed_date)

        # Filter the DataFrame between the specified dates
        filtered_data = data[(data['date'] >= dates[0]) & (data['date'] <= dates[1])]
        
    elif _from:  # If only _from is given
        parsed_from_date = pd.to_datetime(_from, errors='coerce', format='%d-%m-%Y')
        filtered_data = data[data['date'] >= parsed_from_date]
    
    else:  # If neither _from nor _to is provided, get the last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        filtered_data = data[data['date'] >= thirty_days_ago]
    
    # Format the date in 'dd/mm/yy' for JSON output using .loc to avoid SettingWithCopyWarning
    filtered_data.loc[:, 'date'] = filtered_data['date'].dt.strftime('%d/%m/%y')

    # Convert the filtered DataFrame to JSON format
    result_json = filtered_data.to_json(orient='records', date_format='iso')
    return result_json




def bulkresults(input_path , result_type : str, courseId : int, sem : int):
    """This Function Fetches the selected Examination Result in bulk.


                Args:
                    input_path (str) : path to the csv file or excel file with one column titled "enrolment_id"
                    result_type (str) : "main" or "revaluation" or "challenge"
                    sem (int): Semester for which Examination Result needed

                :Returns:
                    json: Returns the Examination Result in following format

                    {"enrollId":
                          {
                                (if challenge say)
                                "enrollId": ENROLLMENT_NUMBER,
                                "name": NAME_OF_STUDENT,
                                "subjects": [{
                                    "subjectCode": SUBJECT_CODE,
                                    "subjectName": SUBJECT_NAME,
                                    "status": PASSING_STATUS_(NO_CHANGE/CHANGE),
                                    "newGrade": NEW_GRADE_(IF_CHANGE)
                                }, {
                                    "subjectCode": SUBJECT_CODE,
                                    "subjectName": SUBJECT_NAME,
                                    "status": PASSING_STATUS_(NO_CHANGE/CHANGE),
                                    "newGrade": NEW_GRADE_(IF_CHANGE)
                                }]
                          },
                    "enrollId":
                          {
                                (if main say)
                                "enrollId": ENROLLMENT_NUMBER,
                                "name": NAME_OF_STUDENT,
                                "status": STATUS_OF_RESULT_(PASS/FAIL/PASS_WITH_GRACE),
                                "sgpa": SGPA,
                                "cgpa": CGPA,
                                "resType": RESULT_TYPE(REGULAR/EX),
                                "subjects": [{
                                    "subject": "CS304- [T]",
                                    "grade": "B"
                                }, {
                                    "subject": "CS304- [P]",
                                    "grade": "B+"
                                }]
                          }
                    }
            """
    results = {}

    if input_path.endswith("csv"):
        reader = pd.read_csv(input_path)
    elif input_path.endswith("xlsx"):
        reader = pd.read_excel(input_path)
    else:
        raise ValueError("Invalid Input file type.")

    def fetch_result(row):
        enrolment_id = row['enrolment_id']
        if enrolment_id:
            stu_result = result(enrolment_id, courseId)
            if result_type == 'main':
                fetched_result = stu_result.getMain(sem)
            elif result_type == 'revaluation':
                fetched_result = stu_result.getReval(sem)
            elif result_type == 'challenge':
                fetched_result = stu_result.getChlng(sem)
            else:
                raise ValueError("Invalid result_type. Choose from 'main', 'revaluation', or 'challenge'.")
            return enrolment_id, json.loads(fetched_result)
        return None

    with ThreadPoolExecutor(max_workers=2) as executor:
        future_to_enrolment = {executor.submit(fetch_result, row): row for _, row in reader.iterrows()}
        
        for future in as_completed(future_to_enrolment):
            _result = future.result()
            if _result:
                enrolment_id, fetched_result = _result
                results[enrolment_id] = fetched_result

    return json.dumps(results)
