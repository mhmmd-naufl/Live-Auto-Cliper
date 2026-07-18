import { useState, useEffect, useRef } from "react";

const API = "http://127.0.0.1:8000";

export default function ActionCenter({
  threshold,
  setThreshold,
  isMonitoring,
  obsConfig,
}) {
  const [activeThreshold, setActiveThreshold] = useState(threshold);
  const [activePersistence, setActivePersistence] = useState(1.0);
  const [activePreRoll, setActivePreRoll] = useState(10);

  const [localThreshold, setLocalThreshold] = useState(threshold.toString());
  const [thresholdError, setThresholdError] = useState("");

  const [localPersistence, setLocalPersistence] = useState("1.0");
  const [persistenceError, setPersistenceError] = useState("");

  const [localPreRoll, setLocalPreRoll] = useState("10");
  const [preRollError, setPreRollError] = useState("");

  const [folderPath, setFolderPath] = useState("");
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [browsingFolder, setBrowsingFolder] = useState(false);

  const messageTimeoutRef = useRef(null);

  useEffect(() => {
    return () => {
      if (messageTimeoutRef.current) clearTimeout(messageTimeoutRef.current);
    };
  }, []);

  // Load konfigurasi awal dari backend
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [statusRes, configRes] = await Promise.all([
          fetch(`${API}/obs/monitor/status`),
          fetch(`${API}/config`),
        ]);

        if (statusRes.ok) {
          const statusData = await statusRes.json();
          if (typeof statusData.persistence_duration === "number") {
            setActivePersistence(statusData.persistence_duration);
            setLocalPersistence(statusData.persistence_duration.toString());
          }
          if (typeof statusData.pre_roll === "number") {
            setActivePreRoll(statusData.pre_roll);
            setLocalPreRoll(statusData.pre_roll.toString());
          }
        }

        if (configRes.ok) {
          const configData = await configRes.json();
          if (configData.file_path) setFolderPath(configData.file_path);
          if (typeof configData.threshold_db === "number") {
            setActiveThreshold(configData.threshold_db);
            setLocalThreshold(configData.threshold_db.toString());
            setThreshold(configData.threshold_db);
          }
        }
      } catch (err) {
        console.error("Gagal memuat konfigurasi awal:", err);
      }
    };

    fetchInitialData();
  }, []);

  const handleBrowseFolder = async () => {
    setBrowsingFolder(true);
    try {
      const res = await fetch(`${API}/file-picker`);
      if (!res.ok) throw new Error("Gagal mengakses file picker backend");
      const data = await res.json();
      if (data.success && data.path) setFolderPath(data.path);
    } catch (err) {
      console.error("File picker error:", err);
      setMessage("❌ Gagal membuka browser folder");
    } finally {
      setBrowsingFolder(false);
    }
  };

  const handleSliderChange = (e) => {
    const val = Number(e.target.value);
    setLocalThreshold(val.toString());
    setThreshold(val);
    setThresholdError("");
  };

  const handleThresholdInput = (e) => {
    const raw = e.target.value;
    setLocalThreshold(raw);
    if (raw === "" || raw === "-") {
      setThresholdError("Nilai harus antara -60 dan 0 dBFS");
      return;
    }
    const val = Number(raw);
    if (!isNaN(val) && val >= -60 && val <= 0) {
      setThreshold(val);
      setThresholdError("");
    } else {
      setThresholdError("Nilai harus antara -60 dan 0 dBFS");
    }
  };

  const handlePersistenceInput = (e) => {
    const raw = e.target.value;
    setLocalPersistence(raw);
    const val = Number(raw);
    if (raw === "" || isNaN(val) || val <= 0) {
      setPersistenceError("Durasi harus berupa angka lebih dari 0 detik");
    } else {
      setPersistenceError("");
    }
  };

  const handlePreRollInput = (e) => {
    const raw = e.target.value;
    setLocalPreRoll(raw);
    const val = Number(raw);
    if (raw === "" || isNaN(val) || val < 0) {
      setPreRollError("Pre-roll tidak boleh negatif");
    } else {
      setPreRollError("");
    }
  };

  const handleSave = async () => {
    const tVal = Number(localThreshold);
    const pVal = Number(localPersistence);
    const prVal = Number(localPreRoll);

    if (isNaN(tVal) || tVal < -60 || tVal > 0) {
      setThresholdError("Nilai harus antara -60 dan 0 dBFS");
      return;
    }
    if (isNaN(pVal) || pVal <= 0) {
      setPersistenceError("Durasi harus lebih dari 0 detik");
      return;
    }
    if (isNaN(prVal) || prVal < 0) {
      setPreRollError("Pre-roll tidak boleh negatif");
      return;
    }
    if (!folderPath.trim()) {
      setMessage("❌ Folder penyimpanan hasil tidak boleh kosong");
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
          threshold_db: tVal,
          file_path: folderPath,
          persistence_duration: pVal,
        }),
      });

      if (!res.ok) throw new Error("Gagal menyimpan konfigurasi ke database");

      const syncResponses = await Promise.all([
        fetch(`${API}/obs/monitor/threshold?value=${tVal}`, { method: "POST" }),
        fetch(`${API}/obs/monitor/persistence?value=${pVal}`, { method: "POST" }),
        fetch(`${API}/obs/monitor/preroll?value=${prVal}`, { method: "POST" }),
      ]);

      if (syncResponses.some((r) => !r.ok)) {
        throw new Error("Config tersimpan di DB, namun gagal diterapkan ke modul monitor");
      }

      setThreshold(tVal);
      setActiveThreshold(tVal);
      setActivePersistence(pVal);
      setActivePreRoll(prVal);
      setMessage("✅ Konfigurasi disimpan & diterapkan");

      if (messageTimeoutRef.current) clearTimeout(messageTimeoutRef.current);
      messageTimeoutRef.current = setTimeout(() => setMessage(""), 3000);
    } catch (err) {
      setMessage(`❌ ${err.message || "Gagal menghubungi backend"}`);
    } finally {
      setSaving(false);
    }
  };

  const sliderValue = isNaN(Number(localThreshold))
    ? activeThreshold
    : Math.max(-60, Math.min(0, Number(localThreshold)));

  const thresholdChanged = Number(localThreshold) !== activeThreshold;
  const persistenceChanged = Number(localPersistence) !== activePersistence;
  const preRollChanged = Number(localPreRoll) !== activePreRoll;

  return (
    <div className="bg-[#16171f] rounded-xl border border-[#2a2b35] p-4 h-full">
      <h3 className="text-sm font-bold tracking-wider text-white mb-4">
        Action Center
      </h3>

      <div className="flex flex-col gap-4">
        {/* Threshold Section */}
        <div>
          <div className="flex justify-between items-center mb-1">
            <label className="text-xs text-gray-400">
              Threshold Sensitivity
              {isMonitoring && (
                <span className="ml-2 text-yellow-500 text-[10px]">● kalibrasi aktif</span>
              )}
            </label>
            <div className="flex items-center gap-2">
              <span className="text-[10px] text-gray-500">Aktif:</span>
              <span className="text-yellow-400 font-bold text-xs">{activeThreshold} dBFS</span>
              {thresholdChanged && (
                <>
                  <span className="text-gray-600 text-xs">→</span>
                  <span className="text-[10px] text-gray-500">Preview:</span>
                  <span className="text-blue-400 font-bold text-xs">{localThreshold} dBFS</span>
                </>
              )}
            </div>
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
              type="text"
              value={localThreshold}
              onChange={handleThresholdInput}
              className={`w-20 bg-[#0e0f14] border rounded px-2 py-1.5 text-xs text-center focus:outline-none
                ${thresholdError
                  ? "border-red-500 text-red-400"
                  : thresholdChanged
                    ? "border-blue-500 text-blue-400"
                    : "border-[#2a2b35] text-white focus:border-yellow-500"
                }`}
            />
          </div>
          <div className="flex justify-between text-[10px] text-gray-600 mt-0.5">
            <span>-60 dBFS (sensitif)</span>
            <span>0 dBFS (tidak sensitif)</span>
          </div>
          {thresholdError && <p className="text-[10px] text-red-400 mt-1">⚠️ {thresholdError}</p>}
          {thresholdChanged && !thresholdError && (
            <p className="text-[10px] text-blue-400 mt-1">ℹ️ Belum disimpan — tekan SAVE untuk menerapkan</p>
          )}
        </div>

        {/* Persistence Duration Section */}
        <div>
          <div className="flex justify-between items-center mb-1">
            <label className="text-xs text-gray-400">Durasi Delay (Persistence)</label>
            <div className="flex items-center gap-2">
              <span className="text-[10px] text-gray-500">Aktif:</span>
              <span className="text-yellow-400 font-bold text-xs">{activePersistence}s</span>
              {persistenceChanged && (
                <>
                  <span className="text-gray-600 text-xs">→</span>
                  <span className="text-[10px] text-gray-500">Preview:</span>
                  <span className="text-blue-400 font-bold text-xs">{localPersistence}s</span>
                </>
              )}
            </div>
          </div>
          <div className="flex items-center gap-2">
            <input
              type="text"
              value={localPersistence}
              onChange={handlePersistenceInput}
              disabled={isMonitoring}
              className={`w-24 bg-[#0e0f14] border rounded px-2 py-1.5 text-sm disabled:opacity-50 focus:outline-none
                ${persistenceError
                  ? "border-red-500 text-red-400"
                  : persistenceChanged
                    ? "border-blue-500 text-blue-400"
                    : "border-[#2a2b35] text-white focus:border-yellow-500"
                }`}
            />
            <span className="text-xs text-gray-500">detik</span>
          </div>
          {persistenceError && <p className="text-[10px] text-red-400 mt-1">⚠️ {persistenceError}</p>}
          {persistenceChanged && !persistenceError && (
            <p className="text-[10px] text-blue-400 mt-1">ℹ️ Belum disimpan — tekan SAVE untuk menerapkan</p>
          )}
        </div>

        {/* Pre-roll Duration Section */}
        <div>
          <div className="flex justify-between items-center mb-1">
            <label className="text-xs text-gray-400">Durasi Pre-Roll</label>
            <div className="flex items-center gap-2">
              <span className="text-[10px] text-gray-500">Aktif:</span>
              <span className="text-yellow-400 font-bold text-xs">{activePreRoll}s</span>
              {preRollChanged && (
                <>
                  <span className="text-gray-600 text-xs">→</span>
                  <span className="text-[10px] text-gray-500">Preview:</span>
                  <span className="text-blue-400 font-bold text-xs">{localPreRoll}s</span>
                </>
              )}
            </div>
          </div>
          <div className="flex items-center gap-2">
            <input
              type="text"
              value={localPreRoll}
              onChange={handlePreRollInput}
              disabled={isMonitoring}
              className={`w-24 bg-[#0e0f14] border rounded px-2 py-1.5 text-sm disabled:opacity-50 focus:outline-none
                ${preRollError
                  ? "border-red-500 text-red-400"
                  : preRollChanged
                    ? "border-blue-500 text-blue-400"
                    : "border-[#2a2b35] text-white focus:border-yellow-500"
                }`}
            />
            <span className="text-xs text-gray-500">detik</span>
          </div>
          <p className="text-[10px] text-gray-600 mt-0.5">Konteks video sebelum momen highlight</p>
          {preRollError && <p className="text-[10px] text-red-400 mt-1">⚠️ {preRollError}</p>}
          {preRollChanged && !preRollError && (
            <p className="text-[10px] text-blue-400 mt-1">ℹ️ Belum disimpan — tekan SAVE untuk menerapkan</p>
          )}
        </div>

        {/* Folder Path Section */}
        <div>
          <label className="text-xs text-gray-400 block mb-1">Folder Hasil</label>
          <div className="flex gap-2">
            <input
              type="text"
              value={folderPath}
              onChange={(e) => setFolderPath(e.target.value)}
              disabled={isMonitoring}
              placeholder="Memuat folder penyimpanan..."
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
        </div>

        {/* Save Button */}
        <div className="flex items-center gap-3">
          <button
            onClick={handleSave}
            disabled={saving || !!thresholdError || !!persistenceError || !!preRollError}
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
            ⚠️ Persistence, pre-roll, dan folder hanya bisa diubah saat monitoring berhenti.
            Slider threshold bisa digeser untuk kalibrasi real-time.
          </p>
        )}
      </div>
    </div>
  );
}