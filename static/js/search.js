addShow = function( show, last_viewed ) {
	$.ajax({
		url: "/add",
		type: "POST",
		data: { 'show': show, 'last-viewed': last_viewed },
		dataType: 'json',
		beforeSend: function(data) {
			$("#loading-gif").css("display", "inline");
		},
		success: function(data) {
			$("#loading-gif").css("display", "none");
			location.reload();
		}	
	});
}

//increase last viewed
updateShow = function() {
	$.ajax({
		url: "/update",
		type: "POST",
		data: { 'show': show, 'last-viewed': last_viewed },
		dataType: 'json',
		beforeSend: function(data) {
			$("#loading-gif").css("display", "inline");
		},
		success: function(data) {
			$("#loading-gif").css("display", "none");
			location.reload();
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
				$("#add-show").click( function(event){
					event.preventDefault();
					addShow( $("#query").val(), $("#last-viewed").val() );
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