import { useState } from "react";

const ConnectionPanel = () => {
  // State untuk menyimpan konfigurasi form
  const [config, setConfig] = useState({
    obs_host: "127.0.0.1",
    obs_port: "4455",
    obs_password: "Test123",
  });

  // State status koneksi & loading
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState("");

  // Handler untuk mendeteksi perubahan input form
  const handleChange = (e) => {
    const { name, value } = e.target;
    setConfig((prev) => ({ ...prev, [name]: value }));
  };

  // Fungsi Menghubungkan ke OBS (POST /connect)
  const handleConnect = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:8000/obs/connect", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          obs_host: config.obs_host,
          obs_port: parseInt(config.obs_port, 10),
          obs_password: config.obs_password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setIsConnected(true);
        setMessage("Berhasil terhubung ke OBS Studio!");
      } else {
        setMessage(`Gagal: ${data.detail || "Terjadi kesalahan"}`);
      }
    } catch {
      setMessage("Gagal menghubungi backend. Pastikan FastAPI sudah jalan.");
    } finally {
      setIsLoading(false);
    }
  };

  // Fungsi Memutuskan Koneksi (POST /disconnect)
  const handleDisconnect = async () => {
    setIsLoading(true);
    setMessage("");

    try {
      const response = await fetch("http://127.0.0.1:8000/obs/disconnect", {
        method: "POST",
      });

      if (response.ok) {
        setIsConnected(false);
        setMessage("Koneksi ke OBS berhasil diputus.");
      } else {
        setMessage("Gagal memutuskan koneksi.");
      }
    } catch {
      setMessage("Gagal menghubungi backend.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={styles.card}>
      <h2 style={styles.title}>Koneksi OBS Studio</h2>

      {/* Indikator Status */}
      <div style={styles.statusContainer}>
        <span>Status: </span>
        <span
          style={
            isConnected ? styles.statusConnected : styles.statusDisconnected
          }
        >
          {isConnected ? "● Terhubung" : "○ Terputus"}
        </span>
      </div>

      {/* Form Input */}
      <form onSubmit={handleConnect} style={styles.form}>
        <div style={styles.inputGroup}>
          <label style={styles.label}>OBS Host / IP</label>
          <input
            type="text"
            name="obs_host"
            value={config.obs_host}
            onChange={handleChange}
            disabled={isConnected || isLoading}
            style={styles.input}
            required
          />
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>OBS Port</label>
          <input
            type="number"
            name="obs_port"
            value={config.obs_port}
            onChange={handleChange}
            disabled={isConnected || isLoading}
            style={styles.input}
            required
          />
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>OBS Password</label>
          <input
            type="password"
            name="obs_password"
            value={config.obs_password}
            onChange={handleChange}
            disabled={isConnected || isLoading}
            style={styles.input}
            placeholder="Masukkan password websocket OBS"
          />
        </div>

        {/* Tombol Aksi */}
        {!isConnected ? (
          <button type="submit" disabled={isLoading} style={styles.btnConnect}>
            {isLoading ? "Menghubungkan..." : "Connect ke OBS"}
          </button>
        ) : (
          <button
            type="button"
            onClick={handleDisconnect}
            disabled={isLoading}
            style={styles.btnDisconnect}
          >
            {isLoading ? "Memutuskan..." : "Disconnect"}
          </button>
        )}
      </form>

      {/* Log Pesan */}
      {message && <p style={styles.message}>{message}</p>}
    </div>
  );
};

// CSS-in-JS Sederhana untuk Styling Dashboard
const styles = {
  card: {
    background: "#1e1e24",
    color: "#fff",
    padding: "24px",
    borderRadius: "8px",
    width: "350px",
    boxShadow: "0 4px 6px rgba(0,0,0,0.3)",
    fontFamily: "Arial, sans-serif",
    margin: "20px auto",
  },
  title: {
    margin: "0 0 16px 0",
    fontSize: "20px",
    borderBottom: "1px solid #333",
    paddingBottom: "8px",
  },
  statusContainer: { marginBottom: "20px", fontSize: "14px" },
  statusConnected: { color: "#4edf7a", fontWeight: "bold" },
  statusDisconnected: { color: "#ff4d4d", fontWeight: "bold" },
  form: { display: "flex", flexDirection: "column", gap: "12px" },
  inputGroup: { display: "flex", flexDirection: "column", gap: "4px" },
  label: { fontSize: "12px", color: "#aaa" },
  input: {
    padding: "8px",
    borderRadius: "4px",
    border: "1px solid #444",
    background: "#2a2a35",
    color: "#fff",
  },
  btnConnect: {
    padding: "10px",
    background: "#007bff",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    fontWeight: "bold",
  },
  btnDisconnect: {
    padding: "10px",
    background: "#dc3545",
    color: "#fff",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    fontWeight: "bold",
  },
  message: {
    marginTop: "12px",
    fontSize: "12px",
    textAlign: "center",
    color: "#ddd",
  },
};

export default ConnectionPanel;
