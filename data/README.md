# Data files

The analysis notebook expects this file:

- `lightcast_job_postings.csv`

This file is **not stored in Git** (it is listed in `.gitignore` because it exceeds GitHub’s 100 MB limit).

## Setup

1. Obtain the Lightcast job postings CSV from your course materials or team shared drive.
2. Save it in this folder as `data/lightcast_job_postings.csv`.
3. Run `quarto preview` from the project root.

Without this file, `analysis.qmd` will fail when Quarto runs the Python chunks.
