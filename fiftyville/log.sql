-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Get list of tables at my disposale and there layouts
.schema

-- Get description of crime scene
SELECT description, year
FROM crime_scene_reports
WHERE month = 7 AND day = 28
AND street = 'Humphrey Street';

-- Get vehicles in the bakery around the time of the robbery
SELECT * FROM bakery_security_logs
WHERE year = 2021
AND month = 7
AND day = 28;

-- LINK names to license plates that were at the bakery
SELECT DISTINCT people.name, people.license_plate FROM people
JOIN bakery_security_logs
ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.year = 2021
AND bakery_security_logs.month = 7
AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10;

-- ALL the interviews that took place on the day of the robbery
SELECT * FROM interviews WHERE year = 2021 AND month = 7 and day = 28;

-- Show all the people who left the scene withing 10 minites like Ruth said in her interview
SELECT DISTINCT people.name, people.license_plate FROM people
JOIN bakery_security_logs
ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.year = 2021
AND bakery_security_logs.month = 7
AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute BETWEEN 15 AND 25
AND bakery_security_logs.activity = "exit";

-- Show the people who withdrew money from the atm on Leggett Street
SELECT amount, name, phone_number, passport_number, license_plate FROM atm_transactions
JOIN bank_accounts
ON atm_transactions.account_number = bank_accounts.account_number
JOIN people
ON bank_accounts.person_id = people.id
WHERE atm_transactions.year = 2021
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_transactions.atm_location = "Leggett Street"
AND atm_transactions.transaction_type = "withdraw";

-- Show who masde a call for a 1 minute after the robbery
SELECT name, passport_number, license_plate FROM people
JOIN phone_calls
ON phone_calls.caller = people.phone_number
WHERE phone_calls.year = 2021
AND phone_calls.month = 7
AND phone_calls.day = 28
AND phone_calls.duration < 60;

-- Combine all results
SELECT name, passport_number FROM people
JOIN phone_calls
ON phone_calls.caller = people.phone_number
JOIN bank_accounts
ON bank_accounts.person_id = people.id
JOIN bakery_security_logs
ON bakery_security_logs.license_plate = people.license_plate
JOIN atm_transactions
ON atm_transactions.account_number = bank_accounts.account_number
WHERE phone_calls.year = 2021
AND phone_calls.month = 7
AND phone_calls.day = 28
AND phone_calls.duration < 60
AND atm_transactions.year = 2021
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_transactions.atm_location = "Leggett Street"
AND atm_transactions.transaction_type = "withdraw"
AND bakery_security_logs.year = 2021
AND bakery_security_logs.month = 7
AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute BETWEEN 15 AND 25
AND bakery_security_logs.activity = "exit";

-- Find flight id and seat from passport number
SELECT * FROM passengers
WHERE passengers.passport_number = (
    SELECT passport_number FROM people
    JOIN phone_calls
    ON phone_calls.caller = people.phone_number
    JOIN bank_accounts
    ON bank_accounts.person_id = people.id
    JOIN bakery_security_logs
    ON bakery_security_logs.license_plate = people.license_plate
    JOIN atm_transactions
    ON atm_transactions.account_number = bank_accounts.account_number
    WHERE phone_calls.year = 2021
    AND phone_calls.month = 7
    AND phone_calls.day = 28
    AND phone_calls.duration < 60
    AND atm_transactions.year = 2021
    AND atm_transactions.month = 7
    AND atm_transactions.day = 28
    AND atm_transactions.atm_location = "Leggett Street"
    AND atm_transactions.transaction_type = "withdraw"
    AND bakery_security_logs.year = 2021
    AND bakery_security_logs.month = 7
    AND bakery_security_logs.day = 28
    AND bakery_security_logs.hour = 10
    AND bakery_security_logs.minute BETWEEN 15 AND 25
    AND bakery_security_logs.activity = "exit"
);

