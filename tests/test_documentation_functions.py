import unittest
from pathlib import Path

from testfixtures import TempDirectory
from src.IntuneCD.documentation_functions import md_file, \
    write_table, \
    assignment_table, \
    remove_characters, \
    clean_list, \
    document_configs, \
    document_management_intents, \
    get_md_files


class TestDocumentationFunctions(unittest.TestCase):

    def setUp(self):
        self.directory = TempDirectory()
        self.directory.create()
        self.directory.makedir("config")
        self.directory.makedir("intent/test")

    def tearDown(self):
        self.directory.cleanup()

    def test_md_file_does_not_exist(self):
        """The md file should be returned."""
        md_file(f"{self.directory.path}/test_file_name.md")

        self.assertTrue(
            Path(f"{self.directory.path}/test_file_name.md").exists())

    def test_md_file_exists(self):
        """The md file should be returned."""
        self.directory.write("test_file_name.md", "md", encoding="utf-8")

        md_file(f"{self.directory.path}/test_file_name.md")
        with open(f"{self.directory.path}/test_file_name.md", "r") as f:
            self.assertEqual(f.read(), '')

    def test_write_table(self):
        """The table should be returned."""
        self.table_data = [['test', 'test'], ['test', 'test']]
        self.expected_table = '|setting|value||-------|-----||test   |test ||test   |test |'

        self.result = write_table(self.table_data)
        self.string = str(self.result)

        self.assertEqual(
            ''.join(
                self.string.splitlines()),
            self.expected_table)

    def test_assignment_table(self):
        """The table should be returned."""
        self.table_data = {
            'assignments': [
                {
                    'intent': 'apply',
                    'target': {
                        '@odata.type': "#test",
                        'groupName': 'test-group',
                        'deviceAndAppManagementAssignmentFilterId': 'test-filter',
                        'deviceAndAppManagementAssignmentFilterType': 'test'}}]}
        self.expected_table = '|intent|  target  |filter type|filter name||------|----------|-----------|-----------||apply |test-group|test       |test-filter|'

        self.result = assignment_table(self.table_data)
        self.string = str(self.result)

        self.assertEqual(''.join(
            self.string.splitlines()), self.expected_table)

    def test_remove_characters(self):
        """The string should be returned."""
        self.string = '@[test]{}'

        self.assertEqual(remove_characters(self.string), 'test')

    def test_clean_list_list(self):
        """The list should be returned."""
        self.list = [{'teamIdentifier': 'test', 'bundleId': 'test'}]
        self.expected_list = ['teamIdentifier: test, bundleId: test']
        self.result = clean_list(self.list)

        self.assertEqual(self.result, self.expected_list)

    def test_clean_list_dict(self):
        """The list should be returned."""
        self.dict = {'appName': 'test', 'type': '#microsoft.graph.iosVppApp'}
        self.expected_list = ['appName', 'type']
        self.result = clean_list(self.dict)

        self.assertEqual(self.result, self.expected_list)

    def test_clean_list_string(self):
        """The list should be returned."""
        self.string = ['test']
        self.expected_list = ['test']
        self.result = clean_list(self.string)

        self.assertEqual(self.result, self.expected_list)

    def test_document_configs(self):
        """The list should be returned."""
        self.directory.write(
            "config/test_file_name.json",
            '{"test": "test", "name": "test", "description": "test", "assignments": [{"intent": "apply", "target": {"@odata.type": "#test", "groupName": "test-group", "deviceAndAppManagementAssignmentFilterId": "test-filter", "deviceAndAppManagementAssignmentFilterType": "test"}}]}',
            encoding="utf-8")
        self.expected_data = '#test##testDescription:test###Assignments|intent|target|filtertype|filtername||------|----------|-----------|-----------||apply|test-group|test|test-filter||setting|value||-------|-----||test|test||name|test|'

        document_configs(
            f"{self.directory.path}/config",
            f"{self.directory.path}/test.md",
            'test',
            10,
            split=False)
        with open(f"{self.directory.path}/test.md", "r") as f:
            self.data = f.read()
            self.result = ''.join([line.strip() for line in self.data])

        self.assertEqual(self.result, self.expected_data)

    def test_document_management_intents(self):
        """The list should be returned."""
        self.directory.write(
            "intent/test/test_file_name.json",
            '{"test": "test", "name": "test", "description": "test", "settingsDelta": [{"test": "test", "definitionId": "deviceConfiguration--macOSEndpointProtectionConfiguration_fileVaultNumberOfTimesUserCanIgnore","valueJson": "1","value": 1}], "assignments": [{"intent": "apply", "target": {"@odata.type": "#test", "groupName": "test-group", "deviceAndAppManagementAssignmentFilterId": "test-filter", "deviceAndAppManagementAssignmentFilterType": "test"}}]}',
            encoding="utf-8")
        self.expected_data = '#intent##testDescription:test###Assignments|intent|target|filtertype|filtername||------|----------|-----------|-----------||apply|test-group|test|test-filter||setting|value||-----------------------------------|-----||test|test||name|test||fileVaultNumberOfTimesUserCanIgnore|1|'

        document_management_intents(
            f"{self.directory.path}/intent/",
            f"{self.directory.path}/test.md",
            'intent',
            split=False)
        with open(f"{self.directory.path}/test.md", "r") as f:
            self.data = f.read()
            self.result = ''.join([line.strip() for line in self.data])

        self.assertEqual(self.result, self.expected_data)
