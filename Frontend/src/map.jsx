import { useState, useEffect } from "react";
import "./App.css";
import "leaflet/dist/leaflet.css";
import { MapContainer, TileLayer, Polyline } from "react-leaflet";

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

  return (
    <div className="w-30 h-dvj">
      <MapContainer center={[20.593, 78.962]} zoom={5} scrollWheelZoom={true}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Draw the route on the map using Polyline */}
        {route.length > 0 && <Polyline positions={route} color="blue" />}
      </MapContainer>
    </div>
  );
}

export default Map;
