<html>
    <head>
        <title>Flight Delays</title>
        <style>
            .chartHeader {text-align: center}
            .carrierChart {
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
    <div class="carrierChart"></div>
    <script src="https://d3js.org/d3.v4.min.js"></script>
    <script src="js/dimple.v2.3.0.min.js"></script>
    <script type="text/javascript">
    d3.csv("data/flight_data.csv", drawCarrierChart);
    
    function drawCarrierChart (data) {
        d3.select(".carrierChart")
            .append("h1")
            .attr("class", "carrierChart")
            .text("How often are flights delayed?");
        d3.select(".carrierChart")
            .append("h2")
            .attr("class", "carrierChart")
            .text("Chance of Delay by Airline and Year");
        var svg = dimple.newSvg(".carrierChart", 800, 520);
        var carrierChart = new dimple.chart(svg, data);
        carrierChart.setBounds(90,30,520,330);
        var x = carrierChart.addTimeAxis("x", "Year", "%Y", "%Y");
        var y = carrierChart.addMeasureAxis("y", "DepDelay");
        y.tickFormat = ".0%"
        y.title = "% of Flights Delayed by More Than 15 Minutes"
        var bubbleSeries = carrierChart.addSeries("UniqueCarrier", dimple.plot.bubble);
        var lineSeries = carrierChart.addSeries(null, dimple.plot.line);
        lineSeries.aggregate = dimple.aggregateMethod.avg;
        airlineLegend = carrierChart.addLegend(630, 5, 100, 380, "left", bubbleSeries);

        carrierChart.draw(800);

        // orphan legends from chart
        carrierChart.legends = [];

        // get a list of all of the filterValues
        var filterValues = dimple.getUniqueValues(data, "UniqueCarrier");
        var allValues = filterValues;

        airlineLegend.shapes.selectAll("rect")
            .on("click", function (e) {
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
                });
        
        svg.selectAll("legend_header")
            .data(["Click to filter"])
            .enter()
            .append("text")
                .attr("x", 630)
                .attr("y", 10)
                .attr("class", "legend_header")
                .text(function (d) { return d });
            
        svg.selectAll("select_all")
            .data(["Show All"])
            .enter()
            .append("text")
                .attr("x", 630)
                .attr("y", 405)
                .attr("class", "click_text")
                .text(function (d) { return d })
                .on("click", function (e) {
                    filterValues = allValues;
                    carrierChart.data = dimple.filterData(data, "UniqueCarrier", filterValues);
                    airlineLegend.shapes.selectAll("rect")
                        .style("opacity", .8);
                    carrierChart.draw(800);
                });
    }
    </script>
</html>