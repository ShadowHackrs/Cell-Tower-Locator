# Cell-Tower-Locator
Cell Tower Locator is a sophisticated Python-based tool designed for mapping and analyzing cellular network infrastructure across the world. This tool empowers researchers, network engineers, and telecommunications professionals with powerful capabilities for cellular network analysis and visualization.

![Cell Tower Locator Screenshot]([images/screenshot.png](https://github.com/ShadowHackrs/Cell-Tower-Locator/blob/b92e26184005e302043cf27bb7369a5b967249ee/cell.PNG))

### 🌐 Follow Me
[![Website](https://img.shields.io/badge/Website-shadowhackr.com-blue)](https://www.shadowhackr.com)
[![Facebook](https://img.shields.io/badge/Facebook-Tareq.DJX-blue)](https://www.facebook.com/Tareq.DJX/)
[![Twitter](https://img.shields.io/badge/Twitter-ShadowHackrs-blue)](https://x.com/ShadowHackrs)
[![Instagram](https://img.shields.io/badge/Instagram-shadowhackr-purple)](https://www.instagram.com/shadowhackr)
[![YouTube](https://img.shields.io/badge/YouTube-ShadowHackers-red)](https://www.youtube.com/@ShadowHackers)

### Key Highlights
- 📍 Precise tower location mapping with coverage visualization
- 🌍 Support for 12 Arab countries and their major network operators
- 📊 Advanced signal strength and coverage analysis
- 🔄 Real-time data processing and visualization
- 🛡️ Privacy-focused and ethical usage guidelines

### Perfect For
- 📡 Network Engineers
- 🔬 Telecommunications Researchers
- 📊 Coverage Analysis Specialists
- 🏢 Telecom Companies
- 🎓 Academic Research

### Why Choose Cell Tower Locator?
- **Comprehensive Coverage**: Supports all major Arab telecom operators
- **User-Friendly**: Simple CLI interface with clear instructions
- **Accurate Analysis**: Advanced algorithms for precise location and coverage estimation
- **Modern Visualization**: Interactive maps with multiple viewing options
- **Flexible Usage**: Supports both single tower and batch processing
- **Regular Updates**: Maintained and updated regularly

Advanced cell tower mapping and analysis tool for the Arab world, supporting networks across 12 countries including Jordan, Saudi Arabia, UAE, Egypt, Iraq, Kuwait, Qatar, Bahrain, Oman, Lebanon, Syria, and Yemen.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

## 📋 Table of Contents
- [Features](#-features)
- [Supported Networks](#-supported-networks)
- [Installation](#-installation)
- [Usage](#-usage)
- [Examples](#-examples)
- [Advanced Features](#-advanced-features)
- [Customization](#-customization)
- [Contributing](#-contributing)
- [Support](#-support)

## ✨ Features

### 🗺️ Interactive Mapping
- Green-colored tower markers with coverage circles
- Multiple map styles (OpenStreetMap, Dark Mode, Terrain)
- Distance and area measurement tools
- Automatic nearby tower detection
- Signal strength heatmap visualization
- Custom tower markers and popups
- Layer control for different data views

### 📡 Network Analysis
- Comprehensive coverage analysis
- Signal strength estimation
- Frequency band detection
- Network type identification (2G/3G/4G/5G)
- Coverage radius calculation
- Interference analysis

### 🛠️ Advanced Tools
- User-friendly command-line interface
- Flexible data input (optional MCC-MNC)
- Batch tower processing
- Export capabilities
- Custom data visualization

## 🌐 Supported Networks

### Middle East
- **Jordan**
  - Zain JO (416-1)
  - Orange JO (416-77)
  - Umniah (416-3)

- **Saudi Arabia**
  - STC (420-1)
  - Mobily (420-3)
  - Zain SA (420-4)

- **UAE**
  - Etisalat (424-2)
  - Du (424-3)

### North Africa
- **Egypt**
  - Vodafone EG (602-2)
  - Orange EG (602-1)
  - Etisalat EG (602-3)
  - WE (602-4)

### Gulf Region
- **Kuwait**, **Qatar**, **Bahrain**, **Oman**
  - All major operators supported
  - Full 5G network coverage
  - Detailed frequency information

### Levant
- **Lebanon**, **Syria**, **Iraq**
  - Major operators included
  - Coverage maps
  - Network specifications

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ShadowHackrs/Cell-Tower-Locator
   cd cell-tower-locator
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Requirements
- Python 3.6+
- Required packages:
  ```
  folium>=0.12.0
  requests>=2.25.0
  rich>=10.0.0
  ```

## 💻 Usage

### Basic Usage
```bash
python cell_tower_locator.py
```

### Data Input Format

1. **Cell ID**
   - Unique identifier for the cell tower
   - Example: `1365506`
   - Required field

2. **LAC/TAC**
   - Location Area Code/Tracking Area Code
   - Example: `614`
   - Required field

3. **MCC-MNC** (Optional)
   - Mobile Country Code-Mobile Network Code
   - Example: `416-1` (Zain Jordan)
   - Press Enter to skip

### Example Session
```
Cell ID: 1365506
LAC/TAC: 614
MCC-MNC: 416-1

✅ Tower Location Found!
📍 Coordinates: 31.952200, 35.928400
📡 Type: 4G
📶 Frequency: 2100 MHz
🔋 Signal Strength: -75 dBm
```

## 🎯 Examples

### Single Tower Analysis
```python
# Example code for analyzing a single tower
tower = {
    "cid": 1365506,
    "lac": 614,
    "mcc": 416,
    "mnc": 1
}
```
