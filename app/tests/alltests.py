import unittest
def suite():
    modules_to_test = ( \
        'test_core', \
        'test_models', 
        'test_utility'
    ) 
    alltests = unittest.TestSuite()
    for module in map(__import__, modules_to_test):
        alltests.addTest(unittest.findTestCases(module))
    return alltests

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
