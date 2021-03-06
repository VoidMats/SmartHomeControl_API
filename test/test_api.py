
#! /bin/python3
# -*- coding: utf-8 -*-

# Adding temporarily path to enviroment
import sys
sys.path.append("../")
# Third part imports
import unittest
import requests
import time
from datetime import datetime, timedelta
# Our written python scripts
#from config import TestingConfig

endpoint = 'http://192.168.1.52:5055/'
#endpoint = 'http://localhost:5054/'

"""
Important note - Gunicorn and Flask developement server uses different error codes
during a failure.
"""

sensor_id = None
sensor_id2 = None
sensor_id3 = None
temperature_rowid = None

class TestAPI(unittest.TestCase):

     # Setup and teardown
    def setUp(self):
        print("\n===========================================")
        print("  RUNNING METHOD ", self.id().split('.')[-1])
        print("===========================================\n")
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    #===============================================================
    # RUN TESTS
    #===============================================================

    def test_0_Login_Logout(self):

        # ===== TEST WRONG METHOD =====
        url = endpoint + "auth/login"
        headers = {'Content-Type': 'application/json'}
        payload = {
            'username':'test',
            'password':'test'
        }
        req = requests.put(url, headers=headers, json=payload)
        print("*** Answer testLogin : WRONG METHOD ***")
        print("URL: ", url)
        print("PAYLOAD: ", payload)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code,405, msg=req.status_code)

        # ===== TEST WITHOUT TOKEN =====
        url = endpoint + "auth/login"
        headers = {'Content-Type': 'application/json'}
        payload = {
            'username':'test',
            'password':'test'
        }
        req = requests.post(url, headers=headers, json=payload)
        print("\n*** Answer testLogin : WITHOUT TOKEN ***")
        print("URL: ", url)
        print("PAYLOAD: ", payload)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 200, msg=req.status_code)
        token = req.json()['data']

        # ===== TEST WRONG METHOD =====
        url = endpoint + "auth/logout"
        headers = {'Content-Type': 'application/json'}
        req = requests.put(url, headers=headers)
        print("*** Answer test_Logout : WRONG METHOD ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code,405, msg=req.status_code)

        # ===== TEST WITH TOKEN =====
        url = endpoint + "auth/logout"
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        req = requests.get(url, headers=headers)
        print("\n*** Answer test_Logout : WITH TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 200, msg=req.status_code)

    def test_1_AddSensor(self):

        # ===== TEST WITH WRONG HEADER =====
        url = endpoint + "temperature/sensor"
        req = requests.post(url)
        print("*** Answer testAddSensor : WRONG HEADER ***")
        print("URL: ", url)
        print("ANSWER: ", req.text)
        self.assertEqual(req.status_code, 401, msg=req.status_code)

        # ===== TEST WRONG METHOD =====
        url = endpoint + "temperature/sensor"
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format('')}
        payload = {
            'name':'test1',
            'folder':'28-0516b501daff',
            'position':'test_position',
            'unit':'c',
            'comment':'test sensor - first'
        }
        req = requests.put(url, headers=headers, json=payload)
        print("*** Answer testAddSensor : WRONG METHOD ***")
        print("URL: ", url)
        print("PAYLOAD: ", payload)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code,405, msg=req.status_code)

        # ===== TEST WITHOUT TOKEN =====
        url = endpoint + "temperature/sensor"
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format('')}
        payload = {
            'name':'test1',
            'folder':'28-0516b501daff',
            'position':'test_position',
            'unit':'c',
            'comment':'test sensor - first'
        }
        req = requests.post(url, headers=headers, json=payload)
        print("\n*** Answer testAddSensor : WITHOUT TOKEN ***")
        print("URL: ", url)
        print("PAYLOAD: ", payload)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 422, msg=req.status_code)

        # ===== TEST WITH TOKEN =====
        req = self.login('test', 'test')
        token = req.json()['data']

        url = endpoint + "/temperature/sensor"
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        payload = {
            'name':'test1',
            'folder':'28-0516b501daff',
            'position':'test_position',
            'unit':'c',
            'comment':'test sensor - first'
        }
        req = requests.post(url, headers=headers, json=payload)
        print("*** Answer testAddSensor : WITH TOKEN ***")
        print("URL: ", url)
        print("PAYLOAD: ", payload)
        print("HEADERS: ", headers)
        print(req.text)
        global sensor_id 
        sensor_id = req.json()['data']
        self.assertEqual(req.status_code, 201, msg=req.status_code)
        self.assertEqual(req.json()['msg'], 'Success', msg=req.json())

    def test_2_GetSensor(self):

        # ===== TEST WITH WRONG HEADER =====
        url = endpoint + "/temperature/sensor/" + str(sensor_id)
        req = requests.get(url)
        print("*** Answer testGetSensor : WRONG HEADER ***")
        print("URL: ", url)
        print("ANSWER: ", req.text)
        self.assertEqual(req.status_code, 401, msg=req.status_code)

        # ===== TEST WRONG METHOD =====
        url = endpoint + "temperature/sensor/" + str(sensor_id)
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format('')}
        req = requests.put(url, headers=headers)
        print("*** Answer testGetSensor : WRONG METHOD ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code,405, msg=req.status_code)

        # ===== TEST WITHOUT TOKEN =====
        url = endpoint + "temperature/sensor/" + str(sensor_id)
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format('')}
        req = requests.get(url, headers=headers)
        print("\n*** Answer testGetSensor : WITHOUT TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 422, msg=req.status_code)

        # ===== TEST WITH TOKEN =====
        req = self.login('test', 'test')
        token = req.json()['data']

        url = endpoint + "temperature/sensor/" + str(sensor_id)
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        req = requests.get(url, headers=headers)
        print("*** Answer testGetSensor : WITH TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 200, msg=req.status_code)
        self.assertEqual(req.json()['msg'], 'Success', msg=req.json())


    def test_3_GetAllSensor(self):

        # ===== TEST WITH WRONG HEADER =====
        url = endpoint + "/temperature/sensor"
        req = requests.get(url)
        print("*** Answer testGetAllSensor : WRONG HEADER ***")
        print("URL: ", url)
        print("ANSWER: ", req.text)
        self.assertEqual(req.status_code, 401, msg=req.status_code)

        # ===== TEST WRONG METHOD =====
        url = endpoint + "temperature/sensor"
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format('')}
        req = requests.put(url, headers=headers)
        print("*** Answer testGetAllSensor : WRONG METHOD ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code,405, msg=req.status_code)

        # ===== TEST WITHOUT TOKEN =====
        url = endpoint + "temperature/sensor"
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format('')}
        req = requests.get(url, headers=headers)
        print("\n*** Answer testGetAllSensor : WITHOUT TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 422, msg=req.status_code)

        # ===== TEST WITH TOKEN =====
        req = self.login('test', 'test')
        token = req.json()['data']

        # Adding one more sensor
        url = endpoint + "/temperature/sensor"
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        payload = {
            'name':'test2',
            'folder':'28-0516b501daff',
            'position':'test_position',
            'unit':'c',
            'comment':'test sensor - second'
        }
        req = requests.post(url, headers=headers, json=payload)
        global sensor_id2 
        sensor_id2 = req.json()['data']
        
        # Get all sensors
        url = endpoint + "/temperature/sensor"
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        req = requests.get(url, headers=headers)
        print("*** Answer testGetAllSensor : WITH TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 200, msg=req.status_code)
        self.assertEqual(req.json()['msg'], 'Success', msg=req.json())
        #self.assertEqual(req.json()['sensor'][0][0], sensor_id, req.json()['sensor'][0])
        #self.assertEqual(req.json()['sensor'][1][0], sensor_id2, req.json()['sensor'][1])

    def test_4_DeleteSensor(self):

        # ===== TEST WITH WRONG HEADER =====
        global sensor_id
        global sensor_id2
        url = endpoint + "temperature/sensor/" + str(sensor_id)
        req = requests.delete(url)
        print("*** Answer testDeleteSensor : WRONG HEADER ***")
        print("URL: ", url)
        print("ANSWER: ", req.text)
        self.assertEqual(req.status_code, 401, msg=req.status_code)

        # ===== TEST WRONG METHOD =====
        url = endpoint + "temperature/sensor/" + str(sensor_id)
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format('')}
        req = requests.put(url, headers=headers)
        print("*** Answer testDeleteSensor : WRONG METHOD ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code,405, msg=req.status_code)

        # ===== TEST WITHOUT TOKEN =====
        url = endpoint + "temperature/sensor/" + str(sensor_id)
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format('')}
        req = requests.delete(url, headers=headers)
        print("\n*** Answer testDeleteSensor : WITHOUT TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 422, msg=req.status_code)

        # ===== TEST WITH TOKEN =====
        req = self.login('test', 'test')
        token = req.json()['data']

        # Delete first sensor
        url = endpoint + "temperature/sensor/" + str(sensor_id)
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        req = requests.delete(url, headers=headers)
        print("\n*** Answer testDeleteSensor : WITHOUT TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 200, msg=req.status_code)

        # Delete second sensor
        url = endpoint + "temperature/sensor/" + str(sensor_id2)
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        req = requests.delete(url, headers=headers)
        self.assertEqual(req.status_code, 200, msg=req.status_code)

        # Get all sensors
        url = endpoint + "temperature/sensor"
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        req = requests.get(url, headers=headers)
        print("*** Answer testGetAllSensor : WITH TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 200, msg=req.status_code)
        #self.assertEqual(len(req.json()['sensor']), 0)

    def test_5_EventpoolStart(self):

        req = self.login('test', 'test')
        token = req.json()['data']

        url = endpoint + "/temperature/sensor"
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        payload = {
            'name':'test3',
            'folder':'28-0516b501daff',
            'position':'test_position',
            'unit':'c',
            'comment':'test sensor - first'
        }
        req = requests.post(url, headers=headers, json=payload)
        global sensor_id3 
        sensor_id3 = req.json()['data']
        self.assertEqual(req.status_code, 201, msg=req.status_code)

        # ===== TEST WITH WRONG HEADER =====
        url = endpoint + "temperature/start/5"
        req = requests.get(url)
        print("*** Answer testEventpoolStart : WRONG HEADER ***")
        print("URL: ", url)
        print("ANSWER: ", req.text)
        self.assertEqual(req.status_code, 401, msg=req.status_code)

        # ===== TEST WRONG METHOD =====
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format('')}
        req = requests.put(url, headers=headers)
        print("*** Answer testEventpoolStart : WRONG METHOD ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code,405, msg=req.status_code)

        # ===== TEST WITHOUT TOKEN =====
        req = requests.get(url, headers=headers)
        print("\n*** Answer testEventpoolStart : WITHOUT TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 422, msg=req.status_code)

        # ===== TEST WITH TOKEN =====
        req = self.login('test', 'test')
        token = req.json()['data']

        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        req = requests.get(url, headers=headers)
        print("*** Answer testEventpoolStart : WITH TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print("READING SENSOR: ", sensor_id3)
        print(req.text)
        self.assertEqual(req.status_code, 200, msg=req.status_code)

        # Sleep for 16 s
        print("We will sleep for 16 s. Please check server that test_function has been triggered")
        time.sleep(16)


    def test_6_EventpoolStop(self):

        # ===== TEST WITH WRONG HEADER =====
        url = endpoint + "temperature/stop"
        req = requests.get(url)
        print("*** Answer testEventpoolStop : WRONG HEADER ***")
        print("URL: ", url)
        print("ANSWER: ", req.text)
        self.assertEqual(req.status_code, 401, msg=req.status_code)

        # ===== TEST WRONG METHOD =====
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format('')}
        req = requests.put(url, headers=headers)
        print("*** Answer testEventpoolStop : WRONG METHOD ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code,405, msg=req.status_code)

        # ===== TEST WITHOUT TOKEN =====
        req = requests.get(url, headers=headers)
        print("\n*** Answer testEventpoolStop : WITHOUT TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 422, msg=req.status_code)

        # ===== TEST WITH TOKEN =====
        req = self.login('test', 'test')
        token = req.json()['data']

        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        req = requests.get(url, headers=headers)
        print("*** Answer testEventpoolStartStop : WITH TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 200, msg=req.status_code)

        # ===== REMOVE SENSOR =====
        url = endpoint + "temperature/sensor/" + str(sensor_id3)
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        req = requests.delete(url, headers=headers)
        self.assertEqual(req.status_code, 200, msg=req.status_code)

    def test_7_ReadTemp(self):

        # ====== ADDING ONE SENSOR ======
        req = self.login('test', 'test')
        token = req.json()['data']

        url = endpoint + "/temperature/sensor"
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        payload = {
            'name':'test1',
            'folder':'28-0516b501daff',
            'position':'test_position',
            'unit':'c',
            'comment':'test sensor - first'
        }
        req = requests.post(url, headers=headers, json=payload)
        print("*** Answer testReadTemp - Adding sensor : WITH TOKEN ***")
        print("URL: ", url)
        print("PAYLOAD: ", payload)
        print("HEADERS: ", headers)
        print(req.text)
        global sensor_id 
        sensor_id = req.json()['data']
        self.assertEqual(req.status_code, 201, msg=req.status_code)

        # ===== TEST WITH WRONG HEADER =====
        url = endpoint + "temperature/read/" + str(sensor_id)
        req = requests.get(url)
        print("*** Answer testReadTemp : WRONG HEADER ***")
        print("URL: ", url)
        print("ANSWER: ", req.text)
        self.assertEqual(req.status_code, 401, msg=req.status_code)

        # ===== TEST WRONG METHOD =====
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format('')}
        req = requests.put(url, headers=headers)
        print("*** Answer testReadTemp : WRONG METHOD ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code,405, msg=req.status_code)

        # ===== TEST WITHOUT TOKEN =====
        req = requests.get(url, headers=headers)
        print("\n*** Answer testReadTemp : WITHOUT TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 422, msg=req.status_code)

        # ===== TEST WITH TOKEN =====
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        req = requests.get(url, headers=headers)
        print("*** Answer testReadTemp : WITH TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 200, msg=req.status_code)

        # ===== REMOVE THE SENSOR =====
        url = endpoint + "temperature/sensor/" + str(sensor_id)
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        req = requests.delete(url, headers=headers)
        self.assertEqual(req.status_code, 200, msg=req.status_code)

    def test_8_GetTemp(self):

        # ===== TEST WITH WRONG HEADER =====
        url = endpoint + "temperature"
        req = requests.get(url)
        print("*** Answer testGetTemp : WRONG HEADER ***")
        print("URL: ", url)
        print("ANSWER: ", req.text)
        self.assertEqual(req.status_code, 405, msg=req.status_code)

        # ===== TEST WRONG METHOD =====
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format('')}
        req = requests.put(url, headers=headers)
        print("*** Answer testGetTemp : WRONG METHOD ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code,405, msg=req.status_code)

        # ===== TEST WITHOUT TOKEN =====
        url = endpoint + "temperature"
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format('')}
        req = requests.post(url, headers=headers)
        print("\n*** Answer testGetTemp : WITHOUT TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 422, msg=req.status_code)

        # ===== TEST WITH TOKEN =====
        req = self.login('test', 'test')
        token = req.json()['data']

        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        dt =datetime.utcnow() - timedelta(seconds=30)
        payload = {
            'sensor' : sensor_id3,
            'start_date' : dt.strftime('%Y-%m-%d %H:%M:%S'),
            'end_date' : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        req = requests.post(url, headers=headers)
        print("*** Answer testGetTemp : WITH TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print("PAYLOAD: ", payload)
        print("GET VALUES FROM SENSOR: ", sensor_id3)
        print(req.text)
        global temperature_rowid
        print(req.json())
        temperature_rowid = req.json()['data'][0][0]
        self.assertEqual(req.status_code, 200, msg=req.status_code)

    def test_9_DeleteTemp(self):

        # ===== TEST WITH WRONG HEADER =====
        url = endpoint + "temperature/" + str(temperature_rowid)
        req = requests.delete(url)
        print("*** Answer testDeleteTemp : WRONG HEADER ***")
        print("URL: ", url)
        print("ANSWER: ", req.text)
        self.assertEqual(req.status_code, 401, msg=req.status_code)

        # ===== TEST WRONG METHOD =====
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format('')}
        req = requests.put(url, headers=headers)
        print("*** Answer testDeleteTemp : WRONG METHOD ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code,405, msg=req.status_code)

        # ===== TEST WITHOUT TOKEN =====
        req = requests.delete(url, headers=headers)
        print("\n*** Answer testDeleteTemp : WITHOUT TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 422, msg=req.status_code)

        # ===== TEST WITH TOKEN =====
        req = self.login('test', 'test')
        token = req.json()['data']

        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        req = requests.delete(url, headers=headers)
        print("*** Answer testDeleteTemp : WITH TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print("DELETE TEMPERATURE ROW: ", temperature_rowid)
        print(req.text)

        self.assertEqual(req.status_code, 200, msg=req.status_code)

    def test_10_GetDevices(self):

        # ===== TEST WITH WRONG HEADER =====
        url = endpoint + "temperature/devices"
        print(url)
        req = requests.get(url)
        print("*** Answer testGetDevices : WRONG HEADER ***")
        print("URL: ", url)
        print("ANSWER: ", req.text)
        self.assertEqual(req.status_code, 401, msg=req.status_code)

        # ===== TEST WRONG METHOD =====
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format('')}
        req = requests.put(url, headers=headers)
        print("*** Answer testGetDevices : WRONG METHOD ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code,405, msg=req.status_code)

        # ===== TEST WITHOUT TOKEN =====
        req = requests.get(url, headers=headers)
        print("\n*** Answer testGetDevices : WITHOUT TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print(req.text)
        self.assertEqual(req.status_code, 422, msg=req.status_code)

        # ===== TEST WITH TOKEN =====
        req = self.login('test', 'test')
        token = req.json()['data']

        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        req = requests.get(url, headers=headers)
        print("*** Answer testGetDevices : WITH TOKEN ***")
        print("URL: ", url)
        print("HEADERS: ", headers)
        print("DEVICES ON NODE: ", req.json()['data'])
        print(req.text)

        self.assertEqual(req.status_code, 200, msg=req.status_code)

    #===============================================================
    # INTERNAL METHODS
    #===============================================================

    def login(self, user, pwd) -> requests:
        url = endpoint + "auth/login"
        headers = {'Content-Type': 'application/json'}
        payload = {
            'username':user,
            'password':pwd
        }
        return requests.post(url, headers=headers, json=payload)



# Run REST_quality unittest
if __name__ == '__main__':
    unittest.main()
