# Credit Bureau Score Simulator

A Java 17 application that turns sample credit records into an explainable score. Select a consumer and a date to see their score, the reasons behind it, and their repayment history.

This is an educational simulator using sample data, not a real lending-decision service.

## Try it online

- [Live website](https://credit-bureau-simulator-1.onrender.com/)
- [Watch the 5-minute demo](https://drive.google.com/file/d/1SN3hPIqT2C11b2c6BdzIoXf50E6bnkyY/view?usp=drivesdk)

## Project deliverables

- **README with run steps:** see below.
- **Design document:** [PDF](docs/DesignDocument.pdf) and [Markdown](docs/DesignDocument.md).
- **Full automated test suite:** [test source](src/test/java/com/creditbureau/simulator), [fixtures](test-data), and [testing guide](docs/Testing.md).
- **Decision log:** [design choices and trade-offs](docs/DecisionLog.md).
- **Demo video:** [5-minute walkthrough](https://drive.google.com/file/d/1SN3hPIqT2C11b2c6BdzIoXf50E6bnkyY/view?usp=drivesdk).

## Run on your computer

### 1. Check the requirements

Install Git, JDK 17 or later, and Maven 3.8 or later. Check Java and Maven:

```sh
java -version
mvn -version
```

### 2. Download the project

```sh
git clone https://github.com/syedibad52/credit-bureau-simulator.git
cd credit-bureau-simulator
```

Already downloaded it? Open a terminal in the folder containing `pom.xml`.

### 3. Build and test

```sh
mvn clean verify
```

This runs all automated tests and creates `target/credit-bureau-simulator-1.0.0.jar`.

### 4. Start the website

```sh
java -jar target/credit-bureau-simulator-1.0.0.jar serve --data ./sample-data
```

Open [http://localhost:8080](http://localhost:8080). Keep the terminal running while using the website. Press **Ctrl+C** in that terminal to stop it.

Run from the project folder so the server can find `index.html` and `sample-data`. The default port is 8080; the `PORT` environment variable overrides it.

### 5. Try three examples

Set **As-Of** to **2026-10-31**, select a consumer, and click **Evaluate Score**:

- **CON-004:** score **900**, showing the maximum-score limit.
- **CON-003:** score **650**, showing a risk cap for a recent serious late payment.
- **CON-010:** score **NA**, showing insufficient credit history.

Explore the factor cards, consumer profile, 36-month repayment grid, and applied business rules.

## Run the full test suite

```sh
mvn test
```

The checked-in suite has **39 tests in 13 classes**. The local verification on **16 November 2026** passed all 39, with no failures, errors, or skipped tests.

GitHub Actions runs Maven verification on pushes and pull requests. See [Actions](https://github.com/syedibad52/credit-bureau-simulator/actions) for current results. Detailed reports are generated in `target/surefire-reports/` and uploaded as a CI artifact.

The [testing guide](docs/Testing.md) explains individual test commands and coverage limits.

## How it works

1. Read credit accounts, enquiries, and events from CSV files.
2. Keep records available on the selected date.
3. Merge duplicate submissions for the same account.
4. Build a 36-month repayment history.
5. Calculate payment history, utilisation, credit age, credit mix, and enquiry contributions.
6. Apply score limits and risk overrides.
7. Return the score, explanations, accounts, and rule IDs.

Eligible profiles start at 300. Positive factors add points and hard enquiries can subtract points. Scores are limited to 300-900, with lower caps for serious risk events. Insufficient history returns NA.

## Technology and folders

- `index.html`: HTML, CSS, and JavaScript dashboard.
- `src/main/java/`: Java backend, HTTP API, CLI, and scoring logic.
- `src/test/java/`: JUnit 5 unit and integration tests.
- `sample-data/`: dashboard examples.
- `test-data/`: focused integration-test fixtures.
- `docs/`: design, decisions, business rules, and testing.
- `.github/workflows/tests.yml`: automated test workflow.

The Java service can serve both the dashboard and API on Render. An optional Vercel frontend proxy is also included. See the [deployment guide](docs/Deployment.md).

## Troubleshooting

- **Java or Maven is not recognized:** install it, add its bin folder to PATH, and reopen the terminal.
- **Port 8080 is busy:** stop the process using that port, or set `PORT` to a free port.
- **Missing data or wrong page:** start the server from the folder containing `pom.xml`, `index.html`, and `sample-data`.
- **Score differs from the demo:** check the consumer ID and as-of date.

See the [documentation index](docs/README.md) for more detail.
