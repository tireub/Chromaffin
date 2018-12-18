## Description:

This is the 13th project of the OpenClassrooms Python Application Developper
course.

**This project aims** to provide biologists studying vesicle movement within chrmoaffin cells analysis tools.**
For more information regarding the reach of this project please refer to **https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0087242**

**The application is a GUI** aimed for biologists studying neurosecretory vesicles behaviour. It provides statistical analysis of vesicular behaviour within the cell, usually in chemically stimulated studies.

**How does it work?**
The main function is app.py which runs the GUI functions and links to the associated database.

**What is the goal?**
This program aims to give biologists access to complex calculations and statistical analysis of large sample data with a user-friendly interface.
It provides a link between Physicists/Mathematicians who might work on the project (backend part) and the Biologists (end user) via an interface.


## How you can help

* If you have any questions regarding the code or the different functions,
* If you would like to see a new function developped,
* If you feel the GUI appearance could be improved,
* If you have any bug report,
please contact guillaume.maucort@gmail.com

* If you are a physician/mathematician and would like to sharpen the behaviour sorting parameters and functions, please contact guillaume.maucort@gmail.com

* If you are a developper, you can check the work in progress file to see which functions are currently expected and the priority for each.
* Only complete functionality pull requests wiil be accepted.


## Installation and configuration


## User's guide

###Start page 
Basic welcome page summarising informations about the project and asking for a confirmation before going further within the GUI.

##General display 
The GUI is mainly composed of three thumbnails to allow for navigation between the main functions of the program, by clicking on the requested thumbnail name.
The current thumbnail is highlighted with a bold font.

### Cell thumbnail
The cell thumbnail provides an overview of the cells included in the database.

!["Cell thumbnail" ](/Docs/Screenshots/Cell_options.png)

**The red-highlighted element** is a display of the tracked vesicles' trajectories over time.
The usual navigation options of a Matplotlib graph are available via the navbar located at the bottom.

**The green-highlighted** part of the thumbnails allows the selection of the desired cell to display and displays informations about this cell.

**The yellow-highlighted** part gives the opportunity to select filters to apply to the graph.
There are currently two main display options for the vesicles trajectoried, one being scattered points and the other colored lines linking two consecutive positions color-coded depending of time. Even though the line display is more readable and representative, it takes some time to calculate, thus the default display is scattered dots for a quicker display.
You can choose to display the membrane positions on top of the vesicle trajectories in order to have a better view of the vesicle's relative position. The default state is hidden to improve display reaction and provide a nicer image.
The last part allows for a segregation of vesicles to be displayed depending on their behaviour before and after stimulation. Select the wanted behaviours to display before ticking the "Apply filters" checkbox.

**The blue-highlighted element** allows for the import of new elements to the database and the different calculations associated. 
All the database modifications are done via these functions.

### Vesicle thumbnail
The vesicle thumbnail gives the user the ability to look at specific vesicles informations.

!["Vesicle thumbnail" ](/Docs/Screenshots/VesicleOptions.png)

**The blue-highlighted element** is the navigation panel for this thumbnail. 
It allows the user to select the specific cell he wishes to study. 
He then has the ability to navigate between the different components via next/previous buttons or by entering a particular vesicle number.

**The yellow-highlighted part** displays a summary of information about the vesicle. 
It displays the name of the cell, the vesicle number within this cell, 
the number of frames during which the vesicle has been tracked, 
and its behaviour before and after stimulation.

**The red-highlighted part** shows a 3D (x, y, t) representation of the vesicle trajectory during its tracking duration.

**The green-highlighted part** is a representation of the MSD calculated for the vesicle and it's fitting curve. 
More information about the MSD can be found in the Calculations section.


### Statistics thumbnail
The statistics thumbnail provides statistical information 

!["Statistics thumbnail" ](/Docs/Screenshots/Statistics.png) 

**The yellow-highlighted element** displays a summary of the statistics displayed, including the current display mode, the type of stimulation for which we display statistics, wether or not all the cells with this particular type of stimulation are included, the number of cells concerned and the total number of vesicles involved for this statistical display.

**The green-highlighted element** asks the user for the type of stimulation study he/her wishes to get. 
There is also an option to remove certain cells from the statistics (not yet working). 
Finally it asks for the original behaviour for the particular changes studies.

**The blue-highlighted element** allows for the navigation between the different types of analysis by pressing a button.

!["Change behaviour" ](/Docs/Screenshots/Populationchanges.png) | !["Change vs original" ](/Docs/Screenshots/Changevsori.png) | !["Switch distance to the membrane" ](/Docs/Screenshots/Changevsdist.png)


## Calculations




## Planned future improvements

#### Features to be added:
* Several functions of data export from the matplotlib graphs obtained in the statistics thumbnail.
* Ability to export the statistics data in other forms than graphs (raw data, raw data per cell, etc.) to be able to create custom graphs for publications.

#### Display improvements 
* Ability to zoom on a single graph in the 9quadrants view
* Thumbnails update after new import

#### Calculations 
* Improve calculation time for segmental display of trajectories within cell thumbnail

#### Code
* Factorisation (mainly for the pages.py function)
* Divide pages.py in several files (one for each page ideally)

#### V2
* Edges for each frame
* Cell edges detection module
* Added statistical reports

