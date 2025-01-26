import sys
import os
import unittest

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.api import app

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_gwpointdata_success(self):
        response = self.app.get('/api/gwpointdata')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)
        print(response.json)

    # def test_get_gwpointdata_file_not_found(self):
    #     # Temporarily rename the file to simulate file not found
    #     os.rename('/home/martin/Documents/GitHub/fpl/backend/data/final/formatted_data_gw_23.json', 
    #               '/home/martin/Documents/GitHub/fpl/backend/data/final/formatted_data_gw_23.json.bak')
    #     response = self.app.get('/api/gwpointdata')
    #     self.assertEqual(response.status_code, 404)
    #     self.assertIn('application/json', response.content_type)
    #     self.assertEqual(response.json, {"error": "File not found"})
    #     # Rename the file back to its original name
    #     os.rename('/home/martin/Documents/GitHub/fpl/backend/data/final/formatted_data_gw_23.json.bak', 
    #               '/home/martin/Documents/GitHub/fpl/backend/data/final/formatted_data_gw_23.json')

if __name__ == '__main__':
    unittest.main()