# Bingo Project - Git History Insights

## Recent Development (March 2025)
- Latest commit: `da9cde7` - feat: persist state (main branch)
- Feature branch exists: `feature/persisting-state` with WIP changes
- Author: Jonathan Irvin <djfoxyslpr@gmail.com>

## Version History
- Current version: v1.1.4 (released via semantic versioning)
- Major milestones:
  - v1.0.0: Major release with semantic versioning established
  - v0.1.0: Initial modular architecture refactoring
  
## Key Development Patterns
1. **Conventional Commits**: Strictly follows format (feat, fix, chore, docs, test, refactor)
2. **Automated Releases**: Uses python-semantic-release with [skip ci] tags
3. **PR-based Workflow**: Features developed in branches, merged via PRs
4. **Code Quality**: Every PR includes formatting (black, isort) and testing

## Recent Changes (v1.1.4)
- State persistence implementation (March 16, 2025)
- Health check improvements with JSON formatting
- Import sorting and formatting fixes
- Added comprehensive state persistence tests (459 lines)
- Enhanced board builder tests (257 lines)

## Architecture Evolution Timeline
1. Initial monolithic `main.py` implementation
2. Modular refactoring (v0.1.0) - split into src/ structure
3. UI improvements - closed game message display
4. NiceGUI 2.11+ compatibility fixes
5. State persistence across app restarts (latest)

## Testing Evolution
- Started with basic tests
- Added comprehensive unit tests (80% coverage)
- Latest: Extensive state persistence testing
- Focus on UI synchronization and user tracking

## CI/CD Pipeline
- GitHub Actions for automated testing and releases
- Disabled Docker and Helm workflows (kept as reference)
- Semantic versioning based on commit messages
- Automatic CHANGELOG.md updates