//run SelectID on selecting option from dropdown 
d3.selectAll("#selDataset").on("change", SelectID);
//function selecting value from drop down and running all other functions
url = "https://project2-cheng-musah-dion.herokuapp.com/api/v1.0/raw_main"
function SelectID() {
    d3.json(url).then((data) => {
        //console.log(data);
        //console.log(data.names);
        var dropper = d3.selectAll("#selDataset");
        var stored_id = dropper.property('value');
        console.log(stored_id);
        //demographics(stored_id);
        //barchart(stored_id);
        //bubblechart(stored_id);
        //gauge(stored_id)
    });
}
/*
//Demographic function to input demographic data into info box
function demographics(selection) {
    d3.json(url).then((data) => {
        console.log(data.metadata);
        var selection_index = data.names.indexOf(selection);
        var selected_belly = data.metadata[selection_index]
        console.log(selected_belly);
        //select and clear demographic info box, then input newly selected data
        var demo_data = d3.selectAll("#sample-metadata");
        demo_data.selectAll("*").remove();
        Object.entries(selected_belly).map(([key, index]) => {
            demo_data.append("p").text(`${key}: ${index}`);
        });
    
    });
}
//Fucntion to create horizontal bar chart of the top 10 OTU's for selected ID
function barchart(selection) {
    d3.json("samples.json").then((data) => {
        console.log(data.samples);
        
        var filteredData = data.samples.filter(d => d.id === selection);
        console.log(filteredData[0]);
        
        var sorted_samples = filteredData[0].sample_values.sort((a,b) => b.sample_values - a.sample_values);
        var top_samples = sorted_samples.slice(0,10).reverse();
        var otu_ids = filteredData[0].otu_ids.slice(0,10).reverse();
        var otu_labels = filteredData[0].otu_labels.slice(0,10).reverse();
        renamed_ids = [];
        otu_ids.forEach(d => renamed_ids.push(`OTU ${d}`));
        //console.log(renamed_ids);
        // Trace1 for the Data
        var trace1 = {
            x: top_samples,
            y: renamed_ids,
            text: otu_labels,
            type: "bar",
            orientation: "h"
        };
        
        // data
        var data = [trace1];
        
        // Apply the group bar mode to the layout
        var layout = {
            margin: {
            l: 75,
            r: 100,
            t: 0,
            b: 100
            }
        };
        
        // Render the plot to the div tag with id "bar"
        Plotly.newPlot("bar", data, layout);
  
    });
}
//Fucntion to create bubble chart visualising the relative sample size for all OTU's for selected ID
function bubblechart(selection) {
    d3.json("samples.json").then((data) => {
    var filteredData = data.samples.filter(d => d.id === selection);
    console.log(filteredData[0]);
        var trace1 = {
        x: filteredData[0].otu_ids,
        y: filteredData[0].sample_values,
        mode: 'markers',
        marker: {
            size: filteredData[0].sample_values,
            color: filteredData[0].otu_ids,
            cmin: Math.min(filteredData[0].otu_ids),
            cmax: Math.max(filteredData[0].otu_ids),
            colorscale: 'spectral'
        }
        };
        var meh = [trace1];
        var layout = {
            title: 'Marker Size',
            showlegend: false,
        };
        // Render the plot to the div tag with id "bubble"
        Plotly.newPlot('bubble', meh, layout);
    });
}
//Function to create gauge visualising how often belly button is washed for a selected ID
function gauge(selection) {
    d3.json("samples.json").then((data) => {
        var filtered = data.metadata.filter(sample => sample.id == selection);
        // log wash frequency
        console.log(filtered[0].wfreq)
        var data = [
            {
                type: "indicator",
                mode: "gauge",        
                domain: { x: [0, 1], y: [0, 1] },
                gauge: {
                    axis: {
                        range: [null, 10],
                        ticks: "inside",
                        nticks: 20,
                    },
                    steps: 
                    [
                        
                        {range: [0,1], color: 'rgb(255, 255, 175)', line:{width: 3}},
                        {range: [1,2], color: 'rgb(220, 255, 204)', line:{width: 3}},
                        {range: [2,3], color: 'rgb(230, 255, 204)', line:{width: 3}},
                        {range: [3,4], color: 'rgb(217, 255, 204)', line:{width: 3}},
                        {range: [4,5], color: 'rgb(204, 255, 204)', line:{width: 3}},
                        {range: [5,6], color: 'rgb(204, 255, 217)', line:{width: 3}},
                        {range: [6,7], color: 'rgb(204, 255, 220)', line:{width: 3}},
                        {range: [7,8], color: 'rgb(204, 255, 242)', line:{width: 3}},
                        {range: [8,9], color: 'rgb(204, 255, 255)', line:{width: 3}},
                        {range: [9,10], color: 'rgb(204, 242, 255)', line:{width: 3}},   
                    ],
                    bar: {
                        thickness : 0.25,
                        color: 'green'}
                },
        
                value: filtered[0].wfreq,
        
                title: { text: `Belly Button Washing Frequency` },
                subtitle: {text: `# Scrubs per week`}
            }
        ];
        var layout = { height: 500, margin: { t: 0, b: 0 } };
        // Render the plot to the div tag with id "gauge"
        Plotly.newPlot('gauge', data, layout);
    });
}
*/
//Function to load all data and populate dropdown on startup
function init() {
    d3.json(url).then((data) => {
        console.log(data);
        //console.log(data.team_name);
        var dropper = d3.selectAll("#selDataset");
        var drop_id = dropper.selectAll('option')
            .data(data)
            .enter()
            .append("option")
            .attr('value', d => d)
            .text( d => `ID: ${d}`)
        console.log(drop_id);
        SelectID()
    });
}
//run init function
init()

