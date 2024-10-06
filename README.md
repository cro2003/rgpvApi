# RGPV API
RGPV API wrapper, written in Python.

## Installation

### Install Using Pypi

You can install the package directly from Pypi:

```bash
pip install rgpvApi
```

### Local Setup and Installation Guide

Follow these steps to set up the project on your local machine.

#### 1. Clone the Repository

Start by cloning the repository from GitHub. Open your terminal and run:

```bash
git clone https://github.com/cro2003/rgpvApi.git
```

Navigate to the project directory:

```bash
cd rgpvApi
```

#### 2. Set Up a Virtual Environment (Optional but Recommended)

It is recommended to use a virtual environment to avoid conflicts with other packages. To create and activate a virtual environment:

```bash
python3 -m venv venv
```

- On **Windows**:
  ```bash
  venv\Scripts\activate
  ```

- On **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

#### 3. Install Dependencies

Install all necessary packages using `pip`. Run the following command:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not present, manually install the dependencies:

```bash
pip install io requests pytesseract beautifulsoup4 Pillow
```

#### 4. Install Tesseract OCR

The project uses `pytesseract`, which requires the Tesseract OCR software.

- On **Windows**:  
  Download and install Tesseract OCR from [this link](https://sourceforge.net/projects/tesseract-ocr-alt/files/tesseract-ocr-setup-3.02.02.exe/download). During installation, note down the installation path.  
  Add the Tesseract path to your environment variables:
  ```
  C:\Program Files\Tesseract-OCR
  ```

- On **macOS**:  
  Use `brew` to install Tesseract:
  ```bash
  brew install tesseract
  ```

- On **Linux (Ubuntu/Debian)**:
  ```bash
  sudo apt-get install tesseract-ocr
  ```

**In case you encounter issues installing Tesseract** on any platform, please refer to the [Official Tesseract Installation Guide](https://tesseract-ocr.github.io/tessdoc/Installation.html) for detailed instructions.

#### 5. Verify Installation

After installing all dependencies, verify the installation by running:

```bash
python -c "import io, requests, pytesseract, bs4, PIL; print('All dependencies are installed successfully!')"
```

If everything is correctly installed, you should see:
```
All dependencies are installed successfully!
```

#### 6. Run the Project

You can now start using the RGPV API project as per the usage instructions provided below.

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
[Email: cro@chirag.software](mailto:cro@chirag.software)

## Contributing

If you wish to contribute to this project, feel free to fork the repository and create a pull request with your changes. Please refer to the [GitHub Issues](https://github.com/cro2003/rgpvApi/issues) section for any existing issues or to raise new ones.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Thank you for using the **RGPV API**! If you encounter any issues, please reach out or raise an issue in the repository.
