# ModGen Course Development Routine

This routine is responsible for the automated generation of course modules for AESOP AI Academy. It identifies courses that have been added to `courses-data.json` with a `live: false` status, generates their content using Claude, and saves the resulting HTML files to the repository.

Once all modules for a course are generated and committed, this routine triggers the `ModGen Course Activation` skill to make the course live.

## Functionality

- Reads `courses-data.json` to find courses pending development.
- Uses Anthropic (Claude) via Polaris's agent system to generate detailed HTML content for each module, adhering to AESOP's brand voice and linguistic guidelines.
- Saves generated module HTML files to the appropriate course directories.
- Updates the course status in `courses-data.json` to reflect generation completion.
- Commits new module files and updated `courses-data.json` to the `main` branch of the `AesopScott/Aesop` repository.
- Initiates the `ModGen Course Activation` skill upon successful completion of all modules for a course.

## Setup

This routine requires:

- Read/write access to the `AesopScott/Aesop` GitHub repository.
- Access to the Anthropic API (via Polaris configuration).

## Execution

This routine is designed to run continuously, checking for new course development tasks. It processes one course at a time until its modules are fully generated.

## Output

- Generated HTML files for course modules.
- Updates to `courses-data.json`.
- Git commits to the `main` branch.
- Trigger for the `ModGen Course Activation` skill.
