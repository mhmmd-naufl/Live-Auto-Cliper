import { useState } from "react";

function ConfirmModal({ isOpen, title, message, onConfirm, onCancel, confirmLabel = "Hapus", danger = true }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onCancel}
      />
      {/* Modal */}
      <div className="relative bg-[#1a1b24] border border-[#2a2b35] rounded-xl p-5 w-72 shadow-2xl">
        {/* Icon */}
        <div className={`w-10 h-10 rounded-full flex items-center justify-center mx-auto mb-3 ${danger ? "bg-red-900/40" : "bg-yellow-900/40"}`}>
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke={danger ? "#f87171" : "#facc15"} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          </svg>
        </div>

        {/* Title */}
        <h3 className="text-sm font-bold text-white text-center mb-1">{title}</h3>

        {/* Message */}
        <p className="text-xs text-gray-400 text-center mb-4">{message}</p>

        {/* Buttons */}
        <div className="flex gap-2">
          <button
            onClick={onCancel}
            className="flex-1 px-3 py-2 rounded-lg text-xs font-semibold bg-[#2a2b35] hover:bg-[#3a3b45] text-gray-300 transition-colors"
          >
            Batal
          </button>
          <button
            onClick={onConfirm}
            className={`flex-1 px-3 py-2 rounded-lg text-xs font-bold transition-colors ${
              danger
                ? "bg-red-600 hover:bg-red-500 text-white"
                : "bg-yellow-500 hover:bg-yellow-400 text-black"
            }`}
          >
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}

export default function HighlightsLog({ logs, onDelete, onClearAll, onLoadMore, hasMore }) {
  const [deleteTarget, setDeleteTarget] = useState(null); // id log yang mau dihapus
  const [showClearAll, setShowClearAll] = useState(false);

  const visibleLogs = Array.isArray(logs) ? logs : [];

  const handleConfirmDelete = () => {
    onDelete(deleteTarget);
    setDeleteTarget(null);
  };

  const handleConfirmClearAll = () => {
    onClearAll();
    setShowClearAll(false);
  };

  return (
    <>
      <ConfirmModal
        isOpen={deleteTarget !== null}
        title="Hapus Log"
        message="Log ini akan dihapus secara permanen. Tindakan ini tidak dapat dibatalkan."
        confirmLabel="Hapus"
        danger={true}
        onConfirm={handleConfirmDelete}
        onCancel={() => setDeleteTarget(null)}
      />

      <ConfirmModal
        isOpen={showClearAll}
        title="Hapus Semua Log"
        message="Seluruh riwayat highlight akan dihapus permanen. Tindakan ini tidak dapat dibatalkan."
        confirmLabel="Hapus Semua"
        danger={true}
        onConfirm={handleConfirmClearAll}
        onCancel={() => setShowClearAll(false)}
      />

      <div className="bg-[#16171f] rounded-xl border border-[#2a2b35] p-4 h-full flex flex-col">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-bold tracking-wider text-white">History</h3>
          {visibleLogs.length > 0 && (
            <button
              onClick={() => setShowClearAll(true)}
              className="text-xs text-red-400 hover:text-red-300 font-semibold cursor-pointer transition-colors"
            >
              Hapus Semua
            </button>
          )}
        </div>

        <div
          className="flex-1 overflow-y-auto flex flex-col gap-1.5 pr-1"
          style={{ scrollbarWidth: "thin", scrollbarColor: "#2a2b35 transparent" }}
        >
          {visibleLogs.length === 0 ? (
            <div className="text-center text-gray-600 text-xs mt-8">
              Belum ada highlight yang direkam
            </div>
          ) : (
            <>
              {visibleLogs.map((log) => (
                <LogItem
                  key={log.id}
                  log={log}
                  onDelete={(id) => setDeleteTarget(id)}
                />
              ))}
              {hasMore ? (
                <button
                  onClick={onLoadMore}
                  className="py-2 w-full text-center text-xs text-gray-500 hover:text-gray-300 cursor-pointer transition-colors"
                >
                  ↓ Muat 5 log berikutnya
                </button>
              ) : (
                <div className="py-1 text-center text-xs text-gray-700">
                  — Semua log ditampilkan —
                </div>
              )}
            </>
          )}
        </div>

        {visibleLogs.length > 0 && (
          <div className="mt-2 pt-2 border-t border-[#2a2b35] text-xs text-gray-600 flex justify-between items-center">
            <span>Total: {visibleLogs.length} highlight</span>
            <span>{visibleLogs.filter((l) => l.status === "SUCCESS").length} sukses</span>
          </div>
        )}
      </div>
    </>
  );
}

function LogItem({ log, onDelete }) {
  const time = new Date(log.timestamp).toLocaleTimeString("id-ID", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });

  const isSuccess = log.status === "SUCCESS";

  return (
    <div className={`rounded px-2 py-1.5 text-[11px] border-l-2 shrink-0 ${
      isSuccess ? "border-green-500 bg-green-950/30" : "border-red-500 bg-red-950/30"
    }`}>
      <div className="flex items-center justify-between gap-1">
        <span className="text-gray-400">{time}</span>
        <div className="flex items-center gap-1.5">
          <span className={`font-bold ${isSuccess ? "text-green-400" : "text-red-400"}`}>
            [{log.status}]
          </span>
          <button
            onClick={() => onDelete(log.id)}
            className="text-gray-500 hover:text-red-400 cursor-pointer transition-colors p-0.5"
            title="Hapus log"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="3 6 5 6 21 6"></polyline>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
            </svg>
          </button>
        </div>
      </div>
      <div className="truncate mt-0.5">
        {isSuccess ? (
          <span className="text-gray-300">{log.filename || "-"}</span>
        ) : (
          <span className="text-red-400" title={log.error_message || "Unknown error"}>
            ⚠️ {log.error_message || "Terjadi kesalahan"}
          </span>
        )}
      </div>
      <div className="flex justify-between text-gray-600 mt-0.5">
        <span>{log.trigger_value?.toFixed(1)} dBFS</span>
        <span>{log.duration?.toFixed(1)}s</span>
      </div>
    </div>
  );
}