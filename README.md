# RGPV API
RGPV API wrapper, written in Python.

## Installation
Install using Pypi:
```bash
pip install rgpvApi
```

## Usage
Example code to get Main Result:
```python
import rgpvApi

enrollId = ENROLLMENT_NUMBER
courseId = COURSE_ID
sem = SEMESTER

stu_result = rgpvApi.result(enrollId, courseId)

print(stu_result.getMain(sem))
```

## Contact 
Chirag
<br>[cro@chirag.software](mailto:cro@chirag.software) 

