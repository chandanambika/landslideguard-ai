import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, useMap } from 'react-leaflet';
import L from 'leaflet';
import { MapPin, Info } from 'lucide-react';

// Fix for default Leaflet marker icon in React
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

function MapRecenter({ lat, lon }) {
  const map = useMap();
  useEffect(() => {
    map.setView([lat, lon], 11, { animate: true });
  }, [lat, lon, map]);
  return null;
}

export default function LandslideMap({
  latitude = 20.0,
  longitude = 80.0,
  regionName = 'Monitored Sector',
  riskCategory = 'LOW',
  riskScore = 0
}) {
  const lat = Number(latitude) || 20.0;
  const lon = Number(longitude) || 80.0;

  const getRiskColor = (cat) => {
    switch (cat?.toUpperCase()) {
      case 'CRITICAL':
        return '#EF4444';
      case 'HIGH':
        return '#F97316';
      case 'MODERATE':
        return '#F59E0B';
      default:
        return '#10B981';
    }
  };

  const riskColor = getRiskColor(riskCategory);

  return (
    <div className="glass-panel p-4 rounded-xl border border-slate-800 shadow-md flex flex-col h-full">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <MapPin className="w-4 h-4 text-rose-400" />
          Spatial Risk Zone Map (Leaflet)
        </h3>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
          Simulated Coordinates
        </span>
      </div>

      <div className="flex-1 w-full min-h-[300px] rounded-lg overflow-hidden border border-slate-800 relative z-0">
        <MapContainer
          center={[lat, lon]}
          zoom={11}
          scrollWheelZoom={false}
          className="w-full h-full"
        >
          {/* OpenStreetMap Base Tile Layer */}
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <MapRecenter lat={lat} lon={lon} />

          {/* Location Marker */}
          <Marker position={[lat, lon]}>
            <Popup>
              <div className="text-xs font-sans text-slate-900 p-1">
                <strong className="block text-sm">{regionName}</strong>
                <span>Coordinates: {lat.toFixed(4)}, {lon.toFixed(4)}</span><br />
                <span>Risk Category: <strong>{riskCategory}</strong></span><br />
                <span>Risk Score: <strong>{riskScore}/100</strong></span>
              </div>
            </Popup>
          </Marker>

          {/* Risk Perimeter Buffer Circle */}
          <Circle
            center={[lat, lon]}
            radius={2500}
            pathOptions={{
              color: riskColor,
              fillColor: riskColor,
              fillOpacity: 0.28,
              weight: 2,
            }}
          />
        </MapContainer>
      </div>

      <p className="text-[11px] text-slate-400 mt-2 flex items-center gap-1">
        <Info className="w-3.5 h-3.5 text-slate-400 shrink-0" />
        Geospatial marker represents simulated coordinate centroid. Not a certified hazard demarcation map.
      </p>
    </div>
  );
}
