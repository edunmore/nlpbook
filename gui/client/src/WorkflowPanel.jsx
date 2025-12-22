import { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import { Star, Trash2, Plus, Check, ChevronRight, Sparkles, FileText, Map, BookOpen } from 'lucide-react';
import './WorkflowPanel.css';

const API_BASE = 'http://localhost:8000/api';

function WorkflowPanel({ currentWorld, onRefresh }) {
    const [workflowStage, setWorkflowStage] = useState('brainstorm');
    const [concepts, setConcepts] = useState([]);
    const [chapterMap, setChapterMap] = useState('');
    const [chapterCards, setChapterCards] = useState([]);
    const [currentCardIndex, setCurrentCardIndex] = useState(0);
    const [chapters, setChapters] = useState([]);
    const [currentChapterIndex, setCurrentChapterIndex] = useState(0);
    const [isGenerating, setIsGenerating] = useState(false);
    const [genOutput, setGenOutput] = useState('');
    const [config, setConfig] = useState({});
    const [newConcept, setNewConcept] = useState({ concept: '', nlp_source: '', description: '', scene_idea: '' });

    useEffect(() => {
        loadConfig();
        loadBrainstorm();
        loadChapterMap();
        loadChapterCards();
        loadChapters();
    }, [currentWorld]);

    const loadConfig = async () => {
        try {
            const res = await axios.get(`${API_BASE}/world-config`, { params: { world: currentWorld } });
            setConfig(res.data);
            setWorkflowStage(res.data.workflow_stage || 'brainstorm');
        } catch (err) {
            console.error(err);
        }
    };

    const loadBrainstorm = async () => {
        try {
            const res = await axios.get(`${API_BASE}/brainstorm`, { params: { world: currentWorld } });
            setConcepts(res.data.concepts || []);
        } catch (err) {
            console.error(err);
        }
    };

    const loadChapterMap = async () => {
        try {
            const res = await axios.get(`${API_BASE}/chapter-map`, { params: { world: currentWorld } });
            setChapterMap(res.data.content || '');
        } catch (err) {
            console.error(err);
        }
    };

    const loadChapterCards = async () => {
        try {
            const res = await axios.get(`${API_BASE}/steering/files`, { params: { world: currentWorld, category: 'chapter-cards' } });
            setChapterCards(res.data.files || []);
        } catch (err) {
            console.error(err);
        }
    };

    const loadChapters = async () => {
        try {
            const res = await axios.get(`${API_BASE}/chapters`, { params: { world: currentWorld } });
            setChapters(res.data || []);
        } catch (err) {
            console.error(err);
        }
    };

    const updateRating = (index, rating) => {
        const updated = [...concepts];
        updated[index].rating = rating;
        setConcepts(updated);
    };

    const deleteConcept = (index) => {
        const updated = concepts.filter((_, i) => i !== index);
        setConcepts(updated);
    };

    const addConcept = () => {
        if (!newConcept.concept) return;
        setConcepts([...concepts, { ...newConcept, rating: 3, approved: false, source_file: 'User Added' }]);
        setNewConcept({ concept: '', nlp_source: '', description: '', scene_idea: '' });
    };

    const saveBrainstorm = async () => {
        try {
            await axios.post(`${API_BASE}/brainstorm`, { concepts, world: currentWorld });
            setGenOutput('Brainstorm saved!');
        } catch (err) {
            setGenOutput('Error saving: ' + err.message);
        }
    };

    const approveBrainstorm = async () => {
        // Mark all rated >= 3 as approved
        const approved = concepts.map(c => ({ ...c, approved: c.rating >= 3 }));
        await axios.post(`${API_BASE}/brainstorm`, { concepts: approved, world: currentWorld });
        await axios.post(`${API_BASE}/brainstorm/approve`, null, { params: { world: currentWorld } });
        setWorkflowStage('map_generate');
        setGenOutput('Brainstorm approved! Ready to generate chapter map.');
    };

    // Generic generation with Polling
    const runGenerationTask = async (taskName, apiCall, reloadCallback) => {
        setIsGenerating(true);
        setGenOutput(`${taskName} started...`);
        try {
            await apiCall();

            // Poll logs until completion
            const pollInterval = setInterval(async () => {
                try {
                    const res = await axios.get(`${API_BASE}/logs`);
                    const logs = res.data.logs;
                    const recentLogs = logs.slice(-10); // Look at last 10 lines

                    // Check for general completion or specific task completion signals
                    // The backend scripts often print "Process finished with code 0"
                    const isComplete = recentLogs.some(l =>
                        l.includes("Process finished with code 0") ||
                        l.includes("Saved timeline") ||
                        l.includes("Saved: ") ||
                        l.includes("Error:")
                    );

                    if (isComplete) {
                        clearInterval(pollInterval);
                        setIsGenerating(false);
                        setGenOutput(`${taskName} complete!`);
                        if (reloadCallback) reloadCallback();
                    }
                } catch (e) {
                    console.error("Polling error", e);
                }
            }, 1000);

            // Safety timeout (2 minutes)
            setTimeout(() => {
                clearInterval(pollInterval);
                if (isGenerating) setIsGenerating(false);
            }, 120000);

        } catch (err) {
            setGenOutput('Error: ' + err.message);
            setIsGenerating(false);
        }
    };

    const generateBrainstorm = () => {
        const maxFiles = config.source_max_files || 5;
        runGenerationTask(
            'Brainstorm Generation',
            () => axios.post(`${API_BASE}/generate/brainstorm`, { world: currentWorld, count: maxFiles }),
            loadBrainstorm
        );
    };

    const generateMap = () => {
        const chapterCount = config.chapter_count || 10;
        runGenerationTask(
            'Chapter Map Generation',
            () => axios.post(`${API_BASE}/generate/map`, { world: currentWorld, count: chapterCount }),
            loadChapterMap
        );
    };

    const saveChapterMap = async () => {
        try {
            await axios.post(`${API_BASE}/chapter-map`, chapterMap, {
                params: { world: currentWorld },
                headers: { 'Content-Type': 'application/json' }
            });
            setGenOutput('Chapter map saved!');
        } catch (err) {
            setGenOutput('Error saving: ' + err.message);
        }
    };

    const approveMap = async () => {
        await saveChapterMap();
        await axios.post(`${API_BASE}/chapter-map/approve`, null, { params: { world: currentWorld } });
        setWorkflowStage('cards_generate');
        setGenOutput('Map approved! Ready to generate chapter cards.');
    };

    const generateNextCard = () => {
        const nextNum = chapterCards.length + 1;
        runGenerationTask(
            `Card ${nextNum} Generation`,
            () => axios.post(`${API_BASE}/generate/cards`, { world: currentWorld, count: 1, start: nextNum }),
            loadChapterCards
        );
    };

    const generateNextChapter = () => {
        const nextNum = chapters.length + 1;
        runGenerationTask(
            `Chapter ${nextNum} Generation`,
            () => axios.post(`${API_BASE}/generate/chapters`, { world: currentWorld, count: 1, start: nextNum }),
            () => { loadChapters(); if (onRefresh) onRefresh(); }
        );
    };

    const renderStars = (rating, index) => {
        return [1, 2, 3, 4, 5].map(star => (
            <Star
                key={star}
                size={16}
                fill={star <= rating ? '#fbbf24' : 'transparent'}
                stroke={star <= rating ? '#fbbf24' : 'var(--muted)'}
                style={{ cursor: 'pointer' }}
                onClick={() => updateRating(index, star)}
            />
        ));
    };

    const stages = [
        { key: 'brainstorm', label: 'Brainstorm', icon: Sparkles },
        { key: 'map_generate', label: 'Chapter Map', icon: Map },
        { key: 'cards_generate', label: 'Chapter Cards', icon: FileText },
        { key: 'chapters_generate', label: 'Chapters', icon: BookOpen },
    ];

    return (
        <div className="workflow-panel">
            {/* Stage Progress */}
            <div className="workflow-stages">
                {stages.map((s, i) => (
                    <div
                        key={s.key}
                        className={`stage ${workflowStage === s.key || workflowStage.startsWith(s.key.split('_')[0]) ? 'active' : ''}`}
                        onClick={() => setWorkflowStage(s.key)}
                    >
                        <s.icon size={18} />
                        <span>{s.label}</span>
                        {i < stages.length - 1 && <ChevronRight size={14} className="chevron" />}
                    </div>
                ))}
            </div>

            {/* Brainstorm Review */}
            {workflowStage.startsWith('brainstorm') && (
                <div className="workflow-section">
                    <div className="section-header">
                        <h3>Brainstorm Review</h3>
                        <div className="section-actions">
                            <button onClick={generateBrainstorm} disabled={isGenerating} className="secondary-btn">
                                <Sparkles size={14} /> Generate from Source
                            </button>
                        </div>
                    </div>

                    {concepts.length === 0 ? (
                        <div className="empty-state">No concepts yet. Click "Generate from Source" to start.</div>
                    ) : (
                        <div className="concept-list">
                            {concepts.map((c, i) => (
                                <div key={i} className="concept-card">
                                    <div className="concept-header">
                                        <div className="stars">{renderStars(c.rating, i)}</div>
                                        <button className="icon-btn danger" onClick={() => deleteConcept(i)}><Trash2 size={14} /></button>
                                    </div>
                                    <h4>{c.concept}</h4>
                                    {c.nlp_source && <div className="nlp-source">NLP: {c.nlp_source}</div>}
                                    <p>{c.description}</p>
                                    <div className="scene-idea"><strong>Scene:</strong> {c.scene_idea}</div>
                                    <div className="source-file">Source: {c.source_file}</div>
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Add New Concept */}
                    <div className="add-concept">
                        <h4><Plus size={14} /> Add Your Own Concept</h4>
                        <input
                            placeholder="Concept name"
                            value={newConcept.concept}
                            onChange={e => setNewConcept({ ...newConcept, concept: e.target.value })}
                        />
                        <input
                            placeholder="NLP Source (optional)"
                            value={newConcept.nlp_source}
                            onChange={e => setNewConcept({ ...newConcept, nlp_source: e.target.value })}
                        />
                        <textarea
                            placeholder="Description"
                            value={newConcept.description}
                            onChange={e => setNewConcept({ ...newConcept, description: e.target.value })}
                        />
                        <input
                            placeholder="Scene idea"
                            value={newConcept.scene_idea}
                            onChange={e => setNewConcept({ ...newConcept, scene_idea: e.target.value })}
                        />
                        <button onClick={addConcept} className="secondary-btn"><Plus size={14} /> Add</button>
                    </div>

                    <div className="workflow-actions">
                        <button onClick={saveBrainstorm} className="secondary-btn">Save Changes</button>
                        <button onClick={approveBrainstorm} className="primary-btn" disabled={concepts.length === 0}>
                            <Check size={14} /> Approve & Continue
                        </button>
                    </div>
                </div>
            )}

            {/* Chapter Map Review */}
            {workflowStage.startsWith('map') && (
                <div className="workflow-section">
                    <div className="section-header">
                        <h3>Chapter Map Review</h3>
                        <div className="section-actions">
                            <button onClick={generateMap} disabled={isGenerating} className="secondary-btn">
                                <Map size={14} /> Generate Map
                            </button>
                        </div>
                    </div>

                    {!chapterMap ? (
                        <div className="empty-state">No map yet. Click "Generate Map" to create one.</div>
                    ) : (
                        <div className="map-editor">
                            <textarea
                                value={chapterMap}
                                onChange={e => setChapterMap(e.target.value)}
                                rows={20}
                            />
                        </div>
                    )}

                    <div className="workflow-actions">
                        <button onClick={saveChapterMap} className="secondary-btn">Save Changes</button>
                        <button onClick={approveMap} className="primary-btn" disabled={!chapterMap}>
                            <Check size={14} /> Approve & Continue
                        </button>
                    </div>
                </div>
            )}

            {/* Chapter Cards Review */}
            {workflowStage.startsWith('cards') && (
                <div className="workflow-section">
                    <div className="section-header">
                        <h3>Chapter Cards ({chapterCards.length} created)</h3>
                        <div className="section-actions">
                            <button onClick={generateNextCard} disabled={isGenerating} className="secondary-btn">
                                <FileText size={14} /> Generate Next Card
                            </button>
                        </div>
                    </div>

                    {chapterCards.length === 0 ? (
                        <div className="empty-state">No cards yet. Click "Generate Next Card" to start.</div>
                    ) : (
                        <div className="cards-list">
                            {chapterCards.map((card, i) => (
                                <div key={i} className="card-item" onClick={() => setCurrentCardIndex(i)}>
                                    <FileText size={14} />
                                    <span>{card}</span>
                                </div>
                            ))}
                        </div>
                    )}

                    <div className="workflow-actions">
                        <button
                            onClick={() => setWorkflowStage('chapters_generate')}
                            className="primary-btn"
                            disabled={chapterCards.length === 0}
                        >
                            <Check size={14} /> Proceed to Chapters
                        </button>
                    </div>
                </div>
            )}

            {/* Chapter Generation */}
            {workflowStage.startsWith('chapters') && (
                <div className="workflow-section">
                    <div className="section-header">
                        <h3>Chapters ({chapters.length} written)</h3>
                        <div className="section-actions">
                            <button onClick={generateNextChapter} disabled={isGenerating} className="secondary-btn">
                                <BookOpen size={14} /> Generate Next Chapter
                            </button>
                        </div>
                    </div>

                    {chapters.length === 0 ? (
                        <div className="empty-state">No chapters yet. Click "Generate Next Chapter" to start.</div>
                    ) : (
                        <div className="chapters-list">
                            {chapters.map((ch, i) => (
                                <div key={i} className="chapter-item-small">
                                    <BookOpen size={14} />
                                    <span>{ch.filename}</span>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}

            {/* Output Log */}
            {genOutput && (
                <div className="gen-output">
                    <pre>{genOutput}</pre>
                </div>
            )}
        </div>
    );
}

export default WorkflowPanel;
