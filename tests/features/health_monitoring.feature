Feature: Health Monitoring and System Status
  As a system administrator
  I want to monitor the health and status of the bingo application
  So that I can ensure it's running properly and debug issues

  Background:
    Given the bingo application is running

  Scenario: Health endpoint availability
    When I send a GET request to "/health"
    Then I should receive a 200 OK response
    And the response should be in JSON format

  Scenario: Health endpoint reports user counts
    Given 3 users are on the main page
    And 5 users are on the stream page
    When I check the health endpoint
    Then it should report 3 root path users
    And it should report 5 stream path users
    And it should report 8 total users

  Scenario: Health endpoint during high load
    Given 100 users are connected
    When I check the health endpoint
    Then the response time should be under 100ms
    And the user counts should be accurate

  Scenario: User connection tracking
    When a user connects to the main page
    Then the root path user count should increment
    When the user disconnects
    Then the root path user count should decrement

  Scenario: Stream connection tracking
    When a user connects to the stream page
    Then the stream path user count should increment
    When the user disconnects
    Then the stream path user count should decrement

  Scenario: Connection recovery
    Given a user is connected to the main page
    When their connection drops temporarily
    And they reconnect within 5 seconds
    Then the user count should remain stable
    And their game state should be preserved

  Scenario: Memory usage monitoring
    When I monitor the application over time
    Then memory usage should remain stable
    And there should be no memory leaks
    And garbage collection should work properly

  Scenario: Error logging
    When an error occurs in the application
    Then it should be logged with appropriate severity
    And the error should include stack trace information
    And the application should continue running

  Scenario: Performance metrics
    When I measure application performance
    Then page load time should be under 2 seconds
    And tile click response should be under 50ms
    And board generation should be under 100ms