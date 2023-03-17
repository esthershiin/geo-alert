"""
Unit tests for functions in main.py.

"""

from main import *
import unittest
import time

class TestAlert(unittest.TestCase):
    def test_send_email(self):
        timestamp = time.time()
        subject = 'Test Alert - {}'.format(timestamp)
        msg = 'This unit test tests that email alerts are being sent.'
        send_email(subject, msg)
           

class TestGeolocation(unittest.TestCase):
    
    json1 = ''
    json2 = ''
    
    def test_extract_and_convert_geolocation(self):
        return 
    