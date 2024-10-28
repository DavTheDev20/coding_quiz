How to run application:

1. Create python virtual enviornment by runnning the `python -m venv .venv` command
2. Access this virtual enviornment:
   - Windows: `.venv/Scripts/activate`
   - MAC: `.venv/bin/activate`
3. Install all python packages from requirements.txt file with the command `python -m pip install -r requirements.txt`
4. Create .env file and include the below variables _NOTE: application uses mysql database_:
   - DB_USER (user for mysql instance)
   - DB_PASSWORD (password for mysql instance)
   - DB_HOST (host for mysql instance, localhost if running locally)
   - DB_PORT (port for mysql instance, 3306 if running locally)
5. Run application with `python main.py` command

_Note: Ensure that schema (coding_quiz_db) is created in mysql before running application for first time_
