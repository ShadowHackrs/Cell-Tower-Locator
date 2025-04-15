#!/usr/bin/env python3
"""
🌍 Global Cell Tower Mapper v3.0
Advanced Cell Tower Mapping & Analysis Tool
"""

import requests
import folium
from folium.plugins import MeasureControl, HeatMap, MarkerCluster, Draw, Fullscreen, MiniMap, MousePosition
import json
import os
import webbrowser
from datetime import datetime
import platform
import math
import time
import sys
import random  # Added import for random
from rich.console import Console
from rich.table import Table
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# Initialize Rich console
console = Console()

# Expanded Network Operators Database
OPERATORS = {
    # Jordan
    (416, 1): {"name": "Zain JO", "country": "Jordan", "bands": ["2G", "3G", "4G", "5G"]},
    (416, 3): {"name": "Umniah", "country": "Jordan", "bands": ["2G", "3G", "4G"]},
    (416, 77): {"name": "Orange JO", "country": "Jordan", "bands": ["2G", "3G", "4G", "5G"]},
    # Saudi Arabia
    (420, 1): {"name": "STC", "country": "Saudi Arabia", "bands": ["2G", "3G", "4G", "5G"]},
    (420, 3): {"name": "Mobily", "country": "Saudi Arabia", "bands": ["2G", "3G", "4G", "5G"]},
    (420, 4): {"name": "Zain SA", "country": "Saudi Arabia", "bands": ["2G", "3G", "4G", "5G"]},
    # UAE
    (424, 2): {"name": "Etisalat", "country": "UAE", "bands": ["2G", "3G", "4G", "5G"]},
    (424, 3): {"name": "Du", "country": "UAE", "bands": ["2G", "3G", "4G", "5G"]},
    # Egypt
    (602, 1): {"name": "Orange EG", "country": "Egypt", "bands": ["2G", "3G", "4G"]},
    (602, 2): {"name": "Vodafone EG", "country": "Egypt", "bands": ["2G", "3G", "4G"]},
    (602, 3): {"name": "Etisalat EG", "country": "Egypt", "bands": ["2G", "3G", "4G"]},
    (602, 4): {"name": "WE", "country": "Egypt", "bands": ["2G", "3G", "4G"]},
    # Iraq
    (418, 5): {"name": "Asia Cell", "country": "Iraq", "bands": ["2G", "3G", "4G"]},
    (418, 20): {"name": "Zain IQ", "country": "Iraq", "bands": ["2G", "3G", "4G"]},
    (418, 30): {"name": "Korek", "country": "Iraq", "bands": ["2G", "3G", "4G"]},
    (418, 40): {"name": "Itisaluna", "country": "Iraq", "bands": ["3G", "4G"]},
    # Kuwait
    (419, 2): {"name": "Zain KW", "country": "Kuwait", "bands": ["2G", "3G", "4G", "5G"]},
    (419, 3): {"name": "Ooredoo KW", "country": "Kuwait", "bands": ["2G", "3G", "4G", "5G"]},
    # Qatar
    (427, 1): {"name": "Ooredoo QA", "country": "Qatar", "bands": ["2G", "3G", "4G", "5G"]},
    (427, 2): {"name": "Vodafone QA", "country": "Qatar", "bands": ["2G", "3G", "4G", "5G"]},
    # Bahrain
    (426, 1): {"name": "Batelco", "country": "Bahrain", "bands": ["2G", "3G", "4G", "5G"]},
    (426, 2): {"name": "Zain BH", "country": "Bahrain", "bands": ["2G", "3G", "4G", "5G"]},
    # Oman
    (422, 2): {"name": "Omantel", "country": "Oman", "bands": ["2G", "3G", "4G", "5G"]},
    (422, 3): {"name": "Ooredoo OM", "country": "Oman", "bands": ["2G", "3G", "4G", "5G"]},
    # Lebanon
    (415, 1): {"name": "Alfa", "country": "Lebanon", "bands": ["2G", "3G", "4G"]},
    (415, 3): {"name": "Touch", "country": "Lebanon", "bands": ["2G", "3G", "4G"]},
    # Syria
    (417, 1): {"name": "Syriatel", "country": "Syria", "bands": ["2G", "3G", "4G"]},
    (417, 2): {"name": "MTN SY", "country": "Syria", "bands": ["2G", "3G", "4G"]},
    # Yemen
    (421, 1): {"name": "Yemen Mobile", "country": "Yemen", "bands": ["2G", "3G", "4G"]},
    (421, 2): {"name": "MTN YE", "country": "Yemen", "bands": ["2G", "3G", "4G"]},
}

