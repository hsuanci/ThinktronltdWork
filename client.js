 
  var map = L.map('map', {
                center: [25.017600999059294,121.52678668498991],
                zoom: 7,
            });
  
  var baselayer =L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                maxZoom: 18,
                attribution: 'Map data © <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',      
                }).addTo(map);
                            
  var json_breakfast = new L.layerGroup();

            $.ajax({                                       
                url: 'http://18.236.149.178:8000/api/workproject/raw_sql_query/',
                type: "GET", 
                dataType: "json",
                  success: function (AQIdata) {
                  for (var i=0; i< AQIdata.length; i++){
                       marker = new L.marker([AQIdata[i].latitude,AQIdata[i].longitude]).bindPopup('SiteName:'+AQIdata[i].sitename+'<br>'+'County:'+AQIdata[i].county+'<br>'+'AQI:'+AQIdata[i].aqi+'<br>'+'Publishtime:'+AQIdata[i].publishtime).openPopup().addTo(map).on('click', onClick);;
                  }
                     function onClick(e) {
                        $.getJSON('http://18.236.149.178:8000/api/workproject/raw_sql_query/?longitude='+this.getLatLng().lng, function(datastream) {
                          var datachart = [];
                          var datatime = [];
                             for (var i=0; i< datastream.length; i++){
                                 datachart.push(parseInt(datastream[i].aqi))
                                 datatime.push(datastream[i].publishtime)
                              }
                                   Highcharts.chart('container', {
                                                   chart: {
                                                            type: 'line'
                                                          },
                                                   title: {
                                                             text: 'Time series AQI monitoring data'
                                                          },
                                                             subtitle: {
                                                               text: 'Source: https://taqm.epa.gov.tw/taqm/tw/default.aspx'
                                                             },
                                                             xAxis: {
                                                               type: 'DateTime',
                                                               categories:datatime
                                                             },
                                                             yAxis: {
                                                               title: {
                                                                  text: 'AQI'
                                                               }
                                                             },
                                                             plotOptions: {
                                                               line: {
                                                                  dataLabels: {
                                                                      enabled: true
                                                                  },
                                                                      enableMouseTracking: false
                                                               }
                                                             },
                                                             series: [{
                                                                name: 'AQI',
                                                                data: datachart
                                                             }]
                                                   });
                          });
                     }

                   },
                         error: function () {
                              console.log("error");
                         }
                 });          