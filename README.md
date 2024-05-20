# Scraping second-hand car markets in Lithuania

## Table of contents
1. [Introduction](#introduction)
   1. [Installation](#installation)
   2. [Usage](#usage)
   3. [Project Requirements](#project-requirements)
2. [Component overview](#component-overview)
   1. [Main class](#main-class)
   2. [Scraping](#scraping)
   3. [Graphical User Interface](#graphical-user-interface)
   4. [Storage](#storage)
   5. [Notifications](#notifications)
3. [Issues and solutions](#issues-and-solutions)
4. [Results and Conclusions](#results-and-conclusions)


## Introduction

Our team has noticed that when looking for a used vehicle, there are multiple platforms that host second-hand car ads. 
As such, it can get tedious looking through all of them to find what is needed. Furthermore, you would have to register
for many different services to get updates about new listing and reminders. 
We decided to make a tool that scrapes the 3 main platforms: [Autogidas](https://autogidas.lt "Autogidas car market"), 
and [BRC](https://lt.brcauto.eu "BRC").
Then, all 3 platforms will be checked at a desired interval for new listings. 

### Installation

1. Download the repository either as a .zip file or using `git clone`.
2. Navigate to the root folder of the project and install the python libraries using `pip install -r requirements.txt`
3. Depending on your operating system, if you have a MacOS device, install the `macos-notifications` library using pip: `pip install macos-notifications`. If you have a Windows device, use `pip install win10toast`.
4. Navigate to the `dmbs.py` file and run it to create the database file with all the required tables.

### Usage

1. To launch the application, run `GUI.py`.
   <img width="499" alt="GUI base" src="https://github.com/ignasbut/OOPScraping/assets/154370264/72834b6b-d021-41dd-80bc-123d41ed2e8d">

2. Enter your desired make, model, and any additional search variables.
   <img width="499" alt="GUI input" src="https://github.com/ignasbut/OOPScraping/assets/154370264/810511bf-03c1-4a65-95af-957f7af3a535">

3. Press "Add", this will do the initial scrape of the cars.
   <img width="499" alt="GUI added" src="https://github.com/ignasbut/OOPScraping/assets/154370264/88478cdf-fc84-4abe-a1db-d47d6fc300eb">

4. Press "Update" after the initial scraping is done, to update the listings once again and start the interval checking.
   <img width="499" alt="GUI updated" src="https://github.com/ignasbut/OOPScraping/assets/154370264/ecc386c8-049b-43f5-982e-61866869a67b">

5. You will be reminded hourly to check for new car listings. 
   <img width="499" alt="GUI   Noti" src="https://github.com/ignasbut/OOPScraping/assets/154370264/ee0ffadb-768c-4a1c-b89d-79142c8fd086">


### Project Requirements

The main requirements are to use: the 4 pillars of OOP, and at least 2 design patterns.

The first that is used is class abstraction. This is accoplisehd in the `car.py` file, where a base abstract class is created
and further subclasses are created with inheritance to the base class:

```python
from abc import ABC, abstractmethod


class Car(ABC):
    def __init__(self, brand, model=None, transmission=None, engine_volume=None, fuel_type=None, driven_wheels=None):
        self.brand = brand
        self.model = model
        self.transmission = transmission
        self.engine_volume = engine_volume
        self.fuel_type = fuel_type
        self.driven_wheels = driven_wheels

    @abstractmethod
    def return_car(self):
        pass
```

Next, there is Inheritance. The `ListingExtension` class inherits from the `Listing class`, adding on some attributes:

```python
class ListingExtension(Listing):
    def __init__(self, brand, model, year, mileage, transmission, engine_volume, fuel_type, driven_wheels, price, url,
                 location, desc, color):
        super().__init__(brand, model, year, mileage, transmission, engine_volume, fuel_type, driven_wheels, price, url,
                         location)
        self.desc = desc
        self.color = color
```

Then, there is Encapsulation. This resides in the `dbms.py` file where the database is managed: 

```python
class CarDB:
    _instance = None

    def __create_connection(self):
        try:
            self.__conn = sqlite3.connect(self.__database, check_same_thread=False)
            print("Database connection established successfully.")
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
```

Lastly, there is Polymorphism. This is expressed as overriding in our `car.py` file via the base class and subclasses:

```python

class Car(ABC):

   ....

   @abstractmethod
   def return_car(self):
     pass

class Query(Car):

   ....

   def return_car(self):
     return vars(self)

class Listing(Car):

   ....

   def return_car(self):
      return [self.brand, self.model, self.year, self.mileage, self.transmission, self.engine_volume, self.fuel_type,
             self.driven_wheels, self.price, self.url, self.location]

class ListingExtension(Listing):

   ....

   def return_car(self):
     return [self.brand, self.model, self.year, self.mileage, self.transmission, self.engine_volume, self.fuel_type,
             self.driven_wheels, self.price, self.url, self.location, self.color, self.desc]

```

For the two design patterns, we chose having a Decorator, and a Singleton.

The Singleton is in `dbms.py`, and is expressed as so:

```python

class CarDB:
    _instance = None

    def __new__(cls, database):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__database = database
            cls._instance.__conn = None
            cls._instance.__create_connection()
        return cls._instance
```

As for the Decorator, it can be found in `scraping.py`:

```python
def decorator(src, *args):

    for arg in src:
        arg = importlib.import_module(arg)
        arg.get_objects(*args)
```
***

## Component overview

The project consists of mainly 4 components: Scraping, Graphical User Interface (GUI), Storage, and Notifications. 

Each of these components are interlinked and use each others functions, with the GUI loop being the main driver of the 
functions. 

### Main class
The main class that is used as a foundation for all the project's functions is stored in car.py.
First, there is the base class called `Car`, which inherits `ABC` from the `abc` module that is installed by default in
Python. This makes `Car` and abstract class and from there, the needed classes are created with their unique changes.

The subclasses of `Car` are `Query` and `Listing`, with `ListingExtension` being a subclass of `Listing` with their own
abstract methods. The `Query` class is used to create a query object that is then sent to the scraping modules and
the `Listing` class is used to create an object of a vehicle that can be stored into an array and then sent to the database
for storage. For example, this is a line of code that is used to create a Listing object and add it to an array:

```
arr.append(Listing(make, model, year, mileage, gearbox, engine_vol, fuel_type, driven_wheels, price, url, location))
```

In GUI.py, a similar thing is done when creating a query:

```
query = Query(self.brand, self.model, self.year_from, self.year_to, self.mileage_from, self.mileage_to, self.transmission,
                      self.engine_vol, self.fuel, self.driven_wheels, self.price_from, self.price_to)
```

### Scraping

The scraping is mainly made in two parts: the individual scraping scripts, and the main controller. 

When the query is sent from the GUI, it is sent to the controller. There, the input information is parsed to set the
values correctly before sending it to the decorator. Once at the decorator, the information is passed to each scraping
module via threads. Each scraping module gets its own separate thread so that everything can run in parallel. This is
the decorator function that is used to start and stop the threads:

```python
import importlib, threading
def decorator(src, *args):
    arr = []
    threads = []
    for arg in src:
        arg = importlib.import_module(arg)
        threads.append(threading.Thread(target=arg.get_objects, args=[*args]))

    for thread in threads:
        print(f"Starting thread {thread.name}")
        thread.start()

    for thread in threads:
        print("thread disabled")
        thread.join()
```

The use of the `importlib` library is so that each scraping module can be imported by a string. This is done so that the
scraping modules are imported only when they are needed to start the threads. Into each target scraping module, the
initial arguments from the query are passed as an array.

### Graphical User Interface
In the initial stages of development, our team deliberated between Tkinter and Kivy for the project's graphical 
user interface (GUI). Kivy was ultimately chosen due to its cross-platform compatibility, ensuring accessibility 
on common operating systems like macOS and Windows. Building the GUI involved learning Kivy Language, a new language
specifically designed for constructing app layouts within the Kivy framework.  While limited resources and the 
complexity of Kivy's documentation presented initial challenges, our team persevered, leveraging online resources 
to gain a comprehensive understanding of the language. By project completion, we had successfully navigated these 
hurdles and established a solid grasp of Kivy Language's functionalities. 

### Storage
It was important for our project that the data is inserted into the database, remained there even after the program terminates. Because of this we have chosen SQLite, which provides a reliable and persistent storage solution for car data. 

The main challenge was to think of a logic, according to which, we would have to, both, store all the data, but at the same time extract only the new ones. The logic that our team has thought was this: create two tables, from the scraping the data goes directly into the second table, then a check is carried out, if in the second table there are machines that are also present in the first, then they are deleted from the second, otherwise they are also added to the first. In this way in the second table there are only new announcements.

Another thing we paid attention to was the checking part. Because it is obvious that some machines can have several similar parameters, if not almost all. Therefore we decided to use the URL as the main parameter for checking the machines in the two tables.

***


### Notifications
Since system notifications play a crucial role in keeping users informed and engaged, we implemented them in our
Python project to gain a deeper understanding of their functionalities. To provide a seamless user experience (UX)
and make the application easier to use across different operating systems, we opted for a cross-platform notification approach. This allowed us to explore
the nuances of notification systems while ensuring our application effectively delivers critical messages to users
regardless of their platform. This not only improves the application's utility but also fosters a more consistent 
and informative user experience. 

***

## Issues and solutions
Our initial approach with the notifications encountered a significant hurdle. We were unable to establish a background 
process within a single thread that could trigger user notifications at designated intervals. To overcome this 
challenge, we opted to integrate system notifications directly into our project. While system notifications 
presented their own set of obstacles, we identified "plyer" as a leading library for this functionality. Unfortunately, 
upon further investigation, we discovered that "plyer" is no longer actively maintained. To navigate this roadblock, we 
adopted a dual-library approach. We implemented separate libraries tailored to specific operating systems, requiring 
additional effort but ultimately ensuring consistent notification functionality across platforms. In our rush to finish NotiCar's development, we wanted to make our notifications more than just pretty decorations. We tried to use asyncio to make them functional, but it didn't work out. Luckily, we discovered that Kivy had its own tools for this. With some tweaks to our code, our notifications became more than just visuals – they now serve a real purpose in the user experience.

A mild issue that we encountered while working on scrapting Autogidas, was the scrping being broken by Ads. During
initial development, the scraping was developed and tested on a network that had dns-filtering (i.e. AdBlocking)
capabilities. After testing the same functionality on a different network, the scraping script was inoperable.
The sheer amount of ads and pop-ups broke the scraping functionality and massively extended the loading times of the
website. This forced us to look for a solution on how to block those advertisements. Our first attempt was trying to
load an ad-blocking extension and couple it to the webdriver, but that did not work and the extension would never
be loaded into the webdriver. While troubleshooting this, we came across a new library called `seleniumbase`, which
contains the functionality of different webdriver forks, such as `undetected_chromedriver`, and this had built-in
ad-blocking capabilities. After replacing the libraries, the scraping resumed working as it did before. 

Our development process continued with a series of refinements, updates, and rigorous testing. However, we encountered 
a significant setback when our web scraping functionality was blocked by autogidas.lt. Initially, we assumed that it was
a temporary blockage due to frequent requests and is limited to an IP-ban. To our dismay, the websites was still 
blocking the webdriver requests even after using a VPN service to change IP's, meaning, that it was a stricter,
and most likely a permanent ban of the website. This was confirmed after trying to run the scraping script on different
devices, which provided the same results, that the website was "actively refusing the requests".

This was a massive setback and due to the time constraints, we were not able to figure out and make adjustments to the 
scraping scripts to overcome the block, if possible. Instead, we finished the scraping configuration for BRC and were
more mindful of not overloading the website with frequent requests while testing.


***

## Results and conclusions
