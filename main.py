"""
This script short polls clinician statuses every 60 seconds, retrieving the 
geolocations of each clinician (ID's 1-7). If a clinician is located outside 
of the boundary region OR we fail to successfuly retrieve a clinician's 
location, we send an email alert to sprinter-eng-test@guerrillamail.info.

"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from shapely.geometry import Point, Polygon
from datetime import datetime
import requests
import time

# ++++++++++++++++++++
#    Polling Logic
# ++++++++++++++++++++

def main():
    url = "https://3qbqr98twd.execute-api.us-west-2.amazonaws.com/test/clinicianstatus/{}"
    # url = "https://httpstat.us/503" # for testing

    while True:
        print("Polling")
        for clinician_id in range(1, 7):
            response = requests.get(url.format(clinician_id), timeout=15)
            
            # API call successful
            if response.status_code == 200:
                # extract geolocation
                geolocation = response.json()
                location, bounds = extract_and_convert_geolocation(geolocation)
                # check if clinician is out of safety boundaries
                in_boundary = clinician_in_boundary(location, bounds)
                # if out of safety boundaries, send email alert
                if not in_boundary:
                    print("Clinician {} out of bounds, sending email alert.".format(clinician_id))
                    now = datetime.now()
                    timestamp = now.strftime("%m/%d/%Y %H:%M:%S")
                    subject = "[GEO-ALERT] Clinician Out of Safety Zone"
                    msg = "Phlebotomist with ID #{} was spotted outside of their safety zone.\n\nUTC Time: {}\n"\
                        "Last location: ({}, {})\n".format(clinician_id, timestamp, location.x, location.y)
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
        print("Sleeping")
        time.sleep(60)
        
        
# ++++++++++++++++++++
#  Geolocation Logic
# ++++++++++++++++++++

def extract_and_convert_geolocation(geolocation):
    """ Takes in the geolocation json information and extracts 
    the clinician's location and safe zone boundaries. It then 
    converts the extracted data in geometry objects (point and 
    polygons).

    Args:
        geolocation (dict): json-encoded geolocation information

    Returns:
        Point: clinician's location
        List[Polygon]: list of safe zone boundaries
    """
    location, bounds = None, []
    for feat in geolocation['features']:
        # Point --> clinician coords
        if feat['geometry']['type'] == 'Point':
            location = Point(feat['geometry']['coordinates'])  
        # Polygon --> boundary lines  
        else:
            for poly in feat['geometry']['coordinates']:
                bounds.append(Polygon(poly))
    return location, bounds

def clinician_in_boundary(location, bounds):
    """ Checks if the clinician's location is within
    or on the boundary line of any of the safe zones 
    in bounds.

    Args:
        location (Point): clinician's location
        bounds (List[Polygon]): list of safe zone boundaries

    Returns:
        bool: True if clinician is in safe zone,
        False otherwise.
    """
    in_boundary = False
    for b in bounds:
        if b.contains(location) or b.touches(location):
            in_boundary = True
            break
    return in_boundary

        
# ++++++++++++++++++++
#    Alerting Logic
# ++++++++++++++++++++

def send_email(subject, msg):
    """ Constructs email with input subject and message text and
    sends email via starttls from geoalerts.sh@gmail.com to
    sprinter-eng-test@guerrillamail.info. If it fails to send
    an email alert, it raises an exception.

    Args:
        subject (str): email subject text
        msg (str): email body text
    """
    mail = MIMEMultipart()
    mail["From"] = "geoalerts.sh@gmail.com"
    mail["To"] = "sprinter-eng-test@guerrillamail.info"
    mail["Subject"] = subject
    mail.attach(MIMEText(msg))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # port 587 for starttls
        server.ehlo() # identification
        server.starttls() # secure connection
        server.ehlo() # secure identification
        server.login("geoalerts.sh@gmail.com", "qjwestzgdhdvykdz")  # login
        server.sendmail("geoalerts.sh@gmail.com", "sprinter-eng-test@guerrillamail.info", mail.as_string()) # send email
        print("Email sent.")
    except Exception as e:
        print('Failed to send email alert. Exception:', e)
    finally: 
        server.quit() # stop server


# ++++++++++++++++++++    
#     Driver Code
# ++++++++++++++++++++

if __name__ == "__main__":
    main()
