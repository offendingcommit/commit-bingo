Feature: Board Generation and Phrase Management
  As a bingo game administrator
  I want to customize and generate bingo boards
  So that games can have relevant and varied content

  Background:
    Given I have a phrases.txt file with bingo phrases

  Scenario: Loading phrases from file
    When the application starts
    Then phrases should be loaded from "phrases.txt"
    And empty lines should be ignored
    And whitespace should be trimmed from phrases

  Scenario: Handling insufficient phrases
    Given the phrases file contains only 10 phrases
    When I try to generate a board
    Then the board generation should fail gracefully
    And an appropriate error message should be shown

  Scenario: Seeded board generation
    When I generate a board with seed "test123"
    And I generate another board with seed "test123"
    Then both boards should have identical phrase arrangements
    
  Scenario: Random board generation without seed
    When I generate a board without a seed
    And I generate another board without a seed
    Then the boards should have different phrase arrangements

  Scenario: Board iteration tracking
    Given the board iteration is 1
    When I generate a new board
    Then the board iteration should be 2
    And the iteration should be displayed to users

  Scenario: Phrase uniqueness on board
    When a board is generated
    Then each phrase should appear only once on the board
    And no phrase should be repeated except "FREE SPACE"

  Scenario: Phrase text processing
    Given I have phrases with multiple spaces
    When the board displays the phrases
    Then consecutive spaces should be preserved
    And line breaks should be handled appropriately

  Scenario: Special characters in phrases
    Given phrases contain emojis and special characters
    When the board is generated
    Then all special characters should display correctly
    And UTF-8 encoding should be maintained

  Scenario: Dynamic phrase updates
    Given the game is running with a board
    When I update the phrases.txt file
    And I click "New Board"
    Then the new board should use the updated phrases

  Scenario: Phrase length distribution
    When I analyze the loaded phrases
    Then short phrases (1-10 chars) should use larger fonts
    And medium phrases (11-20 chars) should use medium fonts
    And long phrases (21+ chars) should use smaller fonts