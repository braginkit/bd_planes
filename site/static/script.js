var mymap = L.map('mapid')
    .on('mousemove', (e) => {
    mousemove(e);
  })
    .on('click', (e) => {
    draw_rectangle(e.latlng);
    //console.log(e.latlng)
  })
    .setView([54.5, 44.5, ], 5);

var global_Switch = 0;

var arr = [];
var DLayer = new L.LayerGroup();
var RecLayer = new L.LayerGroup();
var airoports = [];
var count = 0;
var bounds = [];
var add_rec = false;
let url = 'http://192.168.191.13:5000/';

var drawOpt = document.querySelectorAll('input[type=radio][name="draw"]');


//L.circle([50.5, 30.5], {radius: 2000}).bindPopup("HI").addTo(mymap);


L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(mymap);



//START DRAW WITH leaflet.hotline.js

function drawHotLine (dataarr) {
    DLayer.clearLayers();
    console.log("Start drawHotLine");

    mass = []

    options = {
        //"height": 
        "weight": 5,
        "outlineWidth": 1,
        "outlineColor": 'black',
        "palette": {
            0.0: 'green',
            0.8: 'yellow',
            1.0: 'red'
        },
        "smoothFactor": 1
            //"min": 
            //"max": 
    }
    var min = dataarr[0].Way.flights.rounds[0].totalfuelwastedless;
    var max = dataarr[0].Way.flights.rounds[0].totalfuelwastedless;
    var period = 0;
    for (i = 1; i < dataarr.length; i++) {
        if (min > dataarr[i].Way.flights.rounds[0].totalfuelwastedless) {
            min = dataarr[i].Way.flights.rounds[0].totalfuelwastedless
        }
        if (max < dataarr[i].Way.flights.rounds[0].totalfuelwastedless) {
            max = dataarr[i].Way.flights.rounds[0].totalfuelwastedless
        }
    }

    period = max - min;
    //console.log(min,max,period)
    for (i = 0; i < dataarr.length; i++) {
        var test_percent = (dataarr[i].Way.flights.rounds[0].totalfuelwastedless - min)/period;
        //console.log(test_percent);
        var test_color = '';
        

        if (test_percent<0.5) {
            test_color = "#" + Math.trunc(255*test_percent).pad(2,16) + "ff00";
        }
        else {
            test_color = "#ff" + Math.trunc(255*(1 - test_percent)).pad(2,16) + "00";
        }

        //console.log(test_color)
        polyline = new L.Polyline(dataarr[i].Way.coordinates.points, { 
                                                                    color: test_color, 
                                                                    stroke: true, 
                                                                    weight: 2
                                                                }
                                )

        mass.push(polyline);
        //mass.push(L.hotline(dataarr[i].Way.coordinates.points0, options));
        mass[i].bindPopup(
                        "Откуда: " +                                    dataarr[i].Way.from.toString() + '<br>' + 
                        "Куда: " +                                      dataarr[i].Way.to.toString() + '<br>' + 
                        "Рейс: " +                                      dataarr[i].Way.flights.flightname.toString() +"<br>" + 
                        "Дата:" +                                       dataarr[i].Way.flights.rounds[0].data.toString() + '<br>' + 
                        "Самолет: " +                                   dataarr[i].Way.flights.rounds[0].airplane.toString() + "<br>" + 
                        "Путь: " +                                      dataarr[i].Way.flights.rounds[0].km.toFixed(2).toString() +  " км<br>" + 
                        "Гарант. затраченного топлива: " +              dataarr[i].Way.flights.rounds[0].totalfuelwastedless.toFixed(2).toString() +" кг.<br>" + 
                        "Предпол-ное кол-во затраченного топлива: " +   dataarr[i].Way.flights.rounds[0].totalfuelwastedmax.toFixed(2).toString()  + " кг<br>" +
                        "Гарант-е кол-во выбросов CO2: "  +             dataarr[i].Way.flights.rounds[0].totalemissionsless.toFixed(2).toString() + " кг<br>" + 
                        "Предпол-е кол-во выбросов CO2: " +             dataarr[i].Way.flights.rounds[0].totalemissionsmax.toFixed(2).toString() + " кг"
                        );
        
        DLayer.addLayer(mass[i]);
    }

    
    DLayer.addTo(mymap);
}

