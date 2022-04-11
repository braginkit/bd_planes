
function drawMethod(key) {
	switch (key) {
		case 2:
			// statements_1
			drawHeat(arr);
			break;
		case 3:	
			// statements_1
			drawHeatMap(arr);
			break;
		case 0:
			// statements_def
			drawHotLine(arr);
			break;
		default: break;
	}
}


function show_stat (stat) {
	element = document.getElementById("stat");
    console.log(stat);

    if (stat.air_list_all.length) {
		console.log(stat.air_list_all.length)
	}

    var str = "Всего самолетов: " + stat.air_count_all.toString() +
    		"\nГарант-е кол-во выбросов CO2 всего: " + stat.co2_min_all.toFixed(2).toString() + " кг." +
    		"\nПредпол-е кол-во выбросов CO2 всего: " + stat.co2_max_all.toFixed(2).toString()  + " кг." +
    		"\nСписок самолетов:";
    element.innerText = str;
    var list_str = ''
    for (i = 0; i < stat.air_list_all.length; i++){
    	list_str += stat.air_list_all[i] + "\n";
    }
    //list_str = list_str[0:-1];
    console.log(list_str);
    element = document.getElementById("stat_list");
    element.innerText = list_str;
}


Array.prototype.forEach.call(drawOpt, function(radio) {
		radio.addEventListener('change',  function(event) {
			global_Switch = parseInt(this.value)
	   		drawMethod(global_Switch); 
	   });
});


$("#getdata").click(function() {
	console.log("Get all data from server");
	send_ajax({ 
            type: 'GET',
            path: 'get_all',
            success: function(result){
						arr = result[1];
						show_stat(result[0]);
						
						console.log(arr.length)
						drawMethod(global_Switch);
					}
	});
});

//get list of airoports
send_ajax({ 
            type: 'GET',
            path: 'airoports',
            success: function(result){
						airoports = result;
						airList()
					}
});
