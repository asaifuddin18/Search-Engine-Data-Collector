
const links = JSON.parse(document.getElementById('links').textContent);
var labels = null;
var info = null;
var stats_local = null;
try {
    labels = JSON.parse(document.getElementById('labels').textContent);
} catch(error) {
    
}

var past_accuracy = null;
var past_precision = null;
var past_f1 = null;
var past_recall = null;
var data_x = null;
var order = null;
var object = null;
var class_count = JSON.parse(document.getElementById('class_count').textContent);
var error_ = null;
wordsToPass = [];
try {
    past_accuracy = JSON.parse(document.getElementById('past_accuracy').textContent);
    past_precision = JSON.parse(document.getElementById('past_precision').textContent);
    past_f1 = JSON.parse(document.getElementById('past_f1').textContent);
    past_recall = JSON.parse(document.getElementById('past_recall').textContent);
    data_x = JSON.parse(document.getElementById('data_x').textContent);
    order = JSON.parse(document.getElementById('order').textContent);
    object = JSON.parse(document.getElementById('object').textContent);
    error_ = JSON.parse(document.getElementById('error').textContent);
} catch(error) {
    
}
/**
 * Logic for submitting annotations
 */
document.getElementById('submit_annotation').addEventListener("click", function(event) {
    var res = document.getElementsByClassName("ezO2md");
    annotation_string = "";
    for (var i = 1; i < res.length + 1; i++) {
        var y = document.getElementById("y" + i.toString());
        var n = document.getElementById("n" + i.toString());
        if (y.classList.contains("btn-success")) {
            annotation_string += "1";
        } else if (n.classList.contains("btn-danger")) {
            annotation_string += "0";
        } else {
            alert("Please mark search result #" + i.toString() + " as Homepage or Not Homepage before continuing.");
            return
        }
    }
    var wordString = "";
    for (var i = 0; i < wordsToPass.length; i++) {
        wordString += wordsToPass[i] + "~";
    }
    document.location.href = "/" +'edit/' + annotation_string + "/" + wordString;
})
/**
 * Logic for toggling annotation buttons & pre-selecting inferences from ML model
 */
window.onload = function() {
    var res = document.getElementsByClassName("ezO2md");
    document.getElementById("add_feature").addEventListener("click", function(event) {
        var text = "";
        if (window.getSelection) {
            text = window.getSelection().toString();
        } else if (document.selection && document.selection.type != "Control") {
            text = document.selection.createRange().text;
        }
        var toAlert = "Word: " + text + " added";
        wordsToPass.push(text);
        alert(toAlert);
    })
    for (var i = 1; i < res.length + 1; i++) {
        document.getElementById("y" + i.toString()).addEventListener("click", function(event) {
            event.target.classList.add("btn-success");
            var num = event.target.id.slice(1);
            var n = document.getElementById("n" + num);
            if (n.classList.contains("btn-danger")) {
                n.classList.remove("btn-danger");
            }
        })
        document.getElementById("n" + i.toString()).addEventListener("click", function(event) {
            event.target.classList.add("btn-danger");
            var num = event.target.id.slice(1);
            var n = document.getElementById("y" + num);
            if (n.classList.contains("btn-success")) {
                n.classList.remove("btn-success");
            }
        })
    }

    if (labels) {
        for (var i = 0; i < labels.length; i++) {
            if (labels[i] == 1) {
                document.getElementById("y" + (i+1).toString()).classList.add("btn-success");
            } else {
                document.getElementById("n" + (i+1).toString()).classList.add("btn-danger");
            }
        }
    }
}
/**
 * Initializes graph
 */
var ctx = document.getElementById("myChart");
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: data_x,
        datasets: [{
            data: past_accuracy,
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#0275d8',
            borderWidth: 4,
            pointBackgroundColor: '#0275d8',
            label: "Accuracy"
          },
          {
            data: past_precision,
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#5cb85c',
            borderWidth: 4,
            pointBackgroundColor: '#5cb85c',
            label: "Precision"
          },
          {
            data: past_recall,
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#5bc0de',
            borderWidth: 4,
            pointBackgroundColor: '#5bc0de',
            label: "Recall"
          },
          {
            data: past_f1,
            lineTension: 0,
            backgroundColor: 'transparent',
            borderColor: '#f0ad4e',
            borderWidth: 4,
            pointBackgroundColor: '#f0ad4e',
            label: "F1 Score"
          }]
        },
        options: {
          scales: {
            xAxes: [{
                ticks: {
                    fontColor: 'white'
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Number of Annotations',
                    fontSize: 10,
                    fontColor: 'white'
                }
            }],
            yAxes: [{
              ticks: {
                beginAtZero: true,
                max: 1,
                fontColor: 'white'
              },
              scaleLabel: {
                  display: true,
                  labelString: 'Metrics',
                  fontSize: 10,
                  fontColor: 'white'
              }
            }]
          },
          legend: {
            position: 'top',
            fontColor: 'white'

        }
    }
});
/**
 * Initializes pie graph
 */
var pieData = {
    labels: order,
    datasets: [
      {
        data: class_count,
        backgroundColor: [
           "#0275d8", 
           "#5cb85c"
        ]
    }]
  };
  
  var ctx = document.getElementById("myData").getContext("2d");
  var pie_chart = document.getElementById("myData");
  if (class_count[0] == 0) {
      pieData.style.visibility = 'hidden';
  }
  var myPieChart = new Chart(ctx, {
    type: 'pie',
    data: pieData,
  });
/*window.onbeforeunload = function(){
    return 'Are you sure you want to leave?';
};*/