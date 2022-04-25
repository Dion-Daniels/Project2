var svgWidth = 960;
var svgHeight = 500;

var margin = {
  top: 20,
  right: 40,
  bottom: 80,
  left: 100
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// Create an SVG wrapper, append an SVG group that will hold our chart,
// and shift the latter by left and top margins.
var svg = d3
  .select("#scatter")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight + 50);

// Append an SVG group
var chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Retrieve data from the .db file
function setTablesDropdown() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'RocketLeague.db', true);
    xhr.responseType = 'arraybuffer';
  
    xhr.onload = function(e) {
      var uInt8Array = new Uint8Array(this.response);
      var db = new SQL.Database(uInt8Array);
      var tables = db.exec("SELECT * FROM sqlite_master WHERE type = 'view'");
  
      var indexOfName;
      tables[0].columns.forEach((ele,i) => { if (ele === 'name') indexOfName = i })
  
      let dropdownHTML = '';
      for (var i = 0; i < tables[0].values.length; i++) {
        let tableName = tables[0].values[i][indexOfName];
        if (tableName !== 'MISTATS')
          dropdownHTML += "<option value='" + tableName + "'>" + tableName + "</option>";
      }
  
      document.getElementById('views').innerHTML = dropdownHTML;
    }
  
    xhr.send();
  }
  
  
  setTablesDropdown();

  function toggleView() { 
    document.getElementById('dashboard').innerHTML = '';
  
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'RocketLeague.db', true);
    xhr.responseType = 'arraybuffer';
  }
