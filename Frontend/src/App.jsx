import { useState } from "react";
import "./App.css";
import logo from './assets/g1.png'
import ports from './data/indian_ocean_ports.json';
import shipTypesData from './data/ship_data.json'
import "leaflet/dist/leaflet.css";
import { MapContainer, TileLayer, Polyline, Marker, Popup } from "react-leaflet";
import 'leaflet-providers';
import axios from "axios";
import la from './assets/arr.png'


function App() {

  const [Start, setStart] = useState([22.535744, 88.299581]);
  const [End, setEnd] = useState([22.535744, 88.299581]);
  const [Shipdata, setShipdata] = useState({})
  const [data, setData] = useState({});
  const [route, setRoute] = useState([]);
  const [init, setInit] = useState(true)

  const putstart = (e) => {
    const selectedCoords = e.target.value.split(',').map(Number);
    setStart(selectedCoords);
  };

  const putend = (e) => {
    const selectedCoords = e.target.value.split(',').map(Number);
    setEnd(selectedCoords);
  };
  const callApi = () => {
    console.log(Start, End)
    const data = {
      "start": Start,
      "end": End,
      "ship": {
        "shipType": "Cargo",
        "Loa": 2414.0,
        "Draft": 1241.0,
        "Displ": 2414.0,
        "Power": 440.0,
        "Load": 2200.0,
        "Speed": 15.0,
        "Beam": 30.0
      }
    }
    console.log("Sending request to server...");

    axios.post("http://127.0.0.1:5000/map", data)
      .then((response) => {
        console.log("Request successful");
        setData(response.data);
        setRoute(response.data['path'])
        setInit(false);
      })
      .catch((error) => {
        console.error(`Failed to send request: ${error.message}`);
      });

  }


  return (
    <>
      <div className="w-full h-full">
        <MapContainer
          center={[20.593, 78.962]}
          zoom={5}
          scrollWheelZoom={true}
          className="absolute top-0 left-0 w-full h-full z-0"
        >
          <TileLayer
            url="https://tiles.stadiamaps.com/tiles/alidade_satellite/{z}/{x}/{y}{r}.jpg"
          // attribution='&copy; CNES, Distribution Airbus DS, © Airbus DS, © PlanetObserver (Contains Copernicus Data) | &copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

          />

          {route.length > 0 && (
            <>
              <Polyline positions={route} color="#5BC4FF" />
              <Marker position={route[0]}>
                <Popup>Starting point</Popup>
              </Marker>
              <Marker position={route[route.length - 1]}>
                <Popup>Destination point</Popup>
              </Marker>
            </>
          )}
        </MapContainer>
        {init ? <>
          <div className=" bg-[#e8e8e8] scrollbar-thin shadow-2xl fixed bottom-5 left-10 top-5 p-10 bg-white rounded-lg shadow-lg z-50 overflow-auto">
            <img src={logo} className="mx-12 my-5" />
            <hr className="border-t border-gray-300 w-full" />
            <br />
            <>
              <label className='mb-[10px] block text-base font-medium text-dark dark:text-black'>
                Starting Port
              </label>
              <div className='relative z-20'>
                <select onChange={putstart} className='block w-full appearance-none bg-white border border-gray-300 dark:bg-dark-2 dark:border-gray-600 text-black dark:text-white py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:border-blue-500'>

                  {ports.map(
                    (fullname, latitude, longitude) => {
                      return (
                        <option value={[fullname['latitude'], fullname['longitude']]} className='dark:bg-dark-2'>{fullname['fullname']}</option>
                      )
                    }
                  )}
                </select>
                <span className='absolute right-4 top-1/2 z-10 mt-[-2px] h-[10px] w-[10px] -translate-y-1/2 rotate-45 border-r-2 border-b-2 border-body-color'></span>
              </div>
            </>
            <>
              <label className='mb-[10px] block text-base font-medium text-dark dark:text-black'>
                Destination Port
              </label>
              <div className='relative z-20'>
                <select onChange={putend} className='block w-full appearance-none bg-white border border-gray-300 dark:bg-dark-2 dark:border-gray-600 text-black dark:text-white py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:border-blue-500'>

                  {ports.map(
                    (fullname, latitude, longitude) => {
                      return (
                        <option value={[fullname['latitude'], fullname['longitude']]} className='dark:bg-dark-2'>{fullname['fullname']}</option>
                      )
                    }
                  )}
                </select>
                <span className='absolute right-4 top-1/2 z-10 mt-[-2px] h-[10px] w-[10px] -translate-y-1/2 rotate-45 border-r-2 border-b-2 border-body-color'></span>
              </div>
            </>
            <br />
            <hr className="border-t border-gray-300 w-full" />
            <br />
            <>
              <label className='mb-[10px] block text-base font-medium text-dark dark:text-black'>
                Ship Type
              </label>
              <div className='relative z-20'>
                <select className='block w-full appearance-none bg-white border border-gray-300 dark:bg-dark-2 dark:border-gray-600 text-black dark:text-white py-2 px-4 pr-8 rounded leading-tight focus:outline-none focus:border-blue-500'>
                  {shipTypesData.ship_types.map((category, index) => (
                    <optgroup key={index} label={category.category}>
                      {category.types.map((type, typeIndex) => (
                        <option key={typeIndex} value={type}>
                          {type}
                        </option>
                      ))}
                    </optgroup>
                  ))}
                </select>
                <span className='absolute right-4 top-1/2 z-10 mt-[-2px] h-[10px] w-[10px] -translate-y-1/2 rotate-45 border-r-2 border-b-2 border-body-color'></span>
              </div>
            </>
            <br />
            <>
              <label className='mb-[10px] block text-base font-medium text-dark dark:text-black'>
                Length Overall (LOA)
              </label>
              <input
                type='text'
                placeholder='Default Input'
                className='bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 '
              />
            </>
            <br />
            <>
              <label className='mb-[10px] block text-base font-medium text-dark dark:text-black'>
                Beam
              </label>
              <input
                type='text'
                placeholder='Default Input'
                className='bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 '
              />
            </>
            <br />
            <>
              <label className='mb-[10px] block text-base font-medium text-dark dark:text-black'>
                Draft
              </label>
              <input
                type='text'
                placeholder='Default Input'
                className='bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 '
              />
            </>
            <br />
            <>
              <label className='mb-[10px] block text-base font-medium text-dark dark:text-black'>
                Displacement
              </label>
              <input
                type='text'
                placeholder='Default Input'
                className='bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 '
              />
            </>
            <br />
            <>
              <label className='mb-[10px] block text-base font-medium text-dark dark:text-black'>
                Power
              </label>
              <input
                type='text'
                placeholder='Default Input'
                className='bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 '
              />
            </>
            <br />
            <>
              <label className='mb-[10px] block text-base font-medium text-dark dark:text-black'>
                Cargo Load
              </label>
              <input
                type='text'
                placeholder='Default Input'
                className='bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 '
              />
            </>
            <br />
            <>
              <label className='mb-[10px] block text-base font-medium text-dark dark:text-black'>
                Service Speed
              </label>
              <input
                type='text'
                placeholder='Default Input'
                className='bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 '
              />
            </>
            <br />
            <button className="m-3 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-40 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800" onClick={() => { callApi() }}>Get Route</button>
          </div>
        </>
          :
          <>
            <div className="fixed bottom-5 left-5 p-5 px-10 bg-white rounded-lg shadow-lg z-50">
              <p className="text-sm font-medium">ETA : {Math.floor(data['eta'])} Hrs.</p>
              {/* <p className="text-sm font-medium">Estimated Fuel Usage : {data['fuel']}</p> */}
              <p className="text-sm font-medium">Distance : {Math.floor(data['km'])} KMs</p>
            </div>
            
              <button className="fixed top-5 right-5 bg-white rounded-lg shadow-2xl z-50 w-10 h-10 items-center flex justify-center" onClick={()=>{setInit(true);setRoute([])}}><img src={la} className="w-5 h-5 z-51"/></button>
            
          </>}



      </div>
    </>
  );
}

export default App;
