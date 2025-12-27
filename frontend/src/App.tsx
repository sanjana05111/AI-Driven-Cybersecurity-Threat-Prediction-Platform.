import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import FileAnalysis from './pages/Analysis';
import Streaming from './pages/Streaming';
import NetworkSecurity from './pages/Network';
import AttackMap from './pages/AttackMap';
import AIChat from './pages/AIChat';
import Analytics from './pages/Analytics';
import PCAPAnalysis from './pages/PCAPAnalysis';
import LiveMonitor from './pages/LiveMonitor';

function App() {
  return (
    <Router>
      <div className="flex min-h-screen bg-cyber-black animated-bg">
        <Sidebar />
        <main className="flex-1 h-screen overflow-y-auto overflow-x-hidden">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/analysis" element={<FileAnalysis />} />
            <Route path="/streaming" element={<Streaming />} />
            <Route path="/network" element={<NetworkSecurity />} />
            <Route path="/map" element={<AttackMap />} />
            <Route path="/ai" element={<AIChat />} />
            <Route path="/stats" element={<Analytics />} />
            <Route path="/pcap" element={<PCAPAnalysis />} />
            <Route path="/monitor" element={<LiveMonitor />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;