//*** View controller

	//////////////////////////////////////////////// general //////////////////////////////////////////////
	$(function() { 
			$(".structure").colResizable();
			
			// Buttons
			$( "input:submit, button, input:button", "#dashboard" ).button();
			
			// Dropdown
			 $( ".combobox" ).combobox();
			
			// Tabs
			$('#tabs').tabs();
			
			// List
			$( "#list" ).selectable({
				cancel: 'a'
			});
		
			// Progressbar
			$("#progressbar").progressbar({
				value: 0
			});
			
			// File input
			$('#files').button().file().choose(function(e, input) {
				var x = input.val().length-1;
				console.log(x);
				if ( (input.val().substr(x-4,x)) == '.html' ) {
					file = input.val();
					$('#filename').text(file);
					alert("'"+file+"' source file selected !");
				}
				else {
					alert("Please select a HTML source file !");
				}
			}); 
			
			// Evaluate button
			$("#eval").click(function() { 
				$( "#dialog-form" ).dialog( "open" );
				$('#eval').attr("disabled", true); 
			});
			
			// Apply button
			$("#modify").click(function() {
				$('#list').empty();
				modify();
			});
			
			// Deploy button
			$("#dep").click(function() {
				deploy();
			});
			
			// OK button
			$("#ok").click(function() { 
				$('#resolve').hide();
				
				// Select next result
				var id = parseInt($('form').attr('issue'), 10);	
				var next = id + 1;	
				$("#"+next).find("a").click();
			});
			
			// Skip button
			$("#skip").click(function() {
				var r_id = $('form').attr('issue');
				if ( list.results[r_id].status!='skipped' ) {  
					list.results[r_id].setStatus('skipped'); 
					list.skips++;
					alert('This issue is '+list.results[r_id].status); 
				}
				$('#resolve').hide();
			});
			
			// Auto correct button
			$("#autocorct").click(function() {
				var r_id = $('form').attr('issue');
				autoCorrect(r_id);
			});

	});
	
	///////////////////////////////////////////// progress controller ///////////////////////////////////////
	function calcProgress() {
		var prsntg = (list.resolves/list.total)*100; 
		$("#progressbar").progressbar({value: prsntg});
		$("#summary").html("Summary: &nbsp;&nbsp;&nbsp;&nbsp; Total-"+list.total+" &nbsp;&nbsp;&nbsp;&nbsp; Resolved-"+list.resolves+" &nbsp;&nbsp;&nbsp;&nbsp; Skipped-"+list.skips);
		$("#p").html(Math.round(prsntg*Math.pow(10,2))/Math.pow(10,2)+" %");
	}
	
	//////////////////////////////////////////// sourcecode controller /////////////////////////////////////

	function setSrcode(source) { 
		setLine(source);
		
		// replacing lessthans, linebreaks and whitespaces
		var newcode = ((source.replace(/\</g,"&lt")).replace(/\n/g,'<br>')).replace(/ \//g,'/'); 
		$('#code').html(newcode);
		
		// initial evaluation
		scanner.scan(source);
		list.setResults(); 
	}
		
	function modify() {	
		// evaluation after changes
		try{ 
			var plain = (($('#code').html()).replace(/<font style="background-color: red;">/g,'')).replace(/<\/font>/g,''); 
			var cd = ((plain.replace(/\&lt;/g,"<")).replace(/\&gt;/g,">")).replace(/\<br>/g,'\n');
			
			setLine(cd);
			
			scanner.scan(cd);
			list.update(); 
			calcProgress();
			
		} catch(e) {
			alert("Inappropriate source code ! \n");
		}
		
	}
	
	function setLine(code) {
		// setting lines numbers according to the line breaks in the code
		var lines = code.match(/\n/g).length;
		$('#lines').empty();
		for (var i=1; i<lines+3; i++) {
			$('#lines').append(i+'<br>');
		}
	}
	
	function getLine(element) { 
		var srcode = ((($('#code').html()).replace(/\&lt;/g,"<")).replace(/\&gt;/g,">")).replace(/\<br>/g,'\n');
		var e = element.slice(1,-2); 	
		var i = srcode.indexOf(e);				
		
		if (i != -1) {
			var n = srcode.slice(0,i);  
			var count = n.match(/\n/g); 
			var line = count.length;
			return line;
		}		
	}
	
	//////////////////////////////////////////// resultlist controller //////////////////////////////////////
	function showResult(rslt) { 
			var text = features[rslt.feature].error+' - line '+rslt.line+' - '+rslt.status;
			var fn = "showFeature(features['"+rslt.feature+"']); showDetails('"+rslt.id+"');";
			var clss = 'ui-widget-content';
			
			switch(rslt.status)
			{
				case "resolved":
					clss = 'ui-widget-content list-resolved';
					break;
				case "skipped":
					clss = 'ui-widget-content list-skipped';
					break;
				default:
					clss = 'ui-widget-content';
			}
		  
			$('#list').append(
				$('<li>').attr('class',clss).attr('id',rslt.id).append(
					$('<a>').attr('href','#').attr('onClick',fn).append(text) 
				)
			);  
	}
	
	
	//////////////////////////////////////////// details controller /////////////////////////////////////////
	// getFeature() set feature tab area
	function showFeature(ftr) { 				
		var title = ftr.title;
		var dis = ftr.disability;
		var prio = ftr.priority;
		var des = ftr.description;
		var sol = ftr.solution;
				
		var outMsg = 	"<span class='headings'>Title: </span><br/><span class='data'>" + title + "</span><br/><br/>" +
						"<span class='headings'>Disability: </span><br/>" + dis + "<br/><br/>" + 
						"<span class='headings'>Priority level: </span><br/>" + prio + "<br/><br/>" +
						"<span class='headings'>Description: </span><br/>" + des + "<br/><br/>" + 
						"<span class='headings'>Solution: </span><br/>" + sol;
			
		$("#feature").html(outMsg);
	}
	
	// getResult() set resolve tab area
	function showDetails(rid) {
		$('#resolve').show();
		$('form').attr('issue',rid);
		
		var fid = list.results[rid].feature;
		var elemnt = list.results[rid].element;
		var lnum = list.results[rid].line; 	
		
		//highlight code
		$('li').removeClass("ui-selected");
		$('#'+rid+'').addClass("ui-selected");
		
		var el = (((elemnt.replace(/\</g,"&lt;")).replace(/\>/g,"&gt;")).replace(/\n/g,'<br>')); 
		var cd = (($('#code').html()).replace(/<font style="background-color: lightblue;">/g,'')).replace(/<\/font>/g,''); 
		var s = cd.replace(el,'<font style="background-color: lightblue;">'+el+'</font>'); 
		$("#code").html(s);
		
		$("#des").html(features[fid].solution+"<br><br> Line number "+lnum+"<br><br>"); 
		$("#ele").val(elemnt);
		
		if (fid == 1) {
			elemnt = elemnt.replace('src="','src="../WAG/sourceFiles/');					
		}	
		
		$("#obj").html(elemnt+"<br>");
	}
		
	// combobox function
    (function( $ ) {
        $.widget( "ui.combobox", {
            _create: function() {
                var self = this,
                    select = this.element.hide(),
                    selected = select.children( ":selected" ),
                    value = selected.val() ? selected.text() : select.children( ":first" ).text();
                var input = this.input = $( "<input>" )
                    .insertAfter( select )
                    .val( value )
                    .autocomplete({
                        delay: 0,
                        minLength: 0,
                        source: function( request, response ) {
                            var matcher = new RegExp( $.ui.autocomplete.escapeRegex(request.term), "i" );
                            response( select.children( "option" ).map(function() {
                                var text = $( this ).text();
                                if ( this.value && ( !request.term || matcher.test(text) ) )
                                    return {
                                        label: text.replace(
                                            new RegExp(
                                                "(?![^&;]+;)(?!<[^<>]*)(" +
                                                $.ui.autocomplete.escapeRegex(request.term) +
                                                ")(?![^<>]*>)(?![^&;]+;)", "gi"
                                            ), "<strong>$1</strong>" ),
                                        value: text,
                                        option: this
                                    };
                            }) );
                        },
                        select: function( event, ui ) {
                            ui.item.option.selected = true;
                            self._trigger( "selected", event, {
                                item: ui.item.option
                            });
                        },
                        change: function( event, ui ) {
                            if ( !ui.item ) {
                                var matcher = new RegExp( "^" + $.ui.autocomplete.escapeRegex( $(this).val() ) + "$", "i" ),
                                    valid = false;
                                select.children( "option" ).each(function() {
                                    if ( $( this ).text().match( matcher ) ) {
                                        this.selected = valid = true;
                                        return false;
                                    }
                                });
                                if ( !valid ) {
                                    $( this ).val( "" );
                                    select.val( "" );
                                    input.data( "autocomplete" ).term = "";
                                    return false;
                                }
                            }
                        }
                    })
                    .addClass( "ui-widget ui-widget-content ui-corner-left" );

                input.data( "autocomplete" )._renderItem = function( ul, item ) {
                    return $( "<li></li>" )
                        .data( "item.autocomplete", item )
                        .append( "<a>" + item.label + "</a>" )
                        .appendTo( ul );
                };

                this.button = $( "<button type='button'>&nbsp;</button>" )
                    .attr( "tabIndex", -1 )
                    .attr( "title", "Show All Items" )
                    .insertAfter( input )
                    .button({
                        icons: {
                            primary: "ui-icon-triangle-1-s"
                        },
                        text: false
                    })
                    .removeClass( "ui-corner-all" )
                    .addClass( "ui-corner-right ui-button-icon" )
                    .click(function() {
                        if ( input.autocomplete( "widget" ).is( ":visible" ) ) {
                            input.autocomplete( "close" );
                            return;
                        }

                        $( this ).blur();
                        input.autocomplete( "search", "" );
                        input.focus();
                    });
            },

            destroy: function() {
                this.input.remove();
                this.button.remove();
                this.element.show();
                $.Widget.prototype.destroy.call( this );
            }
        });
    })( jQuery );
	
	
	// dialog function
	$(function() {
		$( "#dialog:ui-dialog" ).dialog( "destroy" );
		
		$( "#dialog-form" ).dialog({
			autoOpen: false,
			height: 300,
			width: 250,
			modal: true,
			buttons: {
				"Evaluate": function() {
					scanner.priority = $('#priority').val();
					var allVals = [];
					$('#disability :checked').each(function() {
						allVals.push($(this).val()); 
					});
					if ( !($.isEmptyObject(allVals)) ) { scanner.rank = allVals; }
					else {alert('Default rank is set !');}
					openWin();
					$( this ).dialog( "close" );
				},
				Cancel: function() {
					$( this ).dialog( "close" );
				}
			}
		}); 
	});