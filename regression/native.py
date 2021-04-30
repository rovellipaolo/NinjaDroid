from regression import run, RegressionSuite


class NativeRegressionSuite(RegressionSuite):
    """
    Native regression tests.
    """

    def set_up(self):
        # self.execute_command("make build")
        # self.execute_command("make install")
        pass

    def tear_down(self):
        self.execute_command("rm -r output/")

    @RegressionSuite.test
    def show_summary(self):
        expected = self.read_plain_text_file("regression/expected/summary.txt")

        result = self.execute_command("ninjadroid regression/data/Example.apk")

        self.assert_plain_text_equal(expected, result)

    @RegressionSuite.test
    def show_extended(self):
        expected = self.read_plain_text_file("regression/expected/extended.txt")

        result = self.execute_command("ninjadroid regression/data/Example.apk --all")

        self.assert_plain_text_equal(expected, result)

    @RegressionSuite.test
    def show_json_summary(self):
        expected = self.read_json_file("regression/expected/summary.json")

        result = self.execute_command("ninjadroid regression/data/Example.apk --json")

        self.assert_json_equal(expected, result)

    @RegressionSuite.test
    def show_json_extended(self):
        expected = self.read_json_file("regression/expected/extended.json")

        result = self.execute_command("ninjadroid regression/data/Example.apk --all --json")

        self.assert_json_equal(expected, result)

    @RegressionSuite.test
    def extract_extended(self):
        expected = self.read_plain_text_file("regression/expected/extract.txt")

        self.execute_command("ninjadroid regression/data/Example.apk --all --extract output/")
        # NOTE: the .jar file checksum changes at every run...
        result = self.execute_command("find output/ -type f -exec md5sum '{}' + | grep -v Example.jar")

        self.assert_plain_text_equal(expected, result)


if __name__ == "__main__":
    run(suite = NativeRegressionSuite())
