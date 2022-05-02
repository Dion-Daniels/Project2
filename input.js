
var granimInstance = new Granim({
    element: '#canvas-interactive',
    name: 'interactive-gradient',
    elToSetClassOn: '.canvas-interactive-wrapper',
    direction: 'diagonal',
    isPausedWhenNotInView: true,
    stateTransitionSpeed: 500,
    states : {
        "default-state": {
            gradients: [
                ['#F9D423', '#ff6633'],
                ['#1A2980', '#26D0CE']
            ],
            transitionSpeed: 4000
        },
    }
});
//var region = "Oceania"
//var player_id = "5f3d8fdd95f40596eae2412e"
//Pull through the region data
url_region = "https://project2-cheng-musah-dion.herokuapp.com/api/v1.0/Oceania"

d3.selectAll("#selDataset").on("change", SelectID);

function SelectID() {
    d3.json(url_region).then((data) => {
        //console.log(data);
        console.log(data.names);
        var dropper = d3.selectAll("#selDataset");
        var stored_id = dropper.property('value');
        console.log(stored_id);
        demographics(stored_id);
        //barchart(stored_id);
        //bubblechart(stored_id);
        //gauge(stored_id)
    });
}

function demographics(selection) {
    d3.json(`https://project2-cheng-musah-dion.herokuapp.com/api/v1.0/Oceania/${selection}`).then((data) => {
        console.log(data);
        //select and clear demographic info box, then input newly selected data
        var demo_data = d3.selectAll("#sample-metadata");
        demo_data.selectAll("*").remove();

        //add up all the goals scored
    var total_goals = (data => data.goals.reduce((a,b) => a + b),0)
    console.log(total_goals)

//build stats table

var table = d3.select("#summary-table");
var tbody = table.select("tbody");
var trow;
for (var i = 0; i < 1; i++) {
  trow = tbody.append("tr");
  trow.append("td").text(data.player_tag);
  trow.append("td").text(data.games.total);
  trow.append("td").text((data.win_percent)+"%");
  trow.append("td").text(data.wins.total_wins);
  trow.append("td").text(data.loses.total_loses);
  trow.append("td").text(data.avg_goals);
  trow.append("td").text(data.avg_assists);
  trow.append("td").text(data.avg_saves);
  trow.append("td").text(data.avg_score);
  trow.append("td")
}

//build bar chart goals by player colour
    var trace1 = {
        x: data.color,
        y: data.goals,
        type: "bar",
        };
          
          var stats = [trace1];
          
          var layout = {
            title: "Goals by Car Color",
            xaxis: { title: "Colour in Game"},
            yaxis: { title: "Total Goals Scored"}
          };
          
    Plotly.newPlot("bar", stats, layout);

// Pie Chart - Wins/Losses
    var trace2 = {
        labels: ["Wins","Loses"],
        values: [data.wins.total_wins, data.loses.total_loses],
        type: 'pie'
    };

        var stats2 = [trace2]

        var layout2 = {
            title: "Player Wins/Losses",
        };

    Plotly.newPlot("pie", stats2, layout2);

//build line chart goals/assists/saves over games
var trace3 = {
    x: data.game_id,
    y: data.goals,
    type: 'scatter',
    name: "Goals"
};

var trace4 = {
    x: data.game_id,
    y: data.assists,
    type: 'scatter',
    name: "Assists"
};

var trace5 = {
    x: data.game_id,
    y: data.saves,
    type: 'scatter',
    name: "Saves"
}
var trace6 = {
    x: data.game_id,
    y: data.score,
    name: 'yaxis2 data',

    yaxis: 'y2',
    type: 'scatter',
    name: "Score"
}

var allstats = [trace3, trace4, trace5, trace6 ];

var layout3 = {
    title: "Goals, Assists and Saves each Game",
    xaxis: { Title:"Games",
    showticklabels: false},
    yaxis: {title: 'yaxis title'},
    yaxis2: {
        title: 'yaxis2 title',
        titlefont: {color: 'rgb(148, 103, 189)'},
        tickfont: {color: 'rgb(148, 103, 189)'},
        overlaying: 'y',side: 'right'

},
    labels:{}
}

Plotly.newPlot("scatter", allstats, layout3)
    });
}

function init() {
    d3.json(url_region).then((data) => {
        //console.log(data);
        console.log(data.player_tag);
        var dropper = d3.selectAll("#selDataset");
        var drop_id = dropper.selectAll('option')
            .data(data.player_tag)
            .enter()
            .append("option")
            .attr('value', d => d)
            .text( d => `Player Tag:  ${d}`)
        console.log(drop_id);
        SelectID()
    });
  // Use the first sample from the list to build the initial plots
}

//run init function
init()

var button = d3.select("#reset_button");
button.on("click",runReset);

function runReset () {
    console.log("works")
    d3.event.preventDefault();
    d3.select("#table_body").selectAll("tr:not(:last-child)").remove();
}
