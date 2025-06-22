Feature: Persistent Game State
  As a bingo game player
  I want my game state to persist across app restarts
  So that I don't lose progress if the app needs to restart

  Background:
    Given I have a bingo game in progress
    And I have clicked tiles at positions "(0,1)", "(2,3)", and "(4,4)"
    And the game header shows "BINGO!"

  @critical @known-issue-13
  Scenario: State persists through graceful restart
    When the app restarts gracefully
    Then the clicked tiles should remain at "(0,1)", "(2,3)", and "(4,4)"
    And the header should still show "BINGO!"
    And the board should show the same phrases

  @critical @known-issue-13
  Scenario: State persists through unexpected restart
    When the app crashes and restarts
    Then the clicked tiles should remain at "(0,1)", "(2,3)", and "(4,4)"
    And the header should still show "BINGO!"
    And the board should show the same phrases

  @critical @known-issue-13
  Scenario: State persists when code changes trigger reload
    When I modify a source file
    And NiceGUI triggers a hot reload
    Then the game state should be preserved
    And all clicked tiles should remain clicked

  @critical @known-issue-13
  Scenario: Multiple users maintain separate views after restart
    Given User A is on the main page
    And User B is on the stream page
    When the app restarts
    Then User A should see the interactive board with saved state
    And User B should see the read-only board with saved state
    And both users should see the same clicked tiles

  @known-issue-13
  Scenario: Concurrent updates are handled correctly
    Given two users are playing simultaneously
    When User A clicks tile "(1,1)"
    And User B clicks tile "(3,3)" at the same time
    And the app saves state
    Then both clicks should be preserved
    And the state should contain both "(1,1)" and "(3,3)"

  @edge-case
  Scenario: Corrupted state is handled gracefully
    Given the game has saved state
    When the stored state becomes corrupted
    And the app tries to load state
    Then the app should not crash
    And a fresh game should be initialized
    And an error should be logged

  @future
  Scenario: State migration handles version changes
    Given the game has state saved in an old format
    When the app starts with a new state format
    Then the old state should be migrated successfully
    And all game data should be preserved

  @implemented
  Scenario: Stream view shows closed game state on initial load
    Given the game has been closed
    When a user navigates to the stream page
    Then they should see "GAME CLOSED" message
    And they should not see the bingo board

  @implemented
  Scenario: Stream view updates when game is closed while viewing
    Given a user is viewing the stream page
    And the game is currently open
    When the game is closed from the main page
    Then the stream view should update to show "GAME CLOSED"
    And the bingo board should be hidden on the stream view

  @future @server-side-persistence
  Scenario: State shared between different browsers
    Given User A clicks tile "(1,1)" in Chrome
    When User B opens the game in Firefox
    Then User B should see tile "(1,1)" as clicked
    And both users should see the same game state

  @future @performance
  Scenario: Debounced saves reduce disk I/O
    When I rapidly click 10 tiles within 1 second
    Then the state should be saved to disk only once
    And all 10 clicks should be preserved
    And disk I/O should be minimized

  @future @server-side-persistence
  Scenario: Atomic state updates prevent corruption
    Given two users click different tiles simultaneously
    When User A clicks "(1,1)"
    And User B clicks "(2,2)" at the exact same time
    Then both clicks should be saved
    And the state file should not be corrupted

  @future @operations
  Scenario: State backup and recovery
    Given the game has been running for a week
    When I check the state backup directory
    Then I should see periodic backup files
    And I should be able to restore from any backup