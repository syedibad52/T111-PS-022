# Decision log

Recorded: 16 November 2026. This log explains the current implementation retrospectively; it does not claim these decisions were originally made on this date.

## 1. Java 17 and Maven

**Choice:** use Java for the backend and Maven for builds and tests.
**Why:** Java provides decimal arithmetic, calendar dates, and mature testing tools. Maven gives reviewers one build command.
**Trade-off:** local development requires a JDK and Maven.

## 2. A simple web stack

**Choice:** use HTML, CSS, vanilla JavaScript, and the JDK HTTP server.
**Why:** the dashboard needs no separate frontend build process.
**Trade-off:** JSON responses and UI state are managed manually. A larger application may benefit from dedicated frameworks.

## 3. CSV data and in-memory storage

**Choice:** load CSV records into DataStore.
**Why:** the demonstration is reproducible without database setup.
**Trade-off:** the store is not a durable transactional database. Larger datasets and concurrent workloads need a different persistence design.

## 4. Date filtering before scoring

**Choice:** filter records by the requested as-of date before merging and scoring.
**Why:** future information must not influence an earlier point-in-time report.
**Trade-off:** date boundaries need careful testing. Historical recalculation after dispute resolution is a separate behavior.

## 5. Merge repeated account submissions

**Choice:** match lender and account type, with open dates within 30 days and amounts within 5 percent. Use the latest eligible submission for current values and retain monthly history.
**Why:** repeated submissions should not become extra credit accounts.
**Trade-off:** matching is based on project rules; stronger account identifiers would be useful in production. Matching requires the same lender, not cross-lender deduplication.

## 6. Explainable factor calculators

**Choice:** keep each factor in a separate calculator and return contributions, explanations, and rule IDs.
**Why:** reviewers can understand and test individual scoring rules.
**Trade-off:** a fixed rule-based simulator does not establish predictive accuracy for real lending.

## 7. Exact decimals and explicit risk limits

**Choice:** use BigDecimal for financial calculations. Check thin files and apply risk caps explicitly.
**Why:** boundaries such as exactly 30 percent utilisation must behave predictably. Insufficient history returns NA, and the strictest applicable risk cap wins.
**Trade-off:** rounding and date windows still need boundary tests; decimal arithmetic alone cannot ensure correctness.

## 8. Repeatable tests and continuous integration

**Choice:** keep all JUnit tests and fixtures in Git. Run Maven verification on GitHub pushes and pull requests.
**Why:** developers and reviewers can repeat the checks.
**Trade-off:** the existing 39 tests cover backend scenarios. Browser automation, load tests, and measured code coverage are not included.

## 9. Link the demonstration video

**Choice:** link the supplied Google Drive video and Render website in the README.
**Why:** reviewers can open the demonstration without a large video in Git.
**Trade-off:** viewing depends on the external services and the video's sharing settings.
