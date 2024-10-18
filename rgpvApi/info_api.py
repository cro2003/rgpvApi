import json
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
class info():
    """This Class have Information About the Package"""

    @staticmethod
    def help():
        """This Function Prints all the Functions present in this Package"""
        print("Fetch Main Result - result_api.result.getMain\nFetch Revaluation Result - result_api.result.getReval\nFetch Revaluation Result - result_api.result.getChlng\nList of CourseId - info_api.info.courseId\nList of CollgeId - info_api.info.clgId")

    @staticmethod
    def courseId():
        """This Function have Course Id for the different Course


        :Returns:
            json: Returns the Course Id in following format
                  {
                    COURSE_NAME: COURSE_ID
                  }
        """
        return json.dumps({'B.E': '1', 'B.Tech.': '24', 'M.C.A.': '5', 'B.Pharmacy': '2', 'B.Pharmacy(PCI)': '43', 'B.Arch.': '11', 'M.Pharmacy': '7', 'M.E.': '6', 'M.Tech.': '8', 'B.E.(PTDC)': '10', 'M.Tech. (PT)': '20', 'MAM': '21', 'MCA (DD)': '23', 'Diploma': '3', 'Ph.D.': '44', 'Pharm D.': '51', 'M.Arch.': '22', 'M.C.A.(2Year)': '53', 'M.B.A.': '4', 'B.Tech.(PTDC)': '42', 'M.Pharm-PCI': '71'})

    @staticmethod
    def clgId():
        """This Function have College Ids for Different College which are Affiliated to RGPV


        :Returns:
            json: Returns the College Id in following format
                  {
                    COLLEGE_NAME: COLLEGE_ID
                  }
        """
        return json.dumps({'VNS Group of Institutions': '0106', 'Ravi Shankar College of Pharmacy': '0135', 'Bansal College of Pharmacy': '0136', 'Lakshmi Narain College of Pharmacy': '0137', 'NRI Institute of Pharmacy': '0138', 'Bhopal Institute of Technology & Science - Pharmacy, Bangrasia': '0139', 'Bhabha Pharmacy Research Institute': '0140', 'Globus College of Pharmacy': '0141', 'NRI Institute of Pharmaceutical Science': '0142', 'Malhotra College ': '0143', 'Millennium College of Pharmacy': '0144', 'Oriental College of Pharmacy': '0145', 'Patel College of Pharmacy': '0417', 'Radharaman College of Pharmacy': '0147', 'Rajiv Gandhi College of Pharmacy': '0148', 'Sagar Institute of Research & Technology - Pharmacy': '0149', 'TIT College of Pharmacy': '0150', 'Truba Institute of Pharmacy': '0151', 'RKDF School of Pharmaceutical Sciences': '0155', 'Technocrat Institute of Technology [ Pharmacy ]': '0165', "People's Institute of Pharmacy & Research Center": '0169', 'Radharaman Institute of Pharmaceutical Sciences': '0170', 'Mittal Institute of Technology': '0180', 'Sagar Institute of Research, Technology & Science [Pharmacy]': '0193', 'Gyan Ganga Institute of Technology & Science': '0206', 'Sardar Patel College of Technology [ Pharmacy ]': '0209', 'Shri Ram Institute of Technology [Pharmacy]': '0211', 'Guru Ramdas Khalsa Institute of Science & Technology [Pharmacy]': '0212', 'Shri Ram Institute of Pharmacy': '0231', 'Shri Ram Group of Institutions': '0232', 'Shri Rawatpura Sarkar Institute of Pharmacy, Jabalpur': '0237', 'Oriental Institute of Pharmacy, Lalburra,Balaghat': '0238', 'Laxmi Bai Sahuji College of Pharmacy': '0239', 'Gracious College of Pharmacy': '0241', 'Shri Ram Institute of Technology': '0205', 'Shree Balaji College OF Pharmacy': '0248', 'DR.Bhagat Singh Rai College OF Pharmacy': '0249', 'Shivam College Of Pharmacy': '0250', 'Rewa College of Pharmacy': '0304', 'Rajiv Gandhi Institute of Pharmacy': '0305', 'Gulab Kali Memorial College of Pharmacy': '0310', 'Shrikrishna Pharmacy College': '0311', 'Shri Rama Krishna College of Pharmacy ': '0312', 'Aditya College of Pharmacy ': '0313', 'Shri Rawatpura Sarkar Institute of Pharmacy': '0316', 'Shri Sahaj Institute of Pharmacy': '0401', 'NRI Institute of Research & Technology': '0511', 'IES School of Pharmacy': '0513', 'Sagar Institute of Pharmacy & Technology': '0514', 'Vivekanand College of Pharmacy': '0516', 'Kailash Narayan Patidar College of Pharmacy': '0518', 'Mittal Institute of Pharmacy': '0519', 'Millennium College of Pharmacy & Science': '0522', 'Swami Vivekanand College of Pharmacy': '0826', 'IES Institute of Pharmacy': '0554', 'Raghukul College of Pharmacy, Bhopal': '0555', 'Corporate Institute of Pharmacy, Bhopal': '0556', 'Surabhi College of Pharmacy': '0557', 'Akhil Bharti College of Pharmacy': '0558', 'Indira Institute of Professional Studies ': '0559', 'Vaishnavi Institute of Pharmacy': '0560', 'Sam College of Pharmacy ': '0561', 'S.D. College of Pharmacy': '0562', 'Technocrat Institute of Technology And Science-Pharmacy': '0568', 'Novel College of Pharmacy': '0569', 'Sagar Institute of Pharmaceutical Science': '0602', 'Adina Institute of Pharmaceutical Science': '0603', 'Bhagyodaya Tirth Pharmacy College': '0604', 'Vedic Institute of Pharmaceutical Education & Research': '0605', 'Daksh Institute of Pharmaceutical Science': '0606', 'Baba Loknath Indian Inst.of Phar.Sc. & Res.Centre': '0615', 'Adina College of Pharmacy': '0617', 'Shri Rawatpura Sarkar College ': '0618', 'Shanti College of Pharmacy ': '0619', 'Khajuraho Institute of Pharmaceutical Sciences': '0620', 'Babulal Tarabai Institute Pharmaceutical Science ': '0621', 'Om Sai Naath College of Pharmacy': '0622', 'Gyan Sagar College Of Pharmacy': '0623', 'Balaji Pharmacy College': '0624', 'Ojaswini Pharmacy College': '0625', 'B R Nahata College of Pharmacy': '0703', 'Dr. Shri R M S Inst. Sc.& Tech. ( College of Pharmacy) , Bhanpura': '0706', 'Mahakal Institute of Pharmaceutical Studies': '0707', 'Mandsaur Institute of Pharmacy': '0710', 'Ujjain Institute of Pharmaceutical Sciences': '0711', 'Royal Institute of Management & Advanced Studies': '0720', 'Gyanodya Institute of Pharmacy ': '0726', 'Radhadevi Ramchandra Mangal Institute Bhatkhera ': '0727', 'SHRI G.S. INSTITUTE OF TECHNOLOGY & SCIENCE': '0801', 'Smirti College of Pharmaceutical Education': '0804', 'College of Pharmacy, IPS Academy': '0811', 'GRY Institute of Pharmacy, Borawan': '0816', 'Central India Institute of Pharmacy': '0824', 'Lakshmi Narain College of Pharmacy (RCP)': '0825', 'RKDF Institute of Pharmaceutical Sciences': '0840', 'Charak Institute of Pharmacy, Mandleshwar': '0841', 'B M College of Pharmaceutical Education & Research': '0843', 'Chordia Institute of Pharmacy': '0844', 'Indore Institute of Pharmacy': '0845', 'Modern Institute of Pharmaceutical Sciences': '0846', 'LNCT School of Pharmacy Indore': '0847', 'Nutanben Mansukhbhai Turakhia Gujarati College of Pharmacy': '0848', 'Nimar Institute of Pharmacy, Dhamnod': '0849', 'Oriental College of Pharmacy & Research': '0860', 'Shri Bherulal Pharmacy Institute': '0864', 'Sri Satya Sai Pharmacy Research Institute': '0865', 'Acropolis Institute of Pharmaceutical Education & Research': '0866', 'Subhdeep College of Pharmacy': '0867', 'Vikrant Institute of Pharmacy': '0869', 'Sri Aurobindo Inst. of Pharmacy': '0879', 'MATHURADEVI INSTITUTE OF PHARMACY, INDORE': '0888', 'THAKAUR S K SINGH MEMORIAL PHARMACY COLLEGE': '0889', 'Chameli devi Institute of Pharmacy, Indore': '0890', 'Jagadguru Dattatray College of Pharmacy, Indore': '0891', 'Compfeeders Aisect College of Professional Studies,  Indore': '0892', 'Oxford International College, Indore': '0893', 'Indore Mahavidhyalaya, Indore': '0894', 'Vinayaka College of Pharmacy': '0895', 'Vidyasagar College of Pharmacy ': '0896', 'R D Memorial College of Pharmacy and Research Indore ': '0897', 'Shivajirao Kadam Institute of Pharmaceutical Education and Research': '0898', 'Parijat College of Pharmacy, Indore': '0899', 'Sri Ram Nath Singh College of Pharmacy, Gormi': '0909', 'Sun Institute of Pharmaceutical Education & Research, Lahar': '0911', 'Shri Rawatpura Institute of Pharmacy': '0919', 'Shri Ram College of Pharmacy': '0920', 'Shri Ram Nath Singh Institute of Pharmaceutical Sc.': '0921', 'Pranav Institute of Pharmaceutical Sciences & Research': '0922', 'Institute of Professional Studies College of Pharmacy': '0923', 'Nagaji Institute of Pharmaceutical Science': '0925', 'Gurukul Institute of Pharmaceutical Science & Research': '0933', 'Bhartiya Vidya Mandir College of Pharmacy': '0944', 'Laxman Seth Pharmacy College ': '0955', 'Prathavi College of Pharmacy': '0956', 'Jai Institute of Pharmaceutical Sciences & Research': '0959', 'Shivnath Singh College ': '0960', 'Divine International Group of Institutions': '0961', 'Ansh College of Pharmacy ': '0962', 'Jain College': '0963', 'Radha Krishna College of Pharmacy ': '0964', 'Jai Shri Shyam College': '0965', 'Meera Devi Pharmacy College': '0966', 'B.R.College': '0968', 'Vedant Institute of Professional Study': '0969', 'Awadh Madhav College Of Pharmacy': '0970', 'V.E.E. Academy Shalupura': '0971', 'Yuva Institute of Pharmacy': '0972', 'Shanti College of Pharmacy': '0974', 'University Institute of  Technology, RGPV': '0101', 'Lakshmi Narain College of Technology': '0103', 'RKDF Institute of Science & Technology': '0104', 'Oriental Institute of Science & Technology': '0105', 'Samrat Ashok Technological Institute': '0108', 'Sri Satya Sai Institute of Science & Technology': '0109', 'Technocrat Institute of Technology': '0111', 'Bansal Institute of Science & Technology': '0112', 'Truba Institute of Engg. & Information Technology, GANDHI NAGAR, BHOPAL': '0114', 'NRI Institute of Information Science & Technology': '0115', "All Saints' College of Technology": '0116', 'Scope College of Engineering': '0121', 'Bhopal Institute of Technology & Science, Bangrasia': '0124', 'Shree Institute of Science & Technology': '0125', 'Oriental College of Technology': '0126', 'Bansal College of Engineering': '0127', 'Patel College of Science & Technology': '0828', 'Bhabha Engineering Research Institute': '0129', 'Globus Engineering College': '0130', 'J.N. College of Technology': '0131', 'Radha Raman Institute of Technology & Science': '0132', 'Sagar Institute of Research & Technology': '0133', 'RKDF College of Engineering': '0156', 'Lakshmi Narain College of Technology & Science': '0157', 'Radharaman Engineering College': '0158', 'Rajeev Gandhi Proudyogiki Mahavidylaya': '0159', 'Swami Vivekanand College of Science & Technology': '0160', 'Acropolis Institute of Technology & Research': '0827', "All Saints' College of Engineering": '0172', 'Bansal Institute of Research & Technology': '0173', 'Bhopal Institute of Technology, Bangrasia': '0174', 'Lakshmi Narain College of Technology Excellence': '0176', 'IES College of Technology': '0177', 'Jai Narain College of Technology & Science': '0178', 'Millennium Institute of Technology & Science': '0179', 'Patel Institute of Technology': '0181', "People's College of Research & Technology": '0182', 'Rukmani Devi Institute of Science & Technology, Misrod': '0185', 'Sagar Institute of Research, Technology & Science': '0186', 'Sagar Institute of Science & Technology, Pipalner Gandhi Nagar Bhopal.': '0187', 'SAM College of Engineering & Technology': '0188', 'Technocrats Institute of Technology [Excellence]': '0191', 'Technocrats Institute of Technology & Science': '0192', 'Trinity Institute of Technology & Research': '0198', 'Technocrats Institute of Technology - Advance': '0199', 'Jabalpur Engineering College': '0201', 'Guru Ramdas Khalsa Institute of Science & Technology': '0235', 'Hitkarni College of Engineering & Technology': '0203', 'Takshshila Institute of Engineering & Technology': '0207', 'Gyan Ganga College of Technology': '0208', 'Shri Ram Institute of Science & Technology': '0213', 'Vindhya Institute of Technology & Science': '0302', 'Laxmi Bai Sahuji Institute of Engineering & Technology': '0215', 'SGBM Institute of Technology & Science': '0216', 'Saraswati Institute of Engineering & Technology': '0219', 'Sardar Patel College of Technology': '0221', 'St. Aloysius Institute of Technology': '0223', 'Radhaswami Institute of Technology': '0224', 'Faculty of Engg. Global Nature Care Sangathan Group of Instt.': '0225', 'Prakash Institute of Engg. & Technology': '0227', 'Annie Institute of Technology and Research Centre': '0236', 'Rewa Engineering College': '0301', 'Rewa Institute of Technology': '0303', 'Jawaharlal Nehru College of Technology': '0306', 'Aditya College of Technology & Science': '0307', 'UIT Shahdol': '0308', 'Sagar Institute of Research & Technology Excellence': '0501', 'Corporate Institute of Science & Technology': '0502', 'IASSCOM Fortune Institute of Technology': '0503', 'Kailash Narayan Patidar College of Science & Technology': '0505', 'Bansal Institute of Research, Technology & Science': '0506', 'Surabhi College of Engineering & Technology': '0508', 'Patel Institute of Engineering & Science': '0509', 'Laxmipati Institute of Science & Technology': '0510', 'Bagula Mukhi College of Technology': '0525', 'IES Institute of Technology and Management': '0526', 'RKDF College of Technology': '0527', 'Mansarover Institute of Science & Technilogy': '0529', 'Madhav Proudyogiki Mahavidyalaya': '0530', 'Vidhyapeeth Institute of Science & Technology': '0531', 'Sha-Shib College of Technology': '0532', 'Truba College of Science & Technology': '0533', 'Maxim Institute of Technology': '0534', 'Girdhar Siksha Evam Samaj Kalyan Samiti Group of Inst.': '0535', 'Sagar Institute of Science Technology & Engineering': '0536', 'Sagar Institute of Science & Technology & Research': '0537', 'Kopal Institute of Science & Technology': '0538', 'Bhopal Institute of Technology & Management': '0539', 'Millennium Institute of Technology': '0540', 'Shri Ram College of Technology': '0541', 'Satyam Edu. & Social Welfare Society Group of Instt.': '0542', 'Malhotra Technical Research Institute': '0543', 'AISECT Institute of Science & Technology': '0544', 'Shri Balaji Institute of Technology & Mgmt.': '0545', 'Vaishnavi Inst. of Tech. & Science': '0546', 'Sparta Institute of Tech. & Mgmt.': '0548', 'Corporate Institute of Research & Technology, Hataikheda': '0552', 'H.L. Agrawal College of Engineering': '0553', 'I G Engineering College': '0601', 'Ojaswini Institute of Management & Technology': '0607', 'Babulal Tarabai Institute of Research & Technology': '0608', 'Infinity Management & Engineering College': '0610', 'Adina Institute of Science & Technology': '0612', 'Gyan Sagar College of Engineering': '0613', 'Pt.Devprabhakar Shastri College of Tech.': '0614', 'Engineering College Nowgong,': '0616', 'Ujjain Engineering College': '0701', 'Mandsaur Institute of Technology': '0702', 'Mahakal Institute of Technology': '0704', 'Mahakal Institute of Technology & Science': '0712', 'Alpine Institute of Technology': '0713', 'Mahakal Institute of Technology & Management': '0714', 'Prashanti Institute of Technology & Science': '0715', 'Late Ramoti Devi Institute of Engineering': '0716', 'Synergy Institute of Technology': '0717', 'Shri Yogindra Sagar Institute of Technology & Science': '0718', 'Shri Guru Sandipani Institute of Technology & Science': '0722', 'Srajan Institute of Technology Management & Science': '0723', 'New-Tech Institute  of Engineering Science & Technology': '0725', 'Shri Vaishnav Institute  of  Technology & Science': '0802', 'Jawaharlal Institute of Technology, Borawan': '0805', 'Institute of Engineering & Science, IPS Academy': '0808', 'Medicap Institute of Technology & Management': '0812', 'Lakshmi Narain College of Technology and Science (RIT)': '0817', 'Indore Institute of Science & Technology': '0818', 'Central India Institute of Technology': '0819', 'Malwa Institute of Technology': '0821', 'Swami Vivekanand College of Engineering': '0822', 'Sri Dadaji Institute of Technology & Science': '0823', 'Sushila Devi Bansal College of Technology': '0829', 'Astral Institute of Technology & Research': '0831', 'CHAMELI DEVI GROUP OF INSTITUTIONS, Khandwa Road, Indore ': '0832', 'Sushila Devi Bansal College of Engineering': '0834', 'LNCT (Bhopal) Indore Campus': '0835', 'Sanghvi Institute of Management & Science': '0837', 'Techno Engineering College Indore': '0838', 'B M College of Technology': '0850', 'Mathura Devi Institute of Technology & Management': '0852', 'Priyatam Institute of Technology & Management': '0854', 'RKDF School of Engineering': '0855', 'Shiv Kumar Singh Institute of Technology & Science': '0856', 'Star Academy of Technology & Management': '0857', 'Vikrant Institute of Technology & Management, Borkhedi, Mohow': '0858', 'Sanghvi Institute of Engineering & Technology': '0861', 'Malwa Institute of Science & Technology': '0862', 'Prestige Institute of Engineering Management & Research': '0863', 'Global Institute of Engineering & Science, Sendhwa': '0870', 'Nalin Institute of Technology': '0872', 'Sri Aurobindo Institute of Technology': '0873', 'Indore Institute of Science & Technology-II': '0874', 'Shivajirao Kadam Institute of Technology and Management - Technical Campus': '0875', 'Medi-Caps Institute of Science & Technology': '0876', 'Mandsaur Inst. of Tech.': '0880', 'Sardar Patel Inst. of Tech. & Mgmt.': '0881', 'Shreejee Inst. of Tech. & Mgmt.': '0882', 'THAKUR SHIVKUMAR SINGH MEMORIAL ENGINEERING COLLEGE': '0884', 'Vidyasagar Institute of Technology': '0885', 'Sri Parashuram Institute of Technology and Research': '0886', 'UIT JHABUA': '0887', 'Madhav Institute of Technology & Science': '0901', 'Rustam Ji Institute  of Technology': '0902', 'Maharana Pratap College of Technology': '0903', 'Shri Ram College of Engineering & Management, Banmore': '0904', 'Institute of Technology & Management': '0905', 'Shri Rawatpura Sarkar Institute of Technology & Science': '0913', 'Institute of Information Technology & Management': '0915', 'Gwalior Engineering College': '0916', 'Nagaji Institute of Technology & Management': '0917', 'IPS College of Technology & Management': '0928', 'Shri Ram Institute of Information Technology, Banmore': '0929', 'Gwalior Institute of Information Technology': '0932', 'Vikrant Institute of Technology & Management': '0936', 'NRI College of Engineering & Management': '0937', 'IMT Group of Institutions': '0938', 'Malwa Institute of Technology & Management': '0939', 'Hindustan Inst. of Tech. Sc. & Mgmt.': '0946', 'Integral Institute of Information Technology & Management': '0947', 'Bethesda Institute of Technology & Sciences': '0953', 'SAKSHI INSTITUTE OF TECHNOLOGY & MANAGEMENT': '0954', 'UNIVERSITY POLYTECHNIC,RGPV': '0006', 'School of Applied Management, RGPV, UTD': '0008', 'Mahakoshal College of Science': '0240', 'Mekalsuta College of Managemant ': '0243', 'Oriental Institute OF Management ': '0244', 'Medhavi Institute of management Jabalpur': '0245', 'Aditya College Of Management SATNA': '0315', 'Jawaharlal Institute of Technology and Management': '0402', 'International School of Business Adminisration': '0405', 'Asian Institute Of Professional Studies': '0406', 'Excel Business School ': '0407', 'Swatantra Sainani Institute of Business Management': '0408', 'Shri Jain Diwakar Mahavidyalaya': '0409', 'Little Angel Institute Of Professional Studies': '0410', 'Astral Institute Of Business Management ': '0411', 'Sahib Institute of Management and Research': '0412', 'Victoria College ': '0413', 'Shri Ravindranath Tagore Institute Of Professional Studies ': '0414', 'Sardar Vallabh Bhai Patel Mahavidyalaya ': '0415', 'Shri Gyan Shiksha Mahavidyalaya ': '0416', 'Victoria College': '0563', 'Poise College': '0564', 'Parakh College': '0565', 'Gurukripa College of Professional Studies': '0566', 'Lakshmi Narain College of Management GWALIOR': '0973', 'Govt. Geetanjali Girls College': '0107', 'Maharishi Centre For Educational Excellence': '0117', 'Institute of Professional Education & Research': '0118', 'Technocrat Institute of Technology [MCA]': '0163', 'Oriental Institute of Science & Technology [MCA]': '0167', "People's Institute of Management & Research": '0168', 'Technocrats Institute of Technology [MBA]': '0194', 'Oriental College of Management': '0196', 'Shri Ram Institute of Technology [MCA]': '0210', 'Shri Ram Institute of Management [ MCA ]': '0222', 'Jawaharlal Institute Of Technology Borawan ': '0403', 'Shri Sai Institute of Technology': '0705', 'Prestige Institute of Management': '0907', 'Gyanodaya Institute of Professional Studies Neemuch(M.P)': '0724', 'Maharaja Ranjit Singh Group of Institutions': '0803', 'Shri Vaishnav Institute of Management': '0807', 'School of Computer Application, IPS Academy': '0810', 'Pioneer Institute of Professional Studies': '0814', 'SHRI RAOJIBHAI GOKALBHAI PATEL GUJARATI PROFESSIONAL INSTITUTE': '0815', 'Sanghvi Institute of Management & Science [MBA]': '0859', 'Indore Institute of Computer Application': '0871', 'Boston College for Professional Studies': '0906', 'Institute of Technology & Management [MCA]': '0926', 'Divine International Group of Institution': '0951', "National Institute of Technical Teacher's Training and Research,Bhopal": '0012', 'School of Pharmaceutical Sciences, UTD, RGPV': '0001', 'School of Information Technology, UTD, RGPV': '0002', 'School of Energy & Environment Management, UTD,RGPV': '0003', 'School of Bio-Technology,UTD, RGPV': '0004', 'School of Nanotechnology, RGPV, UTD': '0005', 'School of Biomolecular Engineering and Biotechnology': '0010', 'Baderia Global Institute of Engineering And Management': '0246', 'Technocrats Institute of Technology - Computer Science and Engineering': '0567', 'School of Architecture, RGPV, UTD': '0009', 'Hitkarni College of Architecture': '0233', 'Bagula Mukhi College of Arch.& Planning': '0549', 'School of Architecture,IPS Academy': '0809', 'SDPS College of Architecture': '0842', 'University Dual Degree Integrated PG Program': '0007', 'Satpuda College OF Engineering & Polytechnic BALAGHAT': '0242', 'Shri Rama Krishna College Of Engineering Science And Management': '0314', 'UIT,RGPV, Shivpuri': '0967', 'Acropolis Institute of Design': '0404'})
    
    @staticmethod
    def fetch_alerts():
        """
        Placeholder function for fetching alerts from the RGPV website.
        
        This function is expected to:
        - Send a GET request to the RGPV website.
        - Parse the HTML content to extract alerts from the alert modal.
        - Structure the extracted alert text and associated link (if any) into a JSON format.

        Returns:
        str: JSON formatted string containing alert information, each with:
        - 'date': Placeholder value "Not available".
        - 'alert': The extracted alert text.
        - 'link': The link associated with the alert (if available).
        """
        pass
    
    @staticmethod
    def get_notifications( _from=None, _to=None):
        """
        Placeholder function for fetching notifications from the RGPV website with optional date filtering.
        
        This function is expected to:
        - Fetch HTML content from the notification page on the RGPV website.
        - Extract and parse the notification details, including date, title, and link.
        - Filter notifications based on the provided _from and _to date range.
        - If no dates are provided, return notifications from the last 30 days.
        - Fetch alerts using `fetch_alerts` and combine the alerts with notifications if relevant.

        Parameters:
        _from (str): Start date in 'dd-mm-yyyy' format.
        _to (str): End date in 'dd-mm-yyyy' format.

        Returns:
        str: JSON formatted string containing the filtered notifications, with:
        - 'date': Formatted date in 'dd/mm/yy'.
        - 'alert': The notification title.
        - 'link': The link to the notification.
        """
        pass

