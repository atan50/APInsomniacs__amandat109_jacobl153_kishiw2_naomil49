# Somni Bites by APInsomniacs
## Roster
Amanda Tan: Project Lead + overall system/file structure\
Naomi Lai: Routing + favorites page\
Jacob Lukose: Database\
Kishi Wijaya: HTML & CSS

## Description 
Somni Bites is a website for any food-related content where users may access catalogs of food, recipes, and news. Any visitors to the site may view these catalogs, which detail various foods and their nutritional information, substitutions, and product searches; recipes and their cooking tips; and food-related top stories. Logged in users have access to a greater variety of features. In addition to viewing the above, they may favorite and add notes to any content of interest. They may also find nearby grocery stores using their location.

## Install Guide:
  To install, go to the top of the page and click the green button that says "Code". In the dropdown that appears, click "Download Zip" at the bottom. Extract the zip from your downloads into your home directory. <br>

OR
  
  To clone the repository, go to the top of the page and click the green button that says "Code". In the dropdown that appears, choose either "HTTPS" or "SSH" under the "Clone" section and copy the provided URL. Open up your computer's terminal and type "git clone {URL HERE}"
## Launch Codes:
  Instructions:
  1. Make a python virtual environment

      a. Open up your device's terminal

      b. Type ```$ python3 -m venv {path name}``` or ```$ py -m venv {path name}```

      c. Type in one of the commands into your terminal for your specific OS to activate the environment

      - Linux: ```$ . {path name}/bin/activate```
    
      - Windows Command Prompt: ```> {path name}\Scripts\activate```

      - Windows PowerShell: ```> . .\{path name}\Scripts\activate```

      - MacOS: ```$ source {path name}/bin/activate```

      (If successful, the command line should display the name of your virtual environment: ```({path name})$ ```)

      d. When done, type ```$ deactivate``` to deactivate the virtual environment

  3. Ensure your virtual environment is activated

  4. Access the repository by typing ```$ cd coolbeans__evanc107_amandat109_dannym2789_jiayingz16```

  5. Type ```$ pip install -r requirements.txt``` to install the required modules

 - If terminal returns ```zsh: command not found: pip```, type ```$ pip3 install -r requirements.txt``` because ```$ pip``` is for python2.

  6. Type ```$ python3 app/app.py``` to run the application

  7. Copy / type "http://127.0.0.1:5000" or "http://localhost" onto a browser to view the website

----
Credit: Install Guide and Launch Codes from CoolBeans P00
