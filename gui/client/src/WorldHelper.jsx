import { useState, useEffect } from 'react';
import axios from 'axios';
import { Save, AlertTriangle, Plus, Trash, Globe } from 'lucide-react';
import './WorldHelper.css';

const API_BASE = 'http://localhost:8000/api';

function WorldHelper({ currentWorld }) {
    const [config, setConfig] = useState(null);
    const [loading, setLoading] = useState(false);
    const [generating, setGenerating] = useState(false);
    const [logs, setLogs] = useState([]);

    // Log Polling
    useEffect(() => {
        let interval;
        if (generating) {
            interval = setInterval(fetchLogs, 1000);
        }
        return () => clearInterval(interval);
    }, [generating]);

    const fetchLogs = async () => {
        try {
            const res = await axios.get(`${API_BASE}/logs`);
            const newLogs = res.data.logs;
            setLogs(newLogs);

            // Check if generation finished successfully
            // Scan last few logs for success message
            const recentLogs = newLogs.slice(-5);
            const success = recentLogs.some(l => l.includes("Updated config:") || l.includes("World generation complete"));

            if (success) {
                setGenerating(false);
                fetchConfig();
            }
        } catch (e) {
            console.error("Log error", e);
        }
    }

    useEffect(() => {
        fetchConfig();
    }, [currentWorld]);

    const fetchConfig = async () => {
        setLoading(true);
        try {
            // Pass world param
            const res = await axios.get(`${API_BASE}/world-config`, { params: { world: currentWorld } });
            const data = res.data;
            if (!data.characters) data.characters = [];
            setConfig(data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const saveConfig = async () => {
        try {
            await axios.post(`${API_BASE}/world-config`, config, { params: { world: currentWorld } });
            alert('World Config Saved!');
        } catch (err) {
            console.error(err);
            alert('Error saving config');
        }
    };

    const updateField = (field, value) => {
        setConfig({ ...config, [field]: value });
    };

    // Character Management
    const addCharacter = () => {
        const newChar = { name: "New Character", role: "Support", description: "", tags: [] };
        setConfig({ ...config, characters: [...config.characters, newChar] });
    };

    const removeCharacter = (index) => {
        const newChars = [...config.characters];
        newChars.splice(index, 1);
        setConfig({ ...config, characters: newChars });
    };

    const updateCharacter = (index, field, value) => {
        const newChars = [...config.characters];
        newChars[index][field] = value;
        setConfig({ ...config, characters: newChars });
    };

    const autoGenWorld = async () => {
        setGenerating(true);
        try {
            await axios.post(`${API_BASE}/generate/world`, { world: currentWorld });
            // Polling handles the rest
        } catch (err) {
            console.error(err);
            setGenerating(false);
        }
    };

    const generateStoryline = async () => {
        setGenerating(true);
        try {
            await axios.post(`${API_BASE}/generate/storyline`, { world: currentWorld });
        } catch (err) {
            console.error(err);
        }
    };

    const generateChapters = async () => {
        if (!confirm("⚠️ This will generate NEW chapters based on the timeline. Ensure you have backed up any manual work. Continue?")) return;

        setGenerating(true);
        try {
            await axios.post(`${API_BASE}/generate/chapters`, { world: currentWorld, count: 5, start: 1 });
        } catch (err) {
            console.error(err);
        }
    };

    const generateCards = async () => {
        setGenerating(true);
        try {
            await axios.post(`${API_BASE}/generate/cards`, { world: currentWorld, count: 5, start: 1 });
        } catch (err) {
            console.error(err);
        }
    };

    if (loading || !config) return <div>Loading config...</div>;

    return (
        <div className="world-helper">
            <h2><Globe size={20} /> World Builder: {currentWorld}</h2>

            <div className="info-banner" style={{ background: 'rgba(6, 182, 212, 0.1)', padding: '12px', borderRadius: '8px', marginBottom: '20px', fontSize: '14px', border: '1px solid rgba(6, 182, 212, 0.3)' }}>
                <strong>How to use AI:</strong> Type instructions like <code>AI: make the tone darker</code> into any field below, then click <strong>Auto-Generate (AI)</strong>. The AI will apply your changes even to empty fields!
            </div>

            <div className="config-form">
                <div className="form-section full-width">
                    <label>Book Title</label>
                    <input
                        value={config.title || ''}
                        onChange={(e) => updateField('title', e.target.value)}
                    />
                </div>

                <h3 className="full-width">Characters</h3>
                <div className="characters-list full-width">
                    {config.characters.map((char, idx) => (
                        <div key={idx} className="character-card">
                            <div className="char-header">
                                <input
                                    className="char-name"
                                    value={char.name}
                                    onChange={(e) => updateCharacter(idx, 'name', e.target.value)}
                                    placeholder="Name"
                                />
                                <select
                                    value={char.role}
                                    onChange={(e) => updateCharacter(idx, 'role', e.target.value)}
                                >
                                    <option>Protagonist</option>
                                    <option>Support</option>
                                    <option>Antagonist</option>
                                    <option>Pet</option>
                                    <option>Other</option>
                                </select>
                                <button className="icon-btn danger-text" onClick={() => removeCharacter(idx)}>
                                    <Trash size={14} />
                                </button>
                            </div>
                            <textarea
                                rows={4}
                                placeholder="Description / Traits"
                                value={char.description || ''}
                                onChange={(e) => updateCharacter(idx, 'description', e.target.value)}
                            />
                        </div>
                    ))}
                    <div className="char-actions">
                        <button className="secondary-btn" onClick={addCharacter}>
                            <Plus size={14} /> Add Manual
                        </button>
                        <button className="secondary-btn special" onClick={autoGenWorld} disabled={generating}>
                            ✨ Auto-Generate (AI)
                        </button>
                    </div>
                </div>

                <h3 className="full-width">Setting & Theme</h3>

                <div className="form-group">
                    <label>Setting</label>
                    <textarea
                        rows={5}
                        value={config.setting || ''}
                        onChange={(e) => updateField('setting', e.target.value)}
                    />
                </div>

                <div className="form-group">
                    <label>Theme</label>
                    <textarea
                        rows={5}
                        value={config.theme || ''}
                        onChange={(e) => updateField('theme', e.target.value)}
                    />
                </div>

                <div className="form-group full-width">
                    <label>The Glitch (Inciting Incident)</label>
                    <textarea
                        rows={2}
                        value={config.glitch_concept || ''}
                        onChange={(e) => updateField('glitch_concept', e.target.value)}
                    />
                </div>

                <h3 className="full-width">Inspiration Source</h3>

                <div className="form-group">
                    <label>Source Path (folder with text files)</label>
                    <input
                        value={config.source_path || ''}
                        onChange={(e) => updateField('source_path', e.target.value)}
                        placeholder="e.g., NLP or /path/to/transcripts"
                    />
                </div>

                <div className="form-group">
                    <label>Max Source Files to Process</label>
                    <input
                        type="number"
                        value={config.source_max_files || 10}
                        onChange={(e) => updateField('source_max_files', parseInt(e.target.value))}
                        min={1}
                        max={50}
                    />
                </div>

                <div className="form-group">
                    <label>Target Chapter Count</label>
                    <input
                        type="number"
                        value={config.chapter_count || 10}
                        onChange={(e) => updateField('chapter_count', parseInt(e.target.value))}
                        min={1}
                        max={99}
                    />
                </div>
            </div>

            <div className="actions-bar">
                <button className="primary-btn" onClick={saveConfig}>
                    <Save size={16} /> Save Config
                </button>
                <button className="secondary-btn" onClick={fetchConfig} title="Reload config from disk">
                    Reload Config
                </button>
            </div>

            <div className="generation-zone">
                <h3><AlertTriangle size={18} /> Generation Zone</h3>
                <div className="gen-buttons">
                    <button className="secondary-btn" onClick={generateStoryline} disabled={generating}>
                        Generate Storyline
                    </button>
                    <button className="secondary-btn" onClick={generateCards} disabled={generating}>
                        Generate Cards
                    </button>
                    <button className="secondary-btn danger" onClick={generateChapters} disabled={generating}>
                        Generate Chapters (1-5)
                    </button>
                    <button className="secondary-btn" onClick={() => setGenerating(!generating)}>
                        {generating ? 'Stop Monitoring' : 'Monitor Logs'}
                    </button>
                </div>

                <div className="gen-logs">
                    <div className="log-header">Live Terminal Output</div>
                    <div className="log-content">
                        {logs.length === 0 && <span style={{ opacity: 0.5 }}>Waiting for logs...</span>}
                        {logs.slice().reverse().map((line, i) => (
                            <div key={i}>{line}</div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default WorldHelper;