def fetch_alerts():
    """
    Fetch alerts from the RGPV website.

    This function sends a GET request to the RGPV website, parses the HTML content,
    and extracts alerts from the alert modal. It retrieves the alert text and link,
    if available, and structures this data in a JSON format.

    Returns:
    str: JSON formatted string containing alerts, each with a 'data' key set to 
    "Not available", 'text' for alert text, and 'link' for the associated link (if any).
    """
    url = 'https://www.rgpv.ac.in/'
    # Send a GET request to fetch the HTML content of the website
    response = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Select the alert modal body content using the modal's ID
    modal_body = soup.select_one('#alert-modal .modal-body .tab-content')

    # Initialize the response dictionary
    alerts = []

    # Check if the modal body exists
    if not modal_body:
        return json.dumps(alerts)

    # Get all the alert containers (both ImpText1 and ImpText2)
    alert_items = modal_body.select('.ImpText1, .ImpText2')

    # Loop through each alert item and extract the text and link
    for alert in alert_items:
        # Get the alert text
        alert_text = alert.get_text(strip=True)

        # Get the anchor link inside the alert, if it exists
        alert_link = alert.find('a')['href'] if alert.find('a') else None

        # Add the alert information to the alerts list
        alerts.append({
            "date": "Not available", 
            'alert': alert_text.replace("Click Here to View",""),
            'link': "https://www.rgpv.ac.in"+alert_link
        })

    # Return the response data as JSON format
    return json.dumps(alerts, indent=4)


