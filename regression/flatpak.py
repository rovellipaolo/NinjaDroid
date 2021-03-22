from regression import run, RegressionSuite


class FlatpakRegressionSuite(RegressionSuite):
    """
    Flatpak regression tests.
    """

    BASE_COMMAND = "flatpak-builder --run flatpak/build flatpak/com.github.rovellipaolo.NinjaDroid.yaml "

    def set_up(self):
        # self.execute_command("make build-flatpak")
        pass

    @RegressionSuite.test
    def show_summary(self):
        expected = self.read_plain_text_file("regression/expected/summary.txt")

        result = self.execute_command(self.BASE_COMMAND + "ninjadroid regression/data/Example.apk")

        self.assert_plain_text_equal(expected, result, multiline=False)

    @RegressionSuite.test
    def show_extended(self):
        expected = self.read_plain_text_file("regression/expected/extended.txt")

        result = self.execute_command(self.BASE_COMMAND + "ninjadroid regression/data/Example.apk --all")

        self.assert_plain_text_equal(expected, result, multiline=False)

    @RegressionSuite.test
    def show_json_summary(self):
        expected = self.read_json_file("regression/expected/summary.json")

        result = self.execute_command(self.BASE_COMMAND + "ninjadroid regression/data/Example.apk --json")

        self.assert_json_equal(expected, result)

    @RegressionSuite.test
    def show_json_extended(self):
        expected = self.read_json_file("regression/expected/extended.json")

        result = self.execute_command(self.BASE_COMMAND + "ninjadroid regression/data/Example.apk --all --json")

        self.assert_json_equal(expected, result)


if __name__ == "__main__":
    run(suite = FlatpakRegressionSuite())
