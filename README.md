# Smart-India-Hackathon-2024
Creovate's Submission for SIH'24 


## 📸 Application Screenshots
<div align="center">
  <img src="https://github.com/user-attachments/assets/895e3429-23f8-44f5-b8ff-564fec4cdb77" alt="Ship Routing Interface" width="600"/>
  <br/>
  <em>Main routing interface showing ship route optimization</em>
</div>
<br/>
<div align="center">
  <img src="https://github.com/user-attachments/assets/79aa259f-6404-4451-ab30-56aa6c110503" alt="Route Visualization" width="600"/>
  <br/>
  <em>Advanced route visualization with environmental data overlay</em>
</div>


# Ship Routing Optimization System

A full-stack Ship Routing Optimization System designed to enhance navigational accuracy and adaptive routing for maritime operations. This system leverages advanced algorithms and real-time environmental data to provide optimized ship routes, achieving significant improvements in travel efficiency and cost reduction.

## 🚢 Overview

This project addresses the critical challenge of optimizing ship routes by implementing a comprehensive solution that combines cutting-edge algorithms with real-time data integration. The system is particularly focused on the Indian Ocean region but is designed to be adaptable for global maritime operations.

## ✨ Key Features

- **🧭 Advanced Routing Algorithm**: Implements the Isochrone A* algorithm for optimal navigation paths considering time and environmental factors
- **📡 Real-time Data Integration**: Utilizes live environmental data (currents, waves, winds) for enhanced routing accuracy
- **🌊 Ocean Grid System**: Sophisticated maritime data processing system for accurate route calculations  
- **⚡ Efficiency Gains**: Achieved 13% improvement in travel efficiency through optimized route planning
- **💰 Cost Reduction**: Significantly reduces fuel consumption and operational costs
- **🖥️ Full-Stack Architecture**: Modern web-based interface with robust backend processing

## 🛠️ Technical Stack

### Backend
- **Python** - Core processing engine
- **Flask** - RESTful API framework
- **Pandas** - Data manipulation and analysis
- **Xarray** - GRIB data handling
- **GeoPandas** - Geospatial data processing

### Frontend
- **Tauri.js** - Desktop application framework
- **React** - User interface library
- **Vite.js** - Build tool and development server

### Data Formats
- **GRIB** - Weather and oceanographic data
- **Shapefiles** - Geographical boundaries and features
- **JSON** - Configuration and port data

## 🏗️ System Architecture

<img width="1194" alt="image" src="https://github.com/user-attachments/assets/e149b615-232d-4d94-bd27-5099fe280d61" />


```
┌─────────────────┐    HTTP/API    ┌──────────────────┐
│   Frontend      │◄──────────────►│    Backend       │
│   (Tauri.js)    │                │    (Flask)       │
│                 │                │                  │
│ • User Interface│                │ • Route Calc     │
│ • Visualization │                │ • Data Processing│
│ • Map Display   │                │ • API Endpoints  │
└─────────────────┘                └──────────────────┘
                                            │
                                            ▼
                                   ┌──────────────────┐
                                   │   Data Sources   │
                                   │                  │
                                   │ • GRIB Files     │
                                   │ • Shapefiles     │
                                   │ • Ship Data      │
                                   │ • Port Info      │
                                   └──────────────────┘
```

The system follows a client-server architecture where:

- **Frontend**: Provides user interface for voyage parameters input and route visualization
- **Backend**: Processes routing requests using the Isochrone A* algorithm and manages environmental data
- **Data Layer**: Handles various data types including real-time forecasts and geospatial information

## 🎯 Problem Statement

**Original Challenge**: Development of a versatile and fast algorithm for optimal ship routing

The shipping industry faces significant challenges in route optimization due to:
- Heavy reliance on fossil fuels and associated costs
- Need to balance multiple parameters (fuel efficiency, travel time, safety, comfort)
- Dynamic weather conditions requiring continuous route adaptation
- Lack of publicly available applications for Indian Ocean region

This system addresses these challenges by providing a comprehensive solution that optimizes voyage time and safety while considering fuel efficiency.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- Rust (for Tauri)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ship-routing-optimization.git
   cd ship-routing-optimization
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

1. **Start the Backend**
   ```bash
   cd backend
   python app.py
   ```

2. **Start the Frontend**
   ```bash
   cd frontend
   npm run tauri dev
   ```

## 📊 Data Sources

- **Environmental Data**: [INCOIS OSF Portal](https://incois.gov.in/portal/osf/osf.jsp) for surface currents and wave forecasts
- **Weather Data**: Surface wind forecasts provided by INCOIS
- **Additional Data**: Available through INCOIS collaboration

## 🎥 Resources

- [Visualizing the Optimal Ship Routing Problem](https://www.youtube.com/watch?v=ct9v-mQgYqE)
- [Further Insights into Ship Routing](https://www.youtube.com/watch?v=wCTdHRTWtNI)

## 🏢 Project Information

- **Organization**: Ministry of Earth Sciences
- **Department**: Indian National Center for Ocean Information Services (INCOIS)
- **Category**: Software
- **Theme**: Transportation & Logistics
- **Problem Statement ID**: 1658


## Acknowledgments

- Indian National Center for Ocean Information Services (INCOIS)
- Ministry of Earth Sciences, Government of India
- Contributors and the open-source community

---
