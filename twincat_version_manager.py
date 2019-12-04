import glob
import xml.etree.ElementTree as ET

VERSION_TAGS = {"**/*.Tc*": "ProductVersion", "**/*.tsproj": "TcVersion"}
CORRECT_VERSION = "3.1.4024.0"


def check_versions():
    """
    Checks the Twincat version used to create a file.
    It assumes that the version is stored as an attribute on the top element of the file, the attribute names are
    listed in VERSION_TAGS.
    :return: A dictionary of incorrect files and their version numbers
    """
    incorrect_files = dict()
    for file_path, version_attrib in VERSION_TAGS.items():
        found_files = glob.glob(file_path, recursive=True)
        if not found_files:
            raise IOError("ERROR: No files of type {} found".format(file_path))
        for file in found_files:
            tree = ET.parse(file)
            try:
                found_version = tree.getroot().attrib[version_attrib]
                if found_version != CORRECT_VERSION:
                    incorrect_files[file] = found_version
            except KeyError:
                print("WARNING: No version found for {}".format(file))
    return incorrect_files


if __name__ == "__main__":
    try:
        incorrect_files = check_versions()
        for file, version in incorrect_files.items():
            print("ERROR: {} has incorrect version {}, expected version {}".format(file, version, CORRECT_VERSION))
        if incorrect_files:
            exit(1)
    except IOError as e:
        print(e)  # Likely no files found
        exit(2)
