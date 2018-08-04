# Summary
The visualization was created using flight data from RITA. It presents the percentage of flights that were delayed by more than 15 minutes for each airline between 1987 and 2008. Also included in the github repository is a python script that used parallel processing to aggregate the information from the 22 original data files.

# Design
I wanted to present the data in a way that immersed the viewer in the visualization so I used a martini-glass narrative. It begins with an animation that introduces the data and guides the user toward the message I wanted to convey. First the trend of airline delays is shown as I explain that delays have been increasing. Next the individual airlines are broken out as I show that there are large disparities between some carriers. The final view is an interactive and filterable chart so that the user can continue to explore the data. 

# Feedback
## Reviewer 1
* Initial bar charts allowed comparing the airlines against each other, but not over time. An animation I created in the initial visualizations included too many years to be able to be followed.
* After the visualization was changed to a martini glass narrative some of the text seemed out of place.

**Followup:** I created an aggregated data and used a bubble chart to combine the data on one chart. For the martini glass narrative, I moved the pre chart text to the center of the page, and then shifted it down when the chart was drawn.

## Reviewer 2
* The data lacked the desired impact because most of the averages were close to zero. The reviewer suggested it might have been because airlines were lying about how late their departures were, but I discovered the skew was being caused by a number of outlier flights that were rescheduled to depart several hours early.
**Followup:** I modified the pre-processing script so that it aggregated the percentage of flights per year and airline that were over 15 minutes late.

## Reviewer 3
* The viewer did not realize that the legend was interactive until I told them.

**Followup:**  I added a simple "click to filter" header to guide the user.

## Udacity Feedback
* The Udacity reviewer pointed out that the visualization was exploratory rather than explanatory.

**Followup:** I changed to a martini-glass narrative in which I started with a message, and then finished with an interactive visualization for the viewer to explore.


# Resources
- [Stat-computing.org](http://stat-computing.org/dataexpo/2009/the-data.html)
- [DimpleJS Advanced Examples](http://dimplejs.org/advanced_examples_index.html)
- [Text Transition](https://bl.ocks.org/mbostock/f7dcecb19c4af317e464)