import { useState, useEffect } from "react";
import "./App.css";
import "leaflet/dist/leaflet.css";
import { MapContainer, TileLayer, Polyline, Marker, Popup } from "react-leaflet";

function Map() {
  const [data, setData] = useState(null);

  // Function to get query parameters from the URL
  function getQueryParams() {
    return new URLSearchParams(window.location.search);
  }

  // Function to parse the data from the query parameters
  function parseDataFromQuery() {
    const params = getQueryParams();
    const encodedData = params.get("data");

    if (encodedData) {
      try {
        return JSON.parse(decodeURIComponent(encodedData));
      } catch (error) {
        console.error("Failed to parse data:", error);
        return null;
      }
    }
    return null;
  }

  // useEffect to run when the component mounts
  useEffect(() => {
    const parsedData = parseDataFromQuery();
    if (parsedData) {
      setData(parsedData);
    }
  }, []);

  // Convert the path data into an array of LatLng tuples for Leaflet
  const route = data && data.path ? data.path.map(([lat, lon]) => [lat, lon]) : [];
  console.log(data);

  return (
    <div className="relative w-full h-screen">
      {/* MapContainer with z-index adjusted */}
      <MapContainer
        center={[20.593, 78.962]}
        zoom={5}
        scrollWheelZoom={true}
        className="absolute top-0 left-0 w-full h-full z-0"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Draw the route on the map using Polyline */}
        {route.length > 0 && (
          <>
            <Polyline positions={route} color="blue" />
            <Marker position={route[0]}>
              <Popup>Starting point</Popup>
            </Marker>
            <Marker position={route[route.length - 1]}>
              <Popup>Destination point</Popup>
            </Marker>
          </>
        )}
      </MapContainer>

      {/* Fixed, rounded box in the bottom left corner with z-index to be on top */}
      <div className="fixed bottom-5 left-5 p-3 bg-white bg-opacity-80 rounded-lg shadow-lg z-50">
        <p className="text-sm font-medium">ETA : {Math.floor(data['eta'])} Hrs.</p>
        {/* <p className="text-sm font-medium">Estimated Fuel Usage : {data['fuel']}</p> */}
        <p className="text-sm font-medium">Distance : {Math.floor(data['km'])} KMs</p>
      </div>
    </div>
  );
}

export default Map;
