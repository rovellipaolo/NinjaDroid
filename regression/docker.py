from regression import run, RegressionSuite


class DockerRegressionSuite(RegressionSuite):
    """
    Docker regression tests.
    """

    BASE_COMMAND = "docker run --name ninjadroid -it --rm -v $(pwd)/apks:/apks ninjadroid:latest "
    BASE_COMMAND_WITH_OUTPUT = "docker run --name ninjadroid -it --rm -v $(pwd)/apks:/apks -v $(pwd)/output:/output " \
                               "ninjadroid:latest "

    def set_up(self):
        # self.execute_command("make build-docker")
        self.execute_command("mkdir -p apks")
        self.execute_command("cp regression/data/Example.apk apks/Example.apk")
        self.execute_command("mkdir -p output")
        self.execute_command("chmod 777 output")

    def tear_down(self):
        self.execute_command("rm apks/Example.apk")
        self.execute_command("sudo rm -r output/")

    @RegressionSuite.test
    def show_summary(self):
        expected = self.read_plain_text_file(
            "regression/expected/summary.txt",
            overrides={
                0: "file:    /apks/Example.apk"
            }
        )

        result = self.execute_command(self.BASE_COMMAND + "ninjadroid /apks/Example.apk")

        self.assert_plain_text_equal(expected, result, multiline=False)

    @RegressionSuite.test
    def show_extended(self):
        expected = self.read_plain_text_file(
            "regression/expected/extended.txt",
            overrides={
                0: "file:    /apks/Example.apk",
                22: "signature: SHA1withRSA (weak)"
            }
        )

        result = self.execute_command(self.BASE_COMMAND + "ninjadroid /apks/Example.apk --all")
        # NOTE: the below hack is needed to remove the SHA1withRSA signature algorithm warning...
        result = "\n".join(result.split('\n')[4:])

        self.assert_plain_text_equal(expected, result, multiline=False)

    @RegressionSuite.test
    def show_json_summary(self):
        expected = self.read_json_file("regression/expected/summary.json", overrides={"file": "/apks/Example.apk"})

        result = self.execute_command(self.BASE_COMMAND + "ninjadroid /apks/Example.apk --json")

        self.assert_json_equal(expected, result)

    @RegressionSuite.test
    def show_json_extended(self):
        expected = self.read_json_file(
            "regression/expected/extended.json",
            overrides={
                "file": "/apks/Example.apk",
                "cert": {
                    "fingerprint": {
                        "signature": "SHA1withRSA (weak)"
                    }
                },

            }
        )

        result = self.execute_command(self.BASE_COMMAND + "ninjadroid /apks/Example.apk --all --json")
        # NOTE: the below hack is needed to remove the SHA1withRSA signature algorithm warning...
        result = "\n".join(result.split('\n')[4:])

        self.assert_json_equal(expected, result)

    @RegressionSuite.test
    def extract_extended(self):
        expected = self.read_plain_text_file(
            "regression/expected/extract.txt",
            overrides={
                18: "7ab36f88adf38f96df05c9e024d548ab  output/report-Example.json"
            }
        )

        self.execute_command(self.BASE_COMMAND_WITH_OUTPUT + "ninjadroid /apks/Example.apk --all --extract /output")
        # NOTE: the .jar file checksum changes at every run...
        result = self.execute_command("find output/ -type f -exec md5sum '{}' + | grep -v Example.jar")

        self.assert_plain_text_equal(expected, result)


if __name__ == "__main__":
    run(suite = DockerRegressionSuite())
