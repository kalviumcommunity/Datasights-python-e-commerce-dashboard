# Team GitHub Workflow

## Branching Strategy

Our team follows a feature-branch workflow to keep the `main` branch stable and production-ready.

### Branch Rules
- The `main` branch contains only tested and releasable code.
- Every new feature, bug fix, documentation update, or refactoring task is developed in its own branch.
- Branches follow the naming convention:

```
feature/<short-description>
fix/<short-description>
docs/<short-description>
refactor/<short-description>
chore/<short-description>
```

### Examples
```
feature/data-ingestion
feature/data-validation
fix/missing-values
docs/data-dictionary
refactor/pipeline-structure
chore/update-dependencies
```

### Branch Lifecycle
1. Create a GitHub Issue.
2. Create a feature branch from `main`.
3. Implement the changes.
4. Commit changes using the team's commit convention.
5. Push the branch to GitHub.
6. Open a Pull Request.
7. After approval, merge into `main`.
8. Delete the feature branch after merging.

---

# Commit Message Convention

We follow the Conventional Commit style.

## Format

```
[type]: description
```

### Types
- **feat** – New feature
- **fix** – Bug fix
- **docs** – Documentation updates
- **refactor** – Code restructuring without changing functionality
- **chore** – Maintenance tasks

### Examples

```
feat: add customer transaction dataset

docs: document branching strategy

fix: correct missing value validation

refactor: simplify data preprocessing pipeline

chore: update project dependencies
```

### Why We Use This Convention
- Creates a clean and readable Git history.
- Makes it easier to understand changes.
- Supports automated changelog generation.
- Improves collaboration among team members.

---

# Pull Request Review Process

Every code change must be submitted through a Pull Request before merging into `main`.

## Pull Request Requirements
- A descriptive PR title.
- A summary explaining what changed.
- Reference the related GitHub Issue using:
  - `Closes #IssueNumber`
  - `Fixes #IssueNumber`
- Include testing or validation details when applicable.

## Review Checklist
Code reviewers verify:
- Code correctness
- Readability and maintainability
- Data integrity
- Test coverage
- Documentation updates
- Commit message quality

At least **one approval** is required before merging.

---

# GitHub Issue Tracking

All work begins with a GitHub Issue.

Each issue includes:
- A clear and descriptive title.
- A detailed description.
- Appropriate labels.
- An assignee.
- Acceptance criteria defining when the task is complete.

Issues are linked to Pull Requests using:

```
Closes #1
Fixes #2
```

When the Pull Request is merged, GitHub automatically closes the linked issue.

---

# Collaboration Workflow

```
Create GitHub Issue
        ↓
Create Feature Branch
        ↓
Develop Feature
        ↓
Commit Changes
        ↓
Push Branch
        ↓
Open Pull Request
        ↓
Code Review
        ↓
Approval
        ↓
Merge to Main
        ↓
Delete Feature Branch
```

This workflow ensures that code changes are organized, traceable, and reviewed before becoming part of the production codebase.