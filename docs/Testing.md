# Testing guide

## Run everything

From the repository root (the folder containing pom.xml):

```sh
mvn clean verify
```

This compiles the application, runs all checked-in JUnit tests, and packages the runnable JAR. For tests without packaging, use `mvn test`.

Local verification on 16 November 2026: **39 tests, 0 failures, 0 errors, 0 skipped** across **13 classes**. Check GitHub Actions for later results.

## Included tests

- **Scoring:** 9 classes and 30 tests for payment history, utilisation, credit age, mix, enquiries, thin files, disputes, overrides, and scoring integration.
- **Processing:** 1 class and 3 tests for account-merging boundaries and repeated monthly submissions.
- **Integration:** 3 classes and 6 tests for CLI workflows, historical filtering and recalculation, and deterministic results.

[Test source](../src/test/java/com/creditbureau/simulator) and [integration fixtures](../test-data) are included in the repository.

Test fixtures use CUST-1001-style IDs. Dashboard sample data uses CON-001-style IDs. Choose the matching dataset.

## Run one class or method

```sh
mvn "-Dtest=UtilisationCalculatorTest" test
mvn "-Dtest=FullWorkflowTest" test
mvn "-Dtest=OverrideEngineTest#testDPD90InMonth6TriggersCap" test
```

## Results and automation

Maven prints totals in the terminal and writes XML and text reports to `target/surefire-reports/`.

[The GitHub Actions workflow](../.github/workflows/tests.yml) uses Java 17 and runs on pushes and pull requests. Reports are uploaded even when tests fail. Generated reports and JARs stay out of Git.

## Manual browser check

Start the website using the README. Set the date to 2026-10-31:

1. CON-004 should show 900 with factor cards and a repayment grid.
2. CON-003 should show 650 with BR-36 and its risk-cap explanation.
3. CON-010 should show NA and the thin-file reason.

## Coverage limits

This is the full existing automated suite, not exhaustive coverage. Browser interactions, API error responses, deployment, security, and performance are not covered by this suite. No code-coverage percentage has been measured.

The [test-case map](TestCases.md) lists specific scenarios and rule references.
