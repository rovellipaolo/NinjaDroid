import unittest

from ninjadroid.parsers.apk import APK
from ninjadroid.parsers.cert import Cert, CertFingerprint, CertParticipant, CertValidity
from ninjadroid.parsers.dex import Dex
from ninjadroid.parsers.manifest import AndroidManifest, AppSdk, AppVersion
from tests.utils.file import any_file


class TestAPK(unittest.TestCase):
    """
    Test APK class.
    """

    def test_apk_as_dict(self):
        apk = APK(
            filename="any-apk-file-name",
            size=10,
            md5hash="any-apk-file-md5",
            sha1hash="any-apk-file-sha1",
            sha256hash="any-apk-file-sha256",
            sha512hash="any-apk-file-sha512",
            app_name="any-app-name",
            cert=Cert(
                filename="any-cert-file-name",
                size=20,
                md5hash="any-cert-file-md5",
                sha1hash="any-cert-file-sha1",
                sha256hash="any-cert-file-sha256",
                sha512hash="any-cert-file-sha512",
                serial_number="any-cert-serial-number",
                validity=CertValidity(
                    valid_from="any-cert-validity-from",
                    valid_to="any-cert-validity-to"
                ),
                fingerprint=CertFingerprint(
                    md5="any-cert-fingerprint-md5",
                    sha1="any-cert-fingerprint-sha1",
                    sha256="any-cert-fingerprint-sha256",
                    signature="any-cert-fingerprint-signature",
                    version="any-cert-fingerprint-version"
                ),
                owner=CertParticipant(
                    name="any-cert-owner-name",
                    email="any-cert-owner-email",
                    unit="any-cert-owner-unit",
                    organization="any-cert-owner-organization",
                    city="any-cert-owner-city",
                    state="any-cert-owner-state",
                    country="any-cert-owner-country",
                    domain="any-cert-owner-domain"
                ),
                issuer=CertParticipant(
                    name="any-cert-issuer-name",
                    email="any-cert-issuer-email",
                    unit="any-cert-issuer-unit",
                    organization="any-cert-issuer-organization",
                    city="any-cert-issuer-city",
                    state="any-cert-issuer-state",
                    country="any-cert-issuer-country",
                    domain="any-cert-issuer-domain"
                )
            ),
            manifest=AndroidManifest(
                filename="any-manifest-file-name",
                size=30,
                md5hash="any-manifest-file-md5",
                sha1hash="any-manifest-file-sha1",
                sha256hash="any-manifest-file-sha256",
                sha512hash="any-manifest-file-sha512",
                package_name="any-package-name",
                version=AppVersion(code=1, name="any-version-name"),
                sdk=AppSdk(min_version="10", target_version="15", max_version="20"),
                permissions=[],
                activities=[],
                services=[],
                receivers=[]
            ),
            dex_files=[
                Dex(
                    filename="any-dex-file-name",
                    size=40,
                    md5hash="any-dex-file-md5",
                    sha1hash="any-dex-file-sha1",
                    sha256hash="any-dex-file-sha256",
                    sha512hash="any-dex-file-sha512",
                    strings=[],
                    urls=[],
                    shell_commands=[],
                    custom_signatures=[]
                )
            ],
            other_files=[
                any_file(
                    filename="any-resource-file-name",
                    size=50,
                    md5="any-resource-file-md5",
                    sha1="any-resource-file-sha1",
                    sha256="any-resource-file-sha256",
                    sha512="any-resource-file-sha512"
                )
            ]
        )

        result = apk.as_dict()

        self.assertEqual(
            {
                "file": "any-apk-file-name",
                "size": 10,
                "md5": "any-apk-file-md5",
                "sha1": "any-apk-file-sha1",
                "sha256": "any-apk-file-sha256",
                "sha512": "any-apk-file-sha512",
                "name": "any-app-name",
                "cert": {
                    "file": "any-cert-file-name",
                    "size": 20,
                    "md5": "any-cert-file-md5",
                    "sha1": "any-cert-file-sha1",
                    "sha256": "any-cert-file-sha256",
                    "sha512": "any-cert-file-sha512",
                    "serial_number": "any-cert-serial-number",
                    "validity": {
                        "from": "any-cert-validity-from",
                        "until": "any-cert-validity-to"
                    },
                    "fingerprint": {
                        "md5": "any-cert-fingerprint-md5",
                        "sha1": "any-cert-fingerprint-sha1",
                        "sha256": "any-cert-fingerprint-sha256",
                        "signature": "any-cert-fingerprint-signature",
                        "version": "any-cert-fingerprint-version"
                    },
                    "owner": {
                        "name": "any-cert-owner-name",
                        "email": "any-cert-owner-email",
                        "unit": "any-cert-owner-unit",
                        "organization": "any-cert-owner-organization",
                        "city": "any-cert-owner-city",
                        "state": "any-cert-owner-state",
                        "country": "any-cert-owner-country",
                        "domain": "any-cert-owner-domain"
                    },
                    "issuer": {
                        "name": "any-cert-issuer-name",
                        "email": "any-cert-issuer-email",
                        "unit": "any-cert-issuer-unit",
                        "organization": "any-cert-issuer-organization",
                        "city": "any-cert-issuer-city",
                        "state": "any-cert-issuer-state",
                        "country": "any-cert-issuer-country",
                        "domain": "any-cert-issuer-domain"
                    }
                },
                "manifest": {
                    "file": "any-manifest-file-name",
                    "size": 30,
                    "md5": "any-manifest-file-md5",
                    "sha1": "any-manifest-file-sha1",
                    "sha256": "any-manifest-file-sha256",
                    "sha512": "any-manifest-file-sha512",
                    "package": "any-package-name",
                    "version": {
                        "code": 1,
                        "name": "any-version-name"
                    },
                    "sdk": {
                        "min": "10",
                        "target": "15",
                        "max": "20"
                    },
                    "permissions": []
                },
                "dex": [
                    {
                        "file": "any-dex-file-name",
                        "size": 40,
                        "md5": "any-dex-file-md5",
                        "sha1": "any-dex-file-sha1",
                        "sha256": "any-dex-file-sha256",
                        "sha512": "any-dex-file-sha512",
                        "strings": [],
                        "urls": [],
                        "shell_commands": []
                    }
                ],
                "other": [
                    {
                        "file": "any-resource-file-name",
                        "size": 50,
                        "md5": "any-resource-file-md5",
                        "sha1": "any-resource-file-sha1",
                        "sha256": "any-resource-file-sha256",
                        "sha512": "any-resource-file-sha512",
                    }
                ]
            },
            result
        )


if __name__ == "__main__":
    unittest.main()
