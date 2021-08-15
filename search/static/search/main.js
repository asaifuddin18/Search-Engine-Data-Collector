/**
 * Script that supports home page (search/home.html)
 * Attributes
 * ----------
 * dict_t: dictionary
 *  Dictionary that maps objects names to its query template
 * models: dictonary
 *  Dictionary that maps model short name to its long name
 * qs: list(str)
 *  List of the user input fields IDs
 */

var dict_t = {
    "Professor": ["First Name", "Last Name", "Institution"],
    "Movie": ["Name", "Year"],
    "Electronic": ["Name", "Model No./Year"],
    "Car": ["Make", "Model", "Year"]
};

var models = {
    "rf": "Random Forest",
    "svm": "SVM"
};
var qs = ["q1", "q2", "q3", "q4", "q5", "q6"];
var past_accuracy = null;
var past_precision = null;
var past_f1 = null;
var past_recall = null;
var data_x = null;
var order = null;
var object = null;
var class_count = JSON.parse(document.getElementById('class_count').textContent);
var error_ = null;
/**
 * Attempts to assign values from Django template
 */
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

window.onload = function() {
  /**
   * If an error is passed, alert it to the user
   */
    if (error_) {
      alert(error_);
    }
    /**
     * If the object is already defined, prevent the user from changing the query template
     */
    if (object) {
        var your_object = document.getElementById("your_object");
        your_object.value = object;
        var file_object = document.getElementById("file_object");
        file_object.value = object
        document.getElementById("dropdownMenuButton").style.visibility = "hidden";
        for (var key in dict_t) {
            for (var i = 0; i < qs.length; i++) {
                var curQ = document.getElementById(qs[i]);
                curQ.style.visibility = "hidden";
                curQ.required = false;
            }
            for (var i = 0; i < dict_t[object].length; i++) {
                var curQ = document.getElementById(qs[i]);
                curQ.style.visibility = "visible";
                curQ.placeholder = dict_t[object][i];
                curQ.required = true;
            }
        }
    }
    /**
     * Logic for changing query templates
     */
    for (var key in dict_t) {
        document.getElementById(key).addEventListener("click", function(event) {
            //var queryBox = document.getElementById("your_queries");
            //queryBox.placeholder = "Enter queries following the template: " + dict_t[event.target.id];
            document.getElementById("dropdownMenuButton").textContent = event.target.id;
            var your_object = document.getElementById("your_object");
            var file_object = document.getElementById("file_object");
            file_object.value = event.target.id;
            your_object.value = event.target.id;
            for (var i = 0; i < qs.length; i++) {
                var curQ = document.getElementById(qs[i]);
                curQ.style.visibility = "hidden";
                curQ.required = false;
            }
            
            for (var i = 0; i < dict_t[event.target.id].length; i++) {
                var curQ = document.getElementById(qs[i]);
                curQ.style.visibility = "visible";
                curQ.placeholder = dict_t[event.target.id][i];
                curQ.required = true;
            }
        })
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
                scaleLabel: {
                    display: true,
                    labelString: 'Number of Annotations',
                    fontSize: 20
                }
            }],
            yAxes: [{
              ticks: {
                beginAtZero: true,
                max: 1
              },
              scaleLabel: {
                  display: true,
                  labelString: 'Metrics',
                  fontSize: 20
              }
            }]
          },
          legend: {
            position: 'top',

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
           "#5cb85c", 
           "#5bc0de", 
           "#f0ad4e",
           "#d9534f"
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
    data: pieData
  });