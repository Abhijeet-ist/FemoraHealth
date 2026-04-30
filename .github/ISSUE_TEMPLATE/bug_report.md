name: Bug Report
description: Report a bug to help us improve
title: "[BUG] "
labels: ["bug"]

body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!

  - type: textarea
    id: description
    attributes:
      label: Describe the bug
      description: A clear and concise description of what the bug is
      placeholder: Tell us what went wrong
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to reproduce
      description: Steps to reproduce the behavior
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. See error
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
      description: A clear and concise description of what you expected to happen
      placeholder: Expected...
    validations:
      required: true

  - type: textarea
    id: screenshots
    attributes:
      label: Screenshots
      description: If applicable, add screenshots to help explain your problem
      placeholder: Paste screenshots here

  - type: dropdown
    id: environment
    attributes:
      label: Environment
      options:
        - Python 3.8
        - Python 3.9
        - Python 3.10
        - Python 3.11
        - Python 3.12
        - Other (specify below)
    validations:
      required: true

  - type: textarea
    id: additional
    attributes:
      label: Additional context
      description: Add any other context about the problem here
      placeholder: Additional info...
