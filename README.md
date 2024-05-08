# Scraping second-hand car markets in Lithuania

## Table of contents
1. [Introduction](#Introduction)
2. [Component overview](#Component-overview)
3. [Issues and solutions](issues-and-solutions)
4. [Results and conclusions](#results-and-conclusions)


## Introduction

Our team has noticed that when looking for a used vehicle, there are multiple platforms that host second-hand car ads. 
As such, it can get tedious looking through all of them to find what is needed. Furthermore, you would have to register for 3 different services
to get updates about new listing and such. 
We decided to make a tool that scrapes the 3 main platforms: Autogitas.lt, Autoplius.lt, and lt.brcauto.eu.
Then, all 3 platforms will be checked at a desired interval for new listings. 


## Component overview 

### Scraping


### Graphical User Interface
In the initial stages of development, our team deliberated between Tkinter and Kivy for the project's graphical user interface (GUI). Kivy was ultimately chosen due to its cross-platform compatibility, ensuring accessibility on common operating systems like macOS and Windows. Building the GUI involved learning Kivy Language, a new language specifically designed for constructing app layouts within the Kivy framework.  While limited resources and the complexity of Kivy's documentation presented initial challenges, our team persevered, leveraging online resources to gain a comprehensive understanding of the language. By project completion, we had successfully navigated these hurdles and established a solid grasp of Kivy Language's functionalities. 

### Storage



### Notifications
Since system notifications play a crucial role in keeping users informed and engaged, we implemented them in our Python project to gain a deeper understanding of their functionalities. To provide a seamless user experience (UX) across different operating systems, we opted for a cross-platform notification approach. This allowed us to explore the nuances of notification systems while ensuring our application effectively delivers critical messages to users regardless of their platform. This not only improves the application's utility but also fosters a more consistent and informative user experience.


## Issues and solutions
Our initial approach with the notifications encountered a significant hurdle. We were unable to establish a background process within a single thread that could trigger user notifications at designated intervals. To overcome this challenge, we opted to integrate system notifications directly into our project. While system notifications presented their own set of obstacles, we identified "plyer" as a leading library for this functionality. Unfortunately, upon further investigation, we discovered that "plyer" is no longer actively maintained. To navigate this roadblock, we adopted a dual-library approach. We implemented separate libraries tailored to specific operating systems, requiring additional effort but ultimately ensuring consistent notification functionality across platforms.
Our development process continued with a series of refinements, updates, and rigorous testing. However, we encountered a significant setback when our web scraping functionality was blocked by autogidas.lt. Initially, we suspected a temporary ban, but checks confirmed that our IP address wasn't restricted. (Conclusion: the security of websites are solid, we need to enhance our scraping method).
## Results and conclusions
