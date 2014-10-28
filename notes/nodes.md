# Recent Items

Here is a list of items I have edited recently, sorted by most recently updated.

This view is populated by [`/api/dates`](/api/dates)

<div id='parent-div' style='width:95%;margin:auto'>
</div>

<script src="http://code.jquery.com/jquery-1.11.1.min.js"></script>
<script src="http://d3js.org/d3.v3.min.js" charset="utf-8"></script>
<script src="http://momentjs.com/downloads/moment.js"></script>
<script type='text/javascript'>

$.getJSON('/api/dates', function(res) {
  var items = res['items'];
  d3.select("#parent-div").selectAll("div")
    .data(items)
    .enter().append("div")
      .style("border", "1px solid black")
      .style("padding", "3px")
      .style("display", "inline-block")
      .style("height", "60px")
      .style("width", "240px")
      .style("vertical-align", "middle")
	  .style("margin", "7px")
      .style("text-align", "center")
      .style("background-color", function(d) { 
        var date = new Date(d[0]).getTime();
        var now = new Date().getTime()
        var frac = date / now;
        var brightness = parseInt( (frac*frac*frac*frac*frac*frac*frac*frac) * 220);
        var green = brightness + parseInt(30*frac);
        var blue = brightness + parseInt(50*frac*frac);
        return "rgb(" + brightness + "," + green + "," + blue + ")";
      })
      .append("p")
      	.text(function(d) {
      		return moment(d[0]).fromNow() + ' at ';
        })
        .append("a")
          .text( function (d) { return d[1].replace('http://localhost:9999', '') })
          .attr("href", function (d) { return d[1]; });

});

</script>