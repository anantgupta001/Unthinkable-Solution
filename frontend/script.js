const searchBtn = document.getElementById("searchBtn");
const queryInput = document.getElementById("query");
const resultDiv = document.getElementById("result");
const sourcesDiv = document.getElementById("sources");

// Enable Enter key to search
queryInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        searchBtn.click();
    }
});

searchBtn.addEventListener("click", async () => {
    const query = queryInput.value.trim();
    if (!query) {
        resultDiv.innerHTML = '<p class="error">⚠️ Please enter a query.</p>';
        sourcesDiv.innerHTML = "";
        return;
    }

    // Show loading state
    resultDiv.innerHTML = '<div class="loading">🔍 Searching knowledge base...</div>';
    sourcesDiv.innerHTML = "";
    searchBtn.disabled = true;

    try {
        const response = await fetch("http://127.0.0.1:8000/search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query, top_k: 3 })
        });

        if (!response.ok) {
            throw new Error(`Backend error: ${response.status}`);
        }

        const data = await response.json();
        
        // Display answer
        resultDiv.innerHTML = `
            <div class="answer-container">
                <h3>📝 Answer:</h3>
                <div class="answer-text">${formatAnswer(data.answer)}</div>
                <div class="meta-info">
                    <span>📚 Searched ${data.num_docs_searched} document chunks</span>
                </div>
            </div>
        `;

        // Display sources
        if (data.sources && data.sources.length > 0) {
            sourcesDiv.innerHTML = `
                <h3>🔗 Sources:</h3>
                <div class="sources-list">
                    ${data.sources.map((source, idx) => `
                        <div class="source-item">
                            <strong>Source ${idx + 1}:</strong> ${source.file}
                            <span class="chunk-info">(Chunk ${source.chunk + 1})</span>
                            <span class="similarity">Similarity: ${(source.similarity * 100).toFixed(1)}%</span>
                        </div>
                    `).join('')}
                </div>
            `;
        }

    } catch (err) {
        resultDiv.innerHTML = `
            <div class="error">
                <strong>❌ Error:</strong> ${err.message}
                <br><br>
                <small>Make sure the backend server is running at http://127.0.0.1:8000</small>
            </div>
        `;
        sourcesDiv.innerHTML = "";
        console.error("Search error:", err);
    } finally {
        searchBtn.disabled = false;
    }
});

function formatAnswer(text) {
    // Simple formatting: preserve line breaks and add basic styling
    return text
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/^(.*)$/, '<p>$1</p>');
}
