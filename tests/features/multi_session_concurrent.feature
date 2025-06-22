Feature: Multi-Session Concurrent Access
  As a bingo game host
  I want the game to handle multiple simultaneous users
  So that everyone can play together without conflicts

  Background:
    Given the bingo application is running
    And the board has been generated with test phrases

  Scenario: Multiple users clicking different tiles simultaneously
    Given 3 users are connected to the game
    When user 1 clicks tile at position (0, 0)
    And user 2 clicks tile at position (1, 1)
    And user 3 clicks tile at position (2, 0)
    Then all 3 tiles should be marked as clicked
    And the state file should contain 3 clicked tiles
    And all users should see the same game state

  Scenario: Concurrent game control actions
    Given 2 users are connected to the game
    And user 1 has clicked tile at position (0, 0)
    When user 1 closes the game
    And user 2 tries to click tile at position (1, 1) simultaneously
    Then the game should be in closed state
    And only the first tile should be marked as clicked
    And both users should see the closed game message

  Scenario: State consistency across new connections
    Given user 1 is connected to the game
    And user 1 has clicked tiles at positions (0, 0), (0, 1), (0, 2)
    When user 2 connects to the game
    Then user 2 should see 3 tiles already clicked
    And user 2 should see tiles at positions (0, 0), (0, 1), (0, 2) as clicked

  Scenario: Rapid tile clicking from multiple sessions
    Given 5 users are connected to the game
    When all users rapidly click random tiles
    Then all valid clicks should be registered
    And no clicks should be lost
    And the final state should be consistent across all users

  Scenario: Server restart with active users
    Given 2 users are connected to the game
    And the users have clicked several tiles
    When the server state is saved
    And the server is simulated to restart
    And users reconnect to the game
    Then all previously clicked tiles should remain clicked
    And users can continue playing from where they left off