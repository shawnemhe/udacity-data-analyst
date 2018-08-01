# Summary
The visualization was created using flight data from RITA. It presents the percentage of flights that were delayed by more than 15 minutes for each airline and year in a filterable format for viewer-driven exploration. Also included in the github repository is a python script that used parrellel processing to aggregate the information from the 22 original data files.

# Design
I wanted to present the data in a way that allows the viewer to find the information they found interesting, so I used a viewer-driven narrative structure. I chose a bubble plot so that I could show each airline's information for each year on one chart, and made the airlines filterable so that the viewer can narrow the view down to the airlines they are interested in.

# Feedback
I used a python notebook for data exploration in the first phase. The initial feedback I received was that it the raw format did not convey a straightforward narrative. The average delay times were skewed negative by a large number of flights that were very early, presumably due to rescheduling. A more relavent metric was the chance a flight would be delayed.

I also created multiple dimple visualizations before choosing my final graph. I made graphs for the annual average  and bar charts for the airline averages. The feedback I received at this stage was that the bar charts were not appropriate. Although they allowed the airlines to be compared against each other, they did not give the sense of time I wanted to convey. I tried animating the bar charts over time, but there were too many years for the viewer to be able to follow.

Another important piece of feedback I received was in regards to my data filter. The viewers did not realize that the legend was interactive until I told them. I added a simple "click to filter" header to guide the user.

# Resources
- [Stat-computing.org](http://stat-computing.org/dataexpo/2009/the-data.html)
- [Dimplejs Advanced Examples](http://dimplejs.org/advanced_examples_index.html)