//END DRAW WITH leaflet.hotline.js



//START DRAW with leaflet-heat.js

function drawHeat (dataarr) {
    DLayer.clearLayers();
    heatmap_mass = []


    var min = dataarr[0].Way.flights.rounds[0].totalfuelwastedless;
    var max = dataarr[0].Way.flights.rounds[0].totalfuelwastedless;
    var period = 0;
    for (i = 1; i < dataarr.length; i++) {
        if (min > dataarr[i].Way.flights.rounds[0].totalfuelwastedless) {
            min = dataarr[i].Way.flights.rounds[0].totalfuelwastedless
        }
        if (max < dataarr[i].Way.flights.rounds[0].totalfuelwastedless) {
            max = dataarr[i].Way.flights.rounds[0].totalfuelwastedless
        }
    }

    period = max - min;

    test_arr = []
    heatmap_cfg = {
        radius: 5,
        //max: max,
        blur: 5,
        minOpacity: 0.6,
        gradient: {
            '0.33': 'green',
            '0.66': 'yellow',
            '1.0': 'red'
        }
    }

    for (i = 0; i < dataarr.length; i++) {
        var test = [];
        norm = (dataarr[i].Way.flights.rounds[0].totalfuelwastedless - min)/period;
        for (j = 0; j < dataarr[i].Way.coordinates.points.length; j++) {
            //console.log(dataarr[i].Way.coordinates.points[j].concat(dataarr[i].Way.flights.rounds[0].totalfuelwastedless))
            //dataarr[i].Way.flights.rounds[0].totalfuelwastedless.toFixed(2)
            
            
            test.push(dataarr[i].Way.coordinates.points[j].concat(norm));
            
        }
        //console.log(norm);
        test_arr = test_arr.concat(test)
        //console.log(test_arr)
        //heatmap_mass.push(L.heatLayer(dataarr[i].Way.coordinates.points0, heatmap_cfg));
        
    }
    //console.log(test_arr)
    heatmap_mass.push(L.heatLayer(test_arr, heatmap_cfg));
    DLayer.addLayer(heatmap_mass[0]);
    DLayer.addTo(mymap);
}



function setRadius(r) {
    var radius;
    var pointC = mymap.latLngToContainerPoint(mymap.getCenter());
    var pointX = [pointC.x + 1, pointC.y];


    // convert containerpoints to latlng's
    var latLngC = mymap.containerPointToLatLng(pointC);
    var latLngX = mymap.containerPointToLatLng(pointX);

    // Assuming distance only depends on latitude 
    var distanceX = latLngC.distanceTo(latLngX);
    // 100 meters is the fixed distance here
    var pixels = r / distanceX;

    console.log("Distanse per pixcel = " + distanceX)
    console.log("Zoom = " + mymap.getZoom())
    console.log("Radius in pixcels = " + pixels)
    return pixels
}


//END DRAW with leaflet-heat.js


//START DRAW WITH leaflet-heatmap.js

