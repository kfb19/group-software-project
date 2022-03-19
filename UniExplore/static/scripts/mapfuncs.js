/*
    Authors: Tomas Premoli
    Description:  Map generating function
*/
function mapgen(divName, maxSouth, maxNorth, maxWest, maxEast, minZoom, maxZoom,
    drawBox, boxColor) {
    // map border
    var swest = L.latLng(maxSouth, maxWest),
        neast = L.latLng(maxNorth, maxEast),
        bounds = L.latLngBounds(swest, neast);

    var map = L.map(divName)

    map.invalidateSize();

    var center = [((maxSouth + maxNorth) / 2), ((maxWest + maxEast) / 2)];

    map.setView(center, minZoom);

    // mapbox is also a good tileset for this
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: maxZoom,
        minZoom: minZoom,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // This draws a polygon around the playable area
    var areamarker = [
        [ // Exterior Ring
            [90, -180],
            [90, 180],
            [-90, 180],
            [-90, -180]
        ], // Then holes (interior rings)
        [ // No red in this square
            [maxSouth, maxWest],
            [maxSouth, maxEast],
            [maxNorth, maxEast],
            [maxNorth, maxWest]
        ]
    ];

    // adding polygon to map
    if (drawBox) {
        L.polygon(areamarker, { color: boxColor, weight: 2, fillOpacity: 0.1, interactive: false }).addTo(map);
    }

    map.setMaxBounds(bounds);

    return map;
}




/*
    Authors: Tomas Premoli
    Description: Function responsible for enabling & disabling spoof mode
*/
function devModeToggle(map, button) {
    // These are all dev mode loads
    // This shouldn't render in the template when not a gamemaster/superuser
    var devModeOn = false;
    button.addEventListener("click", function() {
        if (devModeOn) {
            //returning to normal settings
            map.off('click');
            map.removeLayer(watcher[1]);
            watcher = startLocator(map);
            devModeOn = false;
            button.innerHTML = "Enable spoof mode";
        } else {
            // Clearing geolocation watcher
            navigator.geolocation.clearWatch(watcher[0]);

            // Onclick for moving user marker
            map.on('click', function(e) {
                lat = e.latlng.lat;
                lon = e.latlng.lng;

                console.log("Lat: " + lat + ", Lon:" + lon);

                // Set usermarker to clicked location
                watcher[1].setLatLng([lat, lon]).addTo(map);

                // Reload challenges
                determineChallenges(lat, lon);
                
                dailyRiddle(lat,lon)
                
            });

            devModeOn = true;
            button.innerHTML = "Disable spoof mode";
        }
    });
}

/*
    Authors: Tomas Premoli
    Description: Starts userlocation scripts
*/
function startLocator(map, marker = null) {
    if (navigator.geolocation) {
        // watchposition ties a method to every time the user's location changes;
        // here it'll run determineChallenges, Which will update challenge list
        function success(position) {
            usermarker.setLatLng([position.coords.latitude, position.coords.longitude]).addTo(map);

            var addedLoc = position.coords.latitude + ", " +
                position.coords.longitude +
                " at " + position.timestamp;

            console.log(addedLoc);

            determineChallenges(position.coords.latitude, position.coords.longitude);
            dailyRiddle(position.coords.latitude, position.coords.longitude);
           
        }

        function error(err) {
            console.warn('ERROR(' + err.code + '): ' + err.message);
        }

        options = {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 5000
        };

        // if there isn't already a user marker
        if (marker == null) {
            // Creating user marker to move it around with location
            var userIcon = generateUserIcon();

            var usermarker = L.marker([0, 0], { icon: userIcon });
            usermarker.bindPopup("<b>You are here!</b>");
            usermarker.addTo(map);
        }

        // it'll run success if loc gotten, error, if not.
        // Helpful to return watchID and usermarker if we need to use them
        return [navigator.geolocation.watchPosition(success, error, options), usermarker];
    } else {
        console.log("User has declined geolocation access");
    }
}

function generateUserIcon() {
    var userIcon = L.icon({
        iconUrl: "static/images/userMarker.png",
        iconSize: [25, 41], // size of the icon
        iconAnchor: [12.5, 41], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -41], // point from which the popup should open relative to the iconAnchor
        shadowUrl: "static/images/userMarkerShadow.png",
        shadowAnchor: [7, 25],
        shadowSize: [25, 25]
    });
    return userIcon
}

function addChallengeMarker(e, map, maxSouth, maxNorth, maxWest, maxEast, clickLocation,
    id_lat, id_long) {
    lat = e.latlng.lat;
    lon = e.latlng.lng;

    console.log("Lat: " + lat + ", Lon:" + lon);

    var outOfRange = false;

    if (lat < maxSouth) {
        lat = maxSouth;
        outOfRange = true;
    } else if (lat > maxNorth) {
        lat = maxNorth;
        outOfRange = true;
    }

    if (lon < maxWest) {
        lon = maxWest;
        outOfRange = true;
    } else if (lon > maxEast) {
        lon = maxEast;
        outOfRange = true;
    }

    // Clear existing marker
    if (clickLocation != undefined) {
        map.removeLayer(clickLocation);
    }

    // Add a marker to show where you clicked
    clickLocation = L.marker([lat, lon]).addTo(map);

    if (outOfRange)
        clickLocation.bindPopup("Marker has been adjusted to map bounds").openPopup();

    id_lat.value = lat;
    id_long.value = lon;

    return clickLocation;
}

function generateWeeklyIcon() {
    var weeklyIcon = L.icon({
        iconUrl: "static/images/weeklyChallengeMarker.png",
        iconSize: [25, 41], // size of the icon
        iconAnchor: [12.5, 41], // point of the icon which will correspond to marker's location
        popupAnchor: [0, -41], // point from which the popup should open relative to the iconAnchor
        shadowUrl: "static/images/userMarkerShadow.png",
        shadowAnchor: [7, 25],
        shadowSize: [25, 25]
    });
    return weeklyIcon
}

