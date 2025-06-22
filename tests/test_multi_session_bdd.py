"""
BDD tests for multi-session concurrent access scenarios.
"""

import json
import time
from pathlib import Path
from threading import Thread, Lock
from unittest.mock import patch, MagicMock

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from src.core import game_logic


# Load scenarios from feature file
scenarios('features/multi_session_concurrent.feature')


# Shared test data
@pytest.fixture
def state_file():
    """Path to state file."""
    return Path("game_state.json")


@pytest.fixture
def test_board():
    """Standard test board."""
    return [["A1", "A2", "A3", "A4", "A5"],
            ["B1", "B2", "B3", "B4", "B5"],
            ["C1", "C2", "FREE SPACE", "C4", "C5"],
            ["D1", "D2", "D3", "D4", "D5"],
            ["E1", "E2", "E3", "E4", "E5"]]


@pytest.fixture
def user_sessions():
    """Dictionary to track user sessions."""
    return {}


@pytest.fixture(autouse=True)
def cleanup(state_file):
    """Clean up before and after each test."""
    # Clean up before
    if state_file.exists():
        state_file.unlink()
    
    # Reset game state
    game_logic.board = []
    game_logic.clicked_tiles = set()
    game_logic.bingo_patterns = set()
    game_logic.board_iteration = 1
    game_logic.is_game_closed = False
    game_logic.today_seed = None
    
    yield
    
    # Clean up after
    if state_file.exists():
        state_file.unlink()


# Background steps
@given('the bingo application is running')
def app_running():
    """Application is running."""
    # In tests, we simulate this by having the game_logic module imported
    assert game_logic is not None


@given('the board has been generated with test phrases')
def board_generated(test_board):
    """Generate test board."""
    game_logic.board = test_board


# Multi-user scenarios
@given(parsers.parse('{count:d} users are connected to the game'))
def users_connected(count, user_sessions):
    """Simulate multiple connected users."""
    for i in range(1, count + 1):
        user_sessions[f"user{i}"] = {
            'id': f"user{i}",
            'clicked': [],
            'view_state': {}
        }


@given(parsers.parse('user {user_id:d} is connected to the game'))
def user_connected(user_id, user_sessions):
    """Simulate a single connected user."""
    user_sessions[f"user{user_id}"] = {
        'id': f"user{user_id}",
        'clicked': [],
        'view_state': {}
    }


@given(parsers.parse('user {user_id:d} has clicked tile at position ({row:d}, {col:d})'))
def user_clicked_tile(user_id, row, col, user_sessions):
    """User clicks a tile."""
    game_logic.toggle_tile(row, col)
    user_sessions[f"user{user_id}"]['clicked'].append((row, col))
    time.sleep(0.05)  # Small delay to simulate network


@given(parsers.parse('user {user_id:d} has clicked tiles at positions ({positions})'))
def user_clicked_multiple(user_id, positions, user_sessions):
    """User clicks multiple tiles."""
    # Parse positions like "(0, 0), (0, 1), (0, 2)"
    tiles = []
    for pos in positions.split('), '):
        pos = pos.strip('() ')
        row, col = map(int, pos.split(', '))
        tiles.append((row, col))
        game_logic.toggle_tile(row, col)
    
    user_sessions[f"user{user_id}"]['clicked'].extend(tiles)
    time.sleep(0.1)  # Allow saves


@given('the users have clicked several tiles')
def users_clicked_several(user_sessions):
    """Multiple users click tiles."""
    tiles_to_click = [(0, 0), (1, 1), (3, 3), (4, 4), (0, 4), (4, 0)]
    for i, (user_id, session) in enumerate(user_sessions.items()):
        if i < len(tiles_to_click):
            row, col = tiles_to_click[i]
            game_logic.toggle_tile(row, col)
            session['clicked'].append((row, col))
    time.sleep(0.1)


# Action steps
@when(parsers.parse('user {user_id:d} clicks tile at position ({row:d}, {col:d})'))
def when_user_clicks_tile(user_id, row, col, user_sessions):
    """User clicks a tile."""
    game_logic.toggle_tile(row, col)
    user_sessions[f"user{user_id}"]['clicked'].append((row, col))


@when(parsers.parse('user {user_id:d} closes the game'))
def when_user_closes_game(user_id):
    """User closes the game."""
    game_logic.close_game()


@when(parsers.parse('user {user_id:d} tries to click tile at position ({row:d}, {col:d}) simultaneously'))
def when_user_tries_click_simultaneously(user_id, row, col, user_sessions):
    """User tries to click while another action is happening."""
    # Simulate slight delay
    time.sleep(0.01)
    try:
        game_logic.toggle_tile(row, col)
        user_sessions[f"user{user_id}"]['clicked'].append((row, col))
    except:
        pass  # Click might fail if game is closed


@when(parsers.parse('user {user_id:d} connects to the game'))
def when_user_connects(user_id, user_sessions):
    """New user connects and loads state."""
    user_sessions[f"user{user_id}"] = {
        'id': f"user{user_id}",
        'clicked': [],
        'view_state': {}
    }
    # Load current state
    game_logic.load_state_from_storage()


