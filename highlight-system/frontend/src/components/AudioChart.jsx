import { useState, useEffect, useRef } from "react";

const BAR_COUNT = 60;

export default function AudioChart({ currentDbfs, threshold, isMonitoring, isConnected }) {
  const [history, setHistory] = useState(Array(BAR_COUNT).fill(-60));
  const prevDbfs = useRef(null);

  useEffect(() => {
    if (!isMonitoring) return;
    // Update setiap kali currentDbfs berubah, termasuk nilai -60
    if (prevDbfs.current !== currentDbfs) {
      prevDbfs.current = currentDbfs;
      setHistory((prev) => {
        const next = prev.slice(1);
        next.push(currentDbfs);
        return next;
      });
    }
  }, [currentDbfs, isMonitoring]);

  // Reset history saat monitoring stop
  useEffect(() => {
    if (!isConnected) {
      setHistory(Array(BAR_COUNT).fill(-60));
      prevDbfs.current = null;
    }
  }, [isConnected]);

  const toHeight = (dbfs) => {
    const clamped = Math.max(-60, Math.min(0, dbfs));
    return ((clamped + 60) / 60) * 100;
  };

  const thresholdPct = toHeight(threshold);

  return (
    <div className="bg-[#16171f] rounded-xl border border-[#2a2b35] p-4 h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-3">
          <span className="text-xs text-gray-500 font-bold">dBFS</span>
          <span className="text-sm font-bold tracking-wider text-white">
            ROOT MEAN SQUARE <span className="text-yellow-400">(RMS)</span>
          </span>
        </div>
        <div className="text-sm">
          RMS:{" "}
          <span className={`font-bold ${currentDbfs >= threshold ? "text-yellow-400" : "text-gray-400"}`}>
            {currentDbfs.toFixed(0)} dBFS
          </span>
        </div>
      </div>

      {/* Chart Area */}
      <div className="relative flex-1 flex">
        {/* Y-axis labels */}
        <div className="flex flex-col justify-between text-[10px] text-gray-600 pr-2 py-1 w-8">
          {[0, -10, -20, -30, -40, -50, -60].map((v) => (
            <span key={v}>{v}</span>
          ))}
        </div>

        {/* Bar chart */}
        <div className="relative flex-1 bg-[#0e0f14] rounded overflow-hidden">
          {/* Threshold line */}
          <div
            className="absolute w-full border-t border-dashed border-red-500 z-10"
            style={{ bottom: `${thresholdPct}%` }}
          >
            <span className="absolute left-1 -top-4 text-[10px] text-red-400 bg-red-900/60 px-1 rounded">
              Threshold: {threshold} dBFS
            </span>
          </div>

          {/* Bars */}
          <div className="absolute inset-0 flex items-end gap-[2px] px-1 pb-1">
            {history.map((val, i) => {
              const h = toHeight(val);
              const isAbove = val >= threshold;
              const isLatest = i === history.length - 1;
              return (
                <div
                  key={i}
                  className="flex-1 rounded-sm"
                  style={{
                    height: `${Math.max(h, 1)}%`,
                    backgroundColor: isAbove ? "#facc15" : isLatest ? "#4ade80" : "#2a3a2a",
                    opacity: 0.6 + (i / BAR_COUNT) * 0.4,
                    transition: "height 0.1s ease",
                  }}
                />
              );
            })}
          </div>
        </div>
      </div>

      {/* Status */}
      <div className="mt-2 text-center text-xs">
        {isMonitoring ? (
          <span className="text-green-400">● Memantau audio real-time</span>
        ) : (
          <span className="text-gray-600">● Tekan START untuk mulai memantau</span>
        )}
      </div>
    </div>
  );
}