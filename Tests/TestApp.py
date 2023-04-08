import unittest
import time
import subprocess

from Tests.test_user import TestUser

if __name__ == "__main__":
    app = subprocess.Popen(["python3", "../API/main.py"])
    time.sleep(2)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestUser)
    unittest.TextTestRunner(verbosity=2).run(suite)

    app.terminate()

