import unittest
from unittest.mock import call, Mock, patch
from parameterized import parameterized
from tests.utils.file import any_file, any_file_parser, any_file_parser_failure, assert_file_equal, \
    assert_file_parser_called_once_with
from tests.utils.popen import any_popen, assert_popen_called_once_with

from ninjadroid.parsers.cert import CertFingerprint, CertParticipant, CertParser, CertParsingError, CertValidity
from ninjadroid.parsers.file import FileParsingError


# pylint: disable=line-too-long
class TestCertParser(unittest.TestCase):
    """
    Test Cert parser.
    """

    sut = CertParser()

    @patch('ninjadroid.parsers.cert.Popen')
    @patch('ninjadroid.parsers.cert.get_localzone')
    @patch('ninjadroid.parsers.cert.FileParser')
    def test_init(self, mock_file_parser, mock_get_localzone, mock_popen):
        file = any_file()
        mock_parser_instance = any_file_parser(file=file)
        mock_file_parser.return_value = mock_parser_instance
        mock_popen.return_value = any_popen(
            response=b"Owner: CN=OwnerName, OU=OwnerUnit, O=OwnerOrganization, L=OwnerCity, ST=OwnerState, C=OwnerCountry\n" \
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
        )
        mock_get_localzone.return_value.localize.side_effect = ValueError()

        cert = self.sut.parse("any-file-path", "any-file-name")

        assert_file_parser_called_once_with(mock_parser_instance, filepath="any-file-path", filename="any-file-name")
        assert_popen_called_once_with(mock_popen, "keytool -printcert -file any-file-path")
        assert_file_equal(self, expected=file, actual=cert)
        self.assertEqual("558e7595", cert.get_serial_number())
        self.assertEqual(
            CertValidity(valid_from="Sat Jun 27 12:06:13 CEST 2015", valid_to="Tue Feb 26 11:06:13 CET 2515"),
            cert.get_validity()
        )
        self.assertEqual(
            CertFingerprint(
                md5="90:22:EF:0C:DB:C3:78:87:7B:C3:A3:6C:5A:68:E6:45",
                sha1="5A:C0:6C:32:63:7F:5D:BE:CA:F9:38:38:4C:FA:FF:ED:20:52:43:B6",
                sha256="E5:15:CC:BC:5E:BF:B2:9D:A6:13:03:63:CF:19:33:FA:CE:AF:DC:ED:5D:2F:F5:98:7C:CE:37:13:64:4A:CF:77",
                signature="SHA1withRSA",
                version="3"
            ),
            cert.get_fingerprint()
        )
        self.assertEqual(
            CertParticipant(
                name="OwnerName",
                email="",
                unit="OwnerUnit",
                organization="OwnerOrganization",
                city="OwnerCity",
                state="OwnerState",
                country="OwnerCountry",
                domain=""
            ),
            cert.get_owner()
        )
        self.assertEqual(
            CertParticipant(
                name="IssuerName",
                email="",
                unit="IssuerUnit",
                organization="IssuerOrganization",
                city="IssuerCity",
                state="IssuerState",
                country="IssuerCountry",
                domain=""
            ),
            cert.get_issuer()
        )

    @patch('ninjadroid.parsers.cert.Popen')
    @patch('ninjadroid.parsers.cert.FileParser')
    def test_parse_fails_when_file_parser_fails(self, mock_file_parser, mock_popen):
        mock_parser_instance = any_file_parser_failure()
        mock_file_parser.return_value = mock_parser_instance

        with self.assertRaises(FileParsingError):
            self.sut.parse("any-file-path", "any-file-name")
        assert_file_parser_called_once_with(mock_parser_instance, filepath="any-file-path", filename="any-file-name")
        mock_popen.assert_not_called()

    @patch('ninjadroid.parsers.cert.Popen')
    @patch('ninjadroid.parsers.cert.FileParser')
    def test_parse_fails_when_keytool_fails(self, mock_file_parser, mock_popen):
        mock_file_parser.return_value = any_file_parser(file=any_file())
        mock_popen.return_value = any_popen(b"keytool error")

        with self.assertRaises(CertParsingError):
            self.sut.parse("any-file-path", "any-file-name")
        assert_popen_called_once_with(mock_popen, "keytool -printcert -file any-file-path")

    @patch('ninjadroid.parsers.cert.Popen')
    def test_parse_cert(self, mock_popen):
        mock_popen.return_value = any_popen(b"any-cert")

        cert = CertParser.parse_cert("any-file-path")

        assert_popen_called_once_with(mock_popen, "keytool -printcert -file any-file-path")
        self.assertEqual("any-cert", cert)

    @patch('ninjadroid.parsers.cert.datetime')
    @patch('ninjadroid.parsers.cert.get_localzone')
    def test_parse_validity(self, mock_get_localzone, mock_datetime):
        mock_astimezone = Mock()
        mock_get_localzone.return_value.localize.return_value.astimezone.return_value = mock_astimezone
        mock_astimezone.strftime.side_effect = ["2015-06-27 10:06:13Z", "2515-02-26 10:06:13Z"]
        mock_datetime.strptime.return_value = Mock()

        validity = CertParser.parse_validity(
            "Valid from: Sat Jun 27 12:06:13 CEST 2015 until: Tue Feb 26 11:06:13 CET 2515"
        )

        mock_datetime.strptime.assert_has_calls([
            call("Sat Jun 27 12:06:13 CEST 2015", "%a %b %d %H:%M:%S %Z %Y"),
            call("Tue Feb 26 11:06:13 CET 2515", "%a %b %d %H:%M:%S %Z %Y")
        ])
        mock_astimezone.strftime.assert_has_calls([
            call("%Y-%m-%d %H:%M:%SZ"),
            call("%Y-%m-%d %H:%M:%SZ")
        ])
        self.assertEqual(CertValidity(valid_from="2015-06-27 10:06:13Z", valid_to="2515-02-26 10:06:13Z"), validity)


    @patch('ninjadroid.parsers.cert.get_localzone')
    def test_parse_validity_when_localize_fails(self, mock_get_localzone):
        mock_get_localzone.return_value.localize.side_effect = ValueError()

        validity = CertParser.parse_validity(
            "Valid from: Sat Jun 27 12:06:13 CEST 2015 until: Tue Feb 26 11:06:13 CET 2515"
        )

        self.assertEqual(
            CertValidity(valid_from="Sat Jun 27 12:06:13 CEST 2015", valid_to="Tue Feb 26 11:06:13 CET 2515"),
            validity
        )

    def test_parse_fingerprint(self):
        fingerprint = CertParser.parse_fingerprint(
            "Certificate fingerprints:\n"
            "\t MD5: any-md5\n"
            "\t SHA1: any-sha1\n"
            "\t SHA256: any-sha256\n"
            "Signature algorithm name: any-signature\n"
            "Version: any-version"
        )

        self.assertEqual(
            CertFingerprint(
                md5="any-md5",
                sha1="any-sha1",
                sha256="any-sha256",
                signature="any-signature",
                version="any-version"
            ),
            fingerprint
        )

    def test_parse_participant(self):
        owner = CertParser.parse_participant(
            "ParticipantLabel: CN=any-name, OU=any-unit, O=any-organization, L=any-city, ST=any-state, C=any-country",
            pattern="^ParticipantLabel: (.*)$"
        )

        self.assertEqual(
            CertParticipant(
                name="any-name",
                email="",
                unit="any-unit",
                organization="any-organization",
                city="any-city",
                state="any-state",
                country="any-country",
                domain=""
            ),
            owner
        )

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
    def test_looks_like_cert(self, filename, expected):
        result = CertParser.looks_like_cert(filename)

        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
