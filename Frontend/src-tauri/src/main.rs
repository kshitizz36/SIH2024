#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{Manager, Window, WindowBuilder, WindowUrl};
use serde::{Deserialize, Serialize};
use reqwest::blocking::Client;
use serde_json::to_string;
use urlencoding::encode;

#[derive(Serialize, Deserialize, Debug, Clone)]
struct Ship {
    shipType: String,
    Loa: f64,
    Draft: f64,
    Displ: f64,
    Power: f64,
    Load: f64,
    Speed: f64,
    Beam: f64,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
struct RequestData {
    start: (f64, f64),
    end: (f64, f64),
    ship: Ship,
}

#[derive(Serialize, Deserialize, Debug, Clone)]
struct ResponseData {
    path: Vec<(f64, f64)>,
    eta: f64,
    km: f64,
    fuel: f64,
}

fn open_new_window_with_query_params(window: Window, resp: ResponseData) {
    // Serialize the response data to JSON and then URL encode it
    let data_json = to_string(&resp).expect("Failed to serialize data");
    let encoded_data = urlencoding::encode(&data_json);

    // Create a new window with the serialized data in the query parameters
    let url = format!("map.html?data={}", encoded_data);

    let new_window = WindowBuilder::new(
        &window.app_handle(),
        "Map-Route",
        WindowUrl::App(url.into())
    )
    .title("Map")
    .inner_size(400.0, 300.0)
    .build()
    .expect("Failed to open new window");
}

#[tauri::command]
fn map(window: Window, data: RequestData) -> Result<(), String> {
    println!("{:?}", data);

    let client = Client::new();

    println!("Sending request to server...");

    let response = match client
        .post("http://127.0.0.1:5000/map")  // Update with your Flask server URL
        .json(&data)
        .send()
    {
        Ok(resp) => {
            println!("Request successful");
            resp
        },
        Err(err) => return Err(format!("Failed to send request: {}", err)),
    };

    println!("Request sent, waiting for response...");

    let response_data: ResponseData = match response.json() {
        Ok(data) => data,
        Err(err) => return Err(format!("Failed to parse response: {}", err)),
    };

    println!("{:?}", response_data);

    open_new_window_with_query_params(window, response_data);

    Ok(())
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![map])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