def get_notifications(_from=None, _to=None):
    """
    Fetch notifications from RGPV based on specified date filters.

    Parameters:
    _from (str): The start date in 'dd-mm-yyyy' format. Fetch notifications from this date onward.
    _to (str): The end date in 'dd-mm-yyyy' format. Fetch notifications between this and the _from date.

    Returns:
    str: JSON formatted string of notifications with date formatted as 'dd/mm/yy'.
    If no dates are provided, returns notifications from the last 30 days.
    """
    # Fetch the HTML content from the URL
    url = "https://www.rgpv.ac.in/Uni/ImpNoticeArchive.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table containing the notifications
    table = soup.find('table', class_='table table-bordered table-condensed table-striped')

    # Initialize a list to store notifications
    notifications = []

    # Parse the rows in the table
    for row in table.find_all('tr')[2:]:  # Skip the header rows
        cols = row.find_all('td')
        if len(cols) >= 3:
            date_str = cols[1].get_text(strip=True)
            title_tag = cols[2].find('a')  # Get the anchor tag

            # Check if the title tag exists
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag['href']
                
                # Add to notifications list
                notifications.append({
                    'date': date_str,
                    'title': title,
                    'link': link
                })

    # Convert date strings to datetime objects for filtering
    for notification in notifications:
        notification['date'] = datetime.strptime(notification['date'], '%d/%m/%Y')

    # Apply date filtering
    if _from and _to:
        _from_date = datetime.strptime(_from, '%d-%m-%Y')
        _to_date = datetime.strptime(_to, '%d-%m-%Y')
        filtered_notifications = [
            n for n in notifications if _from_date <= n['date'] <= _to_date
        ]
    elif _from:  # If only _from is provided
        _from_date = datetime.strptime(_from, '%d-%m-%Y')
        filtered_notifications = [n for n in notifications if n['date'] >= _from_date]
    else:  # If neither _from nor _to is provided, get the last 30 days
        thirty_days_ago = datetime.now() - timedelta(days=30)
        filtered_notifications = [n for n in notifications if n['date'] >= thirty_days_ago]

    
    a = json.loads(fetch_alerts())
    # Prepare the final output
    output = []
    for notification in filtered_notifications:
        output.append({
            'date': notification['date'].strftime('%d/%m/%y'),  # Format the date
            'alert': notification['title'],
            'link': url
        })
    
    if _from and _to:
        _to_date = datetime.strptime(_to, '%d-%m-%Y')
        if _to_date >= datetime.now() - timedelta(days=30) :
            a.extend(output)
            output = a
    elif _from:
        a.extend(output)
        output = a
    else:
        a.extend(output)
        output = a
    
    return json.dumps(output)
