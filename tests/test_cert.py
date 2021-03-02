from os.path import join
from parameterized import parameterized
import unittest
from unittest.mock import call, Mock, mock_open, patch
from tests.utils.popen import any_popen, assert_popen_called_once_with

from ninjadroid.errors.cert_parsing_error import CertParsingError
from ninjadroid.errors.parsing_error import ParsingError
from ninjadroid.parsers.cert import Cert


class TestCert(unittest.TestCase):
    """
    UnitTest for cert.py.

    RUN: python -m unittest -v tests.test_cert
    """

    FILE_NAME = "CERT.RSA"
    ANY_FILE_SIZE = 906
    ANY_FILE_MD5 = "5026e73a2f0d8091aaf7908cffbc425e"
    ANY_FILE_SHA1 = "37210614d362672e19cdd7940b7f5037de6cbcb8"
    ANY_FILE_SHA256 = "0ba1a5ba50b277bb37d05e8b9d2c6422aad49b90c08e7136d2d7c204ceaaf412"
    ANY_FILE_SHA512 = "e16ce3b471f10043be642472dc4f0156dccb434331c0c1ca19470b7dc0d025d4bb512fc5e77e78011e704b69fe0872e6fd7dee648e87401062f59149695f36f5"

    @staticmethod
    def any_file(
            mock_isfile: Mock,
            mock_access: Mock,
            mock_getsize: Mock,
            mock_md5: Mock,
            mock_sha1: Mock,
            mock_sha256: Mock,
            mock_sha512: Mock
    ):
        mock_isfile.return_value = True
        mock_access.return_value = True
        mock_getsize.return_value = TestCert.ANY_FILE_SIZE
        mock_md5.return_value.hexdigest.return_value = TestCert.ANY_FILE_MD5
        mock_sha1.return_value.hexdigest.return_value = TestCert.ANY_FILE_SHA1
        mock_sha256.return_value.hexdigest.return_value = TestCert.ANY_FILE_SHA256
        mock_sha512.return_value.hexdigest.return_value = TestCert.ANY_FILE_SHA512

    @patch('ninjadroid.parsers.cert.Popen')
    @patch('ninjadroid.parsers.cert.get_localzone')
    @patch('ninjadroid.parsers.file.sha512')
    @patch('ninjadroid.parsers.file.sha256')
    @patch('ninjadroid.parsers.file.sha1')
    @patch('ninjadroid.parsers.file.md5')
    @patch('ninjadroid.parsers.file.getsize')
    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    @patch("builtins.open", new_callable=mock_open)
    def test_init(
            self,
            mock_file,
            mock_isfile,
            mock_access,
            mock_getsize,
            mock_md5,
            mock_sha1,
            mock_sha256,
            mock_sha512,
            mock_get_localzone,
            mock_popen
    ):
        keytool_response = b"Owner: CN=OwnerName, OU=OwnerUnit, O=OwnerOrganization, L=OwnerCity, ST=OwnerState, C=OwnerCountry\n" \
                           b"Issuer: CN=IssuerName, OU=IssuerUnit, O=IssuerOrganization, L=IssuerCity, ST=IssuerState, C=IssuerCountry\n" \
                           b"Serial number: 558e7595\n" \
                           b"Valid from: Sat Jun 27 12:06:13 CEST 2015 until: Tue Feb 26 11:06:13 CET 2515\n" \
                           b"Certificate fingerprints:\n" \
                           b"\t MD5: 90:22:EF:0C:DB:C3:78:87:7B:C3:A3:6C:5A:68:E6:45\n" \
                           b"\t SHA1: 5A:C0:6C:32:63:7F:5D:BE:CA:F9:38:38:4C:FA:FF:ED:20:52:43:B6\n" \
                           b"\t SHA256: E5:15:CC:BC:5E:BF:B2:9D:A6:13:03:63:CF:19:33:FA:CE:AF:DC:ED:5D:2F:F5:98:7C:CE:37:13:64:4A:CF:77\n" \
                           b"Signature algorithm name: SHA1withRSA\n" \
                           b"Subject Public Key Algorithm: 1024-bit RSA key\n" \
                           b"Version: 3"
        mock_popen.return_value = any_popen(keytool_response)
        mock_get_localzone.return_value.localize.side_effect = ValueError()
        self.any_file(mock_isfile, mock_access, mock_getsize, mock_md5, mock_sha1, mock_sha256, mock_sha512)

        cert = Cert("any-file-path", "any-file-name")

        mock_file.assert_called_with("any-file-path", "rb")
        assert_popen_called_once_with(mock_popen, "keytool -printcert -file any-file-path")
        self.assertTrue(len(cert.get_raw_file()) > 0)
        self.assertEqual("any-file-name", cert.get_file_name())
        self.assertEqual(TestCert.ANY_FILE_SIZE, cert.get_size())
        self.assertEqual(TestCert.ANY_FILE_MD5, cert.get_md5())
        self.assertEqual(TestCert.ANY_FILE_SHA1, cert.get_sha1())
        self.assertEqual(TestCert.ANY_FILE_SHA256, cert.get_sha256())
        self.assertEqual(TestCert.ANY_FILE_SHA512, cert.get_sha512())
        self.assertEqual("558e7595", cert.get_serial_number())
        self.assertEqual(
            {
                "from": "Sat Jun 27 12:06:13 CEST 2015",
                "until": "Tue Feb 26 11:06:13 CET 2515",
            },
            cert.get_validity()
        )
        self.assertEqual("90:22:EF:0C:DB:C3:78:87:7B:C3:A3:6C:5A:68:E6:45", cert.get_fingerprint_md5())
        self.assertEqual("5A:C0:6C:32:63:7F:5D:BE:CA:F9:38:38:4C:FA:FF:ED:20:52:43:B6", cert.get_fingerprint_sha1())
        self.assertEqual("E5:15:CC:BC:5E:BF:B2:9D:A6:13:03:63:CF:19:33:FA:CE:AF:DC:ED:5D:2F:F5:98:7C:CE:37:13:64:4A:CF:77", cert.get_fingerprint_sha256())
        self.assertTrue("SHA1withRSA", cert.get_fingerprint_signature())
        self.assertEqual("3", cert.get_fingerprint_version())
        self.assertEqual(
            {
                "name": "OwnerName",
                "email": "",
                "unit": "OwnerUnit",
                "organization": "OwnerOrganization",
                "city": "OwnerCity",
                "state": "OwnerState",
                "country": "OwnerCountry",
                "domain": "",
            },
            cert.get_owner()
        )
        self.assertEqual(
            {
                "name": "IssuerName",
                "email": "",
                "unit": "IssuerUnit",
                "organization": "IssuerOrganization",
                "city": "IssuerCity",
                "state": "IssuerState",
                "country": "IssuerCountry",
                "domain": "",
            },
            cert.get_issuer()
        )

    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    def test_init_with_non_existing_file(self, mock_isfile, mock_access):
        mock_isfile.return_value = False
        mock_access.return_value = True
        with self.assertRaises(ParsingError):
            Cert("any-file-path", "any-file-name")

    @patch('ninjadroid.parsers.file.access')
    @patch('ninjadroid.parsers.file.isfile')
    def test_init_with_non_readable_file(self, mock_isfile, mock_access):
        mock_isfile.return_value = True
        mock_access.return_value = False
        with self.assertRaises(ParsingError):
            Cert("any-file-path", "any-file-name")

    def test_integration_init(self):
        cert = Cert(join("tests", "data", TestCert.FILE_NAME), TestCert.FILE_NAME)

        self.assertTrue(cert is not None)
        self.assertTrue(type(cert) is Cert)

    def test_integration_init_with_non_cert_file(self):
        with self.assertRaises(CertParsingError):
            Cert(join("tests", "data", "Example.apk"))
            Cert(join("tests", "data", "AndroidManifest.xml"))
            Cert(join("tests", "data", "classes.dex"))

    @patch('ninjadroid.parsers.cert.Popen')
    def test_extract_cert_info(self, mock_popen):
        mock_popen.return_value = any_popen(b"any-raw-file")

        raw_file = Cert._extract_cert_info("any-file-path")

        assert_popen_called_once_with(mock_popen, "keytool -printcert -file any-file-path")
        self.assertEqual("any-raw-file", raw_file)

    @patch('ninjadroid.parsers.cert.datetime')
    @patch('ninjadroid.parsers.cert.get_localzone')
    def test_extract_validity(self, mock_get_localzone, mock_datetime):
        mock_astimezone = Mock()
        mock_get_localzone.return_value.localize.return_value.astimezone.return_value = mock_astimezone
        mock_astimezone.strftime.side_effect = ["2015-06-27 10:06:13Z", "2515-02-26 10:06:13Z"]
        mock_datetime.strptime.return_value = Mock()

        validity = Cert._extract_validity("Valid from: Sat Jun 27 12:06:13 CEST 2015 until: Tue Feb 26 11:06:13 CET 2515")

        mock_datetime.strptime.assert_has_calls([
            call("Sat Jun 27 12:06:13 CEST 2015", "%a %b %d %H:%M:%S %Z %Y"),
            call("Tue Feb 26 11:06:13 CET 2515", "%a %b %d %H:%M:%S %Z %Y")
        ])
        mock_astimezone.strftime.assert_has_calls([
            call("%Y-%m-%d %H:%M:%SZ"),
            call("%Y-%m-%d %H:%M:%SZ")
        ])
        self.assertEqual(
            {
                "from": "2015-06-27 10:06:13Z",
                "until": "2515-02-26 10:06:13Z"
            },
            validity
        )


    @patch('ninjadroid.parsers.cert.get_localzone')
    def test_extract_validity_when_localize_fails(self, mock_get_localzone):
        mock_get_localzone.return_value.localize.side_effect = ValueError()

        validity = Cert._extract_validity("Valid from: Sat Jun 27 12:06:13 CEST 2015 until: Tue Feb 26 11:06:13 CET 2515")

        self.assertEqual(
            {
                "from": "Sat Jun 27 12:06:13 CEST 2015",
                "until": "Tue Feb 26 11:06:13 CET 2515",
            },
            validity
        )

    def test_extract_owner(self):
        owner = Cert._extract_owner("Owner: CN=Name, OU=Unit, O=Organization, L=City, ST=State, C=Country")

        self.assertEqual(
            {
                "name": "Name",
                "email": "",
                "unit": "Unit",
                "organization": "Organization",
                "city": "City",
                "state": "State",
                "country": "Country",
                "domain": "",
            },
            owner
        )

    def test_extract_issuer(self):
        issuer = Cert._extract_issuer("Issuer: CN=Name, OU=Unit, O=Organization, L=City, ST=State, C=Country")

        self.assertEqual(
            {
                "name": "Name",
                "email": "",
                "unit": "Unit",
                "organization": "Organization",
                "city": "City",
                "state": "State",
                "country": "Country",
                "domain": "",
            },
            issuer
        )

    @parameterized.expand([
        ["Serial number: any-serial-number", "^Serial number: (.*)$", "any-serial-number"],
        ["Valid from: any-from until: any-until", "^Valid (.*)$", "from: any-from until: any-until"],
        ["from: any-from until: any-until", "^from: (.*)until: ", "any-from"],
        ["from: any-from until: any-until", "until: (.*)$", "any-until"],
        ["\tMD5: any-md5", "^\tMD5: (.*)$", "any-md5"],
        ["\tSHA1: any-sha1", "^\tSHA1: (.*)$", "any-sha1"],
        ["\tSHA256: any-sha256", "^\tSHA256: (.*)$", "any-sha256"],
        ["Owner: any-owner", "^Owner: (.*)$", "any-owner"],
        ["CN=any-owner-name\n", "^CN=(.*)", "any-owner-name"],
    ])
    def test_extract_string_pattern(self, string, pattern, expected):
        result = Cert._extract_string_pattern(string, pattern)

        self.assertEqual(expected, result)

    @parameterized.expand([
        ["META-INF/CERT.RSA", True],
        ["META-INF/CERT.DSA", True],
        ["META-INF/WHATEVER.RSA", True],
        ["META-INF/WHATEVER.DSA", False],
        ["META-INF/NON_CERT.apk", False],
        ["META-INF/NON_CERT.dex", False],
        ["META-INF/NON_CERT.so", False],
        ["AndroidManifest.xml", False],
        ["classes.dex", False],
        ["Example.apk", False]
    ])
    def test_looks_like_a_cert(self, filename, expected):
        result = Cert.looks_like_a_cert(filename)

        self.assertEqual(expected, result)

    def test_integration_dump(self):
        cert = Cert(join("tests", "data", TestCert.FILE_NAME), TestCert.FILE_NAME)

        dump = cert.dump()

        self.assertEqual(TestCert.FILE_NAME, dump["file"])
        self.assertEqual(TestCert.ANY_FILE_SIZE, dump["size"])
        self.assertEqual(TestCert.ANY_FILE_MD5, dump["md5"])
        self.assertEqual(TestCert.ANY_FILE_SHA1, dump["sha1"])
        self.assertEqual(TestCert.ANY_FILE_SHA256, dump["sha256"])
        self.assertEqual(TestCert.ANY_FILE_SHA512, dump["sha512"])
        self.assertEqual("558e7595", dump["serial_number"])


if __name__ == "__main__":
    unittest.main()
