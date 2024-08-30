import { useState, useEffect } from "react";
import { listen } from "@tauri-apps/api/event";
import "./App.css";
import "leaflet/dist/leaflet.css";
import { MapContainer, TileLayer, Polyline, Marker, Popup } from "react-leaflet";

function Map() {
  const [data, setData] = useState(null);
  const [recvDat,setRecvDat] = useState(false);
  function getQueryParams() {
    return new URLSearchParams(window.location.search);
  }
  function parseDataFromQuery() {
    const params = getQueryParams();
    const encodedData = params.get("data");
    if (encodedData) {
      return JSON.parse(decodeURIComponent(encodedData));
    }
    return null;
  }
  useEffect(() => {
    const data = parseDataFromQuery();
    setData(data);
  }, []);

  console.log(data)


  // Convert the path data into an array of LatLng tuples
  const route = recvDat ? data.path.map(([lat, lon]) => [lat, lon]) : [];


  return (
    <div className="w-30 h-dvj">

      <MapContainer center={[20.593, 78.962]} zoom={5} scrollWheelZoom={true}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* Draw the route on the map using Polyline */}
        {route.length > 0 && <Polyline positions={route} color="blue" />}

        {/* Optionally, add markers for each point in the route */}
        {route.map((position, idx) => (
          <Marker key={idx} position={position}>
            <Popup>
              Point {idx + 1}: [{position[0]}, {position[1]}]
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}

export default Map;
