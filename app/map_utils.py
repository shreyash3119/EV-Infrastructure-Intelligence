"""
Map Utilities for EV Infrastructure Intelligence
Enhanced mapping with clustering and custom markers
"""

import folium
from folium import plugins
from typing import Tuple, Optional

def create_map(
    lat: float,
    lon: float,
    popup_content: str,
    marker_color: str = 'blue',
    zoom_start: int = 12
) -> folium.Map:
    """
    Create an interactive Folium map with custom marker
    
    Parameters:
    -----------
    lat : float
        Latitude coordinate
    lon : float
        Longitude coordinate
    popup_content : str
        HTML content for popup
    marker_color : str
        Color of the marker ('red', 'blue', 'green', 'orange')
    zoom_start : int
        Initial zoom level
    
    Returns:
    --------
    folium.Map
    """
    
    # Create base map
    m = folium.Map(
        location=[lat, lon],
        zoom_start=zoom_start,
        tiles='OpenStreetMap',
        control_scale=True
    )
    
    # Add tile layers
    folium.TileLayer('CartoDB positron', name='Light Map').add_to(m)
    folium.TileLayer('CartoDB dark_matter', name='Dark Map').add_to(m)
    
    # Styled popup
    styled_popup = f"""
    <div style="font-family: Arial, sans-serif; width: 300px; padding: 10px;">
        {popup_content}
    </div>
    """
    
    # Icon mapping
    icon_map = {
        'red': 'exclamation-triangle',
        'orange': 'exclamation-circle',
        'green': 'check-circle',
        'blue': 'info-circle'
    }
    
    icon = icon_map.get(marker_color, 'info-circle')
    
    # Add marker
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(styled_popup, max_width=350),
        tooltip="Click for details",
        icon=folium.Icon(color=marker_color, icon=icon, prefix='fa')
    ).add_to(m)
    
    # Add circle marker
    folium.CircleMarker(
        location=[lat, lon],
        radius=25,
        color=marker_color,
        fill=True,
        fillColor=marker_color,
        fillOpacity=0.2,
        popup=folium.Popup(styled_popup, max_width=350)
    ).add_to(m)
    
    # Add fullscreen button
    plugins.Fullscreen(
        position='topright',
        title='Fullscreen',
        title_cancel='Exit Fullscreen',
        force_separate_button=True
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    return m
