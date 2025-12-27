import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  FileSearch,
  Activity,
  Network,
  Globe,
  MessageSquare,
  BarChart3,
  FileCode,
  ShieldAlert
} from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
    { icon: FileSearch, label: 'File Analysis', path: '/analysis' },
    { icon: Activity, label: 'Streaming', path: '/streaming' },
    { icon: Network, label: 'Network Security', path: '/network' },
    { icon: Globe, label: 'Attack Map', path: '/map' },
    { icon: MessageSquare, label: 'SIMBA AI', path: '/ai' },
    { icon: BarChart3, label: 'Analytics', path: '/stats' },
    { icon: FileCode, label: 'PCAP Analysis', path: '/pcap' },
    { icon: ShieldAlert, label: 'Live Monitor', path: '/monitor' },
  ];

  return (
    <aside className="w-64 h-screen glass-morphism sticky top-0 left-0 flex flex-col p-4 z-50">
      <div className="flex items-center gap-3 mb-10 px-2">
        <div className="w-10 h-10 bg-cyber-blue rounded-lg flex items-center justify-center shadow-neon-blue">
          <ShieldAlert className="text-cyber-black" />
        </div>
        <h1 className="text-xl font-bold tracking-tighter text-cyber-blue">CYBER<span className="text-white">SPY</span></h1>
      </div>

      <nav className="flex-1 space-y-2 overflow-y-auto scrollbar-hide">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 group ${isActive
                ? 'bg-cyber-blue/10 border border-cyber-blue/50 text-cyber-blue shadow-[0_0_15px_rgba(0,242,255,0.2)]'
                : 'text-gray-400 hover:bg-white/5 hover:text-white border border-transparent'
              }`
            }
          >
            <item.icon size={20} className="group-hover:scale-110 transition-transform" />
            <span className="font-medium">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="mt-auto p-4 glass-morphism rounded-2xl border-cyber-blue border-opacity-20">
        <div className="text-xs text-gray-500 mb-1">System Status</div>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-cyber-green rounded-full animate-pulse shadow-[0_0_8px_#00ff9f]"></div>
          <span className="text-sm font-mono text-cyber-green uppercase tracking-widest">Secure</span>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
