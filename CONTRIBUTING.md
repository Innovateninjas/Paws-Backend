## Contributing Guidelines 👨‍💻 

###  How to contribute
- Take a look at the existing [Issues](https://github.com/Innovateninjas/Paws-Backend) or [create a new issue](https://github.com/Innovateninjas/Paws-Backend/issues/new/choose)!
- Fork the Repo. Then, create a branch for any issue that you are working on. Finally, commit your work.
- Create a **[Pull Request](https://github.com/Innovateninjas/Paws-Backend)** (_PR_), which will be promptly reviewed and given suggestions for improvements by the community.
- Add screenshots or screen captures to your Pull Request to help us understand the effects of the changes proposed in your PR.

### Setup Instructions

## Without Docker 
1. Fork the repository and clone it.
2. Install the project dependency using `pip install -r requirements.txt`.
3. Run the project using `python manage.py runserver`.
4. Create a new branch using `git checkout -b <branch_name>`
5. For migrations ,  run this commands: 
    ```
      python manage.py makemigrations
      python manage.py migrate
    ```
    if you encounter errors like "aniresfr does not exit" , run :
    ```
       python manage.py makemigrations aniresfr
       python manage.py migrate
    ```


## With Docker 
1. Fork the repository and clone it.
2. Create a new branch using `git checkout -b <branch_name>`
3. Install Docker [Install](https://www.docker.com/get-started/)
4. Ensure `DATABASE_HOST = 'database'` this value is set in the .env file.
5. onces all .env variables are set , run this command `docker-compose up --build`



### Env Setup

**create a .env file in the root of the folder and refer .example.env**

**Secret key** 
- Generate a secret key by running this command in the terminal:

   ``` 
   python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" 
   ```

**Database(mandatory)**
- Set up a postgres db locally or in any cloud provider like vercel, and add the detail in **.env** file. SEE **.example.env**
- With Docker, the PostgreSQL database setup is handled automatically but make sure you added db details in **.env**

**Firebase(mandatory)**
- Go to [Firebase Console](https://console.firebase.google.com/u/0/) and create a new project with  any name(Do not enable the google anlytics for the project if asked )
- Go to project overview -> service account -> generate new private key (it will download the json file) add the values into **.env** 


**database Tools**
- you can used the GUI tool like DBeaver or pgAdmin.
- when setting up ensure the .env variables are same.