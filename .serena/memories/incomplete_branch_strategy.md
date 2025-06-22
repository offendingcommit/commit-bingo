# Strategy for Handling Incomplete Remote Branches

## Overview
When returning to a project with incomplete work in remote branches, a systematic approach helps assess and decide how to proceed with each branch.

## Discovery Commands
```bash
# List all branches
git branch -a

# Find unmerged branches
git branch --no-merged main

# Recent branch activity
git for-each-ref --sort=-committerdate refs/remotes/origin --format='%(committerdate:short) %(refname:short) %(subject)'

# Check specific branch differences
git log main..origin/branch-name --oneline
git diff main...origin/branch-name --stat
```

## Decision Framework

### 1. Create Draft PR
**When**: Work is partially complete but needs visibility
```bash
gh pr create --draft --base main --head branch-name --title "WIP: Description"
```
**Benefits**: 
- Documents intent and approach
- Allows collaboration
- Preserves context
- Shows in PR list for tracking

### 2. Local Continuation
**When**: Work is experimental or very incomplete
```bash
git checkout branch-name
git pull origin branch-name
# Option A: Continue directly
# Option B: Stash current state first
git stash push -m "Previous WIP attempt"
```

### 3. Rebase and Cleanup
**When**: Commits need reorganization before review
```bash
git checkout branch-name
git rebase -i main
# Clean up commit history
```

### 4. Extract Useful Parts
**When**: Some ideas are good but implementation needs restart
```bash
# Cherry-pick specific commits
git cherry-pick commit-hash

# Or create patches
git format-patch main..branch-name
```

## Best Practices

1. **Use Git Worktrees** for isolated testing:
   ```bash
   git worktree add ../project-wip branch-name
   ```

2. **Document Intent**: 
   - Check commit messages for TODOs
   - Look for related issues
   - Add comments to draft PRs

3. **Test Before Deciding**:
   ```bash
   poetry install
   poetry run pytest
   poetry run flake8
   ```

4. **Communicate Status**:
   - Update PR descriptions
   - Close stale branches
   - Document decisions

## Handling "WIP and Broken" Commits

1. First understand what's broken:
   - Run tests to see failures
   - Check linting errors
   - Try running the application

2. Decide on approach:
   - Fix and continue if close to working
   - Extract concepts if fundamentally flawed
   - Archive with explanation if obsolete

3. Clean up before merging:
   - Squash WIP commits
   - Write proper commit messages
   - Ensure all tests pass

## Branch Lifecycle Management

- **Active**: Currently being developed
- **Draft PR**: Under review/discussion
- **Stale**: No activity >30 days
- **Archived**: Kept for reference but not active

Regular cleanup prevents accumulation of dead branches while preserving useful experimental work.