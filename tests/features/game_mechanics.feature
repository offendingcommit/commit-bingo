Feature: Core Game Mechanics
  As a bingo game player
  I want to play an interactive bingo game
  So that I can mark tiles and win with various patterns

  Background:
    Given I have a fresh bingo game
    And the board is generated with phrases from "phrases.txt"

  Scenario: Board generation creates proper layout
    Then the board should be 5x5 tiles
    And the center tile at position "(2,2)" should show "FREE SPACE"
    And the center tile should be pre-clicked
    And all other tiles should contain unique phrases

  Scenario: Clicking tiles toggles their state
    When I click the tile at position "(0,0)"
    Then the tile at "(0,0)" should be marked as clicked
    When I click the tile at position "(0,0)" again
    Then the tile at "(0,0)" should be unmarked

  Scenario: Win by completing a row
    When I click tiles to complete row 1
    Then the header should show "BINGO!"
    And the winning pattern "Row 1" should be recorded

  Scenario: Win by completing a column
    When I click tiles to complete column 3
    Then the header should show "BINGO!"
    And the winning pattern "Column 3" should be recorded

  Scenario: Win by completing main diagonal
    When I click tiles at positions "(0,0)", "(1,1)", "(3,3)", "(4,4)"
    Then the header should show "BINGO!"
    And the winning pattern "Main Diagonal" should be recorded

  Scenario: Win by completing anti-diagonal
    When I click tiles at positions "(0,4)", "(1,3)", "(3,1)", "(4,0)"
    Then the header should show "BINGO!"
    And the winning pattern "Anti-Diagonal" should be recorded

  Scenario: Win with four corners pattern
    When I click tiles at positions "(0,0)", "(0,4)", "(4,0)", "(4,4)"
    Then the header should show "BINGO!"
    And the winning pattern "Four Corners" should be recorded

  Scenario: Win with plus pattern
    When I click all tiles in row 2
    And I click all tiles in column 2
    Then the header should show "BINGO!"
    And the winning pattern "Plus Pattern" should be recorded

  Scenario: Win with blackout pattern
    When I click all tiles on the board
    Then the header should show "BLACKOUT!"
    And the winning pattern "Blackout" should be recorded

  Scenario: Multiple simultaneous wins
    When I click tiles to complete row 2
    And I click tiles to complete column 2
    Then the header should show "DOUBLE BINGO!"
    And both winning patterns should be recorded

  Scenario: Creating a new board resets the game
    Given I have clicked several tiles
    And the header shows "BINGO!"
    When I click the "New Board" button
    Then all tiles except "(2,2)" should be unclicked
    And the header should show "Let's Play Bingo!"
    And the board should have new phrases
    And the board iteration should increment