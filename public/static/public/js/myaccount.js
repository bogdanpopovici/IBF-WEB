function toggle(input, value, option, field) {
	var it = document.getElementById(input);
	var v = document.getElementById(value);
	var o = document.getElementById(option);

	if(it.style.display == "block") {

		$.post('/edit_personal_details/',{
		    'field':   field,
		    'value':   it.value,
		    'csrfmiddlewaretoken':      $('[name="csrfmiddlewaretoken"]').val()
		},function(result){
		    if(result.result=='OK'){
		        v.innerHTML = result.new_value;
		        it.value = ''
		    }
		    else{
		    	alert(result.err_message);
		    }
		});

    	it.style.display = "none";
		o.innerHTML = "Edit";
		v.style.display = "block";
  	}
	else {
		reset();
		it.style.display = "block";
		o.innerHTML = "Save";
		v.style.display = "none";
	}
}

function reset() {
	for (i = 1; i <= 7; i++) {

			var it = document.getElementById('it'+i);
    		it.style.display = "none";
			var v =document.getElementById('s'+i);
    		v.style.display = "block";
			var o = document.getElementById('e'+i);
			o.innerHTML = "Edit";
  		}
}

