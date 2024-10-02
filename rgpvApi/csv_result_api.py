import csv
import json
from rgpvApi import result


def csvresults(input_csv , result_type : str, courseId : int, sem : int):
    """This Function Fetches the selected Examination Result in bulk.


                Args:
                    input_csv (str) : path to the csv file with one column titled "enrolment_id"
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
    results={}
    with open(input_csv, mode='r') as file:
        reader =csv.DictReader(file)
        for row in reader:
            enrolment_id=row.get('enrolment_id')
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
                fetched_result = json.loads(fetched_result)
                results[enrolment_id] = fetched_result
    return json.dumps(results)