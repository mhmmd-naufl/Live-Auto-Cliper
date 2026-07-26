import { useState, useEffect } from "react";
import toast from "react-hot-toast";

const API = "http://127.0.0.1:8000";
const SESSION_KEY = "obs_session";

export default function ConnectionPanel({
  isConnected,
  setIsConnected,
  obsConfig,
  setObsConfig,
}) {
  const [localConfig, setLocalConfig] = useState(() => ({
    host: obsConfig?.obs_host || "127.0.0.1",
    port: String(obsConfig?.obs_port || 4455),
    password: obsConfig?.obs_password || "",
  }));
  const [isLoading, setIsLoading] = useState(false);

  // Auto-reconnect saat refresh jika ada session tersimpan
  useEffect(() => {
    const saved = sessionStorage.getItem(SESSION_KEY);
    if (!saved || isConnected) return;

    const session = JSON.parse(saved);
    setLocalConfig(session);

    (async () => {
      setIsLoading(true);
      try {
        const params = new URLSearchParams({
          host: session.host,
          port: session.port,
          password: session.password,
        });
        const res = await fetch(`${API}/obs/connect?${params}`, { method: "POST" });
        const data = await res.json();
        if (data.success) {
          setIsConnected(true);
          setObsConfig({
            obs_host: session.host,
            obs_port: Number(session.port),
            obs_password: session.password,
          });
          toast.success("Reconnect otomatis berhasil");
        } else {
          sessionStorage.removeItem(SESSION_KEY);
        }
      } catch {
        sessionStorage.removeItem(SESSION_KEY);
      } finally {
        setIsLoading(false);
      }
    })();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setLocalConfig((prev) => ({ ...prev, [name]: value }));
  };

  const handleConnect = async () => {
    setIsLoading(true);
    try {
      const params = new URLSearchParams({
        host: localConfig.host,
        port: localConfig.port,
        password: localConfig.password,
      });
      const res = await fetch(`${API}/obs/connect?${params}`, { method: "POST" });
      const data = await res.json();
      if (data.success) {
        setIsConnected(true);
        setObsConfig({
          obs_host: localConfig.host,
          obs_port: Number(localConfig.port),
          obs_password: localConfig.password,
        });
        sessionStorage.setItem(SESSION_KEY, JSON.stringify(localConfig));
        toast.success("Terhubung ke OBS Studio");
      } else {
        toast.error(data.message || "Gagal terhubung ke OBS Studio");
      }
    } catch {
      toast.error("Gagal menghubungi backend");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDisconnect = async () => {
    setIsLoading(true);
    try {
      await fetch(`${API}/obs/disconnect`, { method: "POST" });
      setIsConnected(false);
      sessionStorage.removeItem(SESSION_KEY);
      toast("Koneksi OBS diputus", { icon: "🔌" });
    } catch {
      toast.error("Gagal memutus koneksi");
    } finally {
      setIsLoading(false);
    }
  };

  const fields = [
    { label: "Host / IP Address", name: "host", type: "text" },
    { label: "Port", name: "port", type: "number" },
    { label: "Password", name: "password", type: "password" },
  ];

  return (
    <div className="bg-[#16171f] rounded-xl border border-[#2a2b35] p-4 h-full flex flex-col">
      <h3 className="text-sm font-bold tracking-wider text-white mb-4">
        OBS — WEBSOCKET
      </h3>

      <div className="flex flex-col gap-3 flex-1">
        {fields.map(({ label, name, type }) => (
          <div key={name} className="flex flex-col gap-1">
            <label className="text-xs text-gray-400">{label}</label>
            <input
              type={type}
              name={name}
              value={localConfig[name]}
              onChange={handleChange}
              disabled={isConnected || isLoading}
              className="w-full bg-[#0e0f14] border border-[#2a2b35] rounded px-2 py-1.5 text-sm text-white disabled:opacity-50 focus:outline-none focus:border-yellow-500"
            />
          </div>
        ))}

        {/* Status koneksi */}
        <div className="mt-2 pt-2 border-t border-[#2a2b35]">
          {isConnected ? (
            <span className="text-xs text-green-400 font-bold flex items-center gap-1">
              ● Terhubung ke OBS Studio
            </span>
          ) : (
            <span className="text-xs text-gray-500 flex items-center gap-1">
              ● Terputus
            </span>
          )}
        </div>

        {/* Connect/Disconnect button */}
        <div className="flex gap-2 pt-2">
          <button
            onClick={isConnected ? handleDisconnect : handleConnect}
            disabled={isLoading}
            className={`flex-1 px-5 py-2 rounded text-sm font-bold transition-colors disabled:opacity-50
              ${isConnected
                ? "bg-red-700 hover:bg-red-600 text-white"
                : "bg-blue-600 hover:bg-blue-500 text-white"
              }`}
          >
            {isLoading ? "Menghubungkan..." : isConnected ? "Disconnect" : "Connect"}
          </button>
        </div>
      </div>
    </div>
  );
}