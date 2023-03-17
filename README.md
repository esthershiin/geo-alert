# geo-alert

REFLECTION:
    1) Although we hardcoded the clinician ID's (1-6) here, we can have a 
       separate txt file where we extract all ID's from before polling. This 
       will be more practical in a real-life system where our clinician IDs 
       list will be constantly growing and updated.

    2) Similarly, we can also have a separate txt file to store a list of 
       emails we should be sending our alerts to. This will help us alert
       multiple parties and update subscription list more easily.
    
    3) It'll also be nice to have a separate config file to store email
       credentials. In a real life scenario, passwords should be kept hidden.
       
RESOURCES:
    - Geometry
        - https://automating-gis-processes.github.io/2017/lessons/L3/point-in-polygon.html
    - Email Alerts
        - https://realpython.com/python-send-email
        - https://levelup.gitconnected.com/an-alternative-way-to-send-emails-in-python-5630a7efbe84
        - https://www.guerrillamail.com/
