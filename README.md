# RGPV API
RGPV API wrapper, written in Python.

## Installation

Install from sources:
```bash
git clone https://github.com/cro2003/rgpvApi.git
cd rgpvApi
python3 -m pip install -e .
```

## Usage
Example code to get Main Result:
```python
from rgpvApi import result

enrollId = ENROLLMENT_NUMBER
courseId = COURSE_ID
sem = SEMESTER

Res = result(enrollId, courseId)

print(Res.getMain(sem))
```

## Contact 
Chirag
<br>[cro@chirag.software](mailto:cro@chirag.software) 

