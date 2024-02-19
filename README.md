# NoteMakingApplication
Note Making application 
To set up this project 
create virtual environment using this commend :
python -m venv env
activate the virtual environment using this command:
env/bin/activate
cd project_folder
git clone https://github.com/Sadaf244/NoteMakingApplication.git
git checkout master
git pull origin master
To install all package run this command:
pip freeze > requirements.txt

Details About Api:

POST Signup:
url- https://notemakingapplication-production.up.railway.app/ws/v1/account/user-signup/
Body-{
    "user_name":"rk61234",
    "email_address":"rk@gmail.com",
    "password":"rk60847855"
}

POST Login:
url: https://notemakingapplication-production.up.railway.app/ws/v1/account/user-login/
Body: {
{    
    "username_or_email":"sadaf@gmail.com",
    "password":"sadaf0847855"
}

POST Create Notes
url: https://notemakingapplication-production.up.railway.app/ws/v1/notes/create-note/
Request Headers
Authorization     Token d7f28cfe9b5418c126032daa9e9577b491e50d20
Body:
{
    "content":"Reading is typically an individual activity, done silently, although on occasion a person reads out loud for other listeners; or reads aloud for one's own use, for better comprehension. "
}

POST Share Notes
url: https://notemakingapplication-production.up.railway.app/ws/v1/notes/share/
Request Headers
Authorization     Token d7f28cfe9b5418c126032daa9e9577b491e50d20
Body:
{
    "note_id":"1",
    "shared_users":[5,2]
}

POST Update Notes
url: http://127.0.0.1:8000/ws/v1/notes/update/1/
Request Headers
Authorization     Token d7f28cfe9b5418c126032daa9e9577b491e50d20
Body:
{
    "content":"apple keeps the doctor away"
}

GET Get Version History
url: https://notemakingapplication-production.up.railway.app/ws/v1/notes/version-history/1/
Request Headers
Authorization     Token d7f28cfe9b5418c126032daa9e9577b491e50d20

GET Get Notes 
url: https://notemakingapplication-production.up.railway.app/ws/v1/notes/1/
Request Headers
Authorization     Token d7f28cfe9b5418c126032daa9e9577b491e50d20
