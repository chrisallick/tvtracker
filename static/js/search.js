addShow = function( show ) {
	$.ajax({
		url: "/add",
		type: "POST",
		data: { 'show': show },
		dataType: 'json',
		beforeSend: function(data) {
			$("#loading-gif").css("display", "inline");
		},
		success: function(data) {
			$("#loading-gif").css("display", "none");
			console.log( data );
		}	
	});
}

submitTopic = function( query ) {
	$.ajax({
		url: "/search",
		data: { 'query': query },
		dataType: 'json',
		beforeSend: function(data) {
			$("#loading-gif").css("display", "inline");
		},
		success: function(data) {
			$("#loading-gif").css("display", "none");
			console.log( data );
			if( data.title ) {
				$("#title").text( data.title );
				$("#link").text( data.link ).attr("href", data.link);
				$("#search-show").append("<a id='add-show' href='#'>add show</a>");
				$("#add-show").click( function(event){
					event.preventDefault();
					addShow( $("#query").val() );
				})
				$("#result").slideDown();
			}
		}
	});
}

$(document).ready( function() {
	$("#submit").click( function(event) {
		event.preventDefault();
		submitTopic( $("#query").val() );
	});

	$("#result").hide();

	$("#query").click( function(event) {
		$(this).val("");
	});
})