-- Get flight origin and destination airports
SELECT airports.id, flights.origin_airport_id, flights.destination_airport_id FROM flights
JOIN airports
ON airports.id = flights.origin_airport_id
WHERE flights.id = (
    SELECT passengers.flight_id FROM passengers
    WHERE passengers.passport_number = (
        SELECT passport_number FROM people
        JOIN phone_calls
        ON phone_calls.caller = people.phone_number
        JOIN bank_accounts
        ON bank_accounts.person_id = people.id
        JOIN bakery_security_logs
        ON bakery_security_logs.license_plate = people.license_plate
        JOIN atm_transactions
        ON atm_transactions.account_number = bank_accounts.account_number
        WHERE phone_calls.year = 2021
        AND phone_calls.month = 7
        AND phone_calls.day = 28
        AND phone_calls.duration < 60
        AND atm_transactions.year = 2021
        AND atm_transactions.month = 7
        AND atm_transactions.day = 28
        AND atm_transactions.atm_location = "Leggett Street"
        AND atm_transactions.transaction_type = "withdraw"
        AND bakery_security_logs.year = 2021
        AND bakery_security_logs.month = 7
        AND bakery_security_logs.day = 28
        AND bakery_security_logs.hour = 10
        AND bakery_security_logs.minute BETWEEN 15 AND 25
        AND bakery_security_logs.activity = "exit")
);

-- Get city of destination airport
SELECT airports.city FROM airports
WHERE airports.id = (
    SELECT flights.destination_airport_id FROM flights
    JOIN airports
    ON airports.id = flights.origin_airport_id
    WHERE flights.id = (
        SELECT passengers.flight_id FROM passengers
        WHERE passengers.passport_number = (
        SELECT passport_number FROM people
        JOIN phone_calls
        ON phone_calls.caller = people.phone_number
        JOIN bank_accounts
        ON bank_accounts.person_id = people.id
        JOIN bakery_security_logs
        ON bakery_security_logs.license_plate = people.license_plate
        JOIN atm_transactions
        ON atm_transactions.account_number = bank_accounts.account_number
        WHERE phone_calls.year = 2021
        AND phone_calls.month = 7
        AND phone_calls.day = 28
        AND phone_calls.duration < 60
        AND atm_transactions.year = 2021
        AND atm_transactions.month = 7
        AND atm_transactions.day = 28
        AND atm_transactions.atm_location = "Leggett Street"
        AND atm_transactions.transaction_type = "withdraw"
        AND bakery_security_logs.year = 2021
        AND bakery_security_logs.month = 7
        AND bakery_security_logs.day = 28
        AND bakery_security_logs.hour = 10
        AND bakery_security_logs.minute BETWEEN 15 AND 25
        AND bakery_security_logs.activity = "exit")
)
);

-- Get person name from passport number
SELECT people.name from people
JOIN passengers
ON passengers.passport_number = people.passport_number
WHERE people.passport_number = (
    SELECT passport_number FROM people
    JOIN phone_calls
    ON phone_calls.caller = people.phone_number
    JOIN bank_accounts
    ON bank_accounts.person_id = people.id
    JOIN bakery_security_logs
    ON bakery_security_logs.license_plate = people.license_plate
    JOIN atm_transactions
    ON atm_transactions.account_number = bank_accounts.account_number
    WHERE phone_calls.year = 2021
    AND phone_calls.month = 7
    AND phone_calls.day = 28
    AND phone_calls.duration < 60
    AND atm_transactions.year = 2021
    AND atm_transactions.month = 7
    AND atm_transactions.day = 28
    AND atm_transactions.atm_location = "Leggett Street"
    AND atm_transactions.transaction_type = "withdraw"
    AND bakery_security_logs.year = 2021
    AND bakery_security_logs.month = 7
    AND bakery_security_logs.day = 28
    AND bakery_security_logs.hour = 10
    AND bakery_security_logs.minute BETWEEN 15 AND 25
    AND bakery_security_logs.activity = "exit"
);

-- Get name of robbers accomplice from phone call
SELECT people.name FROM people
WHERE people.phone_number = (
    SELECT phone_calls.receiver FROM phone_calls
    JOIN people
    ON people.phone_number = phone_calls.caller
    WHERE phone_calls.year = 2021
    AND phone_calls.month = 7
    AND phone_calls.day = 28
    AND phone_calls.duration < 60
    AND people.name = "Bruce"
);