![image](https://github.com/sankalp-7/FocusLearn-YT/assets/104098061/2b7cf0d6-0ae3-46d7-b062-cd10fff78c5c)

# Live Demo

https://github.com/sankalp-7/FocusLearn-YT/assets/104098061/9adf6c3c-0ac0-45eb-9922-93eebd312c20

# Your Ultimate Educational Video Learning Platform

Focus Learn YT is a web application designed to provide students with a distraction-free and educational video learning experience. It combines the features of a video platform with innovative tools such as video summarization and quiz generation. With Focus Learn YT, students can enhance their learning efficiency and test their knowledge after watching videos.

## Key Features

- **Distraction-Free Learning:** Unlike traditional video platforms, Focus Learn YT provides a clean and clutter-free environment, eliminating distractions and focusing on the educational content.

- **Video Summarization:** Long educational videos are condensed into concise summaries, saving time while delivering the essential information.

- **Quiz Generation:** Automatically generate quizzes based on the video content, allowing students to reinforce their understanding through interactive assessments.

- **Responsive Design:** Enjoy a seamless learning experience across various devices, including desktops, tablets, and smartphones.

- **Personal Notes Making:** This feature allows user to create personalized notes on videos.

- **User Profiles:** Added authentication for personal user profiles.

 ## How It Works
 - **Quiz Generation:** When a user clicks a video he has two other options than simply watching the video--He can generate a concise summary of the video by clicking the **summarize** button or generate a quiz based on the video's content by clicking the **generate quiz** button.
 - The quiz is generated as follows--The youtube transcript is retrieved and then sent to chatgpt via api call along with a prompt to generate 10 quiz questions. The questions are then transformed to json format and is integrated at the frontend.
## Getting Started

To start using Focus Learn YT, follow these steps:

1. Clone the repository: `git clone git@github.com:sankalp-7/FocusLearn-YT.git`

2. Install dependencies: `pip install -r requirements.txt`

3. Set up your openAI api and youtube api keys, then: `python manage.py migrate`

4. Run the development server: `python manage.py runserver`

5. Access the app in your web browser at `http://localhost:8000`

*OR*

1. Install Docker, Docker Compose

2. Clone the repository -- `git clone git@github.com:sankalp-7/FocusLearn-YT.git`

3. `docker-compose up --build`

4. open localhost:80 to view the application



## Images 

# LOGIN PAGE

![image](https://github.com/sankalp-7/FocusLearn-YT/assets/104098061/1bba73f1-6d3f-432f-8d8b-c7ae9a7881ab)

# HOME PAGE

![image](https://github.com/sankalp-7/FocusLearn-YT/assets/104098061/87ee2608-5d3f-429f-9b14-f27e3add0f77)


# VIDEOS PAGE

![image](https://github.com/sankalp-7/FocusLearn-YT/assets/104098061/ec72db36-3d3a-4b9b-b01b-2e78d1963883)

# SUMMARY,QUIZ,NOTES,QUERY MODAL

![image](https://github.com/sankalp-7/FocusLearn-YT/assets/104098061/b1473af1-6cfd-4bf3-ad8f-bc52c3539152)


# SUMMARY PAGE

![image](https://github.com/sankalp-7/FocusLearn-YT/assets/104098061/6f461b69-1e05-461e-bd13-8354f2726cf6)

# QUIZ PAGE
## Q1
![image](https://github.com/sankalp-7/FocusLearn-YT/assets/104098061/2471462f-da7f-4eef-b6e0-b2e893c5befa)
## Q2
![image](https://github.com/sankalp-7/FocusLearn-YT/assets/104098061/40f9b289-634d-4747-8d24-cbd5427f65a6)
## Q3
![image](https://github.com/sankalp-7/FocusLearn-YT/assets/104098061/495ed28c-7747-42cb-9567-4667dcc080b7)
And 7 more questions are generated for user to answer...

# QUIZ REVIEW PAGE

![image](https://github.com/sankalp-7/FocusLearn-YT/assets/104098061/a897de84-f3b7-44c0-96e7-e6495ab9e00b)

![image](https://github.com/sankalp-7/FocusLearn-YT/assets/104098061/20f3b04a-9a8f-46ad-8150-b776a15b439b)

![image](https://github.com/sankalp-7/FocusLearn-YT/assets/104098061/721b026f-b36c-4158-b7cd-8bd690718ed3)

![image](https://github.com/sankalp-7/FocusLearn-YT/assets/104098061/4ac68909-bdce-409c-906a-e43eb3b52301)

# Notes View

![image](https://github.com/sankalp-7/FocusLearn-YT/assets/104098061/65f9cb4e-44f9-47a5-98f4-089fee257143)

# Saved Notes

![image](https://github.com/sankalp-7/FocusLearn-YT/assets/104098061/791885d1-887a-411d-b15e-7003ea550a15)