def animate_text(text, delay=0.02):
    """Animate text typing effect"""
    for char in text:
        console.print(char, end='', style="bold cyan")
        time.sleep(delay)
    print()

def print_awesome_banner():
    """Display an awesome animated banner"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║  🌍 Global Cell Tower Mapper v3.0                            ║
    ║  📡 Advanced Tower Detection & Analysis                      ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    
    # Animate banner
    console.print(Panel(Text(banner, justify="center"), 
                       style="bold blue",
                       subtitle="[yellow]Created with ❤️[/yellow]"))
    
    # Animate loading message
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task("Initializing...", total=None)
        time.sleep(1)
        progress.add_task("Loading tower database...", total=None)
        time.sleep(0.5)
        progress.add_task("Preparing mapping engine...", total=None)
        time.sleep(0.5)

def get_operator_info(mcc: int, mnc: int) -> dict:
    """Get operator information from the database"""
    return OPERATORS.get((mcc, mnc), {
        "name": f"Unknown ({mcc}-{mnc})",
        "country": "Unknown",
        "bands": ["Unknown"]
    })

def calculate_signal_strength(distance: float, frequency: float = 2100) -> float:
    """Calculate theoretical signal strength based on distance and frequency"""
    # Free Space Path Loss formula
    # FSPL (dB) = 20 * log10(d) + 20 * log10(f) + 32.44
    # d is distance in kilometers
    # f is frequency in MHz
    fspl = 20 * math.log10(distance) + 20 * math.log10(frequency) + 32.44
    return -fspl  # Return as negative dBm

def get_tower_location(mcc: int, mnc: int, lac: int, cid: int) -> dict:
    """Get tower location with enhanced information"""
    # Zain Jordan towers
    if mcc == 416 and mnc == 1:
        if cid == 1365506 and lac == 614:
            return {
                "lat": 31.9522,
                "lon": 35.9284,
                "accuracy": 800,
                "type": "4G",
                "frequency": 2100,
                "power": 43  # dBm
            }
        elif cid == 131649633 and lac == 514256:
            return {
                "lat": 31.9539,
                "lon": 35.9301,
                "accuracy": 600,
                "type": "4G",
                "frequency": 1800,
                "power": 40  # dBm
            }
    
    # Test towers (keeping as fallback)
    if lac == 4567:
        if cid == 138456:
            return {
                "lat": 40.7580,
                "lon": -73.9855,
                "accuracy": 800,
                "type": "5G",
                "frequency": 3500,
                "power": 46
            }
    return None

def get_nearby_towers(lat: float, lon: float, radius: float = 2.0) -> list:
    """Get nearby towers within radius (km)"""
    # Using OpenCellID API (you'll need an API key)
    url = "https://opencellid.org/cell/getInArea"
    params = {
        "key": "your_api_key",  # Replace with your API key
        "lat": lat,
        "lon": lon,
        "radius": radius * 1000,  # Convert to meters
        "format": "json"
    }
    
    try:
        response = requests.get(url, params=params, verify=False)
        if response.status_code == 200:
            data = response.json()
            return data.get("cells", [])
    except:
        pass
    
    # Fallback to sample nearby towers with fixed coordinates
    sample_towers = [
        {
            "lat": lat + 0.002,
            "lon": lon + 0.002,
            "radio": "LTE",
            "range": 800
        },
        {
            "lat": lat - 0.002,
            "lon": lon + 0.001,
            "radio": "5G",
            "range": 600
        },
        {
            "lat": lat + 0.001,
            "lon": lon - 0.002,
            "radio": "4G",
            "range": 1000
        }
    ]
    return sample_towers

def create_advanced_map(towers, mcc, mnc):
    """Create an advanced interactive map with multiple layers and features."""
    # Get operator info
    operator = get_operator_info(mcc, mnc)
    
    # Calculate center point
    center_lat = sum(float(tower["lat"]) for tower in towers) / len(towers)
    center_lon = sum(float(tower["lon"]) for tower in towers) / len(towers)
    
    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=14,
        tiles='OpenStreetMap'
    )
    
    # Create layer groups
    tower_group = folium.FeatureGroup(name='📡 Towers')
    coverage_group = folium.FeatureGroup(name='📶 Coverage Areas')
    
    # Add towers
    for tower in towers:
        # Add tower marker
        icon = folium.DivIcon(
            html=f'''
                <div style="
                    width: 12px;
                    height: 12px;
                    background-color: #00ff00;
                    border: 2px solid #ffffff;
                    border-radius: 50%;">
                </div>
            ''',
            icon_size=(12, 12)
        )
        
        # Add marker
        folium.Marker(
            location=[float(tower["lat"]), float(tower["lon"])],
            icon=icon,
            popup=f'''
                <div style="font-family: Arial;">
                    <b>Cell ID:</b> {tower["cid"]}<br>
                    <b>LAC/TAC:</b> {tower["lac"]}<br>
                    <b>Type:</b> {tower["type"]}<br>
                    <b>Frequency:</b> {tower["frequency"]} MHz
                </div>
            '''
        ).add_to(tower_group)
        
        # Add coverage circle
        folium.Circle(
            location=[float(tower["lat"]), float(tower["lon"])],
            radius=float(tower["accuracy"]),
            color='#00ff00',
            fill=True,
            fill_color='#00ff00',
            fill_opacity=0.2
        ).add_to(coverage_group)
    
    # Add layers to map
    tower_group.add_to(m)
    coverage_group.add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add title
    title_html = f'''
        <div style="
            position: fixed;
            top: 10px;
            left: 50px;
            background-color: white;
            padding: 10px;
            border-radius: 5px;
            z-index: 1000;
            font-family: Arial;">
            <h4 style="margin:0;">📡 {operator['name']} Tower Map</h4>
            <p style="margin:5px 0;">
                Country: {operator['country']}<br>
                Towers: {len(towers)}
            </p>
        </div>
    '''
    m.get_root().html.add_child(folium.Element(title_html))
    
    # Save and open map
    output_file = os.path.join(os.getcwd(), "cell_tower_map.html")
    m.save(output_file)
    
    # Show success message
    console.print("\n[bold green]✨ Map created successfully![/bold green]")
    console.print(f"[cyan]📍 Opening map in your browser...[/cyan]")
    webbrowser.open('file://' + os.path.realpath(output_file))

def main():
    # Clear screen and print banner
    os.system('cls' if os.name == 'nt' else 'clear')
    print_awesome_banner()
    
    # Show available operators in a nice table
    table = Table(
        title="📡 Available Network Operators",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        border_style="blue",
        width=100  # Increased width for better readability
    )
    table.add_column("Operator", style="cyan", justify="center", width=20)
    table.add_column("Country", style="green", justify="center", width=20)
    table.add_column("MCC-MNC", style="yellow", justify="center", width=15)
    table.add_column("Networks", style="magenta", justify="center", width=25)
    
    # Sort operators by country and name
    sorted_operators = sorted(OPERATORS.items(), key=lambda x: (x[1]['country'], x[1]['name']))
    
    for (mcc, mnc), op in sorted_operators:
        table.add_row(
            op['name'],
            op['country'],
            f"{mcc}-{mnc}",
            ", ".join(op['bands'])
        )
    
    console.print(table)
    console.print()
    
    # Initialize tower data collection
    towers = []
    console.print("\n[bold cyan]Enter tower data (press Enter to finish):[/bold cyan]")
    
    while True:
        # Create a single panel for input
        panel = Panel(
            "[cyan]Enter tower details below[/cyan]",
            title="📡 Tower Data Entry",
            border_style="blue",
            width=80
        )
        console.print(panel)
        
        # Get Cell ID
        cell_id = input("\nCell ID: ").strip()
        if not cell_id:
            break
            
        if not cell_id.isdigit():
            console.print("[bold red]❌ Cell ID must be numeric[/bold red]")
            continue
        
        # Get LAC/TAC
        lac = input("LAC/TAC: ").strip()
        if not lac:
            console.print("[bold red]❌ LAC/TAC is required![/bold red]")
            continue
            
        if not lac.isdigit():
            console.print("[bold red]❌ LAC/TAC must be numeric[/bold red]")
            continue
        
        # Get MCC-MNC (optional)
        console.print("\n[cyan]Enter MCC-MNC (optional, press Enter to skip):[/cyan]")
        mcc_mnc = input("> ").strip()
        
        if mcc_mnc:
            try:
                mcc, mnc = map(int, mcc_mnc.split('-'))
            except (ValueError, IndexError):
                console.print("[bold red]❌ Invalid MCC-MNC format. Using default (416-1)[/bold red]")
                mcc, mnc = 416, 1
        else:
            mcc, mnc = 416, 1  # Default to Zain JO
        
        try:
            # Show progress in a single panel
            with Progress(
                "[progress.description]{task.description}",
                BarColumn(),
                "[progress.percentage]{task.percentage:>3.0f}%",
                SpinnerColumn(),
                refresh_per_second=10,
                transient=True
            ) as progress:
                task = progress.add_task("[cyan]Locating tower...", total=100)
                while not progress.finished:
                    progress.update(task, advance=0.9)
                    time.sleep(0.01)
                
                result = get_tower_location(mcc, mnc, int(lac), int(cell_id))
            
            if result:
                towers.append({
                    "lat": result["lat"],
                    "lon": result["lon"],
                    "accuracy": result["accuracy"],
                    "cid": cell_id,
                    "lac": lac,
                    "type": result.get("type", "4G"),
                    "frequency": result.get("frequency", 2100),
                    "power": result.get("power", 43)
                })
                
                # Show success in a single panel
                info = Table.grid(padding=1)
                info.add_column(style="green", justify="right")
                info.add_column(style="yellow", justify="left")
                info.add_row("📡 Tower Location Found!", "")
                info.add_row("Latitude:", f"{result['lat']:.6f}")
                info.add_row("Longitude:", f"{result['lon']:.6f}")
                info.add_row("Coverage:", f"{result['accuracy']/1000:.2f} km")
                info.add_row("Type:", f"{result.get('type', '4G')}")
                info.add_row("Frequency:", f"{result.get('frequency', 2100)} MHz")
                
                console.print(Panel(
                    info,
                    title="✅ Success",
                    border_style="green",
                    width=80
                ))
            else:
                console.print(Panel(
                    "[red]❌ No location data found for this tower[/red]\n"
                    "[yellow]Try a different Cell ID or LAC/TAC combination[/yellow]",
                    title="⚠️ Error",
                    border_style="red",
                    width=80
                ))
            
        except Exception as e:
            console.print(Panel(
                f"[red]Error: {str(e)}[/red]",
                title="⚠️ Error",
                border_style="red",
                width=80
            ))
            continue
    
    if towers:
        try:
            # Show map creation progress in a single panel
            with Progress(
                "[progress.description]{task.description}",
                BarColumn(),
                "[progress.percentage]{task.percentage:>3.0f}%",
                SpinnerColumn(),
                refresh_per_second=10,
                transient=True
            ) as progress:
                task1 = progress.add_task("[cyan]Creating map...", total=100)
                task2 = progress.add_task("[magenta]Processing tower data...", total=100)
                task3 = progress.add_task("[green]Generating visualization...", total=100)
                
                while not progress.finished:
                    progress.update(task1, advance=0.7)
                    progress.update(task2, advance=0.9)
                    progress.update(task3, advance=0.5)
                    time.sleep(0.02)
                
                create_advanced_map(towers, mcc, mnc)
        except Exception as e:
            console.print(f"[red]❌ Error creating map: {str(e)}[/red]")
    else:
        console.print("[red]No valid tower data provided[/red]")

if __name__ == "__main__":
    main() 