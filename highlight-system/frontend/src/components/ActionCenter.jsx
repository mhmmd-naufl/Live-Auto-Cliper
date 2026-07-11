import { useState } from "react";

const API = "http://127.0.0.1:8000";

export default function ActionCenter({ threshold, setThreshold, isMonitoring, obsConfig }) {
  const [localThreshold, setLocalThreshold] = useState(threshold);
  const [thresholdError, setThresholdError] = useState("");
  const [persistence, setPersistence] = useState(1.0);
  const [folderPath, setFolderPath] = useState("D:\\Kuliah\\TA\\Pre-TA\\Project\\file-highlight");
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [browsingFolder, setBrowsingFolder] = useState(false);

  const handleBrowseFolder = async () => {
    setBrowsingFolder(true);
    try {
      const res = await fetch(`${API}/file-picker`);
      const data = await res.json();
      if (data.success && data.path) setFolderPath(data.path);
    } catch (err) {
      console.error("File picker error:", err);
    } finally {
      setBrowsingFolder(false);
    }
  };

  const handleSliderChange = (e) => {
    const val = Number(e.target.value);
    setLocalThreshold(val);
    setThreshold(val);
    setThresholdError("");
  };

  const handleThresholdInput = (e) => {
    const raw = e.target.value;
    setLocalThreshold(raw);
    const val = Number(raw);
    if (raw === "" || raw === "-") {
      setThresholdError("Nilai harus antara -60 dan 0 dBFS");
      return;
    }
    if (!isNaN(val) && val >= -60 && val <= 0) {
      setThreshold(val);
      setThresholdError("");
    } else {
      setThresholdError("Nilai harus antara -60 dan 0 dBFS");
    }
  };

  const handleSave = async () => {
    const val = Number(localThreshold);
    if (isNaN(val) || val < -60 || val > 0) {
      setThresholdError("Nilai harus antara -60 dan 0 dBFS");
      return;
    }
    if (isNaN(persistence) || persistence <= 0) {
      setMessage("❌ Durasi delay harus lebih dari 0");
      return;
    }

    setSaving(true);
    setMessage("");

    try {
      const res = await fetch(`${API}/config`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          obs_host: obsConfig?.obs_host || "127.0.0.1",
          obs_port: obsConfig?.obs_port || 4455,
          obs_password: obsConfig?.obs_password || "",
          threshold_db: val,
          file_path: folderPath,
          persistence_duration: persistence,
        }),
      });

      const data = await res.json();

      if (res.ok) {
        await fetch(`${API}/obs/monitor/threshold?value=${val}`, { method: "POST" });
        await fetch(`${API}/obs/monitor/persistence?value=${persistence}`, { method: "POST" });
        setThreshold(val);
        setMessage("✅ Konfigurasi disimpan");
      } else {
        setMessage(`❌ Gagal: ${data.detail || "error"}`);
      }
      setTimeout(() => setMessage(""), 3000);
    } catch {
      setMessage("❌ Gagal menghubungi backend");
    } finally {
      setSaving(false);
    }
  };

  const sliderValue = isNaN(Number(localThreshold))
    ? -38
    : Math.max(-60, Math.min(0, Number(localThreshold)));

  return (
    <div className="bg-[#16171f] rounded-xl border border-[#2a2b35] p-4 h-full">
      <h3 className="text-sm font-bold tracking-wider text-white mb-4">Action Center</h3>

      <div className="flex flex-col gap-4">
        {/* Threshold — slider + input angka */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <label className="text-xs text-gray-400">
              Threshold Sensitivity
              {isMonitoring && (
                <span className="ml-2 text-yellow-500 text-[10px]">● kalibrasi aktif</span>
              )}
            </label>
            <span className="text-yellow-400 font-bold text-sm">{sliderValue} dBFS</span>
          </div>
          <div className="flex gap-2 items-center">
            <input
              type="range"
              min={-60}
              max={0}
              step={1}
              value={sliderValue}
              onChange={handleSliderChange}
              className="flex-1 accent-yellow-400 cursor-pointer"
            />
            <input
              type="number"
              min={-60}
              max={0}
              step={1}
              value={localThreshold}
              onChange={handleThresholdInput}
              className={`w-20 bg-[#0e0f14] border rounded px-2 py-1.5 text-xs text-center focus:outline-none
                ${thresholdError
                  ? "border-red-500 text-red-400"
                  : "border-[#2a2b35] text-white focus:border-yellow-500"
                }`}
            />
          </div>
          <div className="flex justify-between text-[10px] text-gray-600 mt-0.5">
            <span>-60 dBFS (sensitif)</span>
            <span>0 dBFS (tidak sensitif)</span>
          </div>
          {thresholdError && (
            <p className="text-[10px] text-red-400 mt-1">⚠️ {thresholdError}</p>
          )}
        </div>

        {/* Persistence Duration */}
        <div>
          <label className="text-xs text-gray-400 block mb-1">Durasi Delay (Persistence)</label>
          <div className="flex items-center gap-2">
            <input
              type="number"
              value={persistence}
              onChange={(e) => setPersistence(Number(e.target.value))}
              disabled={isMonitoring}
              min={0.1}
              step={0.1}
              className="w-24 bg-[#0e0f14] border border-[#2a2b35] rounded px-2 py-1.5 text-sm text-white disabled:opacity-50 focus:outline-none focus:border-yellow-500"
            />
            <span className="text-xs text-gray-500">detik</span>
          </div>
        </div>

        {/* Folder Path */}
        <div>
          <label className="text-xs text-gray-400 block mb-1">Folder Hasil</label>
          <div className="flex gap-2">
            <input
              type="text"
              value={folderPath}
              onChange={(e) => setFolderPath(e.target.value)}
              disabled={isMonitoring}
              placeholder="Contoh: D:\Kuliah\TA\file-highlight"
              className="flex-1 bg-[#0e0f14] border border-[#2a2b35] rounded px-2 py-1.5 text-xs text-white disabled:opacity-50 focus:outline-none focus:border-yellow-500"
            />
            <button
              type="button"
              onClick={handleBrowseFolder}
              disabled={isMonitoring || browsingFolder}
              className="px-3 py-1.5 bg-[#2a2b35] hover:bg-[#3a3b45] rounded text-xs disabled:opacity-50 transition-colors"
            >
              {browsingFolder ? "..." : "Browse"}
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-1">
            ℹ️ Ketik path folder atau klik Browse untuk memilih
          </p>
        </div>

        {/* Save Button */}
        <div className="flex items-center gap-3">
          <button
            onClick={handleSave}
            disabled={saving || !!thresholdError}
            className="px-6 py-2 bg-yellow-500 hover:bg-yellow-400 text-black font-bold text-sm rounded disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {saving ? "Menyimpan..." : "SAVE"}
          </button>
          {message && (
            <span className={`text-xs ${message.startsWith("✅") ? "text-green-400" : "text-red-400"}`}>
              {message}
            </span>
          )}
        </div>

        {isMonitoring && (
          <p className="text-xs text-gray-500 border-t border-[#2a2b35] pt-2">
            ⚠️ Persistence dan folder hanya bisa diubah saat monitoring berhenti.
            Slider threshold bisa digeser untuk kalibrasi real-time.
          </p>
        )}
      </div>
    </div>
  );
}