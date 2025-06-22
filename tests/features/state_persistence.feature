Feature: Persistent Game State
  As a bingo game player
  I want my game state to persist across app restarts
  So that I don't lose progress if the app needs to restart

  Background:
    Given I have a bingo game in progress
    And I have clicked tiles at positions "(0,1)", "(2,3)", and "(4,4)"
    And the game header shows "3 tiles clicked"

  Scenario: State persists through graceful restart
    When the app restarts gracefully
    Then the clicked tiles should remain at "(0,1)", "(2,3)", and "(4,4)"
    And the header should still show "3 tiles clicked"
    And the board should show the same phrases

  Scenario: State persists through unexpected restart
    When the app crashes and restarts
    Then the clicked tiles should remain at "(0,1)", "(2,3)", and "(4,4)"
    And the header should still show "3 tiles clicked"
    And the board should show the same phrases

  Scenario: State persists when code changes trigger reload
    When I modify a source file
    And NiceGUI triggers a hot reload
    Then the game state should be preserved
    And all clicked tiles should remain clicked

  Scenario: Multiple users maintain separate views
    Given User A is on the main page
    And User B is on the stream page
    When the app restarts
    Then User A should see the interactive board with saved state
    And User B should see the read-only board with saved state
    And both users should see the same clicked tiles

  Scenario: Concurrent updates don't cause data loss
    Given two users are playing simultaneously
    When User A clicks tile "(1,1)"
    And User B clicks tile "(2,2)" at the same time
    Then both tiles should be marked as clicked
    And the state should show 5 total clicked tiles

  Scenario: State recovery from corruption
    Given the stored state becomes corrupted
    When the app tries to load the corrupted state
    Then it should log an error
    And it should start with a fresh game
    And it should not crash