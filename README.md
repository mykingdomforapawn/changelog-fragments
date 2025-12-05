# Changelog Fragments Sandbox

A sandbox environment demonstrating the **Changelog Fragment** pattern using an OpenAPI specification and GitHub Actions.

> **AI Disclaimer:** This project was developed with the assistance of AI tools to guide the learning process, explain concepts, and generate automation scripts.

---

## Purpose

This repository serves as a practical demonstration of **"Rolling Changelogs"** or the **"Fragment Pattern"**. Instead of editing a single `CHANGELOG.md` file (which causes merge conflicts in active teams), developers create small, isolated text files ("fragments") for each change. A release process later consumes these fragments to generate the final documentation programmatically.

The project uses a **Smart Home OpenAPI Specification** as the dummy "product" being documented.

---

## The Fragment Workflow

This section outlines the lifecycle of a change in this repository, from development to release.

**Step 1: Modify the Spec**
* A developer creates a branch (e.g., `feature/add-light-dimmer`).
* Modifications are made to `openapi.yaml` (e.g., adding a new schema property).

**Step 2: Add a Changelog Fragment**
* The developer must create a new file in `.changelog/unreleased/`.
* The filename format determines the change category: `description.type.md`.
* **Example:** `.changelog/unreleased/add-dimmer.feature.md`.
* **Content:** A single, neutral sentence describing the change.

**Step 3: Validation (CI)**
* On Pull Request, the **PR Validation** workflow runs.
* It checks the `.changelog/unreleased/` directory.
* **Pass:** A new fragment file is found.
* **Fail:** No fragment is found (blocks the merge).

**Step 4: Release**
* A maintainer triggers the **Release** workflow manually via GitHub Actions.
* The automation script:
    1.  Collects all fragments from `.changelog/unreleased/`.
    2.  Sorts them by type (Feature, Bugfix, etc.).
    3.  Prepends a formatted block to `CHANGELOG.md`.
    4.  Deletes the fragment files.
    5.  Tags the release and uploads assets.

---

## Repository Structure

* `openapi.yaml`: The source of truth for the API (the "code").
* `CHANGELOG.md`: The historical record of all releases.
* `.changelog/unreleased/`: The holding area for pending changes (fragments).
* `.github/workflows/`:
    * `pr_validation.yaml`: Enforces fragment creation.
    * `release.yaml`: Automates versioning and documentation generation.
* `.github/scripts/release_changelog.py`: The logic for aggregating and formatting release notes.

---

## Fragment Types

The system recognizes specific keywords in filenames to categorize changes in the final log.

* `feature`: New functionality (e.g., `new-login.feature.md`).
* `bugfix`: Corrections to existing behavior (e.g., `fix-typo.bugfix.md`).
* `breaking`: Changes that require user intervention (e.g., `rename-id.breaking.md`).
* `docs`: Documentation-only updates (e.g., `update-readme.docs.md`).
* `chore`: Maintenance tasks (e.g., `update-deps.chore.md`).

---

## Setup and Usage

To experiment with this repository locally:

1.  **Clone the repository.**

2.  **Initialize the environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    pip install pre-commit
    ```

3.  **Install Git Hooks:**
    This enforces YAML syntax and linting checks locally before committing.
    ```bash
    pre-commit install
    ```

4.  **Simulate a Release Locally:**
    You can test the generation script without pushing to GitHub.
    ```bash
    # Usage: python .github/scripts/release_changelog.py [version]
    python .github/scripts/release_changelog.py v1.0.0
    ```
    *Note: This will modify CHANGELOG.md and delete files in .changelog/unreleased/.*

---

## Learning Roadmap

This project explores the following DevOps and documentation concepts:

* [x] **Changelog Fragments**: Decoupling release notes from code changes to prevent conflicts.
* [x] **API Design First**: Using OpenAPI (Swagger) as the primary deliverable.
* [x] **CI Validation**: Using GitHub Actions to enforce process rules (checking for missing fragments).
* [x] **Automated Releases**: Scripting the aggregation of documentation and Git tagging.
* [x] **Pre-commit Hooks**: Enforcing code quality and syntax safety locally.
