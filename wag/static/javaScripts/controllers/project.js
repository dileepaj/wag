//*** controllers for dashboard elements
/////////////////////////////////////////////// general //////////////////////////////////////////////

google.load('visualization', '1', { 'packages': ['annotatedtimeline'] });
google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(function(){
	$(function() {
		var	curUser = $('#userid').val();
		var curSite = $('#curSite').text()
       
   		$.ajax({
   			url : '/projectHistory',
            type : 'POST',
            contentType : 'application/json',
      		data : JSON.stringify(
    			{
    				home : curSite    				
    			},
    			null,
    			'\t'
    		),
            dataType : 'json',
            async : false,
	    	success : function(data){
	    		if(data.error){
	    			alert(data.error)
	    		}else{
		    		populateGraph(data.result)
		    		fillHistoryTable(data.result)
					showLatestEvaluation(data.result)
	    		}
			}   		
		});
	   
		fillPagesTable(curSite)
		
		$(document).ajaxSend(function() {
		    $('#spinner').show();
	    });
	    $(document).ajaxComplete(function() {
		    $('#spinner').hide();
	    });
	});
});





/*
	$("#loaderDiv").ajaxStart(function(){
    $(this).show();
 }).ajaxStop(function(){
    $(this).hide();
 });
 
	*/
 


function populateGraph(histData){
	var projData = new google.visualization.DataTable();
	projData.addColumn('date', 'Evaluated Time');
	projData.addColumn('number', 'Number of Violations')
	
	for (var i in histData){
		projData.addRows([
		[new Date(histData[i].time.year, histData[i].time.month, histData[i].time.day, histData[i].time.hour, histData[i].time.minute),
		histData[i].total]
	])	
	var mxValue = histData[i].total
	}
	
	var options = {
        title: 'Evaluation history graph',
        
		vAxis: {title: 'Total defects',minValue:0, maxValue:mxValue*1.75, viewWindowMode:'maximized'}
    };
	
	var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
     chart.draw(projData, options);
	google.visualization.events.addListener(chart, 'select', function(){
        clickedChart1(chart,projData,histData);
    });
		
}

function fillPagesTable(siteName){
	$.ajax({
        	url : '/pagesList',
        	type : 'POST',
        	contentType : 'application/json',
        	data : JSON.stringify(
        						{
        							name : siteName, 
        						},
        						null,
        						'\t'
        	),
        	dataType : 'json',
        	success : function(data){
        		var pages = data.pagesList;
        		for (var i in pages){
					var row = $('<tr></tr>');
					row.append($('<td>').text(pages[i]));
					row.append($('<td>').text("Ok"));
					$('#pages').append(row);
				}		
        	}                    	
       });
}

function fillHistoryTable(histData){
	var curSite = $('#curSite').text()	
	for (var i in histData){
		var row = $('<tr></tr>');
		row.append($('<td>').html('<a href="loadEval?site='+curSite+'&evalNum='+histData[i].evalNum+'&url='+histData[i].homeUrl+'" >'+ histData[i].evalNum+'</a>'));
		row.append($('<td>').text(histData[i].total));
		var evalDate = new Date(histData[i].time.year, histData[i].time.month, histData[i].time.day, histData[i].time.hour, histData[i].time.minute)
		row.append($('<td>').text(evalDate.toDateString()));
		$('#evalHist').append(row);
	}
}

function drawChart2(rowno,histData,datetime ) {
  
  ID = "WAG";

           var data = new google.visualization.DataTable();
			
		   data.addColumn('string', 'ID');
		   data.addColumn('number', 'Defect Category');
		   data.addColumn('number', 'Defect Priority');
		   data.addColumn('string', 'Disability Type');
		   data.addColumn('number', 'Defect Count');
		   data.addColumn('string', 'Title');
		  
		   var arr =new Array();

			 
			 for (var v in histData[rowno].allViolations){
			 ftrId = histData[rowno].allViolations[v].featureId
			 if ( !(ftrId in arr)){
			 
			 obj = {
			 count : 1,
			 title : histData[rowno].allViolations[v].title,
			 prio: parseInt(histData[rowno].allViolations[v].priority),	
			 dissType : histData[rowno].allViolations[v].rank,
			 cat : histData[rowno].allViolations[v].featureId
			 }
			 
			 arr [ftrId] = obj
			 }
			 
			 else {
			  obj = arr[ftrId]
			 obj.count = obj.count+1
			 arr[ftrId] = obj
			 }
			 
			 }
			 
			 for (var a in arr){
			   data.addRows([
					["",  arr[a].cat + 1 , arr[a].prio, arr[a].dissType, arr[a].count,arr[a].title]
				])
		  
			 }
        var options = {
          title:  ' Evaluation bubble graph - ' + datetime,	
		  hAxis: {title: 'Defect Category', maxValue:10, minValue:0, viewWindowMode:'maximized', gridlines:{count:-1}},
		  vAxis: {title: 'Defect priority', maxValue:4,minValue:0, viewWindowMode:'maximized' },
		  bubble: {textStyle: {fontSize: 11}}

        }

        var chart = new google.visualization.BubbleChart(document.getElementById('visualization'));
        chart.draw(data, options);
		
			 
         
      }
	  
	  //Getting the latest evaluation
function showLatestEvaluation(histData){

	 row = histData.length - 1;
	 
	 var rowObj = histData[histData.length - 1]
			
	curDate = rowObj.time.year + " " +  rowObj.time.month +  " " + rowObj.time.day;
	
	drawChart2( row, histData, curDate);
		
}

//Get selected element
function clickedChart1(chart,data,histData)
{

        // grab a few details before redirecting
        var selection = chart.getSelection();
        var rowObj = selection[0].row;
		
		row = histData.length - 1;
     
    curDate = histData[rowObj].time.year + " " +  histData[rowObj].time.month +  " " + histData[rowObj].time.day;
    drawChart2( row, histData, curDate);

}

