# geo-alert

INSTRUCTIONS:
- To run the service, you have to first create an **.env** file at the root directory of the project. The file contents should be 
**password = '{app-password}'**, where {app-password} is the credentials needed to login to the sender email account. 
- Then, simply run **main.py**.


REFLECTION:
- Although we hardcoded the clinician IDs (1-6) here, we can have a separate txt file where we extract all IDs from before polling. This will be more practical in a real-life system where our clinician IDs list will be constantly growing and updated.
- Similarly, we can also have a separate txt file to store a list of emails we should be sending our alerts to. This will help us alert multiple parties and update the subscription list more easily.
- Furthermore, it will be worthwhile to have a system where users can acknowledge alerts to pause alerts for that a specific clinician until the incident is resolved to prevent over-alerting.
    
       
RESOURCES:
- Geometry
    - https://automating-gis-processes.github.io/2017/lessons/L3/point-in-polygon.html
- Email Alerts
    - https://realpython.com/python-send-email
    - https://levelup.gitconnected.com/an-alternative-way-to-send-emails-in-python-5630a7efbe84
    - https://www.guerrillamail.com/
    - https://medium.com/geekculture/how-to-hide-passwords-and-secret-keys-in-your-python-scripts-a8904d5560ec
