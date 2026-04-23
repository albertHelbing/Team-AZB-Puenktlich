# Scrum Retrospective – Iteration: Unit Test Implementation

**Project:** Puenktlich API  
**Retrospective date:** 17.04.2026
**Duration:** 45 minutes
**Participants:** Robin, Bojan, Albert, Ari, Luca, Zein  
**Reviewed iteration / time period:** Last iteration from 20.03.2026 to 27.03.2026, focused on designing, implementing, and validating automated unit tests for the API endpoints in `main.py`.

## 1. Goal of the reviewed iteration

The goal of this iteration was to create a useful automated unit test suite for the API project so that the basic functionality of the backend can be checked quickly and repeatedly. The focus was on testing endpoint behavior in isolation without depending on the real VVS API or the real `vvspy` upstream service.

The implemented test file covers the three existing endpoints:

- `/stops`
- `/trips`
- `/test`

It also covers both normal behavior and important error/edge cases.

## 2. Evidence from the project work

This retrospective is based on concrete outcomes from the iteration:

- The test file contains **8 automated tests** and all of them passed in the local test run.
- The tests isolate external dependencies using monkeypatching and stubs instead of calling real external systems.
- The test suite verifies successful responses, empty-result cases, and upstream failure handling.
- The repository already contains a CI workflow, but the current workflow only runs linting/format checks and does **not** run the new test suite yet.

Examples of concrete evidence:

- `test_get_stops_filters_and_maps` verifies filtering and response mapping for `/stops`.
- `test_get_stops_translates_request_exception_to_502` and `test_trips_translates_request_exception_to_502` verify error translation to HTTP 502.
- `test_trips_returns_null_when_vvspy_returns_no_trips` documents the current behavior when no trip data is returned.
- The CI file `.github/workflows/ci.yml` currently runs Ruff and Prettier checks, but no pytest step.

## 3. What went well

### 1. We achieved isolated unit tests without relying on real external services

This was important because the application depends on `requests.get(...)` and `vvspy.get_trips(...)`. In the tests, these dependencies were replaced with fakes or monkeypatched functions. That made the tests deterministic and fast.

**Why this went well:**
We understood early that calling the real VVS API or the real `vvspy` integration would make the tests unstable and slower. Because of that, the team chose mocking/patching from the start instead of trying to test against live systems.

**Evidence:**
The test file stubs `vvspy` before importing `main`, and then monkeypatches `main.requests.get` and `main.vvspy.get_trips` in multiple tests.

### 2. The tests document intended behavior quite clearly

The test names are descriptive and show the expected behavior directly, for example:

- `test_get_stops_returns_empty_list_when_no_stop_locations`
- `test_trips_returns_duration_minutes`
- `test_test_endpoint_returns_vvspy_result`

This makes the test suite useful not only for validation, but also for understanding how the API is supposed to behave.

**Why this went well:**
The team worked with a clear pattern: each test name states the situation and the expected outcome. That reduced ambiguity and made reviewing easier.

**Evidence:**
The file consistently follows a readable naming style and checks concrete response values, status codes, and payload structures.

### 3. We covered both happy paths and important edge/error cases

The iteration did not stop at “does it work once?”. The tests also check:

- no matching stops,
- missing `locations` key,
- upstream request failures,
- empty trip results.

**Why this went well:**
We did not only think from the implementation perspective, but also from the failure perspective. That helped us create tests that are more useful for regression detection.

**Evidence:**
Several tests focus specifically on error handling and unusual inputs, not only successful calls.

### 4. The resulting suite is fast and repeatable

The complete test run finished quickly and consistently because no real network requests were performed.

**Why this went well:**
The team kept the scope of unit testing small and focused instead of mixing it with integration testing.

**Evidence:**
Local run result during review: **8 tests passed** in about **1.6 seconds**.

## 4. What did not go well / What can be improved

### 1. The tests were added late in the workflow instead of earlier in development

The team created the test suite as its own iteration after the API behavior already existed. That worked, but it meant that we sometimes had to reverse-engineer intended behavior from the existing code instead of defining expected behavior first.

