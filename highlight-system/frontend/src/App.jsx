import ConnectionPanel from "./components/ConnectionPanel.jsx";
import AudioMonitor from "./components/AudioMonitor.jsx";

function App() {
  return (
    <div style={{ 
      backgroundColor: '#121214', 
      minHeight: '100vh', 
      display: 'flex', 
      flexDirection: 'column', // Mengatur posisi ke bawah
      justifyContent: 'center', 
      alignItems: 'center',
      gap: '10px' // Jarak antar card
    }}>
      <ConnectionPanel />
      <AudioMonitor />
    </div>
  );
}

export default App;