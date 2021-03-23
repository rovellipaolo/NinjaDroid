import unittest

from ninjadroid.parsers.dex import Dex


class TestDex(unittest.TestCase):
    """
    Test Dex class.
    """

    def test_dex_as_dict(self):
        dex = Dex(
            filename="any-file-name",
            size=10,
            md5hash="any-file-md5",
            sha1hash="any-file-sha1",
            sha256hash="any-file-sha256",
            sha512hash="any-file-sha512",
            strings=["any-command", "any-string", "any-url"],
            urls=["any-url"],
            shell_commands=["any-command"],
            custom_signatures=[]
        )

        result = dex.as_dict()

        self.assertEqual(
            {
                "file": "any-file-name",
                "size": 10,
                "md5": "any-file-md5",
                "sha1": "any-file-sha1",
                "sha256": "any-file-sha256",
                "sha512": "any-file-sha512",
                "strings": ["any-command", "any-string", "any-url"],
                "urls": ["any-url"],
                "shell_commands": ["any-command"]
            },
            result
        )


if __name__ == "__main__":
    unittest.main()
