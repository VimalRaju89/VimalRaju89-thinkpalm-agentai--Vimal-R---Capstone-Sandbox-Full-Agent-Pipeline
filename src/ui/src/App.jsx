import React, { useState, useEffect } from 'react';
import './index.css';

function App() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState([]);
  const [report, setReport] = useState('');
  const [threadId, setThreadId] = useState(`thread_${Math.random().toString(36).substr(2, 9)}`);

  const runResearch = async () => {
    if (!query) return;
    setLoading(true);
    setLogs(prev => [...prev, { type: 'system', content: `Starting mission: ${query}` }]);
    
    try {
      const response = await fetch('http://localhost:8000/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, thread_id: threadId }),
      });
      
      const data = await response.json();
      if (data.final_report) {
        setReport(data.final_report);
        setLogs(prev => [...prev, { type: 'system', content: 'Mission accomplished. Final report generated.' }]);
      }
      
      if (data.history) {
        setLogs(prev => [
          ...prev, 
          ...data.history.map(msg => ({
            type: msg.includes('Researcher') ? 'researcher' : 'writer',
            content: msg.substring(0, 500) + (msg.length > 500 ? '...' : '')
          }))
        ]);
      }
    } catch (error) {
      setLogs(prev => [...prev, { type: 'error', content: 'Connection failed. Ensure backend is running.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>Nexus Intelligence</h1>
        <p>Advanced Multi-Agent Orchestration Suite</p>
      </header>

      <div className="glass-card search-section">
        <input 
          type="text" 
          placeholder="What would you like to research today?" 
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={loading}
        />
        <button onClick={runResearch} disabled={loading || !query}>
          {loading ? 'Synthesizing...' : 'Submit'}
        </button>
      </div>

      <main className="main-grid">
        <aside className="glass-card">
          <div className="status-indicator">
            <div className={loading ? "pulse" : ""}></div>
            {loading ? "Pipeline Active" : "Standby"}
          </div>
          <div className="agent-log">
            {logs.length === 0 && <p style={{color: 'var(--text-muted)'}}>No activity recorded yet.</p>}
            {logs.map((log, i) => (
              <div key={i} className={`log-item ${log.type}`}>
                {log.content}
              </div>
            ))}
          </div>
        </aside>

        <section className="glass-card">
          <h2 style={{marginBottom: '1rem', fontFamily: 'Outfit'}}>Executive Report</h2>
          <div className="report-view">
            {report || <p style={{color: 'var(--text-muted)'}}>The final synthesis will appear here.</p>}
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
