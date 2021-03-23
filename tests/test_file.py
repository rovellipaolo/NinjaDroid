import unittest

from tests.utils.file import any_file


class TestFile(unittest.TestCase):
    """
    Test File class.
    """

    def test_file_as_dict(self):
        file = any_file(
            filename="any-file-name",
            size=10,
            md5="any-file-md5",
            sha1="any-file-sha1",
            sha256="any-file-sha256",
            sha512="any-file-sha512"
        )

        result = file.as_dict()

        self.assertEqual(
            {
                "file": "any-file-name",
                "size": 10,
                "md5": "any-file-md5",
                "sha1": "any-file-sha1",
                "sha256": "any-file-sha256",
                "sha512": "any-file-sha512",
            },
            result
        )


if __name__ == "__main__":
    unittest.main()
