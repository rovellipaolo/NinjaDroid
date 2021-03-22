from regression import run, RegressionSuite


class DockerRegressionSuite(RegressionSuite):
    """
    Docker regression tests.
    """

    BASE_COMMAND = "docker run --name ninjadroid -it --rm -v ${PWD}/apks:/apks ninjadroid:latest "

    def set_up(self):
        # self.execute_command("make build-docker")
        self.execute_command("cp regression/data/Example.apk apks/Example.apk")

    def tear_down(self):
        self.execute_command("rm apks/Example.apk")

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


if __name__ == "__main__":
    run(suite = DockerRegressionSuite())
