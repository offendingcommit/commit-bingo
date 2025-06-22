Feature: Multi-View Synchronization
  As a bingo game host
  I want the game state to sync between main and stream views
  So that viewers see real-time updates without control access

  Background:
    Given the bingo application is running
    And I have both main view at "/" and stream view at "/stream" open

  Scenario: Stream view shows read-only board
    When I navigate to the stream view
    Then I should see the bingo board
    But I should not see any control buttons
    And clicking tiles should have no effect

  Scenario: Main view shows interactive controls
    When I navigate to the main view
    Then I should see the bingo board
    And I should see "New Board" button
    And I should see "Close Game" button
    And I should see "Reopen Game" button
    And clicking tiles should toggle their state

  Scenario: Tile clicks sync from main to stream
    Given both views show the same board
    When I click tile "(1,1)" in the main view
    Then tile "(1,1)" should appear clicked in the stream view within 0.1 seconds

  Scenario: Header updates sync across views
    Given the header shows "Let's Play Bingo!" in both views
    When I complete a winning pattern in the main view
    Then the stream view header should update to "BINGO!" within 0.1 seconds

  Scenario: Game closure syncs to stream view
    Given the game is open in both views
    When I click "Close Game" in the main view
    Then the stream view should show "GAME CLOSED" message
    And the board should be hidden in the stream view

  Scenario: Game reopening syncs to stream view
    Given the game is closed
    When I click "Reopen Game" in the main view
    Then the stream view should show the board again
    And the header should be visible in the stream view

  Scenario: New board generation syncs to stream
    Given both views show the same board state
    When I click "New Board" in the main view
    Then the stream view should show the new board
    And all previous clicked tiles should be cleared in both views
    And the board iteration should match in both views

  Scenario: Multiple stream viewers see same state
    Given I have 3 stream view windows open
    When I click tile "(3,3)" in the main view
    Then all 3 stream views should show tile "(3,3)" as clicked
    And all views should update within 0.1 seconds

  Scenario: Late-joining stream viewers see current state
    Given the game has several clicked tiles
    And the header shows "BINGO!"
    When a new user navigates to the stream view
    Then they should see all currently clicked tiles
    And they should see the current header text

  Scenario: Disconnection handling
    Given a stream viewer is connected
    When their connection is temporarily lost
    And I make changes in the main view
    And the stream viewer reconnects
    Then they should see the updated game state