function drawHeatMap (dataarr) {
    DLayer.clearLayers();
    //console.log("drawHeatMap in")

    var cfg = {
        // radius should be small ONLY if scaleRadius is true (or small radius is intended)
        // if scaleRadius is false it will be the constant radius used in pixels
        //"fixedRadius": true, // enable use of meters instead of pixels
        "gradient": {
            // enter n keys between 0 and 1 here
            // for gradient color customization
            '.33': 'green',
            '.66': 'yellow',
            '1.00': 'red'
        },
        "blur": 0.45,
        "radius": 3,
        //"radiusMeters": 1500, // set the radius value in meters
        "maxOpacity": 5,
        // scales the radius based on map zoom
        "scaleRadius": false,
        // if set to false the heatmap uses the global maximum for colorization
        // if activated: uses the data maximum within the current map boundaries
        //   (there will always be a red spot with useLocalExtremas true)
        "useLocalExtrema": false,
        // which field name in your data represents the latitude - default "lat"
        latField: 'lat',
        // which field name in your data represents the longitude - default "lng"
        lngField: 'lng',
        // which field name in your data represents the data value - default "value"
        valueField: 'count'
    };


    var heatmapLayer = new HeatmapOverlay(cfg);
    //console.log("start")
    for (i = 0; i < dataarr.length; i++) {
        //console.log("Points:")
        //console.log(dataarr[i].Way.coordinates.points0)
        for (j = 0; j< dataarr[i].Way.coordinates.points.length; j++) {
            //console.log("Points 2:")
            //console.log(dataarr[i].Way.coordinates.points0[j][0])
            heatmapLayer.addData({
                                "lat": dataarr[i].Way.coordinates.points[j][0], 
                                "lng" : dataarr[i].Way.coordinates.points[j][1],
                                "count" : dataarr[i].Way.flights.rounds[0].totalfuelwastedless,
                            });
  
        }  
    }
    DLayer.addLayer(heatmapLayer);
    DLayer.addTo(mymap);
}


//END DRAW WITH leaflet-heatmap.js



//START WORKing WITH AIROPORTS USER

function get_by_date() {
    console.log(0)
    date_air_start = document.querySelector('#date_air_start');

    date_air_end = document.querySelector('#date_air_end');
    
    var date_arr = [date_air_start.value, date_air_end.value];//[year + "-" + month + "-" + date1, year + "-" + month + "-" + date1];

    send_ajax({ 
                type: 'POST',
                path: 'get_by_date',
                data: date_arr,
                success: function(result){
                                arr = result[1];
                                show_stat(result[0]);
                                //console.log(arr.length)
                                drawMethod(global_Switch);
                        }
    }); 
};

function filter_air_by_date() {
    var airList = [];
    for (var i = 0; i < 9; i++) {
        if($('#airports_from'+i).length > 0){
            airList.push($("#airports_from" + i +" :selected").val());
        } else{
            //console.log("airports_from" + i + " not exists");
        }
        if($('#airports_to'+i).length > 0){
            airList.push($("#airports_to" + i +" :selected").val());
        } else{
            //console.log("airports_to" + i + " not exists");
        }  
    }
    date_air_start = document.querySelector('#date_air_start');

    date_air_end = document.querySelector('#date_air_end');
    
    var date_arr = [date_air_start.value, date_air_end.value];
    console.log("по времени и аэропортам")

    send_ajax({ 
        type: 'POST',
        path: 'filter_air_by_date',
        data: [date_arr, airList],
        success: function(result){
            arr = result[1];
            show_stat(result[0]);
            if (arr.length == 0) {
                alert("По заданному запросу " + airList[0] + "-" + airList[1] + " в период" + date_arr[0] +"-" + date_arr[1] +" нет рейсов");
            }
            else {
                //emet0();
                console.log(arr)
                //document.getElementById("em"+count).appendChild(lbl);
                drawMethod(global_Switch);
            }
        }
    }); 
};

function filter_air () {
    var airList = [];
    for (var i = 0; i < 9; i++) {
        if($('#airports_from'+i).length > 0){
            airList.push($("#airports_from" + i +" :selected").val());
        } else{
            //console.log("airports_from" + i + " not exists");
        }
        if($('#airports_to'+i).length > 0){
            airList.push($("#airports_to" + i +" :selected").val());
        } else{
            //console.log("airports_to" + i + " not exists");
        }  
    }
    
    console.log(airList)

    send_ajax({ 
                type: 'POST',
                path: 'filter_air',
                data: airList,
                success: function(result){
                    arr = result[1];
                    show_stat(result[0]);
                    console.log(arr);
                    if (arr.length == 0) {
                        alert("По заданному запросу " + airList[0] + "-" + airList[1] + " нет рейсов");
                    }
                    else {
                        //emet0();
                        console.log(arr)
                        //document.getElementById("em"+count).appendChild(lbl);
                        drawMethod(global_Switch);
                    }
                }
    }); 
}

