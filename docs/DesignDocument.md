# Credit Bureau Score Simulator

## 1. Purpose and user journey

Design document | 16 November 2026

This educational application turns sample credit records into an explainable score. It helps a reviewer understand how records, repayment behavior, and business rules affect a result. It is not a production credit-bureau or lending-decision system.

The user chooses a consumer and an as-of date, then clicks Evaluate Score. The dashboard shows the final score, five factor explanations, consumer profile, account repayment grid, and applied rule identifiers.

### Main requirements

- Use only information available on the requested date.
- Combine repeated submissions for the same account.
- Show 36 months of repayment history.
- Explain every factor contribution and risk cap.
- Return NA when there is insufficient eligible history.
- Support both a browser dashboard and command-line reports.

### System flow

CSV records -> validation -> date filtering -> account merging -> score calculation -> risk caps -> report JSON -> browser dashboard.

The command-line interface uses the same core processing and scoring modules to produce text reports.

### Technology

The backend uses Java 17, Maven, and the JDK HTTP server. The browser interface uses HTML, CSS, and vanilla JavaScript. Tests use JUnit 5. Data is loaded from CSV files into an in-memory store.

<!-- pagebreak -->

## 2. Components and data

### Ingestion

CsvParser and the ingesters read tradelines, enquiries, and events. A tradeline is a lender's account submission. An enquiry records a credit check. An event records a dispute, resolution, or account-status change. Invalid records are represented with rejection reasons in the ingestion results.

### Date filtering and merging

AsOfDateFilter excludes information after the selected date. AccountMergingEngine matches submissions using the same lender, account type, an open-date gap of at most 30 days, and an amount difference of at most 5 percent. Latest eligible values win, while monthly repayment observations are retained.

### Profiles and repayment history

ProfileBuilder aggregates account counts, revolving balances and limits, account age, and credit mix. DPDHistoryEngine builds the 36-month grid. DPD means Days Past Due. Grid categories distinguish on-time payments, late-payment ranges, and missing data.

### Storage

DataStore holds records in memory. The web API loads CSV data when serving consumers and reports. The project has no production database, durable transaction store, or user account system.

### Module locations

- ingestion: parsing and validation.
- processing: filtering, merging, profiles, and repayment history.
- scoring: factor calculators, thin-file checks, disputes, and overrides.
- reporting: command-line report formatting.
- web: dashboard delivery and JSON endpoints.
- domain and persistence: data models and storage abstractions.

<!-- pagebreak -->

## 3. Score calculation and special cases

### Calculation

An eligible profile starts with 300 points. Payment history can add up to 300; utilisation up to 200; age up to 100; mix up to 100. Hard enquiries can subtract up to 100. The result is limited to 300-900 before applying any lower risk cap.

Each factor has a separate calculator. Results include awarded points, explanations, and business-rule identifiers so the dashboard can explain the final number.

### Important rules

- Thin file: fewer than six months of eligible history or no eligible account returns NA. Exactly six months can qualify.
- Utilisation: revolving balance divided by revolving limit. At most 30 percent earns 200 points under the simulator's rules.
- Risk caps: recent 90-plus DPD can cap the result at 650; recent settlement or write-off at 600; suit filed at 550. When several caps apply, the lowest wins.
- Disputes: actively disputed accounts are excluded from scoring. VALID and REMOVED resolutions affect inclusion and historical calculation behavior.
- Precision: financial arithmetic uses BigDecimal; dates use Java calendar types.

### Demonstration scenarios

Use 31 October 2026 for all three examples. CON-004 returns 900 after the maximum-score limit. CON-003 returns 650 after the recent delinquency cap. CON-010 returns NA because history is shorter than six months.

Detailed rule definitions are maintained in docs/BusinessRules.md. Design choices and trade-offs are in docs/DecisionLog.md.

<!-- pagebreak -->

## 4. Interfaces, verification, and deployment

### HTTP endpoints

- GET / serves the dashboard.
- GET /health returns the service health response.
- GET /api/consumers lists available consumer IDs.
- GET /api/report?consumer=CON-004&asOf=2026-10-31 returns a score report.
- GET /api/history returns historical scores using the endpoint's consumer and date parameters.

The browser renders the report into the score gauge, factor cards, account grid, and rule register. The server uses the project index.html when available and also contains an embedded fallback dashboard.

### Verification

Run mvn clean verify from the project root. The complete existing suite contains 39 tests in 13 classes. A local run on 16 November 2026 passed all 39 with no failures, errors, or skipped tests.

Tests cover scoring boundaries, merging, disputes, overrides, historical calculation, CLI workflows, and determinism. Browser automation, performance tests, and measured code coverage are not included. GitHub Actions runs the suite with Java 17 on pushes and pull requests.

### Deployment and limitations

The Docker image packages the Java application and sample data. Render can serve the dashboard and API together. An optional Vercel frontend uses proxy functions to reach the backend. The PORT environment variable selects the server port; local use defaults to 8080.

Production use would require stronger persistence, authentication, request validation, privacy controls, and operational testing. These are future improvements, not implemented capabilities of this demonstration.

### Review links

Live website: https://credit-bureau-simulator-1.onrender.com/

The README links to the supplied five-minute Google Drive demo, the full test suite, and the decision log.
