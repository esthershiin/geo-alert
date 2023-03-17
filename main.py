"""
This script short polls clinician statuses every 60 seconds, retrieving the 
geolocations of each clinician (ID's 1-7). If a clinician is located outside 
of the boundary region OR we fail to successfuly retrieve a clinician's 
location, we send an email alert to sprinter-eng-test@guerrillamail.info.

"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from shapely.geometry import Point, Polygon
from datetime import datetime
import requests
import time

# ++++++++++++++++++++
#    Polling Logic
# ++++++++++++++++++++

def main():
    url = "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/{}"

    while True:
        print("Polling")
        for clinician_id in range(1, 7):
            response = requests.get(url.format(clinician_id), timeout=15)
            
            # API call successful
            if response.status_code == 200:
                
                # extract geolocation
                geolocation = response.json()
                location, bounds = extract_and_convert_geolocation(geolocation)
    
                # check if clinician is out of safety bounds
                in_bound = False
                for b in bounds:
                    if b.contains(location) or b.touches(location):
                        in_bound = True
                        break
                
                # if out of safety bounds, send email alert
                if not in_bound:
                    print("Clinician {} out of bounds, sending email alert.".format(clinician_id))
                    now = datetime.now()
                    timestamp = now.strftime("%m/%d/%Y %H:%M:%S")
                    
                    subject = "[GEO-ALERT] Clinician Out of Safety Zone"
                    msg = "Phlebotomist with ID #{} was spotted outside of their safety zone.\n\nUTC Time: {}\n"\
                        "Last location: {}\nSafety zone: {}\n".format(clinician_id, timestamp, location, bounds)
                    send_email(subject, msg)
                    
            else:
                # failed to retrieve geolocation, send email alert
                print('Failed to retrieve geolocation for clinician {}, sending email alert.'.format(clinician_id))
                now = datetime.now()
                timestamp = now.strftime("%m/%d/%Y %H:%M:%S")
                
                subject = "[GEO-ALERT] Endpoint Failure"
                msg = "ClinicianStatus endpoint failed to retrieve the geolocation of the phlebotomist "\
                    "with ID #{}.\n\nUTC Time: {}\nResponse code: {}\nResponse message: {}\n"\
                    .format(clinician_id, timestamp, response.status_code, response.reason)
                send_email(subject, msg)
        
        # short poll API every 60 seconds
        time.sleep(60)
        
        
# ++++++++++++++++++++
#  Geolocation Logic
# ++++++++++++++++++++

def extract_and_convert_geolocation(geolocation):
    """_summary_

    Args:
        geolocation (_type_): _description_

    Returns:
        _type_: _description_
    """
    location, bounds = None, []
    for feat in geolocation['features']:
        
        # Point --> clinician coords
        if feat['geometry']['type'] == 'Point':
            location = Point(feat['geometry']['coordinates'])
        
        # Polygon --> boundary lines  
        else:
            poly = Polygon(feat['geometry']['coordinates'])
            bounds.append(poly)
    
    return location, bounds
        
        
# ++++++++++++++++++++
#    Alerting Logic
# ++++++++++++++++++++

def send_email(subject, msg):
    """_summary_

    Args:
        subject (_type_): _description_
        msg (_type_): _description_
    """
    mail = MIMEMultipart()
    mail["From"] = "geoalert.eshin@gmail.com"
    mail["To"] = "sprinter-eng-test@guerrillamail.info"
    mail["Subject"] = subject
    mail.attach(MIMEText(msg))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # port 587 for starttls
        server.ehlo() # identification
        server.starttls() # secure conection
        server.ehlo() # secure identification
        server.login("geoalert.eshin@gmail.com", "nxombzymdtrxmtkz")  # login
        server.sendmail("geoalert.eshin@gmail.com", "sprinter-eng-test@guerrillamail.info", mail.as_string()) # send email
    except Exception as e:
        print('Failed to send email alert. Exception:', e)
    finally: 
        server.quit()


# ++++++++++++++++++++    
#     Driver Code
# ++++++++++++++++++++

if __name__ == "__main__":
    main()


"""
 THOUGHTS:
    - have a clinicians.txt file holding all ids and extract ids from that file  
    - store email messages in separate txt file?
    - have a separate config file for email credentials 
    - move different code logics (email / geolocation) into separate files?
    - error handling ?? --> ex: json parsing
    - send email after each polling session or for each client??
    - need safer storage for passwords
    
RESOURCES:
    - Geometry
        - https://automating-gis-processes.github.io/2017/lessons/L3/point-in-polygon.html
    - Email Alerts
        - https://realpython.com/python-send-email
        - https://levelup.gitconnected.com/an-alternative-way-to-send-emails-in-python-5630a7efbe84
        - https://www.guerrillamail.com/
"""