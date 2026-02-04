## I selected Option A:
Reject the request with HTTP 409 Conflict
because it ensures data immutability. If a test_id already exists it requires a manual check or a different Id to be used preventing accidental overwriting of sensitive medical results.


## 1. Why did you choose this framework?
Ans. It is high performance and light weight for building REST APIs.

## 2. Where can this system fail?
Ans. If two users try to POST data at the exact same millisecond the file might become Locked. One of the users will receive a "Database is locked" error and not a success message.

## 3. How would you debug a data inconsistency issue?
Ans.I would first see the SQLite file to see whether the data was saved correctly or is missing.
Second thing will be that I will check whether the code is not accidentally mixing the labels when it pulls data from the database.Then i will again go to postman and send exact data that caused the error.Look at the code's manual validation logic whether it is incorrectly altering the data before it reaches the database.

## 4. What would change in production vs local?
Ans. In production I would use MySQL or PostgreSQL because they can handle thousands of people saving test results at the exact same time without crashing.And will add API key or JWT authentication for security.

## How to Run
1. Install requirements: `pip install fastapi uvicorn`
2. Run server: `uvicorn main:app --reload`
3. Test using Postman