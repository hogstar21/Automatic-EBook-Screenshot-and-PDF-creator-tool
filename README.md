**Welcome to me automatic screenshot and .PDF tool. This tool was built to screenshot many pages of a ebook automatically and then make a PDF out of it. **
--------------------------------------------------------------------------------------------------------------------------------------------------------------
**PART 1 - Do this part first**

To make it work, you will need to download a copy of Python version 3.6 or newer recommended. https://www.python.org/downloads/ Just download the latest stable copy. 

IMPORTANT -- Right before you hit install for Python, the popup screen will ask you if you want to add Python to PATH. Please check yes. What this does is allows you to run Python from any command line or terminal window without specifying its full installation path. 
Bottom line, enabling PATH just makes your life easier. 

Once Python is installed, open Windows Powershell or even just Command Prompt (Win + R and then type cmd)
Then you need to install PyAutoGUI To install. It's super easy. In the terminal (either command prompt or powershell), type the following:

pip install pyautogui

then press ENTER. Let it do it's thing. 

-------------------------------------------------------------------------------------------------------------------------------------------------------------
**PART 2 - Now you're ready to make the program work**

Put the python file in a empty folder to make it easy. Your screenshots will be saved here.
Start up Powershell. Navigate to the directory with the .py file. You navigate terminal by using CD (change directory) commands. 
Use the command "python ebook_screenshot.py" 

OR SIMPLY double click the .py script LOLZ

This will start the program up. Just follow the simple questions. 
A folder in the directory with your python script will automatically be created and all the screenshots will be in there.

**PART 3 - Now the program will make a .pdf if you want**

The program will ask if you want to create a .PDF of the screenshots (in the order they were taken), what the .PDF file name should be, and also if you want to delete the folder with the screenshots.
