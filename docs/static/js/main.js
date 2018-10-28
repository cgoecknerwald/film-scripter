(function() {

	// Strict mode changes previously accepted "bad syntax" into real errors.
	"use strict";

})();

// Generate the output of the trained model on button press
function generate(){
	$.getJSON(window.location.href + "generator", 
		function(data){
			$("#plot-output").html(data.text);
	});
}