function airList () {
    var select1 = document.getElementById("airports_from0");
    var select2 = document.getElementById("airports_to0");

    for (let i = 0; i < airoports.length; i++) {
        select1.options[select1.options.length] = new Option(airoports[i], airoports[i]);
        select2.options[select2.options.length] = new Option(airoports[i], airoports[i]);
    }
};


$("#addair").click(function() {
    if (count >= 9) {
        return;
    }
    count++;

    console.log("Add airoport to");
    var mybr = document.createElement('br');
    document.getElementById("airoports").appendChild(mybr);

    var lbl = document.createElement("LABEL");
    lbl.innerHTML = "Выбрать рейсы от аэропорта:" + count;
    document.getElementById("airoports").appendChild(lbl);


    var airF = document.createElement("SELECT");
    airF.id = "airports_from" + count;
    

    for (var i = 0; i < airoports.length; i++) {
        var option = document.createElement("OPTION");
        option.value = airoports[i];
        option.text = airoports[i];
        //console.log(Object.keys(example_array.Airoports[i]));
        airF.appendChild(option);
    }
    document.getElementById("airoports").appendChild(airF);

    var lbl = document.createElement("LABEL");
    lbl.innerHTML = "до";// + count;
    document.getElementById("airoports").appendChild(lbl);

    var airT = document.createElement("SELECT");
    airT.id = "airports_to" + count;

    for (var i = 0; i < airoports.length; i++) {
        var option = document.createElement("OPTION");
        option.value = airoports[i];
        option.text =airoports[i];
        //console.log(Object.keys(example_array.Airoports[i]));
        airT.appendChild(option);
    }
    document.getElementById("airoports").appendChild(airT);
    /*
    var emet = document.createElement("LABEL");
    emet.innerHTML = "Em:" + count;
    emet.id = "emet" + count;
    console.log("hey")
    document.getElementById("airoports").appendChild(emet);
    */
    //console.log(arr);
});

/*function emet0 () {
    document.getElementById("emet0").innerHTML =  "Откуда: " +                                    arr[0].Way.from.toString() + '<br>' + 
                                                    "Куда: " +                                      arr[0].Way.to.toString() + '<br>' + 
                                                    "Рейс: " +                                      arr[0].Way.flights.flightname.toString() +"<br>" + 
                                                    "Дата:" +                                       arr[0].Way.flights.rounds[0].data.toString() + '<br>' + 
                                                    "Самолет: " +                                   arr[0].Way.flights.rounds[0].airplane.toString() + "<br>" + 
                                                    "Путь: " +                                      arr[0].Way.flights.rounds[0].km.toString() +  " км<br>" + 
                                                    "Гарант. затраченного топлива: " +              arr[0].Way.flights.rounds[0].totalfuelwastedless.toString() +" кг.<br>" + 
                                                    "Предпол-ное кол-во затраченного топлива: " +   arr[0].Way.flights.rounds[0].totalfuelwastedmax.toString()  + "<br>" +
                                                    "Гарант-е кол-во выбросов CO2: "  +             arr[0].Way.flights.rounds[0].totalemissionsless.toString() + " кг<br>" + 
                                                    "Предпол-е кол-во выбросов CO2: " +             arr[0].Way.flights.rounds[0].totalemissionsmax.toString() + " кг"
};
*/
$("#getair").click(function() {
    switch (parseInt($('input[name="choice"]:checked').val())) {
        //по времени
        case 0: {
            get_by_date();
            break;
        }
        //по времени и аэропортам
        case 1: {
            // statements_1
            filter_air_by_date();
            break;
        }
        //по аэропортам
        case 2: {
            // statements_def
            filter_air();
            break;
        }
        default: {
            console.log("Please will write defoult function");
            break;
        }
    }
}); 

