#!/usr/bin/env python3
"""
Script to automatically add pytest marks to test files based on their characteristics.
"""

import re
from pathlib import Path

# Test file categorization
TEST_CATEGORIES = {
    # Pure unit tests
    "unit": [
        "test_state_manager.py",
        "test_file_operations.py",
        "test_helpers.py",
    ],
    
    # Integration tests
    "integration": [
        "test_board_builder.py",
        "test_ui_functions.py",
        "test_state_persistence.py",
        "test_integration.py",
        "test_game_logic.py",  # Has some integration aspects
    ],
    
    # E2E tests
    "e2e": [
        "test_hot_reload_integration.py",
        "test_hot_reload_integration_improved.py",
        "test_multi_session_simple.py",
        "test_multi_session_responsiveness.py",
        "test_multi_session_bdd.py",
        "test_state_persistence_bdd.py",
    ],
}

# Component-specific markers
COMPONENT_MARKERS = {
    "state": ["test_state_manager.py", "test_state_persistence.py", "test_state_persistence_bugs.py", "test_state_persistence_issues.py"],
    "game_logic": ["test_game_logic.py"],
    "ui": ["test_board_builder.py", "test_ui_functions.py"],
    "persistence": ["test_state_persistence.py", "test_state_persistence_bugs.py", "test_hot_reload_integration.py"],
    "sync": ["test_multi_session_simple.py", "test_multi_session_responsiveness.py"],
}

# Characteristic markers
CHARACTERISTIC_MARKERS = {
    "playwright": ["test_hot_reload", "test_multi_session"],
    "slow": ["test_hot_reload", "test_multi_session", "_bdd.py"],
    "requires_app": ["test_hot_reload", "test_multi_session", "test_integration.py"],
}

# Special markers
SPECIAL_MARKERS = {
    "smoke": ["test_state_manager.py::test_initialization", "test_game_logic.py::test_generate_board"],
    "regression": ["test_state_persistence_bugs.py", "test_state_persistence_issues.py"],
    "performance": ["test_multi_session_responsiveness.py"],
}


def get_marks_for_file(filename):
    """Determine which marks should be applied to a test file."""
    marks = set()
    
    # Check speed/scope categories
    for category, files in TEST_CATEGORIES.items():
        if filename in files:
            marks.add(category)
    
    # Check component markers
    for marker, files in COMPONENT_MARKERS.items():
        if filename in files:
            marks.add(marker)
    
    # Check characteristic markers
    for marker, patterns in CHARACTERISTIC_MARKERS.items():
        if any(pattern in filename for pattern in patterns):
            marks.add(marker)
    
    # Check special markers
    for marker, patterns in SPECIAL_MARKERS.items():
        if any(pattern in filename or filename in pattern for pattern in patterns):
            marks.add(marker)
    
    return marks


def add_marks_to_file(filepath):
    """Add pytest marks to a test file."""
    content = filepath.read_text()
    filename = filepath.name
    
    # Skip if already has marks (check for @pytest.mark at class level)
    if re.search(r'^@pytest\.mark\.\w+\s*\nclass\s+Test', content, re.MULTILINE):
        print(f"Skipping {filename} - already has marks")
        return
    
    marks = get_marks_for_file(filename)
    if not marks:
        print(f"No marks for {filename}")
        return
    
    # Sort marks for consistency
    marks = sorted(marks)
    mark_lines = [f"@pytest.mark.{mark}" for mark in marks]
    
    # Add import if not present
    if "import pytest" not in content:
        # Find where to add import
        import_match = re.search(r'^(import .*?)\n\n', content, re.MULTILINE | re.DOTALL)
        if import_match:
            import_section = import_match.group(1)
            content = content.replace(import_section, f"{import_section}\nimport pytest")
        else:
            content = f"import pytest\n\n{content}"
    
    # Add marks to test classes
    def add_marks_to_class(match):
        indent = match.group(1) if match.group(1) else ""
        class_line = match.group(2)
        marks_str = "\n".join(f"{indent}{mark}" for mark in mark_lines)
        return f"{marks_str}\n{indent}{class_line}"
    
    # Match class definitions
    content = re.sub(
        r'^(\s*)class\s+(Test\w+.*?:)$',
        add_marks_to_class,
        content,
        flags=re.MULTILINE
    )
    
    # For files without classes, add marks to individual test functions
    if "class Test" not in content:
        def add_marks_to_function(match):
            indent = match.group(1) if match.group(1) else ""
            async_marker = match.group(2) if match.group(2) else ""
            func_line = match.group(3)
            
            # Build marks including async if needed
            all_marks = mark_lines.copy()
            if async_marker:
                # Already has async marker, just add our marks before it
                marks_str = "\n".join(f"{indent}{mark}" for mark in all_marks)
                return f"{marks_str}\n{indent}{async_marker}\n{indent}{func_line}"
            else:
                marks_str = "\n".join(f"{indent}{mark}" for mark in all_marks)
                return f"{marks_str}\n{indent}{func_line}"
        
        # Match test functions (with or without @pytest.mark.asyncio)
        content = re.sub(
            r'^(\s*)(@pytest\.mark\.asyncio\s*\n)?(\s*def\s+test_\w+.*?:)$',
            add_marks_to_function,
            content,
            flags=re.MULTILINE
        )
    
    filepath.write_text(content)
    print(f"Added marks to {filename}: {', '.join(marks)}")


def main():
    """Main function to process all test files."""
    tests_dir = Path(__file__).parent.parent / "tests"
    
    for test_file in tests_dir.glob("test_*.py"):
        if test_file.name == "test_hot_reload_manual.py":
            # Skip manual test file
            continue
        add_marks_to_file(test_file)


if __name__ == "__main__":
    main()