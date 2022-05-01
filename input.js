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

//build bar chart goals by player colour
    var trace1 = {
        x: data.color,
        y: data.goals,
        type: "bar"
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
        values: [data.wins, data.loses],
        type: 'pie'
    };

        var stats2 = [trace2]

        var layout2 = {
            title: "Player Wins/Losses",
        };

    Plotly.newPlot("pie", stats2, layout2);
    });



function buildTable(games, Win_percent, wins, loses, avg_goals, avg_assists, 
    avg_saves, avg_score) {
    var table = d3.select("#summary-table");
    var tbody = table.select("tbody");
    var games = data.games;
    var Win_percent = data.Win_percent;
    var wins = data.wins;
    var loses = data.loses;
    var avg_goals = data.avg_goals;
    var avg_assists = data.avg_assists;
    var avg_saves = data.avg_saves;
    var avg_score = data.avg_score;
    var trow;
    for (var i = 0; i< 12; i++) {
        trow = tbody.append("tr");
        trow.append("td").text(games);
        trow.append("td").text(Win_percent);
        trow.append("td").text(wins);
        trow.append("td").text(loses);
        trow.append("td").text(avg_goals);
        trow.append("td").text(avg_assists);
        trow.append("td").text(avg_saves);
        trow.append("td").text(avg_score);
    }
}
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

