import { useState, useEffect, useRef, useCallback } from "react";
import ConnectionPanel from "./components/ConnectionPanel.jsx";
import AudioChart from "./components/AudioChart.jsx";
import ActionCenter from "./components/ActionCenter.jsx";
import HighlightsLog from "./components/HighlightsLog.jsx";

const API = "http://127.0.0.1:8000";
const INITIAL_LIMIT = 5;
const PAGE_SIZE = 5;

export default function App() {
  const [isConnected, setIsConnected] = useState(false);
  const [isMonitoring, setIsMonitoring] = useState(false);
  const [currentDbfs, setCurrentDbfs] = useState(-60);
  const [threshold, setThreshold] = useState(0);
  const [sessionTime, setSessionTime] = useState(0);
  const [logs, setLogs] = useState([]);
  const [logLimit, setLogLimit] = useState(INITIAL_LIMIT);
  const [hasMore, setHasMore] = useState(false);
  const [obsConfig, setObsConfig] = useState({
    obs_host: "127.0.0.1",
    obs_port: 4455,
    obs_password: "",
  });

  const sessionRef = useRef(null);
  const pollRef = useRef(null);

  useEffect(() => {
    (async () => {
      try {
        const [cfgRes, logsRes] = await Promise.all([
          fetch(`${API}/config`),
          fetch(`${API}/logs?limit=${INITIAL_LIMIT}`),
        ]);

        if (cfgRes.ok) {
          const cfg = await cfgRes.json();
          if (cfg) {
            if (typeof cfg.threshold_db === "number")
              setThreshold(cfg.threshold_db);
            setObsConfig({
              obs_host: cfg.obs_host || "127.0.0.1",
              obs_port: cfg.obs_port || 4455,
              obs_password: cfg.obs_password || "",
            });
          }
        }

        if (logsRes.ok) {
          const logData = await logsRes.json();
          setLogs(logData);
          setHasMore(logData.length === INITIAL_LIMIT);
        }
      } catch {
        /* silent */
      }
    })();
  }, []);

  const handleLoadMore = useCallback(async () => {
    const newLimit = logLimit + PAGE_SIZE;
    setLogLimit(newLimit);
    try {
      const res = await fetch(`${API}/logs?limit=${newLimit}`);
      if (res.ok) {
        const data = await res.json();
        setLogs(data);
        setHasMore(data.length === newLimit);
      }
    } catch {
      /* silent */
    }
  }, [logLimit]);

  useEffect(() => {
    if (isMonitoring) {
      sessionRef.current = setInterval(
        () => setSessionTime((t) => t + 1),
        1000,
      );
    }
    return () => {
      if (sessionRef.current) clearInterval(sessionRef.current);
      if (!isMonitoring) setSessionTime(0);
    };
  }, [isMonitoring]);

  useEffect(() => {
    if (isMonitoring) {
      pollRef.current = setInterval(async () => {
        try {
          const [monRes, logRes] = await Promise.all([
            fetch(`${API}/obs/monitor/status`),
            fetch(`${API}/logs?limit=${logLimit}`),
          ]);
          const monData = await monRes.json();
          const logData = await logRes.json();
          setCurrentDbfs(monData.current_dbfs ?? -60);
          setLogs(logData);
          setHasMore(logData.length === logLimit);
        } catch {
          /* silent */
        }
      }, 500);
    } else {
      clearInterval(pollRef.current);
    }
    return () => clearInterval(pollRef.current);
  }, [isMonitoring, logLimit]);

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

  const handleDeleteLog = async (id) => {
    if (!window.confirm("Apakah Anda yakin ingin menghapus log ini?")) return;
    try {
      const res = await fetch(`${API}/logs/${id}`, { method: "DELETE" });
      if (res.ok) {
        setLogs((prev) => prev.filter((log) => log.id !== id));
      } else {
        alert("Gagal menghapus log");
      }
    } catch {
      alert("Gagal menghubungi server");
    }
  };

  const handleClearAllLogs = async () => {
    if (
      !window.confirm(
        "Apakah Anda yakin ingin menghapus SEMUA log? Tindakan ini tidak dapat dibatalkan.",
      )
    )
      return;
    try {
      const res = await fetch(`${API}/logs/clear`, { method: "DELETE" });
      if (res.ok) {
        setLogs([]);
        setLogLimit(INITIAL_LIMIT);
        setHasMore(false);
      } else {
        alert("Gagal menghapus semua log");
      }
    } catch {
      alert("Gagal menghubungi server");
    }
  };

  return (
    <div className="min-h-screen overflow-y-auto bg-[#0e0f14] text-white font-sans p-4 flex flex-col items-center">
      <div className="w-full max-w-7xl flex flex-col gap-4">
        {/* Header */}
        <div className="flex items-center justify-between bg-[#16171f] rounded-xl px-5 py-3 border border-[#2a2b35]">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <span
                className={`w-2.5 h-2.5 rounded-full ${isConnected ? "bg-green-400 shadow-[0_0_6px_#4ade80]" : "bg-red-500"}`}
              />
              <span className="text-sm font-semibold tracking-wide">
                OBS Studio
              </span>
            </div>
            {isMonitoring && (
              <div className="text-sm text-gray-400">
                Session Time:{" "}
                <span className="text-yellow-400 font-bold">
                  {formatTime(sessionTime)}
                </span>
              </div>
            )}
          </div>
          <button
            onClick={handleStartStop}
            disabled={!isConnected}
            className={`px-6 py-2 rounded-lg font-bold text-sm tracking-widest transition-all
              ${
                isConnected
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
        <div className="flex gap-4" style={{ height: "260px" }}>
          <div className="flex-1">
            <AudioChart
              currentDbfs={currentDbfs}
              threshold={threshold}
              isMonitoring={isMonitoring}
            />
          </div>
          <div className="w-72">
            <HighlightsLog
              logs={logs}
              onDelete={handleDeleteLog}
              onClearAll={handleClearAllLogs}
              onLoadMore={handleLoadMore}
              hasMore={hasMore}
            />
          </div>
        </div>

        {/* Bottom Row */}
        <div className="flex gap-4">
          <div className="w-96">
            <ConnectionPanel
              isConnected={isConnected}
              setIsConnected={setIsConnected}
              obsConfig={obsConfig}
              setObsConfig={setObsConfig}
            />
          </div>
          <div className="flex-1">
            <ActionCenter
              threshold={threshold}
              setThreshold={setThreshold}
              isMonitoring={isMonitoring}
              obsConfig={obsConfig}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
