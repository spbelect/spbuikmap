function initGoogleMap() {
         
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 12,
          center: {lat: 59.940266, lng: 30.313810},
          mapTypeId: 'roadmap'
        });
//         var markerCluster = new MarkerClusterer(map, [],
//             {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
/*
        var iconBase = 'https://maps.google.com/mapfiles/kml/shapes/';
        var icons = {
          parking: {
            icon: iconBase + 'parking_lot_maps.png'
          },
          library: {
            icon: iconBase + 'library_maps.png'
          },
          info: {
            icon: iconBase + 'info-i_maps.png'
          }
        };*/
        map.data.setStyle(function(feature) {
          return {
            title: feature.getProperty('label'),
            label: {
//               color: '#ff0000',
              fontWeight: 'bold',
              text: feature.getProperty('label')
            },
            icon: {
              url: 'https://maps.gstatic.com/mapfiles/api-3/images/spotlight-poi-dotless2.png',
//               size
//               labelOrigin: [100, 100]
            }
          }
        })
        map.data.addListener('click', function(event) {
          var feat = event.feature;
          var html = ""
          for (var i=0;i<feat.getProperty('uiks').length;i++) {
            uik = feat.getProperty('uiks')[i];
            html += `<div>TIK ` + uik.tik + ` UIK ` + uik.uik + `</div>`
          }
//           "<b>"+feat.getProperty('name')+"</b><br>"+feat.getProperty('description');
//           html += "<br><a class='normal_link' target='_blank' href='"+feat.getProperty('link')+"'>link</a>";
  
          var infowindow = new google.maps.InfoWindow({
              content: html
          });
//           infowindow.setContent(html);
          infowindow.setPosition(event.latLng);
//           infowindow.setOptions({pixelOffset: new google.maps.Size(0,-34)});
          infowindow.open(map);
          
          google.maps.event.addListener(map, 'click', function() {
            infowindow.close();
          });
        });

        map.data.loadGeoJson('/uiks_geo.json');
//         $.get("/uiks_geo.json").done(function(response){alert(JSON.stringify(response));})
      /*
        $.get("/uiks.json").done(function(response){
            alert(JSON.stringify(response));
//             table = [];
            
            for (var coords in response) {
                uiks = response[coords]
                title = 
//                 if ()
//                 console.log(response[uik].coords);
                var marker = new google.maps.Marker({
                    position: response[uik].coords,
        //             icon: icons[feature.type].icon,
//                     icon: null,
                    label: uik,
//                     map: map
                });
                markerCluster.addMarker(marker);
//                 x = `<div><pre>
//                    `+JSON.stringify(response[uik])+`
//                     </pre></div>
//                     `;
//                 var infowindow = new google.maps.InfoWindow({
//                     content: x
//                 });
// 
//                 marker.addListener('click', function() {
//                     infowindow.open(map, marker);
//                 });

            }
        }).fail(function(e){alert('request failed' + JSON.stringify(e))})
        */
} 
