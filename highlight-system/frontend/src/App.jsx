import { useState, useEffect, useRef, useCallback } from "react";
import ConnectionPanel from "./components/ConnectionPanel.jsx";
import AudioChart from "./components/AudioChart.jsx";
import ActionCenter from "./components/ActionCenter.jsx";
import HighlightsLog from "./components/HighlightsLog.jsx";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [currentDbfs, setCurrentDbfs] = useState(-60);
  const [threshold, setThreshold] = useState(-38);
  const [sessionTime, setSessionTime] = useState(0);
  const [logs, setLogs] = useState([]);
  const sessionRef = useRef(null);
  const pollRef = useRef(null);

  // Saat aplikasi mulai, ambil konfigurasi dari backend supaya UI sinkron
  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${API}/config`);
        if (!res.ok) return;
        const cfg = await res.json();
        if (cfg && typeof cfg.threshold_db === 'number') {
          setThreshold(cfg.threshold_db);
        }
      } catch (e) {
        // silent fail
      }
    })();
  }, []);

  // Session timer
  useEffect(() => {
    if (isMonitoring) {
      sessionRef.current = setInterval(() => {
        setSessionTime((t) => t + 1);
      }, 1000);
    } else {
      clearInterval(sessionRef.current);
      setSessionTime(0);
    }
    return () => clearInterval(sessionRef.current);
  }, [isMonitoring]);

  // Poll dBFS dan logs saat monitoring aktif
  useEffect(() => {
    if (isMonitoring) {
      pollRef.current = setInterval(async () => {
        try {
          const [monRes, logRes] = await Promise.all([
            fetch(`${API}/obs/monitor/status`),
            fetch(`${API}/logs?limit=20`),
          ]);
          const monData = await monRes.json();
          const logData = await logRes.json();
          setCurrentDbfs(monData.current_dbfs ?? -60);
          setLogs(logData);
        } catch {
          // silent fail
        }
      }, 500);
    } else {
      clearInterval(pollRef.current);
    }
    return () => clearInterval(pollRef.current);
  }, [isMonitoring]);

  const formatTime = (s) => {
    const h = String(Math.floor(s / 3600)).padStart(2, "0");
    const m = String(Math.floor((s % 3600) / 60)).padStart(2, "0");
    const sec = String(s % 60).padStart(2, "0");
    return `${h}:${m}:${sec}`;
  };

  const handleStartStop = useCallback(async () => {
    if (!isMonitoring) {
      await fetch(`${API}/obs/monitor/start`, { method: "POST" });
      setIsMonitoring(true);
    } else {
      await fetch(`${API}/obs/monitor/stop`, { method: "POST" });
      setIsMonitoring(false);
      setCurrentDbfs(-60);
    }
  }, [isMonitoring]);

  return (
    <div className="min-h-screen bg-[#0e0f14] text-white font-mono p-4 flex flex-col gap-4">
      {/* Header */}
      <div className="flex items-center justify-between bg-[#16171f] rounded-xl px-5 py-3 border border-[#2a2b35]">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className={`w-2.5 h-2.5 rounded-full ${isConnected ? "bg-green-400 shadow-[0_0_6px_#4ade80]" : "bg-red-500"}`} />
            <span className="text-sm font-semibold tracking-wide">OBS Studio</span>
          </div>
          {isMonitoring && (
            <div className="text-sm text-gray-400">
              Session Time: <span className="text-yellow-400 font-bold">{formatTime(sessionTime)}</span>
            </div>
          )}
        </div>
        <button
          onClick={handleStartStop}
          disabled={!isConnected}
          className={`px-6 py-2 rounded-lg font-bold text-sm tracking-widest transition-all
            ${isConnected
              ? isMonitoring
                ? "bg-red-600 hover:bg-red-500 text-white"
                : "bg-green-500 hover:bg-green-400 text-black"
              : "bg-gray-700 text-gray-500 cursor-not-allowed"
            }`}
        >
          {isMonitoring ? "STOP" : "START"}
        </button>
      </div>

      {/* Main Content */}
      <div className="flex gap-4 flex-1">
        {/* Audio Chart — kiri besar */}
        <div className="flex-1">
          <AudioChart currentDbfs={currentDbfs} threshold={threshold} isMonitoring={isMonitoring} />
        </div>
        {/* Highlights Log — kanan */}
        <div className="w-72">
          <HighlightsLog logs={logs} />
        </div>
      </div>

      {/* Bottom Row */}
      <div className="flex gap-4">
        {/* Connection Panel */}
        <div className="w-80">
          <ConnectionPanel
            isConnected={isConnected}
            setIsConnected={setIsConnected}
          />
        </div>
        {/* Action Center */}
        <div className="flex-1">
          <ActionCenter
            threshold={threshold}
            setThreshold={setThreshold}
            isMonitoring={isMonitoring}
          />
        </div>
      </div>
    </div>
  );
}