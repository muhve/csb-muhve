https://github.com/muhve/csb-muhve
Project should work with standard latest version Django installation without any additional packages. So you can run the app by simply running "python -m manage.py runserver" and opening http://127.0.0.1:8000/my_broken_app/ in your browser.

FLAW 1: https://owasp.org/Top10/A01_2021-Broken_Access_Control/
https://github.com/muhve/csb-muhve/blob/main/my_broken_app/views.py#L20

The app allows the user to see other user's tasks. This happens because the user is not anyhow verified when going to specific tasks detail view. So by just navigating to a proper url, anyone can see any task.

To fix the flaw, you can uncomment the lines from 24 to 32. What it does is that it check's if the current logged in user is the same user that has is set as the user for this task. Meaning the user object has the same user_id as the users id is. If it fails to verify this, it will redirect the user to task listing view. We could of course decide to handle this case in any other way too, for example by showing the user some kind on "permission denied" page. The important thing is to make sure, that we don't just trust that the user won't navigate to any url manually, and implement this check for all the routes where we need to make sure the user is only accessing items they have permission to.


FLAW 2: https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/
https://github.com/muhve/csb-muhve/blob/main/mysite/settings.py#L90

The app has all password validation methods disabled. This means that the user can authenticate with any password, possibly even with very weak passwords. User can now register with a simple password like 'password', which would then be very possible for an attacker to guess. 

To fix the flaw, you can uncomment the lines from 91 to 102 in settings.py, to add proper validators for the authentication. Django has these 4 password validator built in, which should be a decent check for a proper password. It requires the password to be long enough, not be only numeric, not too similar to username, and not too common. We could possibly add more validations to it, but it's hard to guarantee a strong password with any validations, and these should be sufficient.


FLAW 3: https://owasp.org/Top10/A03_2021-Injection/
https://github.com/muhve/csb-muhve/blob/main/my_broken_app/views.py#L56

The app uses raw SQL queries when inserting a new task into the system. This is obviously a very bad idea and allows SQL injection attack. For example someone could create a task with following information, to create a new task for any other user in the system, or similarily flood someones tasks:

title: this task will be created for myself
description: asd'), ('injected task', 1, false, '2023-01-01', '2023-01-01', 'this task is added to the user with id 1

By changing the user_id, which here is 1, the user can now inject tasks to any other user. They could also add how many tasks they ever wanted in the list to flood someones tasks.

This SQL injection flaw is very probably vulnerable to way more serious attacks too, like dropping tables or similar, but that would require more advanced SQL queries. 


FLAW 4: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
https://github.com/muhve/csb-muhve/blob/main/mysite/settings.py#L27

The app would now be running in debug mode, which would allow a lot of information for the user about the app, and possible ways to exploit it. This is fine for local development environment, but when deploying the app it is important to set the debug mode to false.

To fix this flaw, the debug mode should be set to FALSE, and if it would be needed in development environment, it could be read from an environment variable. 


FLAW 5: https://owasp.org/Top10/A02_2021-Cryptographic_Failures/
https://github.com/muhve/csb-muhve/blob/main/mysite/settings.py#L23

The app uses very weak secret_key, which makes it vulnerable in a lot of ways, one being its cryptography. These features will be useless without a strong secret_key https://docs.djangoproject.com/en/3.2/topics/signing/

To fix this flaw, one could change the line to be like the one that is now commented out, where the SECRET_KEY is read from an environment variable. The admin just needs to make sure that the environment variable is properly set in the production environment when deploying the app.