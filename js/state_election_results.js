var w = 850,
	h = 5000,
	padding_left = 120,
	padding_top = 50;

// set up scales
xScale = d3.scale.ordinal()
	.rangeRoundBands([0, w], 0.1);

yScale = d3.scale.ordinal()
	.rangeRoundBands([0, h], 0.1);

rScale = d3.scale.sqrt()
	.domain([0, 100]);

// set up axes
var xAxis = d3.svg.axis()
	.scale(xScale)
//	.orient("top")
	.tickSize(0);

var yAxis = d3.svg.axis()
	.scale(yScale)
	.orient("left")
	.tickSize(0);

// set up tooltip
var tip = d3.tip()
	.attr("class", "d3-tip")
	.html(function(d) { if(d.Third_pct > 0) { return "<h3>" + d.State + "</h3><h5>" + d.Year + " Presidential Election</h5>" + 
													"<hr /> Democrat: " + d.Dem_pct + "%" + "<br /> Republican: " + 
													d.Rep_pct + "%" + "<br /> Third Party: " + d.Third_pct + "%"; } 
						else { return "<h3>" + d.State + "</h3><h5>" + d.Year + " Presidential Election</h5>" + 
													"<hr /> Democrat: " + d.Dem_pct + "%" + "<br /> Republican: " + 
													d.Rep_pct + "%"; } })
	.direction('e');

// set up chart
var plot = d3.select("#plot")
  .append("svg")
  	.attr("width", w + padding_left*2)
  	.attr("height", h)
  .append("g")
  	.attr("transform", "translate(" + padding_left + ", -20)");

// load data and draw chart
d3.csv("data/state_election_results.csv", function(d) {

	return {
		Dem_pct: +d.Dem_pct,
		Rep_pct: +d.Rep_pct,
		State: d.State,
		Third_pct: +d.Third_pct,
		Year: d.Year,
		Winner: d.Winner,
		Notes: d.Notes
	};
}, function(error, data) {

	console.log(data);

	// get object of election years and state names to label axes with
	var years = d3.nest().key(function(d) { return d.Year; }).sortKeys(d3.ascending).entries(data);
	var states = d3.nest().key(function(d) { return d.State; }).sortKeys(d3.ascending).entries(data);

	// set domain for scales
	xScale.domain(years.map(function(d) { return d.key; }));
	yScale.domain(states.map(function(d) { return d.key; }));

	// set range for radius scale
	rScale.range([0, (w/years.length)/2]);

	// draw axes
	d3.select("#xaxis")
	  .append("svg")
		.attr("width", w + padding_left*2)
	  	.attr("height", 14)
	  .append("g")
		.attr("class", "axis")
		.attr("transform", "translate(" + padding_left + ", 0)")
		.call(xAxis);

	plot.append("g")
		.attr("class", "axis")
		.call(yAxis);

	// call tooltip
	plot.call(tip);

	// draw circles
	var circles = plot.selectAll("circle")
		.data(data)
		.enter()
	  .append("circle")
	  	.attr("class", "result_circle")
	  	.attr("cx", function(d) { return xScale(d.Year) + xScale.rangeBand()/2; })
	  	.attr("cy", function(d) { return yScale(d.State) + yScale.rangeBand()/2; })
	  	.attr("r", function(d) { if(d.Winner == "Democrat") { return rScale(d.Dem_pct); }
	  							 else if(d.Winner == "Republican") { return rScale(d.Rep_pct); }
	  							 else { return rScale(d.Third_pct); }})
	  	.attr("fill", function(d) { if(d.Winner == "Democrat") { return "#1268B2"; }
	  								else if(d.Winner == "Republican") { return "#FF5048"; }
	  								else { return "Yellow"; }})
	  	.on('mouseover', tip.show)
	  	.on('mouseout', tip.hide);
})