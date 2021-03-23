import unittest

from ninjadroid.parsers.cert import Cert, CertFingerprint, CertParticipant, CertValidity


class TestCert(unittest.TestCase):
    """
    Test Cert class.
    """

    def test_cert_as_dict(self):
        cert = Cert(
            filename="any-file-name",
            size=10,
            md5hash="any-file-md5",
            sha1hash="any-file-sha1",
            sha256hash="any-file-sha256",
            sha512hash="any-file-sha512",
            serial_number="any-serial-number",
            validity=CertValidity(
                valid_from="any-validity-from",
                valid_to="any-validity-to"
            ),
            fingerprint=CertFingerprint(
                md5="any-fingerprint-md5",
                sha1="any-fingerprint-sha1",
                sha256="any-fingerprint-sha256",
                signature="any-fingerprint-signature",
                version="any-fingerprint-version"
            ),
            owner=CertParticipant(
                name="any-owner-name",
                email="any-owner-email",
                unit="any-owner-unit",
                organization="any-owner-organization",
                city="any-owner-city",
                state="any-owner-state",
                country="any-owner-country",
                domain="any-owner-domain"
            ),
            issuer=CertParticipant(
                name="any-issuer-name",
                email="any-issuer-email",
                unit="any-issuer-unit",
                organization="any-issuer-organization",
                city="any-issuer-city",
                state="any-issuer-state",
                country="any-issuer-country",
                domain="any-issuer-domain"
            )
        )

        result = cert.as_dict()

        self.assertEqual(
            {
                "file": "any-file-name",
                "size": 10,
                "md5": "any-file-md5",
                "sha1": "any-file-sha1",
                "sha256": "any-file-sha256",
                "sha512": "any-file-sha512",
                "serial_number": "any-serial-number",
                "validity": {
                    "from": "any-validity-from",
                    "until": "any-validity-to"
                },
                "fingerprint": {
                    "md5": "any-fingerprint-md5",
                    "sha1": "any-fingerprint-sha1",
                    "sha256": "any-fingerprint-sha256",
                    "signature": "any-fingerprint-signature",
                    "version": "any-fingerprint-version"
                },
                "owner": {
                    "name": "any-owner-name",
                    "email": "any-owner-email",
                    "unit": "any-owner-unit",
                    "organization": "any-owner-organization",
                    "city": "any-owner-city",
                    "state": "any-owner-state",
                    "country": "any-owner-country",
                    "domain": "any-owner-domain"
                },
                "issuer": {
                    "name": "any-issuer-name",
                    "email": "any-issuer-email",
                    "unit": "any-issuer-unit",
                    "organization": "any-issuer-organization",
                    "city": "any-issuer-city",
                    "state": "any-issuer-state",
                    "country": "any-issuer-country",
                    "domain": "any-issuer-domain"
                }
            },
            result
        )


if __name__ == "__main__":
    unittest.main()
