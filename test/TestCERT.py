##
# UnitTest for CERT.py.
#
# RUN: python -m unittest -v test.TestCERT
#

from os import listdir
from os.path import join
import unittest

from lib.CERT import CERT, ErrorCERTParsing
from lib.File import ErrorFileParsing


##
# UnitTest for CERT class.
#
class TestCERT(unittest.TestCase):
    cert_properties = {
        "CERT.RSA": {
            "name": "CERT.RSA",
            "size": 906,
            "md5": "5026e73a2f0d8091aaf7908cffbc425e",
            "sha1": "37210614d362672e19cdd7940b7f5037de6cbcb8",
            "sha256": "0ba1a5ba50b277bb37d05e8b9d2c6422aad49b90c08e7136d2d7c204ceaaf412",
            "sha512": "e16ce3b471f10043be642472dc4f0156dccb434331c0c1ca19470b7dc0d025d4bb512fc5e77e78011e704b69fe0872e6fd7dee648e87401062f59149695f36f5",
            "serial_number": "558e7595",
            "validity": {
                "from": "2015-06-27 12:06:13",  # "Sat Jun 27 12:06:13 CEST 2015"
                "until": "2515-02-26 11:06:13",  # "Tue Feb 26 11:06:13 CET 2515"
            },
            "fingerprint_md5": "90:22:EF:0C:DB:C3:78:87:7B:C3:A3:6C:5A:68:E6:45",
            "fingerprint_sha1": "5A:C0:6C:32:63:7F:5D:BE:CA:F9:38:38:4C:FA:FF:ED:20:52:43:B6",
            "fingerprint_sha256": "E5:15:CC:BC:5E:BF:B2:9D:A6:13:03:63:CF:19:33:FA:CE:AF:DC:ED:5D:2F:F5:98:7C:CE:37:13:64:4A:CF:77",
            "fingerprint_signature": "SHA1withRSA",
            "fingerprint_version": "3",
            "owner": {
                "name": "Name",
                "email": "",
                "unit": "Unit",
                "organization": "Organization",
                "city": "City",
                "state": "State",
                "country": "XX",
                "domain": "",
            },
            "issuer": {
                "name": "Name",
                "email": "",
                "unit": "Unit",
                "organization": "Organization",
                "city": "City",
                "state": "State",
                "country": "XX",
                "domain": "",
            },
        },
    }

    ##
    # Set up the test case.
    #
    @classmethod
    def setUpClass(cls):
        cls.certs = {}

        for filename in listdir(join('test', 'data')):
            if filename in cls.cert_properties:
                cls.certs[filename] = CERT(join('test', 'data', filename), filename)
                #print(cls.certs[filename].dump())

    ##
    # Clear the test case.
    #
    @classmethod
    def tearDownClass(cls):
        pass

    ##
    # Set up the test fixture.
    #
    def setUp(self):
        pass

    ##
    # Clear the test fixture.
    #
    def tearDown(self):
        pass

    ##
    # Test the object initialisation.
    #
    def test_init(self):
        for filename in self.certs:
            self.assertTrue(self.certs[filename] is not None)
            self.assertTrue(type(self.certs[filename]) is CERT)

        # Test the class raise when a non-existing file is given:
        with self.assertRaises(ErrorFileParsing):
            CERT(join('test', 'data', 'aaa_this_is_a_non_existent_file_xxx'))

        # Test the class raise when a non-CERT.RSA file is given:
        with self.assertRaises(ErrorCERTParsing):
            CERT(join('test', 'data', 'Example.apk'))
            CERT(join('test', 'data', 'AndroidManifest.xml'))
            CERT(join('test', 'data', 'classes.dex'))

    ##
    # Test the get_raw_file() method.
    #
    def test_get_raw_file(self):
        for filename in self.certs:
            self.assertTrue(len(self.certs[filename].get_raw_file()) > 0)

    ##
    # Test the get_file_name() method.
    #
    def test_get_file_name(self):
        for filename in self.certs:
            self.assertTrue(self.certs[filename].get_file_name() == self.cert_properties[filename]['name'])

    ##
    # Test the get_size() method.
    #
    def test_get_size(self):
        for filename in self.certs:
            self.assertTrue(self.certs[filename].get_size() == self.cert_properties[filename]['size'])

    ##
    # Test the get_md5() method.
    #
    def test_get_md5(self):
        for filename in self.certs:
            self.assertTrue(self.certs[filename].get_md5() == self.cert_properties[filename]['md5'])

    ##
    # Test the get_sha1() method.
    #
    def test_get_sha1(self):
        for filename in self.certs:
            self.assertTrue(self.certs[filename].get_sha1() == self.cert_properties[filename]['sha1'])

    ##
    # Test the get_sha256() method.
    #
    def test_get_sha256(self):
        for filename in self.certs:
            self.assertTrue(self.certs[filename].get_sha256() == self.cert_properties[filename]['sha256'])

    ##
    # Test the get_sha512() method.
    #
    def test_get_sha512(self):
        for filename in self.certs:
            self.assertTrue(self.certs[filename].get_sha512() == self.cert_properties[filename]['sha512'])

    ##
    # Test the get_serial_number() method.
    #
    def test_get_serial_number(self):
        for filename in self.certs:
            self.assertTrue(self.certs[filename].get_serial_number() == self.cert_properties[filename]['serial_number'])

    ##
    # Test the get_validity() method.
    #
    def test_get_validity(self):
        for filename in self.certs:
            self.assertTrue(self.certs[filename].get_validity() == self.cert_properties[filename]['validity'])

    ##
    # Test the get_fingerprint_md5() method.
    #
    def test_get_fingerprint_md5(self):
        for filename in self.certs:
            self.assertTrue(self.certs[filename].get_fingerprint_md5() == self.cert_properties[filename]['fingerprint_md5'])

    ##
    # Test the get_fingerprint_sha1() method.
    #
    def test_get_fingerprint_sha1(self):
        for filename in self.certs:
            self.assertTrue(self.certs[filename].get_fingerprint_sha1() == self.cert_properties[filename]['fingerprint_sha1'])

    ##
    # Test the get_fingerprint_sha256() method.
    #
    def test_get_fingerprint_sha256(self):
        for filename in self.certs:
            self.assertTrue(self.certs[filename].get_fingerprint_sha256() == self.cert_properties[filename]['fingerprint_sha256'])

    ##
    # Test the get_fingerprint_signature() method.
    #
    def test_get_fingerprint_signature(self):
        for filename in self.certs:
            self.assertTrue(self.certs[filename].get_fingerprint_signature() == self.cert_properties[filename]['fingerprint_signature'])

    ##
    # Test the get_fingerprint_version() method.
    #
    def test_get_fingerprint_version(self):
        for filename in self.certs:
            self.assertTrue(self.certs[filename].get_fingerprint_version() == self.cert_properties[filename]['fingerprint_version'])

    ##
    # Test the get_owner() method.
    #
    def test_get_owner(self):
        for filename in self.certs:
            owner = self.certs[filename].get_owner()
            self.assertTrue(owner['name'] == self.cert_properties[filename]['owner']['name'])
            self.assertTrue(owner['email'] == self.cert_properties[filename]['owner']['email'])
            self.assertTrue(owner['unit'] == self.cert_properties[filename]['owner']['unit'])
            self.assertTrue(owner['organization'] == self.cert_properties[filename]['owner']['organization'])
            self.assertTrue(owner['city'] == self.cert_properties[filename]['owner']['city'])
            self.assertTrue(owner['state'] == self.cert_properties[filename]['owner']['state'])
            self.assertTrue(owner['country'] == self.cert_properties[filename]['owner']['country'])
            self.assertTrue(owner['domain'] == self.cert_properties[filename]['owner']['domain'])
    ##
    # Test the get_issuer() method.
    #
    def test_get_issuer(self):
        for filename in self.certs:
            issuer = self.certs[filename].get_issuer()
            self.assertTrue(issuer['name'] == self.cert_properties[filename]['issuer']['name'])
            self.assertTrue(issuer['email'] == self.cert_properties[filename]['issuer']['email'])
            self.assertTrue(issuer['unit'] == self.cert_properties[filename]['issuer']['unit'])
            self.assertTrue(issuer['organization'] == self.cert_properties[filename]['issuer']['organization'])
            self.assertTrue(issuer['city'] == self.cert_properties[filename]['issuer']['city'])
            self.assertTrue(issuer['state'] == self.cert_properties[filename]['issuer']['state'])
            self.assertTrue(issuer['country'] == self.cert_properties[filename]['issuer']['country'])
            self.assertTrue(issuer['domain'] == self.cert_properties[filename]['issuer']['domain'])


if __name__ == '__main__':
    unittest.main()
