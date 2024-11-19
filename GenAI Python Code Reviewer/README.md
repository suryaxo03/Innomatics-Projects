# Overview
This is a simple GenAI Chatbot where it can input a Python script and look for potential bugs and give feedback and suggestions for fixes with accurate bug reports and code snippets.

# How to get a GoogleAI API key?
1) Go to console.cloud.google.com
2) If you are new to Google Cloud, you can see a "Select Project" dropdown on the top left near the Google Cloud logo, select that
3) Click on New Project and give it a name of your choice and click on Create
4) Once created, you will receive a notification that your project has been created successfully
5) This project is required to create an API key
6) Then go to aistudio.google.com/app/apikey
7) Click on "Create API key"
8) It will ask you to select the Google Cloud project, so select the project that you just created
9) Then click on "Create API key in existing project"
10) Once created copy the API key and save it somewhere safe and secure
11) You can use this key to build your GenAI applications

# Code files info
app.py contains the code to a Chatbot-themed application, similar to that of ChatGPT. It can store the history and can be used to bring back the previous if asked\
app_review.py contains an updated code with much better interface and the with separate input and output tabs, anc the input can be written seamlessly too, yet the history won't be saved in this
