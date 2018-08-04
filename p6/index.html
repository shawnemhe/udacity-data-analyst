<html>
    <head>
        <title>Flight Delays</title>
        <style>
            .narration {
                font-family: sans-serif;
                text-align: center;
                font-weight: bold;
            }
            #carrierChart {
                text-align: center;
            }
            .legend_header {
                font-family: sans-serif;
                font-size: 11px;
            }
            .click_text {
                font-family: sans-serif;
                font-size: 10px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div id="carrierChart"></div>
        <script src="https://d3js.org/d3.v4.min.js"></script>
        <script src="js/dimple.v2.3.0.min.js"></script>
        <script type="text/javascript">
            "use strict";

            function draw(data) {
                function fadeText(oldText, newText) {
                    oldText.transition(1000)
                        .attr("opacity", 0)
                        .transition(1000)
                        .attr("opacity", 1)
                        .text(newText);
                }

                function setFilter (e) {
                    /* Modifies filters based on current selection
                    - If all a visible, only the selected item will be retained
                    - Otherwise clicking functions as a include/exclude action
                    - But no less than one filter can be active (no purpose for an empty chart)
                    */
                    var newFilters = [];

                    // If all values are visible, hide all but selected airline
                    if (filterValues === allValues) {
                        newFilters.push(e.aggField.slice(-1)[0]);
                        airlineLegend.shapes.selectAll("rect")
                            .style("opacity", 0.2);
                        d3.select(this).style("opacity", 0.8);
                    } else { // Act as a toggle switch
                        // This indicates whether the item is already visible or not
                        var hide = false;
                        // If the filters contain the clicked shape hide it
                        filterValues.forEach(function (f) {
                            if (f === e.aggField.slice(-1)[0]) {
                                hide = true;
                            } else {
                                newFilters.push(f);
                            }
                        });
                        // Ensure that newFilters is not empty
                        if (newFilters.length === 0) {
                            newFilters.push(e.aggField.slice(-1)[0]);
                            hide = false;
                        }
                        // Hide the shape or show it
                        if (hide) {
                            d3.select(this).style("opacity", 0.2);
                        } else {
                            newFilters.push(e.aggField.slice(-1)[0]);
                            d3.select(this).style("opacity", 0.8);
                        }
                    }
                    // Update the filters
                    filterValues = newFilters;
                    // Filter the data
                    carrierChart.data = dimple.filterData(data, "UniqueCarrier", filterValues);
                    // Redraw chart
                    carrierChart.draw(800);
                }

                // Create the SVG that will display all of the content
                var svg = d3.select("#carrierChart")
                    .append("svg")
                    .attr("width", 800)
                    .attr("height", 520);

                // Prepare the chart
                var carrierChart = new dimple.chart(svg, data);
                carrierChart.setBounds(90, 30, 520, 330);
                carrierChart.staggerDraw = true;
                carrierChart.addTimeAxis("x", "Year", "%Y", "%Y");
                var y = carrierChart.addMeasureAxis("y", "DepDelay");
                y.tickFormat = ".0%";
                y.title = "% of Flights Delayed by More Than 15 Minutes";
                var lineSeries = carrierChart.addSeries(null, dimple.plot.line);
                lineSeries.aggregate = dimple.aggregateMethod.avg;
                var airlineLegend; // To be created later

                // Get data that will be needed for filtering
                var filterValues = dimple.getUniqueValues(data, "UniqueCarrier");
                var allValues = filterValues;

                // Create the narration box that will lead the animation
                var narText = svg.append("text")
                    .attr("class", "narration")
                    .attr("x", 100)
                    .attr("y", 250);

                // calculate the average delay and convert for display as percentage
                var avgChanceDelay = d3.mean(data, function (d) { return d.DepDelay });
                avgChanceDelay = avgChanceDelay.toFixed(2) * 100;

                var introStatement = "Between 1987 and 2008 an average of " +
                    avgChanceDelay +
                    "% of flights were delayed by more than 15 minutes.";

                // Load introductory text
                fadeText(narText, introStatement);

                // Move the text down for the chart
                setTimeout(function () {
                    narText
                        .text("")
                        .attr("y", 430);
                }, 4500);

                // Intro the chart
                setTimeout(fadeText, 5000, narText, "And while the trend has been increasing over time,");

                // Load initial chart
                setTimeout(function () { carrierChart.draw(1500) }, 5000);

                setTimeout(fadeText, 8000, narText, "so has the disparity between the best and worst airlines.");

                // Display worst airlines
                setTimeout(function () {
                    // clear the text
                    fadeText(narText, "");

                    // remove the line series
                    lineSeries.shapes.remove();
                    carrierChart.series = [];

                    // redraw chart
                    carrierChart.addSeries("UniqueCarrier", dimple.series.bubble);
                    airlineLegend = airlineLegend = carrierChart.addLegend(630, 5, 100, 380, "left");
                    carrierChart.draw(1000);

                    // orphan the legend so that it does not change when the filter is updated
                    carrierChart.legends = [];
                    // set the on click event
                    airlineLegend.shapes.selectAll("rect")
                        .on("click", setFilter);
                }, 11000);

                setTimeout(function () {
//                    narText.attr("y", 500);
                    fadeText(narText,
                    "A savvy traveler can reduce the chance of delay by choosing the right airline.");
                }, 13000);

                setTimeout(function () {
                    fadeText(narText, "Use the legend to compare airlines");

                    // add header to the legend
                    svg.append("text")
                        .attr("x", 630)
                        .attr("y", 10)
                        .attr("class", "legend_header")
                        .text("Click to filter");

                    // add show all text with click action
                    svg.append("text")
                        .attr("x", 630)
                        .attr("y", 405)
                        .attr("class", "click_text")
                        .text("Show All")
                        .on("click", function () {
                            filterValues = allValues;
                            carrierChart.data = dimple.filterData(data, "UniqueCarrier", filterValues);
                            airlineLegend.shapes.selectAll("rect")
                                .style("opacity", .8);
                            carrierChart.draw(800);
                        });

                }, 16000);
            }

            d3.csv("data/flight_data.csv", draw);
        </script>
    </body>
</html>