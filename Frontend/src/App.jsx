import { useState } from "react";
import { invoke } from "@tauri-apps/api/tauri";
import "./App.css";
import logo from './assets/g1.png'
import ports from './data/indian_ocean_ports.json';
import shipTypesData from './data/ship_data.json'


function App() {

  const [Start, setStart] = useState();
  const [End, setEnd] = useState();
  const [Shipdata, setShipdata] = useState({})

  const putstart = (e) => { setStart(e.target.value) };

  const sendRust = () => {
    const data = {
      "start": [12.34, 56.78],
      "end": [98.76, 54.32],
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
        <div className="flex bg-yellow-200 items-center content-center p-25 mt-20">
          <div className="bg-red-500 w-1/3 h-1/2 mx-5 flex flex-col">

            <>
              <label className='mb-[10px] block text-base font-medium text-dark dark:text-white'>
                Default Select
              </label>
              <div className='relative z-20'>
                <select onChange={putstart} className='relative z-20 w-full appearance-none rounded-lg border border-stroke dark:border-dark-3 bg-transparent py-[10px] px-5 text-dark-6 outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-gray-2'>

                  {ports.map(
                    (fullname, latitude, longitude) => {
                      return (
                        <option value={(latitude, longitude)} className='dark:bg-dark-2'>{fullname['fullname']}</option>
                      )
                    }
                  )}
                </select>
                <span className='absolute right-4 top-1/2 z-10 mt-[-2px] h-[10px] w-[10px] -translate-y-1/2 rotate-45 border-r-2 border-b-2 border-body-color'></span>
              </div>
            </>
            <>
              <label className='mb-[10px] block text-base font-medium text-dark dark:text-white'>
                Default Select
              </label>
              <div className='relative z-20'>
                <select onChange={putstart} className='relative z-20 w-full appearance-none rounded-lg border border-stroke dark:border-dark-3 bg-transparent py-[10px] px-5 text-dark-6 outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-gray-2'>

                  {ports.map(
                    (fullname, latitude, longitude) => {
                      return (
                        <option value={(latitude, longitude)} className='dark:bg-dark-2'>{fullname['fullname']}</option>
                      )
                    }
                  )}
                </select>
                <span className='absolute right-4 top-1/2 z-10 mt-[-2px] h-[10px] w-[10px] -translate-y-1/2 rotate-45 border-r-2 border-b-2 border-body-color'></span>
              </div>
            </>
          </div>
          <div className="w-0.5 h-60 m-30 bg-[#797979]" />
          <div className="bg-indigo-500 w-1/3 mx-5">
            <div className="">
              <>
                <label className='mb-[10px] block text-base font-medium text-dark dark:text-white'>
                  Ship Type
                </label>
                <div className='relative z-20'>
                  <select className='relative z-20 w-full appearance-none rounded-lg border border-stroke dark:border-dark-3 bg-transparent py-[10px] px-5 text-dark-6 outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-gray-2'>
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
                <label className='mb-[10px] block text-base font-medium text-dark dark:text-white'>
                  Length Overall (LOA)
                </label>
                <input
                  type='text'
                  placeholder='Default Input'
                  className='w-full bg-transparent rounded-md border border-stroke dark:border-dark-3 py-[10px] px-5 text-dark-6 outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-gray-2 disabled:border-gray-2'
                />
              </>
              <>
                <label className='mb-[10px] block text-base font-medium text-dark dark:text-white'>
                  Beam
                </label>
                <input
                  type='text'
                  placeholder='Default Input'
                  className='w-full bg-transparent rounded-md border border-stroke dark:border-dark-3 py-[10px] px-5 text-dark-6 outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-gray-2 disabled:border-gray-2'
                />
              </>
              <>
                <label className='mb-[10px] block text-base font-medium text-dark dark:text-white'>
                  Draft
                </label>
                <input
                  type='text'
                  placeholder='Default Input'
                  className='w-full bg-transparent rounded-md border border-stroke dark:border-dark-3 py-[10px] px-5 text-dark-6 outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-gray-2 disabled:border-gray-2'
                />
              </>
              <>
                <label className='mb-[10px] block text-base font-medium text-dark dark:text-white'>
                  Displacement
                </label>
                <input
                  type='text'
                  placeholder='Default Input'
                  className='w-full bg-transparent rounded-md border border-stroke dark:border-dark-3 py-[10px] px-5 text-dark-6 outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-gray-2 disabled:border-gray-2'
                />
              </>
              <>
                <label className='mb-[10px] block text-base font-medium text-dark dark:text-white'>
                  Power
                </label>
                <input
                  type='text'
                  placeholder='Default Input'
                  className='w-full bg-transparent rounded-md border border-stroke dark:border-dark-3 py-[10px] px-5 text-dark-6 outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-gray-2 disabled:border-gray-2'
                />
              </>
              <>
                <label className='mb-[10px] block text-base font-medium text-dark dark:text-white'>
                  Cargo Load
                </label>
                <input
                  type='text'
                  placeholder='Default Input'
                  className='w-full bg-transparent rounded-md border border-stroke dark:border-dark-3 py-[10px] px-5 text-dark-6 outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-gray-2 disabled:border-gray-2'
                />
              </>
              <>
                <label className='mb-[10px] block text-base font-medium text-dark dark:text-white'>
                  Service Speed
                </label>
                <input
                  type='text'
                  placeholder='Default Input'
                  className='w-full bg-transparent rounded-md border border-stroke dark:border-dark-3 py-[10px] px-5 text-dark-6 outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-gray-2 disabled:border-gray-2'
                />
              </>

            </div>
          </div>
        </div>
        <button onClick={() => { sendRust() }}>btn</button>
      </div>
    </>
  );
}

export default App;
