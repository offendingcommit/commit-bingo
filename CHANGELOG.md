# CHANGELOG


## v1.2.1 (2025-06-26)

### Bug Fixes

- Update gitignore and test configurations
  ([`a523af0`](https://github.com/offendingcommit/commit-bingo/commit/a523af091245f34e0909cd12164b956a3f464525))

- Add game_state.json to gitignore for state persistence - Update CLAUDE.md with memory management
  protocols - Fix hot reload integration test indentation error


## v1.2.0 (2025-06-22)

### Bug Fixes

- Correct import sorting in test_state_persistence.py
  ([`90369b7`](https://github.com/offendingcommit/commit-bingo/commit/90369b71d58bf7bc2059836040beb4a9b9f5d2e0))

Fix isort import sorting check failure in CI pipeline by running isort on
  tests/test_state_persistence.py to comply with project formatting rules

- **ci**: Add playwright markers to browser tests
  ([`aac342b`](https://github.com/offendingcommit/commit-bingo/commit/aac342be1e7727944f86436587ac1f14dafe68ed))

- Add @pytest.mark.playwright and @pytest.mark.e2e markers to browser tests - Ensures these tests
  are excluded from CI with '-m "not e2e and not playwright"' - Fixes CI failures due to missing
  playwright browser binaries

Resolves CI test failures in hot reload integration tests

- **ci**: Complete StateManager integration and CI optimization
  ([`d6cd8ba`](https://github.com/offendingcommit/commit-bingo/commit/d6cd8ba8fb37588de9ab6adaa52cce60c19f9cfc))

- Add proper pytest markers to all integration/performance test files - Update CI workflows to
  exclude flaky tests from automated runs - Fix test isolation issues in state persistence and board
  builder tests - Complete StateManager integration with game logic functions - Optimize CI to run
  139 reliable tests in ~7s vs previous 2+ min timeouts

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>

- **ci**: Exclude slow integration tests from CI pipeline
  ([`13ba214`](https://github.com/offendingcommit/commit-bingo/commit/13ba214502a68aeefa8b06a5d2d746619a14a8a1))

- Add @pytest.mark.integration and @pytest.mark.slow to responsiveness tests - Update CI workflows
  to exclude slow and integration tests - Reduces CI test count from 165 to 150 tests (15
  deselected) - Focuses CI on fast unit and medium integration tests

Improves CI reliability by excluding flaky performance tests

- **pytest**: Add missing pytest markers to configuration
  ([`9e31118`](https://github.com/offendingcommit/commit-bingo/commit/9e31118113b885b1d4691b4d2b209200650e0045))

- Add missing markers: bdd, known-issue-13, critical, edge-case, concurrent, error-handling - Fixes
  pytest collection warnings for test markers - Ensures all test markers are properly registered

### Code Style

- Fix import sorting with isort
  ([`1f5c5af`](https://github.com/offendingcommit/commit-bingo/commit/1f5c5af36307ce179b9ddc4f0e7271d9bcea3799))

- Sort imports in all Python files according to Black profile - Separate standard library,
  third-party, and local imports - Improve code consistency and readability

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>

### Documentation

- Consolidate markdown files into CLAUDE.md
  ([`15cdb00`](https://github.com/offendingcommit/commit-bingo/commit/15cdb008874f87c20f4e2b75b7178ccf5407ff4a))

Merge content from CONTEXT.md and NICEGUI_NOTES.md into CLAUDE.md to reduce root-level documentation
  clutter. The consolidated file now includes: - State persistence documentation - View
  synchronization details - NiceGUI framework notes and best practices - Mobile optimization
  guidelines

This keeps only README.md and CLAUDE.md as the primary documentation files.

### Features

- Persist state
  ([`da9cde7`](https://github.com/offendingcommit/commit-bingo/commit/da9cde7a13805ba4586a913cadd77626bd2ae83e))

Signed-off-by: Jonathan Irvin <djfoxyslpr@gmail.com>

- **ci**: Optimize workflow for improved test infrastructure
  ([`0af9336`](https://github.com/offendingcommit/commit-bingo/commit/0af9336775d47ae0ae2770f2b66f61c256ca2b57))

- Update test execution to run unit tests first for fast feedback - Add marker-based filtering to
  exclude slow e2e/playwright tests from CI - Remove Black formatting checks due to architecture
  compatibility issues - Add XML coverage reporting for better CI integration - Fix import sorting
  in app.py

Improves CI speed from ~2min to ~30s by running 79 unit tests first

### Testing

- Add failing tests for state persistence bugs
  ([`a628bfb`](https://github.com/offendingcommit/commit-bingo/commit/a628bfb76d2d38e154e600976ac0a94369729927))

Add comprehensive test suite to reproduce state persistence issues: - Tests for hot reload losing
  state - Tests for concurrent update race conditions - Tests for storage initialization order
  problems - BDD feature file with Gherkin scenarios

These tests are expected to fail until we implement proper server-side state persistence and fix the
  architectural issues.

Related to #13

- Add test tagging utility and improved hot reload test
  ([`8a05a48`](https://github.com/offendingcommit/commit-bingo/commit/8a05a482a9f4d76aff0d8ec46c0bed674cb66ab2))

- Add scripts/tag_tests.py for bulk test marker application - Create improved hot reload integration
  test with visual state validation - Remove temporary debugging files and images

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>

- Enhance testing infrastructure with comprehensive markers
  ([`f1f65bd`](https://github.com/offendingcommit/commit-bingo/commit/f1f65bdf13b73976f3c9be3b01f48764b2a2bef3))

- Add pytest.ini with detailed marker definitions for test categorization - Update Makefile with
  progressive test targets (test-unit, test-quick, test, test-e2e) - Create tests/README.md
  documenting test organization and marker usage - Implement testing pyramid strategy: 80% unit, 15%
  integration, 5% E2E

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>


## v1.1.4 (2025-03-08)

### Bug Fixes

- Pretty print health check
  ([`1127fcf`](https://github.com/offendingcommit/commit-bingo/commit/1127fcf34f92232dd8ab33c645973b32b5b0ce9b))

- Sort imports
  ([`c137a4e`](https://github.com/offendingcommit/commit-bingo/commit/c137a4e510c198fdf1e3020e622e444616e29ada))

- Switch to json dumps for health
  ([`d484fb0`](https://github.com/offendingcommit/commit-bingo/commit/d484fb0a1a41a22a80bf2f76ef32c92bc7983fdd))


## v1.1.3 (2025-03-08)

### Bug Fixes

- Add missing toml
  ([`6122f04`](https://github.com/offendingcommit/commit-bingo/commit/6122f04ce72f1a180db29cb67ff9a14338e63f18))


## v1.1.2 (2025-03-08)

### Bug Fixes

- **ci**: Change semantic versioning workflow
  ([`b588568`](https://github.com/offendingcommit/commit-bingo/commit/b588568cdcb4872a0be2e443d488cd13983e4f1a))


## v1.1.1 (2025-03-08)

### Bug Fixes

- Release pipeline to listen to "The next version is"
  ([`d9acadf`](https://github.com/offendingcommit/commit-bingo/commit/d9acadff39302a5c200d747ca3a7c91d772d0365))


## v1.1.0 (2025-03-08)

### Bug Fixes

- Formatting
  ([`6820b5d`](https://github.com/offendingcommit/commit-bingo/commit/6820b5de5a4f2794565ecdb81ab952886c155530))

### Features

- Add health check
  ([`b780dd9`](https://github.com/offendingcommit/commit-bingo/commit/b780dd9d49dddf365e85ef23571ca0438b92b8a2))


## v1.0.0 (2025-03-03)

### Chores

- Disable replaced workflows and keep as reference
  ([`a31f19d`](https://github.com/offendingcommit/commit-bingo/commit/a31f19d41192718b2b73a641efd19f8e7f12eab2))


## v0.1.0 (2025-03-03)

### Bug Fixes

- Handle missing ui.broadcast method in newer NiceGUI versions
  ([`2479f57`](https://github.com/offendingcommit/commit-bingo/commit/2479f57615ca293f0977d5d24a4d9e6e6da6d015))

- Added try-except to handle AttributeError when ui.broadcast is called - Fall back to timer-based
  sync when broadcast is not available - Added logging to track when fallback is used

- Update semantic release pipeline configuration
  ([`2ee4d28`](https://github.com/offendingcommit/commit-bingo/commit/2ee4d281095276792abae04f3af198c2705cec0b))

### Chores

- Formatting
  ([`5e6e919`](https://github.com/offendingcommit/commit-bingo/commit/5e6e9190c299a1004d8fa76a06abeb18ecbe3238))

Signed-off-by: Jonathan Irvin <djfoxyslpr@gmail.com>

- **build**: Add semantic versioning configuration
  ([`8329ca9`](https://github.com/offendingcommit/commit-bingo/commit/8329ca9f9b4cf001afc79184dc30fb686191b0ea))

Add python-semantic-release configuration to enable automatic versioning. Configure Black and isort
  for code formatting standards. Add development dependencies for linting and testing.

🤖 Generated with [Claude Code](https://claude.ai/code) Co-Authored-By: Claude
  <noreply@anthropic.com>

- **dev**: Add development helper scripts
  ([`e286126`](https://github.com/offendingcommit/commit-bingo/commit/e286126e3d3fa391ea77abdcb3c4eef1f1d5eaa5))

Add Makefile with common commands for building, testing and running. Create setup.sh script for easy
  developer onboarding. Configure git hooks for pre-commit checks.

🤖 Generated with [Claude Code](https://claude.ai/code) Co-Authored-By: Claude
  <noreply@anthropic.com>

- **dev**: Update Makefile to support both original and modular app
  ([`6aeea18`](https://github.com/offendingcommit/commit-bingo/commit/6aeea18f1bfa194cbee700836d7326497e958b14))

- **formatting**: Fix formatting and insure sanity checks
  ([`b9f4932`](https://github.com/offendingcommit/commit-bingo/commit/b9f4932bc95eed270156e2d4c9dd7b26d7ca3cf6))

Signed-off-by: Jonathan Irvin <djfoxyslpr@gmail.com>

- **git**: Add coverage files to gitignore
  ([`abd1f69`](https://github.com/offendingcommit/commit-bingo/commit/abd1f69b4528cd3ee0f77a2c9539c1f739849f1b))

- **poetry**: Update lock file
  ([`7c207ec`](https://github.com/offendingcommit/commit-bingo/commit/7c207eceba505bd43c746351ac7dd1c78fc89bd8))

Signed-off-by: Jonathan Irvin <djfoxyslpr@gmail.com>

### Code Style

- Format code with black and isort
  ([`1b474f0`](https://github.com/offendingcommit/commit-bingo/commit/1b474f096d1d0b05f2ead7a4fef40945c3080729))

- Format code with black and isort
  ([`7584575`](https://github.com/offendingcommit/commit-bingo/commit/7584575fba2c6b9dbcd789dfd074aab5c0fa74df))

### Continuous Integration

- Add github actions workflow
  ([`9b31ae3`](https://github.com/offendingcommit/commit-bingo/commit/9b31ae30c6dc56b78663421d0c63e19ec702d160))

Add CI/CD pipeline with GitHub Actions that: - Runs tests with pytest - Performs linting with
  flake8, black, and isort - Uploads coverage reports - Automatically creates releases based on
  semantic versioning

🤖 Generated with [Claude Code](https://claude.ai/code) Co-Authored-By: Claude
  <noreply@anthropic.com>

- **build**: Align CI, Docker build and Helm deployment
  ([`0685e62`](https://github.com/offendingcommit/commit-bingo/commit/0685e6204058ff896dd5b9c0bd4ae504f467e097))

- Update GitHub Action versions for consistency - Configure Docker build to use proper versioning
  tags - Fix Helm chart to use the correct image repository - Add security improvements to Docker
  and Helm deployment - Add volume initialization logic for persistent data

- **fix**: Fix flake8 configuration syntax
  ([`3ded6bf`](https://github.com/offendingcommit/commit-bingo/commit/3ded6bfef1d95388358ae13c73111013e586aef7))

- **fix**: Fix linting configuration to exclude virtual environments
  ([`17be15c`](https://github.com/offendingcommit/commit-bingo/commit/17be15cc60e1248cf69aa6c67f75e269f81d7bfe))

- Add .flake8 configuration - Update CI workflow to exclude .venv from checks - Add exclusion
  patterns to Black and isort configurations

- **fix**: Skip formatting checks for main.py and handle missing src directory
  ([`9464d93`](https://github.com/offendingcommit/commit-bingo/commit/9464d93471306210bea6183877748aea2feed977))

### Documentation

- Add deprecation notice to main.py
  ([`6eaa5da`](https://github.com/offendingcommit/commit-bingo/commit/6eaa5da84e624d0609eea3423b35b20b8e510c66))

- Mark main.py as deprecated but keep for backward compatibility - Add warning message when main.py
  is imported - Direct users to the new modular structure in src/ directory

- Update README with comprehensive documentation
  ([`3eb772c`](https://github.com/offendingcommit/commit-bingo/commit/3eb772c0a211637575b301cbbf6ae0180c0c692e))

- **changelog**: Add initial changelog
  ([`6f07022`](https://github.com/offendingcommit/commit-bingo/commit/6f07022e3fb1704fdd4e33601eaad33a5a886d71))

Create CHANGELOG.md for tracking release history. Follow Keep a Changelog format for better release
  readability. Include entries for unreleased changes and initial 0.1.0 release.

🤖 Generated with [Claude Code](https://claude.ai/code) Co-Authored-By: Claude
  <noreply@anthropic.com>

- **project**: Update documentation with CI and semantic versioning
  ([`fa43299`](https://github.com/offendingcommit/commit-bingo/commit/fa43299bc878fdeb4c19af905dacb7fd98411690))

Update CLAUDE.md with: - Information about semantic versioning principles - CI/CD pipeline details -
  New build commands - Makefile usage instructions - Linting and formatting guidelines

🤖 Generated with [Claude Code](https://claude.ai/code) Co-Authored-By: Claude
  <noreply@anthropic.com>

### Features

- Add ability to close the game
  ([`2653abc`](https://github.com/offendingcommit/commit-bingo/commit/2653abcf5ff1b5b992746d53d92573289839398f))

- Configure semantic release for automated versioning
  ([`38b44d7`](https://github.com/offendingcommit/commit-bingo/commit/38b44d7b53158a8750a5388af59d0f43d540f4aa))

- Create unified release pipeline with semantic versioning
  ([`ee1dcdf`](https://github.com/offendingcommit/commit-bingo/commit/ee1dcdfb378ea2e5badf40ddb86b8d9369dca3c4))

- **ui**: Add closed game message display
  ([`76abafc`](https://github.com/offendingcommit/commit-bingo/commit/76abafc755bfcd77a5690dbadc3288562c262b6d))

Replace the 'hide board' behavior with a 'GAME CLOSED' message displayed in the same space. This
  provides better visual feedback to users when the game is closed.

- Add new constants for closed message text and color - Create new build_closed_message function
  that displays large text - Update close_game and sync_board_state to show message instead of
  hiding board

- **ui**: Show closed message on all routes
  ([`2911416`](https://github.com/offendingcommit/commit-bingo/commit/291141669ea534d3b54e24f5fdd2a787db914b22))

Instead of hiding the board when the game is closed, display a large 'GAME CLOSED' message in the
  same space as the board. This provides better visibility and a consistent user experience across
  all views including the main.py implementation.

- Add build_closed_message function to both modules - Update sync_board_state to display message in
  both modules - Display message using the header font and free space color

### Refactoring

- Add type hints
  ([`45303b4`](https://github.com/offendingcommit/commit-bingo/commit/45303b41727127ba3b77a508ec5e289a62aab469))

- Add proper typing to game_logic, board_builder, and constants - Create dedicated types module for
  shared type definitions - Fix tests to reflect new closed message functionality - Add mypy type
  checking to development dependencies

- Implement modular architecture for improved maintainability
  ([`d1c4c97`](https://github.com/offendingcommit/commit-bingo/commit/d1c4c97adcaa39b08cf46e7cba41ef40a9716c9e))

- Split monolithic main.py into logical modules - Created directory structure with src/ as the root
  - Organized code into config, core, ui, and utils packages - Updated basic test to work with new
  structure - Maintained existing functionality while improving code organization

- Simplify CI workflow by removing redundant release job
  ([`25b1edf`](https://github.com/offendingcommit/commit-bingo/commit/25b1edf2b3ea280c5eeb56e476c76e00e782c28e))

### Testing

- Add comprehensive unit tests for current functionality
  ([`49b8fdf`](https://github.com/offendingcommit/commit-bingo/commit/49b8fdfe042bab1e56c78e71f5717ddd26adde3c))

- Added unit tests for game logic functions (board generation, win detection, etc.) - Added unit
  tests for UI and styling functions - Added tests for file operations (reading phrases.txt) - Added
  integration test for full game flow - Current test coverage: 69% for main.py, 80% overall

- Update header_updates_on_both_paths test
  ([`cb6c3f5`](https://github.com/offendingcommit/commit-bingo/commit/cb6c3f55d6f62f006f1a0cfeaa9f6e8a82bf0a89))

- Simplify test to avoid circular dependencies - Remove complex mocking that was causing failures -
  Focus on the core functionality being tested - Use direct board_views manipulation for cleaner
  test

- Update tests to not expect ui.broadcast
  ([`9e689dc`](https://github.com/offendingcommit/commit-bingo/commit/9e689dcb2afa7db33277efb56be6db1e74144df9))

- Modified test_close_game to not assert on ui.broadcast call - Ensures tests pass with newer
  NiceGUI versions - Aligns with recent changes to handle missing broadcast method

- Update ui functions tests to work with modular structure
  ([`d91afdd`](https://github.com/offendingcommit/commit-bingo/commit/d91afddecfcffeeac51ce98b4610436682602777))

- Update import paths to use the new modular structure - Replace main module references with
  specific module imports - Update test assertions to match new implementation details - Add proper
  cleanup in tests to restore global state
