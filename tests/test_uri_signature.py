from parameterized import parameterized
import unittest

from ninjadroid.signatures.uri_signature import UriSignature


class TestUriSignature(unittest.TestCase):
    """
    UnitTest for URI.py.

    RUN: python -m unittest -v tests.test_uri_signature
    """

    uri = UriSignature()

    @parameterized.expand([
        ["http://www.domain.com", True],
        ["https://www.domain.com", True],
        ["http://domain.com", True],
        ["http://www.host.domain.com", True],
        ["http://www.domain.com:80", True],
        ["ftp://domain.com", True],
        ["ftp://domain.com:21", True],
        ["sftp://domain.com", True],
        ["sftp://domain.com:21", True],
        ["ftp://ftp.domain.com", True],
        ["www.domain.com", True],
        ["domain.com", True],
        ["http://www.host.domain.org/index.html", True],
        ["http://www.host.domain.org:80/index.html", True],
        ["http://www.host.domain.org/path/to/index.html", True],
        ["http://www.host.domain.org/path/to/index.html#foo", True],
        ["http://www.host.domain.org/path/to/page.php", True],
        ["http://www.host.domain.org/path/to/page.php?query=value", True],
        ["http://www.host.domain.org/path/to/page.php?a=1&b=2", True],
        ["http://www.host.domain.org/path/to/page.php?a=1&amp;b=2", True],
        ["http://www.host.domain.org/path/to/page.php?a=1&b=2#foo", True],
        ["http://www.host.domain.org:8080/path/to/page.php?a=1&b=2&c=3#foo", True],
        ["www.host.domain.net:8080/path/to/page.php?a=1&b=2&c=3#foo", True],
        ["http://www.host.domain.net/page", True],
        ["http://www.host.domain.net/#foo", True],
        ["http://127.0.0.1", True],
        ["http://127.0.0.1:80", True],
        ["http://127.0.0.1:8080", True],
        ["127.0.0.1", True],
        ["127.0.0.1:80", True],
        ["127.0.0.1:8080", True],
        ["aaaa://www.domain.com", False],
        ["http:////www.domain.com", False],
        ["////www.domain.com", False],
        ["www.domain", False],
        ["127.0.0.1.1.2.3.4", False],
        ["aaaa://127.0.0.1", False],
        ["http:////127.0.0.1", False],
        ["////127.0.0.1", False],
        ["VersionConstants.java", False],
    ])
    def test_is_valid(self, raw_string, expected):
        result = self.uri.is_valid(raw_string)

        self.assertEqual(expected, result)

    @parameterized.expand([
        ["  http://www.domain.com  ", "http://www.domain.com"],
        ["  www.domain.com  ", "www.domain.com"],
        [" http://www.host.domain.com/index.html", "http://www.host.domain.com/index.html"],
        ["  https://www.host.domain.org/path/to/page.php?query=value  ", "https://www.host.domain.org/path/to/page.php?query=value"],
        ["  https://www.host.domain.org/path/to/page.php?a=1&b=2#foo  ", "https://www.host.domain.org/path/to/page.php?a=1&b=2#foo"],
        ["AB  www.domain.com  YZ", "www.domain.com"],
        [" http https://www.host.domain.com/path/to/page.php?a=1&b=2#foo & & #bar ", "https://www.host.domain.com/path/to/page.php?a=1&b=2#foo"],
        ["http://host.domain.net/path/page", "http://host.domain.net/path/page"],
        ["4http://www.host.domain.net/images/pic.png", "http://www.host.domain.net/images/pic.png"],
        ["<a href=\"http://www.host.domain.com\" target=\"_blank\">", "http://www.host.domain.com"],
        ["#http://schemas.android.com/apk/res/", "http://schemas.android.com/apk/res/"],
        ["Publisher ID is not set!  To serve ads you must set your publisher ID assigned from www.admob.com.  Either add it to AndroidManifest.xml under the <application> tag or call", "www.admob.com"],
        ["iSETUP ERROR:  Cannot use the sample publisher ID (a1496ced2842262).  Yours is available on www.admob.com.", "www.admob.com"],
        [" - no match - ", None],
        ["chmod 777", None],
        ["Mozilla/5.0 (Linux; U; Android %s) AppleWebKit/525.10+ (KHTML, like Gecko) Version/3.0.4 Mobile Safari/523.12.2 (AdMob-ANDROID-%s)", None],
    ])
    def test_search(self, raw_string, expected):
        match = self.uri.search(raw_string)

        self.assertEqual(expected, match)


if __name__ == '__main__':
    unittest.main()
