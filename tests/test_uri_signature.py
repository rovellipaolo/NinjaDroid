import unittest

from ninjadroid.signatures.uri_signature import URISignature


class TestURISignature(unittest.TestCase):
    """
    UnitTest for URI.py.

    RUN: python -m unittest -v tests.test_uri_signature
    """

    valid_urls = [
        "http://www.domain.com",
        "https://www.domain.com",
        "http://domain.com",
        "http://www.host.domain.com",
        "http://www.domain.com:80",
        "ftp://domain.com",
        "ftp://domain.com:21",
        "sftp://domain.com",
        "sftp://domain.com:21",
        "ftp://ftp.domain.com",
        "www.domain.com",
        "domain.com",
        "http://www.host.domain.org/index.html",
        "http://www.host.domain.org:80/index.html",
        "http://www.host.domain.org/path/to/index.html",
        "http://www.host.domain.org/path/to/index.html#foo",
        "http://www.host.domain.org/path/to/page.php",
        "http://www.host.domain.org/path/to/page.php?query=value",
        "http://www.host.domain.org/path/to/page.php?a=1&b=2",
        "http://www.host.domain.org/path/to/page.php?a=1&amp;b=2",
        "http://www.host.domain.org/path/to/page.php?a=1&b=2#foo",
        "http://www.host.domain.org:8080/path/to/page.php?a=1&b=2&c=3#foo",
        "www.host.domain.net:8080/path/to/page.php?a=1&b=2&c=3#foo",
        "http://www.host.domain.net/page",
        "http://www.host.domain.net/#foo",
        "http://127.0.0.1",
        "http://127.0.0.1:80",
        "http://127.0.0.1:8080",
        "127.0.0.1",
        "127.0.0.1:80",
        "127.0.0.1:8080",
    ]

    invalid_urls = [
        "aaaa://www.domain.com",
        "http:////www.domain.com",
        "////www.domain.com",
        "www.domain",
        "127.0.0.1.1.2.3.4",
        "aaaa://127.0.0.1",
        "http:////127.0.0.1",
        "////127.0.0.1",
        "VersionConstants.java"
    ]

    strings_containing_urls = {
        '  http://www.domain.com  ': "http://www.domain.com",
        '  www.domain.com  ': "www.domain.com",
        ' http://www.host.domain.com/index.html': "http://www.host.domain.com/index.html",
        '  https://www.host.domain.org/path/to/page.php?query=value  ': "https://www.host.domain.org/path/to/page.php?query=value",
        '  https://www.host.domain.org/path/to/page.php?a=1&b=2#foo  ': "https://www.host.domain.org/path/to/page.php?a=1&b=2#foo",
        'AB  www.domain.com  YZ': "www.domain.com",
        ' http https://www.host.domain.com/path/to/page.php?a=1&b=2#foo & & #bar ': "https://www.host.domain.com/path/to/page.php?a=1&b=2#foo",
        '"http://host.domain.net/path/page': "http://host.domain.net/path/page",
        '4http://www.host.domain.net/images/pic.png': "http://www.host.domain.net/images/pic.png",
        '<a href="http://www.host.domain.com" target="_blank">': "http://www.host.domain.com",
        "#http://schemas.android.com/apk/res/": "http://schemas.android.com/apk/res/",
        'Publisher ID is not set!  To serve ads you must set your publisher ID assigned from www.admob.com.  Either add it to AndroidManifest.xml under the <application> tag or call': "www.admob.com",
        'iSETUP ERROR:  Cannot use the sample publisher ID (a1496ced2842262).  Yours is available on www.admob.com.': "www.admob.com",
    }

    @classmethod
    def setUpClass(cls):
        cls.uri = URISignature()

    def test_is_valid(self):
        for url in TestURISignature.valid_urls:
            is_valid = self.uri.is_valid(url)

            self.assertTrue(is_valid, "URI " + url + " should be valid")

        for url in TestURISignature.invalid_urls:
            is_valid = self.uri.is_valid(url)

            self.assertFalse(is_valid, "URI " + url + " should not be valid")
        pass

    def test_get_matches_in_string(self):
        for string in TestURISignature.strings_containing_urls:
            matches = self.uri.get_matches_in_string(string)

            self.assertEqual(TestURISignature.strings_containing_urls[string], matches)


if __name__ == '__main__':
    unittest.main()
