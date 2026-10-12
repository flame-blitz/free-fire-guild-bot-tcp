import unittest

from network_utils import parse_host_port


class ParseHostPortTests(unittest.TestCase):
    def test_ipv4_endpoint(self):
        self.assertEqual(parse_host_port("10.20.30.40:8080"), ("10.20.30.40", 8080))

    def test_url_endpoint(self):
        self.assertEqual(parse_host_port("https://game.example:443"), ("game.example", 443))

    def test_bracketed_ipv6_endpoint(self):
        self.assertEqual(parse_host_port("[2001:db8::1]:9000"), ("2001:db8::1", 9000))

    def test_unbracketed_ipv6_with_port(self):
        self.assertEqual(parse_host_port("2001:db8::1:9000"), ("2001:db8::1", 9000))

    def test_rejects_missing_or_invalid_port(self):
        for endpoint in ("", "localhost", "localhost:nope", "localhost:0", "localhost:65536"):
            with self.subTest(endpoint=endpoint):
                with self.assertRaises(ValueError):
                    parse_host_port(endpoint)


if __name__ == "__main__":
    unittest.main()
