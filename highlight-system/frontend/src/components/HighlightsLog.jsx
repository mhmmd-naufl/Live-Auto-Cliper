export default function HighlightsLog({ logs }) {
  // Show at most 5 most-recent logs and make the list scrollable
  const visibleLogs = Array.isArray(logs) ? logs.slice(-5).reverse() : [];

  return (
    <div className="bg-[#16171f] rounded-xl border border-[#2a2b35] p-4 h-full flex flex-col">
      <h3 className="text-sm font-bold tracking-wider text-white mb-3">Highlights Log</h3>

      <div className="flex-1 overflow-y-auto max-h-[260px] flex flex-col gap-1.5 pr-1">
        {visibleLogs.length === 0 ? (
          <div className="text-center text-gray-600 text-xs mt-8">
            Belum ada highlight yang direkam
          </div>
        ) : (
          visibleLogs.map((log) => (
            <LogItem key={log.id} log={log} />
          ))
        )}
      </div>

      {/* Footer */}
      {logs.length > 0 && (
        <div className="mt-2 pt-2 border-t border-[#2a2b35] text-xs text-gray-600 flex justify-between items-center">
          <span>Total: {logs.length} highlight</span>
          <span>
            {logs.filter((l) => l.status === "SUCCESS").length} sukses
          </span>
        </div>
      )}
    </div>
  );
}

function LogItem({ log }) {
  const time = new Date(log.timestamp).toLocaleTimeString("id-ID", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });

  const isSuccess = log.status === "SUCCESS";

  return (
    <div className={`rounded px-2 py-1.5 text-[11px] border-l-2 ${
      isSuccess ? "border-green-500 bg-green-950/30" : "border-red-500 bg-red-950/30"
    }`}>
      <div className="flex items-center justify-between gap-1">
        <span className="text-gray-400">{time}</span>
        <span className={`font-bold ${isSuccess ? "text-green-400" : "text-red-400"}`}>
          [{log.status}]
        </span>
      </div>
      <div className="text-gray-300 truncate mt-0.5">{log.filename || "-"}</div>
      <div className="flex justify-between text-gray-600 mt-0.5">
        <span>{log.trigger_value?.toFixed(1)} dBFS</span>
        <span>{log.duration?.toFixed(1)}s</span>
      </div>
    </div>
  );
}
