
import React, { useState, useEffect } from 'react';
import './App.css'; // Reuse basic styles or inline

function PromptModal({ isOpen, onClose, world, filename }) {
    const [content, setContent] = useState("");
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (isOpen && filename) {
            loadContent();
        }
    }, [isOpen, filename]);

    const loadContent = async () => {
        setLoading(true);
        setError(null);
        try {
            const res = await fetch(`/api/prompts/content?world=${world}&filename=${filename}`);
            const data = await res.json();
            if (data.error) {
                setError(data.error);
                setContent("");
            } else {
                setContent(data.content);
            }
        } catch (err) {
            setError("Failed to load prompt: " + err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        setSaving(true);
        try {
            const res = await fetch('/api/prompts/content', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ world, filename, content }),
            });
            const data = await res.json();
            if (data.status === 'ok') {
                onClose(); // Close on success
            } else {
                alert("Error saving: " + data.message);
            }
        } catch (err) {
            alert("Error saving: " + err.message);
        } finally {
            setSaving(false);
        }
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content" style={{ width: '800px', maxWidth: '90vw' }}>
                <h3>Edit Prompt: {filename}</h3>

                {loading && <div>Loading...</div>}
                {error && <div className="error">{error}</div>}

                {!loading && (
                    <textarea
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        style={{
                            width: '100%',
                            height: '500px',
                            fontFamily: 'monospace',
                            fontSize: '14px',
                            backgroundColor: '#1e1e1e',
                            color: '#d4d4d4',
                            border: '1px solid #333',
                            padding: '10px'
                        }}
                    />
                )}

                <div className="modal-actions" style={{ marginTop: '15px', display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
                    <button onClick={onClose} disabled={saving}>Cancel</button>
                    <button onClick={handleSave} disabled={saving || loading} className="primary-btn">
                        {saving ? "Saving..." : "Save Prompt"}
                    </button>
                </div>
            </div>
        </div>
    );
}

export default PromptModal;
