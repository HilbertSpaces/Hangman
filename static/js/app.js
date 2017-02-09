$(document).ready(function(){
	$('.letters').click(function(){
		var id=$(this).attr('id');	
		if (isNaN(id.slice(-2))){
			id=id.slice(-1);
		}
		else {
			id=id.slice(-2);
		}
		//get a JSON object from server route at id location where id is the 1-26 values of A-Z
		$.getJSON('/guess/'+id, function(data){
			var locations=data.locations;
			var finished=data.finished;
			var guesses=data.guesses;
			var inside=data.inside;
			//if(!inside){
			locLength=locations.length
			//iterate over all locations of guessed Letter
			for(var loc=0;loc<locLength;loc++){
				$("#"+(locations[loc]).toString()).text(String.fromCharCode(Number(id)+64));
			}
			if(finished && guesses<10){
				alert('you win!')
				window.location='/sessionCover'
			};
			if(finished){
				alert('you can still Play again!');
				window.location='/sessionCover'
			}
		});
	});
});
