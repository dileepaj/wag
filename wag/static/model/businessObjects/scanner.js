//** Object Scanner **//													

	var scanner = {  
		issues: new Object(),
		priority: 3,		// Level A - All three priorites
		rank: [2,3,5]		// All TB,LV,CB disabilities
	};  

/**
 * Creates the hash-map collection of accessibility violations.
 *
 * @constructor
 */		
	scanner.scan = function (code) { 
		xmlCode = $.parseXML(code); 
		var done = false;
									
		for (var k in features) {							
		if (features.hasOwnProperty(k)) { 
				if (this.isValid(features[k].level, features[k].rank)) {
					this.issues[k] = features[k].rule(xmlCode); 
					done = true;
				}	
		}}
		if (!done) {alert('There are no rules for the selected criteria !');}
	};

/**
 * Calculates the validity of a feature according to the scan profile.
 *
 * @this {scanner}
 * @param {String} prio The priority of the particular feature.
 * @param {Number} rank The disability rank of the particular feature.
 * @return {Boolean} The feature is valid or not.
 */	
	scanner.isValid = function (prio, rank) { 
		var p = (this.priority >= prio);
		
		var r = false;
		$(this.rank).each( function() {
			if((rank%this)==0) { r = true; }
		}); 

		return ( p && r );
	};
	