//** Object Feature **//
	
	var features = new Object();
	
/**
 * Creates an instance of an accessibility feature.
 *
 * @constructor
 * @this {feature}
 * @param {Object} data The xml object that holds data of the feature.
 */		
	var feature = function(data){  
		this.title = $(data).find("TITLE").text();
		this.disability = $(data).find("DISABILITY").text();
		this.rank = $(data).find("DISABILITY").attr('rank');
		this.priority = $(data).find("PRIORITY").text();
		this.level = $(data).find("PRIORITY").attr('level');
		this.error = $(data).find("ERROR").text();
		this.description = $(data).find("DESCRIPTION").text(); 
		this.solution = $(data).find("SOLUTION").text();
		
		this.rule = eval(rules[$(data).attr('id')]); 
	};  	
	
/**
 * Creates the collection of new feature objects.
 *
 * @constructor
 */	
	function makeFeatureCollection(xml) { 
		$(xml).find('FEATURE').each(function() {
			features[$(this).attr('id')] = new feature(this);
		}); 
	}
	

	

