// https://www.w3schools.com/howto/howto_js_rangeslider.asp
var file_slider = document.getElementById("fileRange");
var file_output = document.getElementById("fileTarget");

var text_slider = document.getElementById("textRange");
var text_output = document.getElementById("textTarget");

// When page loads
function fileOnload() {
    var file_slider = document.getElementById("fileRange");
    var file_output = document.getElementById("fileInitial");
    file_output.innerHTML = file_slider.value;

    var text_slider = document.getElementById("textRange");
    var text_output = document.getElementById("textInitial");
    text_output.innerHTML = text_slider.value;
}

file_slider.oninput = function() {
    file_output.innerHTML = this.value;
    var x = document.getElementById("fileInitial");
    if (x.style.display === "none") {
    }
    else {
        x.style.display = "none";
    }
};

text_slider.oninput = function() {
    text_output.innerHTML = this.value;
    var x = document.getElementById("textInitial");
    if (x.style.display === "none") {
    }
    else {
        x.style.display = "none";
    }
};