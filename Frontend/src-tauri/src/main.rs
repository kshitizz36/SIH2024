#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{Manager, Window, WindowBuilder, WindowUrl};
use serde::{Deserialize, Serialize};
use reqwest::blocking::Client;
use serde_json::to_string;
use urlencoding::encode;

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
