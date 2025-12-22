import { useState, useEffect } from 'react';
import axios from 'axios';
import { Save, AlertTriangle, FileText, Settings, BookOpen } from 'lucide-react';
import './WorldHelper.css'; // Re-use styles

const API_BASE = 'http://localhost:8000/api';

function Steering({ currentWorld }) {
    const [fileList, setFileList] = useState([]);
    const [category, setCategory] = useState("prompts"); // prompts, process, canon
    const [selectedFile, setSelectedFile] = useState(null);
    const [content, setContent] = useState("");
    const [fileSource, setFileSource] = useState("global"); // global or world
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchFiles();
        setSelectedFile(null);
        setContent("");
    }, [category, currentWorld]);

    const fetchFiles = async () => {
        try {
            const res = await axios.get(`${API_BASE}/steering/files`, { params: { category, world: currentWorld } });
            setFileList(res.data);
        } catch (e) {
            console.error(e);
        }
    }

    const loadFile = async (filename) => {
        setLoading(true);
        try {
            const res = await axios.get(`${API_BASE}/steering/content`, {
                params: { category, filename, world: currentWorld }
            });
            setContent(res.data.content);
            setFileSource(res.data.source);
            setSelectedFile(filename);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    }

    const saveFile = async () => {
        if (!selectedFile) return;
        try {
            await axios.post(`${API_BASE}/steering/content`, {
                category,
                filename: selectedFile,
                content,
                world: currentWorld
            });
            alert(`Saved ${selectedFile} for world '${currentWorld}'`);
            setFileSource("world"); // It is now an override/local file
        } catch (e) {
            console.error(e);
            alert("Error saving file");
        }
    }

    return (
        <div className="world-helper">
            <h2><Settings size={28} /> Advanced Steering: {currentWorld}</h2>

            <div className="config-form">

                {/* Category Selector */}
                <div className="gen-buttons" style={{ marginTop: 0 }}>
                    <button
                        className={`secondary-btn ${category === 'prompts' ? 'active' : ''}`}
                        onClick={() => setCategory('prompts')}
                        style={{ borderColor: category === 'prompts' ? 'var(--accent-primary)' : '' }}
                    >
                        <FileText size={16} /> Prompts
                    </button>
                    <button
                        className={`secondary-btn ${category === 'process' ? 'active' : ''}`}
                        onClick={() => setCategory('process')}
                        style={{ borderColor: category === 'process' ? 'var(--accent-primary)' : '' }}
                    >
                        <Settings size={16} /> Process
                    </button>
                    <button
                        className={`secondary-btn ${category === 'canon' ? 'active' : ''}`}
                        onClick={() => setCategory('canon')}
                        style={{ borderColor: category === 'canon' ? 'var(--accent-primary)' : '' }}
                    >
                        <BookOpen size={16} /> World Canon
                    </button>
                    <button
                        className={`secondary-btn ${category === 'chapter-cards' ? 'active' : ''}`}
                        onClick={() => setCategory('chapter-cards')}
                        style={{ borderColor: category === 'chapter-cards' ? 'var(--accent-primary)' : '' }}
                    >
                        <FileText size={16} /> Chapter Cards
                    </button>
                </div>

                <div style={{ display: 'flex', gap: '24px', height: '600px' }}>

                    {/* File List */}
                    <div style={{ width: '250px', borderRight: '1px solid var(--border)', overflowY: 'auto' }}>
                        {fileList.map(f => (
                            <div
                                key={f}
                                className={`chapter-item ${selectedFile === f ? 'active' : ''}`}
                                onClick={() => loadFile(f)}
                            >
                                {f}
                            </div>
                        ))}
                    </div>

                    {/* Editor */}
                    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '16px' }}>
                        {selectedFile ? (
                            <>
                                <div className="panel-header" style={{ padding: 0, border: 'none', justifyContent: 'space-between' }}>
                                    <span>{selectedFile}</span>
                                    {fileSource === 'global' && <span style={{ fontSize: '12px', color: 'var(--text-dim)' }}>Global Default (Editing creates World Copy)</span>}
                                    {fileSource === 'world' && <span style={{ fontSize: '12px', color: 'var(--accent-secondary)' }}>World Override Active</span>}
                                </div>
                                <textarea
                                    value={content}
                                    onChange={(e) => setContent(e.target.value)}
                                    style={{ flex: 1, fontFamily: 'JetBrains Mono', fontSize: '14px', lineHeight: '1.5', whiteSpace: 'pre' }}
                                />
                                <div className="actions">
                                    <button className="primary-btn" onClick={saveFile}>
                                        <Save size={16} /> Save Changes
                                    </button>
                                </div>
                            </>
                        ) : (
                            <div className="empty-state">Select a file to edit</div>
                        )}
                    </div>
                </div>

            </div>
        </div>
    );
}

export default Steering;
