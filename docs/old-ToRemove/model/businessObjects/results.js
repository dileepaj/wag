//** Object Result **//

/**
 * Creates an instance of an accessibility violation (result).
 *
 * @constructor
 * @this {result}
 * @param {Number} id 	The identification number of the result.
 * @param {Number} type The id of the corresponding accessibility feature.
 * @param {Object} node The DOM element that cause the violation.
 */		
	var result = function(id,type,node){  			
		this.id = id; 
		this.feature = type;		
		this.element = node;
		this.line = getLine(node);
		this.status = 'unresolve';	
		
	/**
	 * Assigns the particular line number of the result.
	 *
	 * @this {result}
	 */	
		this.resetLine = function() {
			this.line = getLine(this.element);
		}
		
	/**
	 * Assigns the particular status of the result.
	 *
	 * @this {result}
	 * @param {String} status 	The status of the result.
	 */
		this.setStatus = function(status) {
			this.status = status;
		}
	}; 
	
	var list = {
		results: new Object(),
		total: 0,
		resolves: 0,
		skips: 0
	}; 	
	
/**
 * Creates the collection of new result objects.
 *
 * @constructor
 */	
	list.setResults = function () {	
		var items = scanner.issues;
		var i = list.total;
		
		for (var k in items) {							
			if (items.hasOwnProperty(k)) {	
				$.each(items[k], function() { 
					i++;
					list.results[i] = new result(i,k,this);
					showResult(list.results[i]);
				});
			}
		}
		list.total = i;
	}
			
		//** if this element not contains in corresponding issues array, changeStatus into resolved
		//** if this element contains in corresponding issues array, remove it from array  
/**
 * Updates the collection of result objects.
 *
 */		
	list.update = function () {
		var items = scanner.issues;
		var reslt = list.results;
		var i = 0;
		
		for (var k in reslt) {							
			if (reslt.hasOwnProperty(k)) {
				reslt[k].resetLine();
			
				var contains = $.inArray(String(reslt[k].element), items[reslt[k].feature]); 
				if (contains == -1) {
					if ( reslt[k].status=='skipped' ) { list.skips--; }				//resolve a skipped one
					reslt[k].setStatus('resolved'); 								//change status
					i++;
				}
				else {
					if ( reslt[k].status=='resolved' ) 								//unresolve a resolved one
					{ reslt[k].setStatus('unresolve'); }
					items[reslt[k].feature].splice(contains,1); 					// remove
				}
				showResult(reslt[k]);
			}
		}
		list.resolves = i;
		list.setResults();															//add New Results send the new issues object
	}
	
	

	

