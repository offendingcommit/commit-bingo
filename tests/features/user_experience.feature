Feature: User Experience and Interface
  As a bingo game user
  I want a responsive and intuitive interface
  So that I can easily play the game on any device

  Background:
    Given I am using the bingo application

  Scenario: Mobile-friendly touch targets
    When I view the game on a mobile device
    Then all clickable tiles should be at least 44x44 pixels
    And control buttons should have both text and icons
    And the interface should be responsive to screen size

  Scenario: Dynamic text sizing for readability
    When a tile contains a short phrase like "Um"
    Then the text should be displayed in a larger font
    When a tile contains a long phrase
    Then the text should be smaller to fit within the tile
    And text should never overflow the tile boundaries

  Scenario: Visual feedback for interactions
    When I hover over an unclicked tile
    Then the tile should show a hover effect
    When I click a tile
    Then the tile should immediately show clicked styling
    And the transition should be smooth

  Scenario: Font loading and fallbacks
    When the page loads
    Then custom fonts should load from Google Fonts
    And if fonts fail to load
    Then readable fallback fonts should be used

  Scenario: Loading state indication
    When I navigate to the application
    Then I should see a loading indicator
    And once the board is ready
    Then the loading indicator should disappear
    And the game should be interactive

  Scenario: Error handling for user actions
    When I rapidly click multiple tiles
    Then all clicks should be registered correctly
    And the UI should remain responsive
    And no errors should appear in the console

  Scenario: Accessibility features
    When I use keyboard navigation
    Then I should be able to tab through interactive elements
    And pressing Enter should activate the focused element
    And focus indicators should be clearly visible

  Scenario: Board layout consistency
    When I resize the browser window
    Then the board should maintain its square aspect ratio
    And tiles should remain evenly distributed
    And text should remain readable

  Scenario: Control button states
    Given the game is open
    Then the "Close Game" button should be enabled
    And the "Reopen Game" button should be disabled
    When I close the game
    Then the "Close Game" button should be disabled
    And the "Reopen Game" button should be enabled

  Scenario: Page refresh maintains context
    Given I have clicked several tiles
    When I refresh the page
    Then I should return to the same view (main or stream)
    And the game state should be preserved
    And the UI should load without errors