import { useState } from "react";
import { invoke } from "@tauri-apps/api/tauri";
import "./App.css";
import logo from './assets/g1.png'
import ports from './data/indian_ocean_ports.json';
import shipTypesData from './data/ship_data.json'


function App() {

  const [Start, setStart] = useState([0.34534534,2.34534534534]);
  const [End, setEnd] = useState([2.879438579,0.8927498273]);
  const [Shipdata, setShipdata] = useState({})

  const putstart = (e) => {
    const selectedCoords = e.target.value.split(',').map(Number);
    setStart(selectedCoords);
  };

  const putend = (e) => {
    const selectedCoords = e.target.value.split(',').map(Number);
    setEnd(selectedCoords);
  };
  const sendRust = () => {
    console.log(Start,End)
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
    try{
      invoke('map',{data})
    }catch(e){
      console.log(e)
    }
    
  }


  return (
    <>
      <div className="bg-[#e6e6e6] w-full h-screen">
        <img src={logo} />
        <div className="flex items-center content-center p-25 mt-20">
          <div className="w-1/3 h-1/2 mx-5 flex flex-col">

            <>
              <label className='mb-[10px] block text-base font-medium text-dark dark:text-black'>
                Default Select
              </label>
              <div className='relative z-20'>
                <select onChange={putstart} className=''>

                  {ports.map(
                    (fullname, latitude, longitude) => {
                      return (
                        <option value={[fullname['latitude'],fullname['longitude']]} className='dark:bg-dark-2'>{fullname['fullname']}</option>
                      )
                    }
                  )}
                </select>
                <span className='absolute right-4 top-1/2 z-10 mt-[-2px] h-[10px] w-[10px] -translate-y-1/2 rotate-45 border-r-2 border-b-2 border-body-color'></span>
              </div>
            </>
            <>
              <label className='mb-[10px] block text-base font-medium text-dark dark:text-black'>
                Default Select
              </label>
              <div className='relative z-20'>
                <select onChange={putend} className=''>

                  {ports.map(
                    (fullname, latitude, longitude) => {
                      return (
                        <option value={[fullname['latitude'],fullname['longitude']]} className='dark:bg-dark-2'>{fullname['fullname']}</option>
                      )
                    }
                  )}
                </select>
                <span className='absolute right-4 top-1/2 z-10 mt-[-2px] h-[10px] w-[10px] -translate-y-1/2 rotate-45 border-r-2 border-b-2 border-body-color'></span>
              </div>
            </>
          </div>
          <div className="w-0.5 h-60 m-30 bg-[#797979]" />
          <div className="w-1/3 mx-5">
            <div className="">
              <>
                <label className='mb-[10px] block text-base font-medium text-dark dark:text-black'>
                  Ship Type
                </label>
                <div className='relative z-20'>
                  <select className=''>
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

            </div>
          </div>
        </div>
        <button className="m-32 text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-10 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800" onClick={() => { sendRust() }}>Get Route</button>
      </div>
    </>
  );
}

export default App;
