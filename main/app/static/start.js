/*Start JS*/

Number.prototype.pad = function(size,dimension) {
    var s = this.toString(dimension);
    while (s.length < (size || 2)) {s = "0" + s;}
    return s;
}

function send_ajax ({   type = "GET", 
                        path, 
                        success = function(result) {
                            console.log(result);
                        }, 
                        data = null
                    } = {}) 
{
    request = {
                type: type,
                crossDomain: true,
                dataType: 'json',
                headers: {
                    'Access-Control-Allow-Credentials' : true,
                    'Access-Control-Allow-Origin':'*',
                    'Access-Control-Allow-Methods': type,
                    'Access-Control-Allow-Headers':'application/json',
                },
                url: url + path, 
                success: success
            }
    
    if (data != null) {
        request.contentType = "application/json; charset=utf-8";
        request.data = JSON.stringify(data);
    }
    //console.log(request)

    $.ajax(request);
}


//SET DATE TO INPUT DATE
var currentDate = new Date(Date.now()-4*60*60*1000);
//currentDate.setDate(Date.now());
var date1 = currentDate.getDate().toString().padStart(2, 0);
var month = (currentDate.getMonth() + 1 ).toString().padStart(2, 0);
var year = currentDate.getFullYear().toString();

var dateString = year + "-" + month + "-" + date1 ;

date_air_start = document.querySelector('#date_air_start');


// Set the date
date_air_start.value = dateString;


date_air_end = document.querySelector('#date_air_end');


// Set the date
date_air_end.value = dateString;

window.onload = function(){
	var date_arr = ["2020-05-09", "2020-05-10"];//[year + "-" + month + "-" + date1, year + "-" + month + "-" + date1]; // 

	send_ajax({   type: "POST", 
	                path: "get_by_date", 
	                success: function(result) {
	                    arr = result[1];
	                    
						show_stat(result[0]);
						drawMethod(global_Switch);
	                }, 
	                data: date_arr
                    });
};