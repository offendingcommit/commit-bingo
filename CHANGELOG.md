# CHANGELOG


## v1.1.1 (2025-03-08)

### Bug Fixes

- Release pipeline to listen to "The next version is"
  ([`d9acadf`](https://github.com/OffendingCommit/commit-bingo/commit/d9acadff39302a5c200d747ca3a7c91d772d0365))


## v1.1.0 (2025-03-08)

### Bug Fixes

- Formatting
  ([`6820b5d`](https://github.com/OffendingCommit/commit-bingo/commit/6820b5de5a4f2794565ecdb81ab952886c155530))

### Features

- Add health check
  ([`b780dd9`](https://github.com/OffendingCommit/commit-bingo/commit/b780dd9d49dddf365e85ef23571ca0438b92b8a2))


## v1.0.0 (2025-03-03)

### Chores

- Disable replaced workflows and keep as reference
  ([`a31f19d`](https://github.com/OffendingCommit/commit-bingo/commit/a31f19d41192718b2b73a641efd19f8e7f12eab2))


## v0.1.0 (2025-03-03)

### Bug Fixes

- Handle missing ui.broadcast method in newer NiceGUI versions
  ([`2479f57`](https://github.com/OffendingCommit/commit-bingo/commit/2479f57615ca293f0977d5d24a4d9e6e6da6d015))

- Added try-except to handle AttributeError when ui.broadcast is called - Fall back to timer-based
  sync when broadcast is not available - Added logging to track when fallback is used

- Update semantic release pipeline configuration
  ([`2ee4d28`](https://github.com/OffendingCommit/commit-bingo/commit/2ee4d281095276792abae04f3af198c2705cec0b))

### Chores

- Formatting
  ([`5e6e919`](https://github.com/OffendingCommit/commit-bingo/commit/5e6e9190c299a1004d8fa76a06abeb18ecbe3238))

Signed-off-by: Jonathan Irvin <djfoxyslpr@gmail.com>

- **build**: Add semantic versioning configuration
  ([`8329ca9`](https://github.com/OffendingCommit/commit-bingo/commit/8329ca9f9b4cf001afc79184dc30fb686191b0ea))

Add python-semantic-release configuration to enable automatic versioning. Configure Black and isort
  for code formatting standards. Add development dependencies for linting and testing.

🤖 Generated with [Claude Code](https://claude.ai/code) Co-Authored-By: Claude
  <noreply@anthropic.com>

- **dev**: Add development helper scripts
  ([`e286126`](https://github.com/OffendingCommit/commit-bingo/commit/e286126e3d3fa391ea77abdcb3c4eef1f1d5eaa5))

Add Makefile with common commands for building, testing and running. Create setup.sh script for easy
  developer onboarding. Configure git hooks for pre-commit checks.

🤖 Generated with [Claude Code](https://claude.ai/code) Co-Authored-By: Claude
  <noreply@anthropic.com>

- **dev**: Update Makefile to support both original and modular app
  ([`6aeea18`](https://github.com/OffendingCommit/commit-bingo/commit/6aeea18f1bfa194cbee700836d7326497e958b14))

- **formatting**: Fix formatting and insure sanity checks
  ([`b9f4932`](https://github.com/OffendingCommit/commit-bingo/commit/b9f4932bc95eed270156e2d4c9dd7b26d7ca3cf6))

Signed-off-by: Jonathan Irvin <djfoxyslpr@gmail.com>

- **git**: Add coverage files to gitignore
  ([`abd1f69`](https://github.com/OffendingCommit/commit-bingo/commit/abd1f69b4528cd3ee0f77a2c9539c1f739849f1b))

- **poetry**: Update lock file
  ([`7c207ec`](https://github.com/OffendingCommit/commit-bingo/commit/7c207eceba505bd43c746351ac7dd1c78fc89bd8))

Signed-off-by: Jonathan Irvin <djfoxyslpr@gmail.com>

### Code Style

- Format code with black and isort
  ([`1b474f0`](https://github.com/OffendingCommit/commit-bingo/commit/1b474f096d1d0b05f2ead7a4fef40945c3080729))

- Format code with black and isort
  ([`7584575`](https://github.com/OffendingCommit/commit-bingo/commit/7584575fba2c6b9dbcd789dfd074aab5c0fa74df))

### Continuous Integration

- Add github actions workflow
  ([`9b31ae3`](https://github.com/OffendingCommit/commit-bingo/commit/9b31ae30c6dc56b78663421d0c63e19ec702d160))

Add CI/CD pipeline with GitHub Actions that: - Runs tests with pytest - Performs linting with
  flake8, black, and isort - Uploads coverage reports - Automatically creates releases based on
  semantic versioning

🤖 Generated with [Claude Code](https://claude.ai/code) Co-Authored-By: Claude
  <noreply@anthropic.com>

- **build**: Align CI, Docker build and Helm deployment
  ([`0685e62`](https://github.com/OffendingCommit/commit-bingo/commit/0685e6204058ff896dd5b9c0bd4ae504f467e097))

- Update GitHub Action versions for consistency - Configure Docker build to use proper versioning
  tags - Fix Helm chart to use the correct image repository - Add security improvements to Docker
  and Helm deployment - Add volume initialization logic for persistent data

- **fix**: Fix flake8 configuration syntax
  ([`3ded6bf`](https://github.com/OffendingCommit/commit-bingo/commit/3ded6bfef1d95388358ae13c73111013e586aef7))

- **fix**: Fix linting configuration to exclude virtual environments
  ([`17be15c`](https://github.com/OffendingCommit/commit-bingo/commit/17be15cc60e1248cf69aa6c67f75e269f81d7bfe))

- Add .flake8 configuration - Update CI workflow to exclude .venv from checks - Add exclusion
  patterns to Black and isort configurations

- **fix**: Skip formatting checks for main.py and handle missing src directory
  ([`9464d93`](https://github.com/OffendingCommit/commit-bingo/commit/9464d93471306210bea6183877748aea2feed977))

### Documentation

- Add deprecation notice to main.py
  ([`6eaa5da`](https://github.com/OffendingCommit/commit-bingo/commit/6eaa5da84e624d0609eea3423b35b20b8e510c66))

- Mark main.py as deprecated but keep for backward compatibility - Add warning message when main.py
  is imported - Direct users to the new modular structure in src/ directory

- Update README with comprehensive documentation
  ([`3eb772c`](https://github.com/OffendingCommit/commit-bingo/commit/3eb772c0a211637575b301cbbf6ae0180c0c692e))

- **changelog**: Add initial changelog
  ([`6f07022`](https://github.com/OffendingCommit/commit-bingo/commit/6f07022e3fb1704fdd4e33601eaad33a5a886d71))

Create CHANGELOG.md for tracking release history. Follow Keep a Changelog format for better release
  readability. Include entries for unreleased changes and initial 0.1.0 release.

🤖 Generated with [Claude Code](https://claude.ai/code) Co-Authored-By: Claude
  <noreply@anthropic.com>

- **project**: Update documentation with CI and semantic versioning
  ([`fa43299`](https://github.com/OffendingCommit/commit-bingo/commit/fa43299bc878fdeb4c19af905dacb7fd98411690))

Update CLAUDE.md with: - Information about semantic versioning principles - CI/CD pipeline details -
  New build commands - Makefile usage instructions - Linting and formatting guidelines

🤖 Generated with [Claude Code](https://claude.ai/code) Co-Authored-By: Claude
  <noreply@anthropic.com>

### Features

- Add ability to close the game
  ([`2653abc`](https://github.com/OffendingCommit/commit-bingo/commit/2653abcf5ff1b5b992746d53d92573289839398f))

- Configure semantic release for automated versioning
  ([`38b44d7`](https://github.com/OffendingCommit/commit-bingo/commit/38b44d7b53158a8750a5388af59d0f43d540f4aa))

- Create unified release pipeline with semantic versioning
  ([`ee1dcdf`](https://github.com/OffendingCommit/commit-bingo/commit/ee1dcdfb378ea2e5badf40ddb86b8d9369dca3c4))

- **ui**: Add closed game message display
  ([`76abafc`](https://github.com/OffendingCommit/commit-bingo/commit/76abafc755bfcd77a5690dbadc3288562c262b6d))

Replace the 'hide board' behavior with a 'GAME CLOSED' message displayed in the same space. This
  provides better visual feedback to users when the game is closed.

- Add new constants for closed message text and color - Create new build_closed_message function
  that displays large text - Update close_game and sync_board_state to show message instead of
  hiding board

- **ui**: Show closed message on all routes
  ([`2911416`](https://github.com/OffendingCommit/commit-bingo/commit/291141669ea534d3b54e24f5fdd2a787db914b22))

Instead of hiding the board when the game is closed, display a large 'GAME CLOSED' message in the
  same space as the board. This provides better visibility and a consistent user experience across
  all views including the main.py implementation.

- Add build_closed_message function to both modules - Update sync_board_state to display message in
  both modules - Display message using the header font and free space color

### Refactoring

- Add type hints
  ([`45303b4`](https://github.com/OffendingCommit/commit-bingo/commit/45303b41727127ba3b77a508ec5e289a62aab469))

- Add proper typing to game_logic, board_builder, and constants - Create dedicated types module for
  shared type definitions - Fix tests to reflect new closed message functionality - Add mypy type
  checking to development dependencies

- Implement modular architecture for improved maintainability
  ([`d1c4c97`](https://github.com/OffendingCommit/commit-bingo/commit/d1c4c97adcaa39b08cf46e7cba41ef40a9716c9e))

- Split monolithic main.py into logical modules - Created directory structure with src/ as the root
  - Organized code into config, core, ui, and utils packages - Updated basic test to work with new
  structure - Maintained existing functionality while improving code organization

- Simplify CI workflow by removing redundant release job
  ([`25b1edf`](https://github.com/OffendingCommit/commit-bingo/commit/25b1edf2b3ea280c5eeb56e476c76e00e782c28e))

### Testing

- Add comprehensive unit tests for current functionality
  ([`49b8fdf`](https://github.com/OffendingCommit/commit-bingo/commit/49b8fdfe042bab1e56c78e71f5717ddd26adde3c))

- Added unit tests for game logic functions (board generation, win detection, etc.) - Added unit
  tests for UI and styling functions - Added tests for file operations (reading phrases.txt) - Added
  integration test for full game flow - Current test coverage: 69% for main.py, 80% overall

- Update header_updates_on_both_paths test
  ([`cb6c3f5`](https://github.com/OffendingCommit/commit-bingo/commit/cb6c3f55d6f62f006f1a0cfeaa9f6e8a82bf0a89))

- Simplify test to avoid circular dependencies - Remove complex mocking that was causing failures -
  Focus on the core functionality being tested - Use direct board_views manipulation for cleaner
  test

- Update tests to not expect ui.broadcast
  ([`9e689dc`](https://github.com/OffendingCommit/commit-bingo/commit/9e689dcb2afa7db33277efb56be6db1e74144df9))

- Modified test_close_game to not assert on ui.broadcast call - Ensures tests pass with newer
  NiceGUI versions - Aligns with recent changes to handle missing broadcast method

- Update ui functions tests to work with modular structure
  ([`d91afdd`](https://github.com/OffendingCommit/commit-bingo/commit/d91afddecfcffeeac51ce98b4610436682602777))

- Update import paths to use the new modular structure - Replace main module references with
  specific module imports - Update test assertions to match new implementation details - Add proper
  cleanup in tests to restore global state
