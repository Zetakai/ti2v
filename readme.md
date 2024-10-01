How to Activate the Virtual Environment
Now that you have created the virtual environment, you will need to activate it before you can use it in your project. On a mac, to activate your virtual environment, run the code below:

source env/bin/activate
This will activate your virtual environment. Immediately, you will notice that your terminal path includes env, signifying an activated virtual environment.

Note that to activate your virtual environment on Widows, you will need to run the following code below (See this link to fully understand the differences between platforms):

 env/Scripts/activate.bat //In CMD
 env/Scripts/Activate.ps1 //In Powershel

Requirements File
Why is a requirements file important to your project? Consider that you package your project in a zip file (without the env folder) and you share with your developer friend.

To recreate your development environment, your friend will just need to follow the above steps to activate a new virtual environment.

Instead of having to install each dependency one by one, they could just run the code below to install all your dependencies within their own copy of the project:

 ~ pip install -r requirements.txt
Note that it is generally not advisable to share your env folder, and it should be easily replicated in any new environment.

Typically your env directory will be included in a .gitignore file (when using version control platforms like GitHub) to ensure that the environment file is not pushed to the project repository.

How to Deactivate a Virtual Environment
To deactivate your virtual environment, simply run the following code in the terminal:

 ~ deactivate

 only support 12.4 cuda for now