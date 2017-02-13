$(document).ready(function(){
	$('.button').on('click',function(){
		window.location='/sessionCover'
	});
	$('.letters').on('click',function(){
		var id=$(this).attr('id');	
		if (isNaN(id.slice(-2))){
			id=id.slice(-1);
		}
		else if(!isNaN(id.slice(-2))){
			id=id.slice(-2);
		}

		$(this).removeClass('letters').addClass('letterUsed');
		//get a JSON object from server route at id location where id is the 1-26 values of A-Z
		$.getJSON('/guess/'+id, function(data){
			var locations=data.locations;
			var finished=data.finished;
			var guesses=data.guesses;
			var inside=data.inside;
			var wordFiller=data.wordFiller;
			var correct=data.correct;
			var wins=data.wins;
			var losses=data.totGames-wins;
			var wrong=guesses-correct;
			var locLength=locations.length;
			//if guess isn't in word then show a new hangman image
			$('#wins').text('Wins: '+wins.toString());
			$('#losses').text('Losses: '+losses.toString());
			if(inside){
				//iterate over all locations of guessed Letter 
				for(var loc=0;loc<locLength;loc++){
					$('#'+(locations[loc]).toString()).text(String.fromCharCode(Number(id)+64));
				}
			}
			else{
				console.log('#image_'+wrong.toString())
					document.getElementById('image_'+wrong.toString()).style.display='block';
			}
			setTimeout(function (){ 
				if(finished && wrong<10){
					alert('You Won! Your record is: '+wins.toString()+' wins and '+losses.toString()+' losses');
					window.location='/sessionCover'
				}
				else if(finished){
					console.log(wordFiller);
					for(var chr in wordFiller){
						var locations=wordFiller[chr];
						var length=locations.length;
						for(var index=0; index<length;index++){
							$('#'+(locations[index]).toString()).text(chr.toUpperCase());
							$('#'+(locations[index]).toString()).addClass('red');
						}
					}
					setTimeout(function(){
						alert('There\'s always next time! Your record is: '+wins.toString()+' wins and '+losses.toString()+' losses');
						window.location='/sessionCover'
					},100000);
				}
			}, 900);
		});
	});
});
