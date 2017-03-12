from abc import ABCMeta, abstractmethod


class DexInterface(metaclass=ABCMeta):
    """
    Parser interface for Android classes.dex file.
    """

    @staticmethod
    @abstractmethod
    def looks_like_a_dex(filename):
        """
        Check whether a given file looks like a classes.dex file.

        :param filename: The name of the file to be checked.
        :return: True if the file looks like a classes.dex file, False otherwise.
        """
        pass

    @abstractmethod
    def dump(self):
        """
        Dump the Dex object into a Dictionary.

        :return: A Dictionary representing the Dex object.
        """
        pass

    @abstractmethod
    def get_strings(self):
        """
        Retrieve the strings in the classes.dex file.

        :return: The list of strings.
        """
        pass

    @abstractmethod
    def get_urls(self):
        """
        Retrieve the URLs in the classes.dex file.

        :return: The list of URLs.
        """
        pass

    @abstractmethod
    def get_shell_commands(self):
        """
        Retrieve the shell commands in the classes.dex file.

        :return: The list of shell commands.
        """
        pass

    def get_custom_signatures(self):
        """
        Retrieve the custom signatures in the classes.dex file.

        :return: The list of custom signatures.
        """
        pass
