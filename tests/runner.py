import unittest
import os

loader = unittest.TestLoader()
print(f'Discovery in "{os.getcwd()}"')
tests = loader.discover(".")
testRunner = unittest.runner.TextTestRunner()
testRunner.run(tests)