**Root cause:**
Our workflow was implementation-first. Testing was treated more like a required deliverable at the end than like a development tool during coding.

**Impact:**
This made it harder to notice design issues early, and it increased the chance that tests describe current code behavior instead of the best intended behavior.

### 2. Some behaviors are tested because they exist, not because they are clearly designed

For example, `/trips` currently returns `None` when no trips are returned. The test documents that behavior, but this is probably not a very explicit API design decision. It is more a consequence of the current implementation than a clearly discussed contract.

**Root cause:**
We did not define the expected API contract in enough detail before writing the tests. Because of that, some tests validate accidental behavior.

**Impact:**
This can make future refactoring harder, because the team may hesitate to improve the endpoint if the tests “lock in” unclear behavior.

**Evidence:**
`test_trips_returns_null_when_vvspy_returns_no_trips` shows this exact case.

### 3. The current CI pipeline does not run the tests yet

The repo already has a CI workflow, which is good, but it only checks linting and formatting. That means regressions in functionality could still be merged without the test suite being executed automatically.

**Root cause:**
Process-wise, quality checks were split: style checks were automated earlier, but test automation was not integrated into the same pipeline during this iteration.

**Impact:**
The benefits of the new tests are reduced, because they currently depend on developers remembering to run them locally.

**Evidence:**
The existing `.github/workflows/ci.yml` contains Ruff and Prettier steps, but no pytest command.

### 4. Test coverage is solid for the current endpoints, but still narrow at code-structure level

We tested endpoint behavior through FastAPI’s `TestClient`, which is good for API-level validation, but the implementation is not structured into smaller helper functions or service classes. Because of that, we can only unit-test at endpoint level and not at finer granularity.

**Root cause:**
The application code in `main.py` is still relatively compact and endpoint-centric. Logic and integration concerns are not yet separated much.

**Impact:**
Future expansion could make testing harder if the same structure continues.

## 5. Actionable improvement measures for the next iteration

### Measure 1: Add automated pytest execution to CI

**Action:** Extend `.github/workflows/ci.yml` with a test job that installs dependencies and runs `pytest`.  
**Owner:** Luca
**Target date / iteration:** 22.05.2026
**Expected benefit:** Every push and pull request will automatically validate both code style and behavior, so regressions are detected earlier.

### Measure 2: Define expected API behavior for edge cases before writing new tests

**Action:** Before implementing or extending endpoints, briefly document expected behavior for special cases such as empty results, invalid upstream data, or missing fields.  
**Owner:** Zein
**Target date / iteration:** 22.05.2026  
**Expected benefit:** Tests will reflect intentional API design decisions instead of accidental implementation details.

### Measure 3: Refactor endpoint logic into smaller helper functions where useful

**Action:** Move reusable or non-trivial logic (for example response mapping and duration calculation) into smaller functions so they can be tested directly.  
**Owner:** Albert  
**Target date / iteration:** 22.05.2026  
**Expected benefit:** Finer-grained tests, easier debugging, and safer refactoring.

### Measure 4: Use a short “test review” checklist in pull requests

**Action:** Add a lightweight checklist to PR reviews, e.g.:

- Are happy path and error path both covered?
- Are external dependencies mocked?
- Are test names descriptive?
- Does the change require CI/test updates?

**Owner:** Bojan mainly & Robin supporting
**Target date / iteration:** 22.05.2026  
**Expected benefit:** Better consistency without adding a lot of process overhead.

## 6. Summary

Overall, the iteration was successful because the team produced a working automated test suite that is fast, isolated, readable, and useful for regression detection. The strongest points were the clean isolation of dependencies, clear test naming, and inclusion of error/edge cases.

The main improvement areas are more process-related than technical: tests should be integrated into CI, expected behavior should be discussed earlier, and the code structure should gradually support more fine-grained testing.

For a student project, this iteration was a good step forward: the test suite is already useful, but the next iteration should make sure the tests become part of the normal development workflow instead of remaining a one-time submission artifact.
