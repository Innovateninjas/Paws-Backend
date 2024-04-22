## Contributing 👨‍💻 

###  How to contribute
- Take a look at the existing [Issues](https://github.com/Innovateninjas/Paws-Backend) or [create a new issue](https://github.com/Innovateninjas/Paws-Backend/issues/new/choose)!
- Fork the Repo. Then, create a branch for any issue that you are working on. Finally, commit your work.
- Create a **[Pull Request](https://github.com/Innovateninjas/Paws-Backend)** (_PR_), which will be promptly reviewed and given suggestions for improvements by the community.
- Add screenshots or screen captures to your Pull Request to help us understand the effects of the changes proposed in your PR.

### Setup && Installation

1. Fork the repository and clone it.
2. Install the project dependency using `pip install -r requirements.txt`.
3. Run the project using `python manage.py runserver`.
4. Create a new branch using `git checkout -b <branch_name>`

**create a .env file in the root of the folder and see .example.env**

**Database(mandatory)**

- Set up a postgres db locally or in any cloud provider like vercel, and add the detail in **.env** file. SEE **.example.env**

**Firebase(mandatory)**

- Go to [Firebase Console](https://console.firebase.google.com/u/0/) and create a new project with any name(Do not enable the google anlytics for the project if asked )  
- Go to project overview  under  *General* tab scroll down add app select web and then copy the firebaseconfig.json(dont try below its deleted already)

- to project overview in firebase  under Cloud Messaging Generate key pair  copy the key and place  it the in **.env** 