//END WORKing WITH AIROPORTS USER


//start DRAWING RECTANGLE



$("#add_rec").click(function() {
    add_rec = true;
    console.log("ADD rectangle " + add_rec);

});

$("#rem_rec").click(function() {
    add_rec = false;
    RecLayer.clearLayers();
    bounds.length = 0
});

function draw_rectangle(latlng) {

    console.log(bounds);
    console.log(latlng);
    //RecLayer.clearLayers();
    /*if (bounds.length == 2 && !add_rec){
        add_rec = true;
        RecLayer.clearLayers();
        bounds.length = 0
    }*/
    if (add_rec && bounds.length < 2) {
        bounds.push([ latlng.lat, latlng.lng ]);
        //console.log(latlng);
    }
    
    if (bounds.length == 2 && add_rec){
        RecLayer.clearLayers();
        var rect = L.rectangle(bounds, { fill: false, weight: 3});
        RecLayer.addLayer(rect);
        RecLayer.addTo(mymap);
        console.log("POST rect")
        switch (parseInt($('input[name="choice"]:checked').val())) {
        //по времени
            case 0: {
                console.log(0)
                date_air_start = document.querySelector('#date_air_start');

                date_air_end = document.querySelector('#date_air_end');
                
                var date_arr = [date_air_start.value, date_air_end.value];//[year + "-" + month + "-" + date1, year + "-" + month + "-" + date1];

                send_ajax({ 
                            type: 'POST',
                            path: 'filter_area_get_by_date',
                            data: [date_arr,bounds],
                            success: function(result){
                                        arr = result[1];
                                        show_stat(result[0]);
                                        console.log("Send Rectangle")
                                        //console.log(arr)
                                        drawMethod(global_Switch);
                                    }
                });

                break;
            }
            //по времени и аэропортам
            case 1: {
                // statements_1
                var airList = [];
                for (var i = 0; i < 9; i++) {
                    if($('#airports_from'+i).length > 0){
                        airList.push($("#airports_from" + i +" :selected").val());
                    } else{
                        //console.log("airports_from" + i + " not exists");
                    }
                    if($('#airports_to'+i).length > 0){
                        airList.push($("#airports_to" + i +" :selected").val());
                    } else{
                        //console.log("airports_to" + i + " not exists");
                    }  
                }
                date_air_start = document.querySelector('#date_air_start');

                date_air_end = document.querySelector('#date_air_end');
                
                var date_arr = [date_air_start.value, date_air_end.value];
                console.log("по времени и аэропортам")

                send_ajax({ 
                    type: 'POST',
                    path: 'filter_area_filter_air_by_date',
                    data: [date_arr, airList, bounds],
                    success: function(result){
                        arr = result[1];
                        
                        if (arr.length == 0) {
                            alert("По заданному запросу " + airList[0] + "-" + airList[1] + " в период" + date_arr[0] +"-" + date_arr[1] +" нет рейсов");
                        }
                        else {
                            //emet0();
                            console.log(arr)
                            //document.getElementById("em"+count).appendChild(lbl);
                            drawMethod(global_Switch);
                            show_stat(result[0]);
                        }
                    }
                }); 
                break;
            }
            //по аэропортам
            case 2: {
                // statements_def
                var airList = [];
                for (var i = 0; i < 9; i++) {
                    if($('#airports_from'+i).length > 0){
                        airList.push($("#airports_from" + i +" :selected").val());
                    } else{
                        //console.log("airports_from" + i + " not exists");
                    }
                    if($('#airports_to'+i).length > 0){
                        airList.push($("#airports_to" + i +" :selected").val());
                    } else{
                        //console.log("airports_to" + i + " not exists");
                    }  
                }
                
                console.log(airList)

                send_ajax({ 
                            type: 'POST',
                            path: 'filter_area_filter_air',
                            data: [airList, bounds],
                            success: function(result){
                                arr = result[1];
                                st = result[0];
                                console.log("Send Rectangle")
                                if (arr.length == 0) {
                                    alert("По заданному запросу " + airList[0] + "-" + airList[1] + " нет рейсов");
                                }
                                else {
                                    //emet0();
                                    //console.log(arr)
                                    //document.getElementById("em"+count).appendChild(lbl);
                                    show_stat(st);
                                    drawMethod(global_Switch);
                                }
                            }
                });
                break;
            }
            default: {
                console.log("Please will write defoult function");
                break;
            }
        }
        add_rec = false;
        //console.log(bounds);
        
        //console.log(bounds[0].lng, bounds[0].lat);
    }
    // body... 
};

