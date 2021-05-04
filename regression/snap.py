from regression import run, RegressionSuite


class SnapRegressionSuite(RegressionSuite):
    """
    Snap regression tests.
    """

    BASE_PATH = "/snap/bin/"  # NOTE: to avoid collision with native install/regression...

    def set_up(self):
        # self.execute_command("make build-snap")
        # self.execute_command("make install-snap")
        pass

    def tear_down(self):
        self.execute_command("rm -r output/")

    @RegressionSuite.test
    def show_summary(self):
        expected = self.read_plain_text_file("regression/expected/summary.txt")

        result = self.execute_command(self.BASE_PATH + "ninjadroid regression/data/Example.apk")

        self.assert_plain_text_equal(expected, result)

    @RegressionSuite.test
    def show_extended(self):
        expected = self.read_plain_text_file(
            "regression/expected/extended.txt",
            overrides={
                22: "\t\tsignature: SHA1withRSA (weak)"
            }
        )

        result = self.execute_command(self.BASE_PATH + "ninjadroid regression/data/Example.apk --all")

        self.assert_plain_text_equal(expected, result)

    @RegressionSuite.test
    def show_json_summary(self):
        expected = self.read_json_file("regression/expected/summary.json")

        result = self.execute_command(self.BASE_PATH + "ninjadroid regression/data/Example.apk --json")

        self.assert_json_equal(expected, result)

    @RegressionSuite.test
    def show_json_extended(self):
        expected = self.read_json_file(
            "regression/expected/extended.json",
            overrides={
                "cert": {
                    "fingerprint": {
                        "signature": "SHA1withRSA (weak)"
                    }
                },

            }
        )

        result = self.execute_command(self.BASE_PATH + "ninjadroid regression/data/Example.apk --all --json")

        self.assert_json_equal(expected, result)

    @RegressionSuite.test
    def extract_extended(self):
        expected = self.read_plain_text_file(
            "regression/expected/extract.txt",
            overrides={
                18: "25ada2132e42197adfaccd8293c8363a  output/report-Example.json"
            }
        )

        self.execute_command(self.BASE_PATH + "ninjadroid regression/data/Example.apk --all --extract output/")
        # NOTE: the .jar file checksum changes at every run...
        result = self.execute_command("find output/ -type f -exec md5sum '{}' + | grep -v Example.jar")

        self.assert_plain_text_equal(expected, result)


if __name__ == "__main__":
    run(suite = SnapRegressionSuite())