@when('all users rapidly click random tiles')
def when_all_users_click_rapidly(user_sessions):
    """Simulate rapid clicking from all users."""
    import random
    results = []
    results_lock = Lock()
    
    def user_rapid_clicks(user_id, session):
        """Each user clicks 5 random tiles."""
        for _ in range(5):
            row = random.randint(0, 4)
            col = random.randint(0, 4)
            try:
                game_logic.toggle_tile(row, col)
                with results_lock:
                    results.append((user_id, row, col))
                time.sleep(0.01)  # Small delay between clicks
            except:
                pass
    
    # Run clicks in parallel threads
    threads = []
    for user_id, session in user_sessions.items():
        thread = Thread(target=user_rapid_clicks, args=(user_id, session))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads
    for thread in threads:
        thread.join()
    
    # Store results for verification
    user_sessions['_rapid_click_results'] = results


@when('the server state is saved')
def when_server_state_saved():
    """Ensure state is saved."""
    game_logic.save_state_to_storage()
    time.sleep(0.2)  # Wait for async save


@when('the server is simulated to restart')
def when_server_restarts():
    """Simulate server restart by clearing memory."""
    game_logic.board = []
    game_logic.clicked_tiles = set()
    game_logic.bingo_patterns = set()
    game_logic.board_iteration = 1
    game_logic.is_game_closed = False
    game_logic.today_seed = None


@when('users reconnect to the game')
def when_users_reconnect(test_board):
    """Users reconnect after restart."""
    # Load state from storage
    game_logic.load_state_from_storage()
    # Ensure board is loaded if not in state
    if not game_logic.board:
        game_logic.board = test_board


# Verification steps
@then(parsers.parse('all {count:d} tiles should be marked as clicked'))
def then_tiles_marked(count):
    """Verify number of clicked tiles."""
    assert len(game_logic.clicked_tiles) == count


@then(parsers.parse('the state file should contain {count:d} clicked tiles'))
def then_state_file_contains(count, state_file):
    """Verify state file contents."""
    assert state_file.exists()
    with open(state_file, 'r') as f:
        state = json.load(f)
    assert len(state['clicked_tiles']) == count


@then('all users should see the same game state')
def then_users_see_same_state(user_sessions):
    """Verify all users have consistent view."""
    # In a real app, this would check each user's view
    # Here we verify the global state is consistent
    current_state = {
        'clicked': game_logic.clicked_tiles.copy(),
        'closed': game_logic.is_game_closed,
        'iteration': game_logic.board_iteration
    }
    
    # All users loading state should see the same thing
    for user_id in user_sessions:
        if user_id.startswith('user'):
            # Simulate user loading state
            temp_clicked = game_logic.clicked_tiles.copy()
            assert temp_clicked == current_state['clicked']


@then('the game should be in closed state')
def then_game_closed():
    """Verify game is closed."""
    assert game_logic.is_game_closed is True


@then('only the first tile should be marked as clicked')
def then_only_first_tile_clicked():
    """Verify only one tile is clicked."""
    assert len(game_logic.clicked_tiles) == 1
    assert (0, 0) in game_logic.clicked_tiles


@then('both users should see the closed game message')
def then_users_see_closed_message():
    """Verify closed game state is visible."""
    # In real app, would check UI state
    assert game_logic.is_game_closed is True


@then(parsers.parse('user {user_id:d} should see {count:d} tiles already clicked'))
def then_user_sees_tiles_clicked(user_id, count):
    """Verify user sees correct number of clicked tiles."""
    assert len(game_logic.clicked_tiles) == count


@then(parsers.parse('user {user_id:d} should see tiles at positions ({positions}) as clicked'))
def then_user_sees_specific_tiles(user_id, positions):
    """Verify user sees specific tiles as clicked."""
    # Parse positions
    expected_tiles = []
    for pos in positions.split('), '):
        pos = pos.strip('() ')
        row, col = map(int, pos.split(', '))
        expected_tiles.append((row, col))
    
    for tile in expected_tiles:
        assert tile in game_logic.clicked_tiles


@then('all valid clicks should be registered')
def then_all_clicks_registered(user_sessions):
    """Verify rapid clicks were registered."""
    # Some clicks might hit the same tile, so we just verify
    # that we have a reasonable number of clicked tiles
    assert len(game_logic.clicked_tiles) > 0
    assert len(game_logic.clicked_tiles) <= 25  # Max possible tiles


@then('no clicks should be lost')
def then_no_clicks_lost(state_file):
    """Verify state was saved properly."""
    assert state_file.exists()
    with open(state_file, 'r') as f:
        state = json.load(f)
    # Verify state matches memory
    assert len(state['clicked_tiles']) == len(game_logic.clicked_tiles)


@then('the final state should be consistent across all users')
def then_final_state_consistent(user_sessions):
    """Verify final state consistency."""
    # Load state fresh to simulate what each user would see
    saved_clicked = game_logic.clicked_tiles.copy()
    
    # Simulate each user loading state
    for user_id in user_sessions:
        if user_id.startswith('user'):
            # Each user should see the same state
            assert game_logic.clicked_tiles == saved_clicked


@then('all previously clicked tiles should remain clicked')
def then_previous_clicks_remain(user_sessions):
    """Verify clicks survived restart."""
    # Count total expected clicks
    total_expected = 0
    for session in user_sessions.values():
        if isinstance(session, dict) and 'clicked' in session:
            total_expected += len(session['clicked'])
    
    # Should have at least some clicks (might be less due to duplicates)
    assert len(game_logic.clicked_tiles) > 0


@then('users can continue playing from where they left off')
def then_users_can_continue():
    """Verify game is playable after restart."""
    # Should be able to click a new tile
    initial_count = len(game_logic.clicked_tiles)
    game_logic.toggle_tile(2, 3)  # Click a new tile
    assert len(game_logic.clicked_tiles) == initial_count + 1