//END DRAWING RECTANGLE

function mousemove (e) {

    //document.getElementById('latlng').textContent = JSON.stringify(e.latlng, null, 2);

    if (add_rec && bounds.length == 1) {
        RecLayer.clearLayers();
        var rect = L.rectangle([bounds[0], [e.latlng.lat, e.latlng.lng]], { fill: true, weight: 1});
        RecLayer.addLayer(rect);
        RecLayer.addTo(mymap);
        //console.log(latlng);
    }
}


$('#date_air_start').change(function(argument) {
    console.log("Date_air_start " + $('#date_air_start').val())

});

$('#date_air_end').change(function(argument) {
    console.log("Date_air_end " + $('#date_air_end').val())
});

$('input[name="choice"]').change(function (argument) {
    
    console.log($('input[name="choice"]:checked').val());
});


$("#test_").click(function() {
    var type = "GET";
    path = "get_all"

    success = function(result){
            dataarr = result[1];
            DLayer.clearLayers();
            show_stat(result[0]);
            mass = []

            for (i = 0; i < dataarr.length; i++) {
                mass.push(new L.Polyline(dataarr[i].Way.coordinates.points, { 
                    color: '#'+i.toString(16) +(255 - i).toString(16) + '00', 
                    stroke: true, 
                    weight: 2
                }
                ));
                //mass.push(L.hotline(dataarr[i].Way.coordinates.points0, options));
                //console.log(dataarr[i].Way.coordinates.points);

                mass[i].bindPopup(
                                "Откуда: " +                                    dataarr[i].Way.from.toString() + '<br>' + 
                                "Куда: " +                                      dataarr[i].Way.to.toString() + '<br>' + 
                                "Рейс: " +                                      dataarr[i].Way.flights.flightname.toString() +"<br>" + 
                                "Дата:" +                                       dataarr[i].Way.flights.rounds[0].data.toString() + '<br>' + 
                                "Самолет: " +                                   dataarr[i].Way.flights.rounds[0].airplane.toString() + "<br>" + 
                                "Путь: " +                                      dataarr[i].Way.flights.rounds[0].km.toFixed(2).toString() +  " км<br>" + 
                                "Гарант. затраченного топлива: " +              dataarr[i].Way.flights.rounds[0].totalfuelwastedless.toFixed(2).toString() +" кг.<br>" + 
                                "Предпол-ное кол-во затраченного топлива: " +   dataarr[i].Way.flights.rounds[0].totalfuelwastedmax.toFixed(2).toString()  + " кг<br>" +
                                "Гарант-е кол-во выбросов CO2: "  +             dataarr[i].Way.flights.rounds[0].totalemissionsless.toFixed(2).toString() + " кг<br>" + 
                                "Предпол-е кол-во выбросов CO2: " +             dataarr[i].Way.flights.rounds[0].totalemissionsmax.toFixed(2).toString() + " кг"
                                );
                //console.log("Poly: 2");
                DLayer.addLayer(mass[i]);
            }

            
            DLayer.addTo(mymap);

        }

    //send_ajax({type: "POST", path: "get_all", data: "Hello"});

    send_ajax({type: type, path: path, success: success});
    
});
