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
		$.getJSON('/'+id, function(data){
			var locations=data.locations;
			locLength=locations.length
			//iterate over all locations of guessed Letter
			for(var loc=0;loc<locLength;loc++){
				$("#"+(locations[loc]).toString()).text(String.fromCharCode(Number(id)+64));
			}
		});
	});
});
