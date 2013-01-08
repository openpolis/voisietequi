Feature: Party speaker answers questions
    As party speaker,
    I want to use a private form with VSQ questions,
    in order to answer the questions for my Party

    Background:
        Given the questions exist in the DB
          and the party exists in the DB

    Scenario:
        Given I have not answered the questions, yet
         When I visit the private URL, with my party-key
          and I fill in the empty answers fields
          and I press the Submit button
         Then the answers are stored into the system
          and the page shows the form with the read-only answers

    Scenario:
        Given I have already answered the questions
         When I visit the private URL, with my party-key
         then the page shows the form with the read-only answers
