"""
Unit tests for functions in main.py.

"""

from main import *
import unittest
import time
           
class TestGeolocation(unittest.TestCase):
    def test_extract_and_convert_geolocation(self):
        geolocation_json = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-122.36685807704926,37.58549990610117]}},{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-122.35615253448486,37.587302598423875],[-122.35954284667967,37.58859486022663],[-122.36168861389159,37.58992110558973],[-122.36383438110352,37.591281332695054],[-122.36885547637938,37.587574655404694],[-122.37164497375488,37.5832556334297],[-122.3671817779541,37.57808608084389],[-122.35954284667967,37.57509301791995],[-122.34821319580078,37.58475201586989],[-122.35035896301268,37.58699653313186],[-122.35615253448486,37.587302598423875]]]}}]}
        location, bounds = extract_and_convert_geolocation(geolocation_json)
        self.assertEqual(location.x, -122.36685807704926)
        self.assertEqual(location.y, 37.58549990610117)
        self.assertEqual(len(bounds), 1)
    
    def test_extract_and_convert_geolocation_multiple_boundaries(self):
        # id #2
        geolocation_json = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-122.28693008422852,37.51483205774519]}},{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-122.30946063995361,37.548218088360116],[-122.31645584106445,37.53875852887022],[-122.29770183563231,37.53882658754147],[-122.30946063995361,37.548218088360116]],[[-122.28710174560547,37.52000599905024],[-122.29216575622559,37.51251728365287],[-122.28238105773926,37.513130024958315],[-122.28710174560547,37.52000599905024]]]}}]}
        location, bounds = extract_and_convert_geolocation(geolocation_json)
        self.assertEqual(location.x, -122.28693008422852)
        self.assertEqual(location.y, 37.51483205774519)
        self.assertEqual(len(bounds), 2)
        # id #3
        geolocation_json = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-122.28693008422852,37.51483205774519]}},{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-122.30946063995361,37.548218088360116],[-122.31645584106445,37.53875852887022],[-122.29770183563231,37.53882658754147],[-122.30946063995361,37.548218088360116]]]}},{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-122.28710174560547,37.52000599905024],[-122.29216575622559,37.51251728365287],[-122.28238105773926,37.513130024958315],[-122.28710174560547,37.52000599905024]]]}}]}
        location, bounds = extract_and_convert_geolocation(geolocation_json)
        self.assertEqual(location.x, -122.28693008422852)
        self.assertEqual(location.y, 37.51483205774519)
        self.assertEqual(len(bounds), 2)
        
    def test_clinician_in_boundary(self):
        geolocation_json = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-121.94313511848449,37.329167628247376]}},{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-121.93468093872069,37.33631625612842],[-121.96249008178712,37.33617976989369],[-121.96523666381836,37.304644804751106],[-121.93708419799805,37.30491789153446],[-121.93777084350586,37.31761533167621],[-121.95150375366211,37.316796206705085],[-121.95219039916992,37.32607910032697],[-121.93708419799805,37.32648861334206],[-121.93468093872069,37.33631625612842]]]}}]}
        location, bounds = extract_and_convert_geolocation(geolocation_json)
        in_boundary = clinician_in_boundary(location, bounds)
        self.assertEqual(in_boundary, True)

    def test_clinician_in_boundary_on_line(self):
        # id #5
        geolocation_json = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-122.0328712463379,37.34537963159846]}},{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-122.04145431518556,37.344368504994286],[-122.0328712463379,37.344368504994286],[-122.0328712463379,37.35760507144896],[-122.04145431518556,37.35760507144896],[-122.04145431518556,37.344368504994286]]]}}]}
        location, bounds = extract_and_convert_geolocation(geolocation_json)
        in_boundary = clinician_in_boundary(location, bounds)
        self.assertEqual(in_boundary, True)
        
    def test_clinician_in_boundary_out(self):
        # id #7
        geolocation_json = {"type":"FeatureCollection","features":[{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[-122.22101211547853,37.478604425233506]}},{"type":"Feature","properties":{},"geometry":{"type":"Polygon","coordinates":[[[-122.26487159729002,37.482282467501285],[-122.24324226379393,37.482282467501285],[-122.24324226379393,37.49855903614401],[-122.26487159729002,37.49855903614401],[-122.26487159729002,37.482282467501285]]]}}]}
        location, bounds = extract_and_convert_geolocation(geolocation_json)
        in_boundary = clinician_in_boundary(location, bounds)
        self.assertEqual(in_boundary, False)
        
        
class TestAlert(unittest.TestCase):
    def test_send_email(self):
        timestamp = time.time()
        subject = 'Test Alert - {}'.format(timestamp)
        msg = 'This unit test tests that email alerts are being sent.'
        send_email(subject, msg)
        
        
if __name__ == "__main__":
    print("Testing Geolocation Logic...")
    geo = TestGeolocation()
    geo.test_extract_and_convert_geolocation()
    geo.test_extract_and_convert_geolocation_multiple_boundaries()
    geo.test_clinician_in_boundary()
    geo.test_clinician_in_boundary_on_line()
    geo.test_clinician_in_boundary_out()
    
    print("Testing Alerting Logic...")
    email = TestAlert()
    email.test_send_email()
    