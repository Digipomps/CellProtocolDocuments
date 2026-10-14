import json
import unittest
from pathlib import Path
from workbench_xctest_receipt import validate_xctest

OLD = Path.home()/'Build/Digipomps/HAVEN/HAVEN-Deploy/_handoff/ARBEIDSBENK/G2-W1-RETEST-20261012'
MANIFEST = json.loads((OLD/'manifest.json').read_text())
LOG = (OLD/'cp-tests.log').read_text()
EXPECTED = MANIFEST['cpTests']


class ReceiptTests(unittest.TestCase):
    def reject(self, log, code=0, expected=EXPECTED):
        with self.assertRaises(ValueError):
            validate_xctest(log, expected, code)

    def test_real_eight_tests_allow_expected_runtime_rejections(self):
        self.assertEqual(len(validate_xctest(LOG, EXPECTED, 0)), 8)

    def test_nonzero_exit_after_all_passed_is_rejected(self):
        self.reject(LOG, 1)

    def test_signal_exit_after_all_passed_is_rejected(self):
        self.reject(LOG, -15)

    def test_real_log_with_interleaved_product_prefix_is_accepted(self):
        log = LOG.replace("Test Case '-[", "product fragmentTest Case '-[")
        self.assertEqual(len(validate_xctest(log, EXPECTED, 0)), 8)

    def test_terminal_before_start_is_rejected(self):
        lines = LOG.splitlines(keepends=True)
        index = next(i for i, line in enumerate(lines) if "Test Case" in line)
        lines[index], lines[index+1] = lines[index+1], lines[index]
        self.reject(''.join(lines))

    def test_cases_outside_bundle_are_rejected(self):
        cases = [line for line in LOG.splitlines(keepends=True) if "Test Case" in line]
        remainder = ''.join(line for line in LOG.splitlines(keepends=True) if "Test Case" not in line)
        self.reject(''.join(cases)+remainder)

    def test_unexpected_test_module_duplicate_is_rejected(self):
        line = next(line for line in LOG.splitlines() if "Test Case" in line and "passed" in line)
        self.reject(LOG+'\n'+line.replace('CellBaseTests.', 'OtherTests.'))

    def test_method_failure_is_rejected(self):
        self.reject(LOG.replace("passed (0.021 seconds)", "failed (0.021 seconds)"))

    def test_method_skip_is_rejected(self):
        self.reject(LOG.replace("passed (0.021 seconds)", "skipped (0.021 seconds)"))

    def test_duplicate_test_is_rejected(self):
        line = next(x for x in LOG.splitlines() if "Test Case" in x and "passed" in x)
        self.reject(LOG + '\n' + line)

    def test_missing_suite_completion_is_rejected(self):
        self.reject(LOG.replace("Test Suite 'CellBaseTests.xctest' passed", "Truncated suite"))

    def test_nonzero_failure_summary_is_rejected(self):
        self.reject(LOG.replace("Executed 8 tests, with 0 failures", "Executed 8 tests, with 1 failures"))

    def test_wrong_test_count_is_rejected(self):
        self.reject(LOG.replace("Executed 8 tests", "Executed 7 tests"))

    def test_missing_root_summary_is_rejected(self):
        self.reject(LOG[:LOG.rfind("Test Suite 'Selected tests' passed")])

    def test_zero_tests_is_not_success(self):
        self.reject("Test Suite 'Selected tests' started at now.\nTest Suite 'Selected tests' passed at now.\n Executed 0 tests, with 0 failures (0 unexpected)\n")

    def test_unexpected_signal_diagnostic_is_rejected(self):
        self.reject(LOG + '\nerror: Exited with unexpected signal code 6\n')

    def test_compiler_error_is_rejected(self):
        self.reject(LOG + '\n/source.swift:12:3: error: compile failure\n')

    def test_failed_suite_is_rejected(self):
        self.reject(LOG.replace("Test Suite 'CellBaseTests.xctest' passed", "Test Suite 'CellBaseTests.xctest' failed"))

    def test_missing_or_duplicate_manifest_refused(self):
        self.reject(LOG, expected=[])
        self.reject(LOG, expected=EXPECTED + EXPECTED[:1])


if __name__ == '__main__':
    unittest.main(verbosity=2)
