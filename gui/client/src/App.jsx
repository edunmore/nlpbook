import { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Book, Edit3, Save, Play, FileText, Settings, Globe, Workflow } from 'lucide-react';
import 'github-markdown-css/github-markdown-dark.css';
import './index.css';
import Steering from './Steering';
import WorldHelper from './WorldHelper';
import WorkflowPanel from './WorkflowPanel';

const API_BASE = 'http://localhost:8000/api';

function App() {
  const [chapters, setChapters] = useState([]);
  const [selectedChapter, setSelectedChapter] = useState(null);
  const [content, setContent] = useState('');
  const [feedback, setFeedback] = useState('');
  const [globalInstructions, setGlobalInstructions] = useState('');
  const [showSettings, setShowSettings] = useState(false);
  const [isRefining, setIsRefining] = useState(false);
  const [refineOutput, setRefineOutput] = useState('');

  // World State
  const [worlds, setWorlds] = useState([]);
  const [currentWorld, setCurrentWorld] = useState('default');
  const [viewMode, setViewMode] = useState('reader'); // reader, builder, steering

  useEffect(() => {
    fetchWorlds();
  }, []);

  useEffect(() => {
    fetchChapters();
    fetchGlobalInstructions();
  }, [currentWorld]);

  const fetchWorlds = async () => {
    try {
      const res = await axios.get(`${API_BASE}/worlds`);
      setWorlds(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const createWorld = async () => {
    const name = prompt("Enter new world name (e.g. cyberpunk-baker):");
    if (!name) return;
    try {
      await axios.post(`${API_BASE}/worlds`, { name });
      await fetchWorlds();
      setCurrentWorld(name);
      setViewMode('builder');
    } catch (err) {
      alert("Error creating world: " + err.message);
    }
  };

  const fetchChapters = async () => {
    try {
      const res = await axios.get(`${API_BASE}/chapters`, { params: { world: currentWorld } });
      setChapters(res.data);
      if (res.data.length === 0) {
        setSelectedChapter(null); // Clear selection if no chapters
      }
    } catch (err) {
      console.error("Failed to load chapters", err);
    }
  };

  const fetchGlobalInstructions = async () => {
    try {
      const res = await axios.get(`${API_BASE}/global-instructions`);
      setGlobalInstructions(res.data.content);
    } catch (err) {
      console.error(err);
    }
  };

  const loadChapter = async (filename) => {
    setSelectedChapter(filename);
    setViewMode('reader');
    try {
      const res = await axios.get(`${API_BASE}/chapters/${filename}`, { params: { world: currentWorld } });
      setContent(res.data.content);
      setFeedback(res.data.feedback || '');
      setRefineOutput('');
    } catch (err) {
      console.error(err);
    }
  };

  const openWorld = () => {
    setSelectedChapter(null);
    setViewMode('builder');
  };

  const openSteering = () => {
    setSelectedChapter(null);
    setViewMode('steering');
  };

  const saveFeedback = async () => {
    if (!selectedChapter) return;
    try {
      await axios.post(`${API_BASE}/chapters/${selectedChapter}/feedback`, { content: feedback }, { params: { world: currentWorld } });
      alert('Feedback saved!');
    } catch (err) {
      console.error(err);
      alert('Error saving feedback');
    }
  };

  const saveGlobalInstructions = async () => {
    try {
      await axios.post(`${API_BASE}/global-instructions`, { content: globalInstructions });
      alert('Global instructions saved!');
    } catch (err) {
      console.error(err);
    }
  };

  const refineChapter = async () => {
    if (!selectedChapter) return;
    setIsRefining(true);
    setRefineOutput('Agent is working... please wait.');
    try {
      // First save local feedback to ensure it's picked up
      await axios.post(`${API_BASE}/chapters/${selectedChapter}/feedback`, { content: feedback }, { params: { world: currentWorld } });

      const res = await axios.post(`${API_BASE}/refine`, {
        chapter: selectedChapter.split('-')[0].replace('CH', ''),
        model: 'gemini',
        world: currentWorld
      });

      if (res.data.status === 'ok') {
        setRefineOutput('Refinement Complete!\nCheck chapters/refined/ folder.');
      } else {
        setRefineOutput(`Error:\n${res.data.output}`);
      }
    } catch (err) {
      setRefineOutput(`Error: ${err.message}`);
    } finally {
      setIsRefining(false);
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">
          <Book size={24} />
          <span>Book<strong>Agent</strong></span>
        </div>

        {/* World Switcher */}
        <div className="world-select">
          <select value={currentWorld} onChange={(e) => {
            if (e.target.value === 'NEW') {
              createWorld();
            } else {
              setCurrentWorld(e.target.value);
            }
          }}>
            {worlds.map(w => <option key={w} value={w}>{w}</option>)}
            <option value="NEW">+ New World...</option>
          </select>
        </div>

        <div className="chapter-list">
          <div
            className={`chapter-item ${viewMode === 'builder' ? 'active' : ''}`}
            onClick={openWorld}
          >
            <Globe size={16} />
            <span>World Config</span>
          </div>
          <div
            className={`chapter-item ${viewMode === 'workflow' ? 'active' : ''}`}
            onClick={() => { setSelectedChapter(null); setViewMode('workflow'); }}
          >
            <Workflow size={16} />
            <span>Planning Workflow</span>
          </div>
          <div
            className={`chapter-item ${viewMode === 'steering' ? 'active' : ''}`}
            onClick={openSteering}
          >
            <Settings size={16} />
            <span>Steering & Prompts</span>
          </div>

          <div className="divider" style={{ height: '1px', background: 'var(--border)', margin: '8px 0' }}></div>
          {chapters.length === 0 && <div style={{ padding: '8px', fontSize: '12px', opacity: 0.6 }}>No chapters yet.</div>}
          {chapters.map((ch) => (
            <div
              key={ch.filename}
              className={`chapter-item ${selectedChapter === ch.filename ? 'active' : ''}`}
              onClick={() => loadChapter(ch.filename)}
            >
              <FileText size={16} />
              <span>{ch.filename.replace('.md', '')}</span>
            </div>
          ))}
        </div>
        <div className="sidebar-footer">
          {/* Legacy Global Settings removed or kept? Let's keep for now */}
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {viewMode === 'builder' ? (
          <WorldHelper currentWorld={currentWorld} />
        ) : viewMode === 'workflow' ? (
          <WorkflowPanel currentWorld={currentWorld} onRefresh={fetchChapters} />
        ) : viewMode === 'steering' ? (
          <Steering currentWorld={currentWorld} />
        ) : selectedChapter ? (
          <>
            <header className="top-bar">
              <h2>{selectedChapter.replace(/-/g, ' ').replace('.md', '')}</h2>
            </header>
            <div className="content-scroll">
              <div className="markdown-body">
                <ReactMarkdown>{content}</ReactMarkdown>
              </div>
            </div>
          </>
        ) : (
          <div className="empty-state">
            <Book size={64} opacity={0.2} />
            <p>Select a chapter to begin reading</p>
          </div>
        )}
      </main>

      {/* Right Panel (Feedback) */}
      {viewMode === 'reader' && (
        <aside className="right-panel">
          <div className="panel-header">
            <Edit3 size={18} />
            <h3>Refinement Station</h3>
          </div>

          {showSettings ? (
            <div className="panel-content">
              <label>Global Improvement Ideas</label>
              <textarea
                value={globalInstructions}
                onChange={(e) => setGlobalInstructions(e.target.value)}
                placeholder="Enter instructions that apply to all chapters..."
              />
              <button className="primary-btn" onClick={saveGlobalInstructions}>
                <Save size={16} /> Save Globals
              </button>
            </div>
          ) : (
            <div className="panel-content">
              <label>Chapter Specific Feedback</label>
              <textarea
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                placeholder="What should be improved in this chapter?"
                disabled={!selectedChapter}
              />
              <div className="actions">
                <button className="secondary-btn" onClick={saveFeedback} disabled={!selectedChapter}>
                  <Save size={16} /> Save Notes
                </button>
                <button className="primary-btn" onClick={refineChapter} disabled={!selectedChapter || isRefining}>
                  <Play size={16} /> {isRefining ? 'Refining...' : 'Refine'}
                </button>
              </div>
              {refineOutput && (
                <div className="output-log">
                  <pre>{refineOutput}</pre>
                </div>
              )}
            </div>
          )}
        </aside>
      )}
    </div>
  );
}

export default App;
