import { useState, useEffect } from "react";
import { listen } from "@tauri-apps/api/event";
import "./App.css";
import "leaflet/dist/leaflet.css";
import { MapContainer, TileLayer, Polyline, Marker, Popup } from "react-leaflet";

function Map() {
  const [data, setData] = useState(null);
  const [recvDat,setRecvDat] = useState(false);

  useEffect(() => {
    // Listen for the custom event sent from the Rust side
    const unlisten = listen("response", (event) => {
      setData(event.payload); 
      setRecvDat(true);
      console.log(data);// Set the received data to state
      console.log("Received custom data:", event.payload);
    });

    
    return () => {
      unlisten.then((fn) => fn());
    };
  }, []);


  // Convert the path data into an array of LatLng tuples
  const route = recvDat ? data.path.map(([lat, lon]) => [lat, lon]) : [];
  console.warn(data)

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
