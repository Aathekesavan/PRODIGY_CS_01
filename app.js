/**
 * METACIPHER - Advanced Cryptography Web Logic
 * Created for PRODIGY_CS_01
 */

// Caesar Cipher Cryptographic Operations
const CaesarCipher = {
    encrypt: function(text, shift, shiftNumbers = false) {
        let result = [];
        // Map negative/large shifts correctly
        let alphaShift = ((shift % 26) + 26) % 26;
        let numShift = ((shift % 10) + 10) % 10;

        for (let i = 0; i < text.length; i++) {
            let char = text[i];
            let code = text.charCodeAt(i);

            if (/[a-zA-Z]/.test(char)) {
                let start = (char === char.toUpperCase()) ? 65 : 97;
                let shiftedChar = String.fromCharCode(start + (code - start + alphaShift) % 26);
                result.push(shiftedChar);
            } else if (/\d/.test(char) && shiftNumbers) {
                let shiftedDigit = String.fromCharCode(48 + (code - 48 + numShift) % 10);
                result.push(shiftedDigit);
            } else {
                result.push(char);
            }
        }
        return result.join('');
    },

    decrypt: function(text, shift, shiftNumbers = false) {
        return this.encrypt(text, -shift, shiftNumbers);
    },

    bruteForce: function(text, shiftNumbers = false) {
        let results = {};
        for (let shift = 1; shift <= 25; shift++) {
            results[shift] = this.decrypt(text, shift, shiftNumbers);
        }
        return results;
    }
};

// UI Elements
const htmlEl = document.documentElement;
const themeToggle = document.getElementById('theme-toggle');

const textInput = document.getElementById('text-input');
const textOutput = document.getElementById('text-output');
const inputCharCount = document.getElementById('input-char-count');

const shiftSlider = document.getElementById('shift-slider');
const shiftInput = document.getElementById('shift-input');
const toggleNumbers = document.getElementById('toggle-numbers');
const toggleLive = document.getElementById('toggle-live');

const btnEncrypt = document.getElementById('btn-encrypt');
const btnDecrypt = document.getElementById('btn-decrypt');
const btnClear = document.getElementById('btn-clear');
const btnCopy = document.getElementById('btn-copy');
const btnBrute = document.getElementById('btn-brute');
const bruteContainer = document.getElementById('brute-container');

// Upgraded UI Elements
const analyticsChars = document.getElementById('analytics-chars');
const analyticsWords = document.getElementById('analytics-words');
const analyticsShift = document.getElementById('analytics-shift');
const analyticsTime = document.getElementById('analytics-time');
const analyticsScoreTxt = document.getElementById('analytics-score-txt');
const analyticsScoreBar = document.getElementById('analytics-score-bar');

const historyContainer = document.getElementById('history-container');
const btnClearHistory = document.getElementById('btn-clear-history');

const btnExportTxt = document.getElementById('btn-export-txt');
const btnExportJson = document.getElementById('btn-export-json');
const btnDownloadRaw = document.getElementById('btn-download-raw');

// Session State
let activeMode = 'encrypt';
let logsHistory = [];

// Dynamic SVG Cipher Wheel Generator
function buildCipherWheel() {
    const svg = document.getElementById('cipher-wheel-svg');
    if (!svg) return;
    svg.innerHTML = ''; // Clear prior nodes

    // Create groups
    const outerG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    outerG.setAttribute('id', 'wheel-outer');
    
    const innerG = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    innerG.setAttribute('id', 'wheel-inner');
    innerG.setAttribute('style', 'transform-origin: 150px 150px; transition: transform 0.45s cubic-bezier(0.4, 0, 0.2, 1);');

    // Outer guide ring
    const oRing = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    oRing.setAttribute('cx', '150');
    oRing.setAttribute('cy', '150');
    oRing.setAttribute('r', '115');
    oRing.setAttribute('fill', 'none');
    oRing.setAttribute('stroke', 'rgba(255, 255, 255, 0.05)');
    oRing.setAttribute('stroke-width', '1.5');
    svg.appendChild(oRing);

    // Inner guide ring
    const iRing = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    iRing.setAttribute('cx', '150');
    iRing.setAttribute('cy', '150');
    iRing.setAttribute('r', '82');
    iRing.setAttribute('fill', 'none');
    iRing.setAttribute('stroke', 'rgba(0, 242, 254, 0.15)');
    iRing.setAttribute('stroke-width', '1.5');
    svg.appendChild(iRing);

    // Center core node
    const hub = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    hub.setAttribute('cx', '150');
    hub.setAttribute('cy', '150');
    hub.setAttribute('r', '5');
    hub.setAttribute('fill', '#00f2fe');
    hub.setAttribute('style', 'filter: drop-shadow(0px 0px 4px rgba(0,242,254,0.6));');
    svg.appendChild(hub);

    // Draw alphabet tags
    for (let i = 0; i < 26; i++) {
        const char = String.fromCharCode(65 + i); // 'A'-'Z'
        const deg = i * (360 / 26);
        const rad = (deg * Math.PI) / 180;

        // Outer Coordinates
        const ox = 150 + 115 * Math.cos(rad);
        const oy = 150 + 115 * Math.sin(rad);
        const oText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        oText.setAttribute('x', ox);
        oText.setAttribute('y', oy + 3.5);
        oText.setAttribute('text-anchor', 'middle');
        oText.setAttribute('fill', '#9ca3af');
        oText.setAttribute('font-size', '10');
        oText.setAttribute('font-family', 'Space Grotesk');
        oText.setAttribute('font-weight', '700');
        oText.setAttribute('transform', `rotate(${deg + 90}, ${ox}, ${oy})`);
        oText.textContent = char;
        outerG.appendChild(oText);

        // Inner Coordinates
        const ix = 150 + 82 * Math.cos(rad);
        const iy = 150 + 82 * Math.sin(rad);
        const iText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        iText.setAttribute('x', ix);
        iText.setAttribute('y', iy + 3);
        iText.setAttribute('text-anchor', 'middle');
        iText.setAttribute('fill', '#00f2fe');
        iText.setAttribute('font-size', '9');
        iText.setAttribute('font-family', 'Space Grotesk');
        iText.setAttribute('font-weight', '700');
        iText.setAttribute('transform', `rotate(${deg + 90}, ${ix}, ${iy})`);
        iText.textContent = char;
        innerG.appendChild(iText);
    }

    svg.appendChild(outerG);
    svg.appendChild(innerG);
}

// Update rotation angle
function setWheelRotation(shift) {
    const inner = document.getElementById('wheel-inner');
    if (inner) {
        // Standardize degrees to match letter rotation
        const deg = (shift % 26) * (360 / 26);
        inner.style.transform = `rotate(-${deg}deg)`;
    }
}

// Security Evaluation Score Card (0-100)
function computeSecurityScore(text, shift) {
    const normShift = ((shift % 26) + 26) % 26;
    if (!text || normShift === 0) return 0;

    let score = 30; // base score for using a valid shift

    // Coprime shifts (odd shifts excluding 13) offer slightly more distribution complexity
    const coprimes = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25];
    if (coprimes.includes(normShift)) {
        score += 15;
    } else if (normShift === 13) {
        score += 5; // ROT13 is weak
    } else {
        score += 10;
    }

    // Text Complexity checks
    if (/[A-Z]/.test(text) && /[a-z]/.test(text)) score += 15; // Mixed case
    if (/\d/.test(text)) score += 10; // Contains numbers
    if (/[^A-Za-z0-9]/.test(text)) score += 15; // Contains symbols

    // Text length scoring
    if (text.length > 150) {
        score += 15;
    } else if (text.length > 50) {
        score += 10;
    } else if (text.length > 10) {
        score += 5;
    }

    return Math.min(score, 100);
}

// Analytics display update helper
function updateAnalytics(durationMs, text, shift) {
    const wordCount = text ? text.trim().split(/\s+/).filter(w => w).length : 0;
    const charCount = text ? text.length : 0;

    analyticsChars.innerText = charCount;
    analyticsWords.innerText = wordCount;
    analyticsShift.innerText = shift;
    analyticsTime.innerText = `${durationMs}ms`;

    const score = computeSecurityScore(text, shift);
    analyticsScoreTxt.innerText = `${score}/100`;
    analyticsScoreBar.style.width = `${score}%`;

    // Dynamic rating colors
    if (score >= 75) {
        analyticsScoreBar.style.backgroundColor = '#22c55e'; // Green
    } else if (score >= 45) {
        analyticsScoreBar.style.backgroundColor = '#eab308'; // Yellow
    } else {
        analyticsScoreBar.style.backgroundColor = '#ef4444'; // Red
    }
}

// Enhanced Toast Banner Alerts
function showToast(message, type = 'success') {
    const existing = document.querySelector('.toast-msg');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = `toast-msg ${type === 'info' ? 'toast-info' : ''}`;
    toast.innerHTML = type === 'success' ? `✓ ${message}` : `ℹ ${message}`;
    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add('show'), 15);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 350);
    }, 2200);
}

// Execution speed wrapper
function calculate() {
    const text = textInput.value;
    const shift = parseInt(shiftInput.value) || 0;
    const shiftNum = toggleNumbers.checked;

    if (!text || text === "Type your plaintext or ciphertext here...") {
        textOutput.value = "";
        updateAnalytics(0, "", shift);
        return;
    }

    const tStart = performance.now();
    let result = "";
    if (activeMode === 'encrypt') {
        result = CaesarCipher.encrypt(text, shift, shiftNum);
    } else {
        result = CaesarCipher.decrypt(text, shift, shiftNum);
    }
    const tEnd = performance.now();
    const duration = (tEnd - tStart).toFixed(2);

    textOutput.value = result;
    updateAnalytics(duration, text, shift);
}

// Clipboard copying
function copyText(text) {
    if (!text) return;
    navigator.clipboard.writeText(text)
        .then(() => {
            showToast('Copied to Clipboard', 'success');
        })
        .catch(err => {
            console.error('Copy failed: ', err);
        });
}

// 📜 Local Storage logs management
function loadHistory() {
    try {
        const stored = localStorage.getItem('metacipher_history');
        logsHistory = stored ? JSON.parse(stored) : [];
        renderHistoryList();
    } catch (e) {
        console.error(e);
        logsHistory = [];
    }
}

function saveHistory() {
    localStorage.setItem('metacipher_history', JSON.stringify(logsHistory));
    renderHistoryList();
}

function appendHistoryItem(type, original, processed, shift) {
    const cleanOrig = original.length > 30 ? original.substring(0, 27) + "..." : original;
    const cleanProc = processed.length > 30 ? processed.substring(0, 27) + "..." : processed;

    const entry = {
        id: Date.now(),
        type,
        origText: original,
        procText: processed,
        label: `${cleanOrig} → ${cleanProc}`,
        shift
    };

    // Remove duplicates
    logsHistory = logsHistory.filter(h => h.label !== entry.label);
    
    // Add to top and limit to 10
    logsHistory.unshift(entry);
    if (logsHistory.length > 10) logsHistory.pop();

    saveHistory();
}

function renderHistoryList() {
    historyContainer.innerHTML = "";
    if (logsHistory.length === 0) {
        historyContainer.innerHTML = '<p class="history-placeholder">No encrypt/decrypt history logs stored.</p>';
        return;
    }

    logsHistory.forEach(item => {
        const row = document.createElement('div');
        row.className = 'history-row';

        const typeLabel = document.createElement('span');
        typeLabel.className = `hist-type ${item.type}`;
        typeLabel.innerText = item.type === 'encrypt' ? 'enc' : 'dec';

        const textSpan = document.createElement('span');
        textSpan.className = 'hist-text';
        textSpan.innerText = item.label;
        textSpan.title = `${item.origText} → ${item.procText}`;

        const actions = document.createElement('div');
        actions.className = 'hist-actions';

        // Load item back to workspace
        const reuseBtn = document.createElement('button');
        reuseBtn.className = 'btn-hist-mini';
        reuseBtn.innerHTML = '🔄';
        reuseBtn.title = "Reuse logs in Workspace";
        reuseBtn.addEventListener('click', () => {
            textInput.value = item.origText;
            shiftInput.value = item.shift;
            syncShiftSlider();
            activeMode = item.type;
            
            // Sync button highlighting
            if (activeMode === 'encrypt') {
                btnEncrypt.classList.add('btn-primary');
                btnEncrypt.classList.remove('btn-secondary');
                btnDecrypt.classList.add('btn-secondary');
                btnDecrypt.classList.remove('btn-primary');
            } else {
                btnDecrypt.classList.add('btn-primary');
                btnDecrypt.classList.remove('btn-secondary');
                btnEncrypt.classList.add('btn-secondary');
                btnEncrypt.classList.remove('btn-primary');
            }

            calculate();
            updateCharCount();
            showToast('Logs loaded back to workspace', 'info');
        });

        // Delete item from list
        const delBtn = document.createElement('button');
        delBtn.className = 'btn-hist-mini';
        delBtn.innerHTML = '❌';
        delBtn.title = "Delete logs row";
        delBtn.addEventListener('click', () => {
            logsHistory = logsHistory.filter(h => h.id !== item.id);
            saveHistory();
            showToast('Logs item deleted', 'info');
        });

        actions.appendChild(reuseBtn);
        actions.appendChild(delBtn);

        row.appendChild(typeLabel);
        row.appendChild(textSpan);
        row.appendChild(actions);

        historyContainer.appendChild(row);
    });
}

// 📁 Exporting File Utilities
function triggerDownload(content, filename, contentType) {
    const blob = new Blob([content], { type: contentType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

function exportTXT() {
    const text = textOutput.value;
    if (!text || text === "Result output will appear here...") {
        showToast('No result output to export!', 'info');
        return;
    }
    triggerDownload(text, `metacipher-output-${Date.now()}.txt`, 'text/plain');
    showToast('Export TXT Completed', 'success');
}

function exportJSON() {
    const orig = textInput.value;
    const proc = textOutput.value;
    const shiftVal = parseInt(shiftInput.value) || 0;
    
    if (!proc || proc === "Result output will appear here...") {
        showToast('No session data to export!', 'info');
        return;
    }

    const report = {
        application: "METACIPHER",
        timestamp: new Date().toISOString(),
        engine: "Caesar Cryptography V1.0",
        parameters: {
            shiftKey: shiftVal,
            mode: activeMode,
            digitShifting: toggleNumbers.checked
        },
        payload: {
            originalText: orig,
            processedText: proc
        },
        metrics: {
            charactersCount: orig.length,
            wordsCount: orig.trim().split(/\s+/).filter(w => w).length,
            securityScore: computeSecurityScore(orig, shiftVal)
        }
    };

    triggerDownload(JSON.stringify(report, null, 2), `metacipher-audit-${Date.now()}.json`, 'application/json');
    showToast('Export JSON Completed', 'success');
}

// Sync counts
function updateCharCount() {
    const text = textInput.value;
    if (text === "Type your plaintext or ciphertext here...") {
        inputCharCount.innerText = "0 chars";
    } else {
        inputCharCount.innerText = `${text.length} chars`;
    }
}

// Sync controllers
function syncShiftSlider() {
    let val = parseInt(shiftInput.value);
    if (isNaN(val)) return;
    let normalized = ((val % 26) + 26) % 26;
    shiftSlider.value = normalized;
    setWheelRotation(normalized);
}

function syncShiftInput() {
    shiftInput.value = shiftSlider.value;
    setWheelRotation(parseInt(shiftSlider.value));
}

// Event hooks
shiftSlider.addEventListener('input', () => {
    syncShiftInput();
    if (toggleLive.checked) calculate();
});

shiftInput.addEventListener('input', () => {
    syncShiftSlider();
    if (toggleLive.checked) calculate();
});

textInput.addEventListener('input', () => {
    updateCharCount();
    if (toggleLive.checked) calculate();
});

toggleNumbers.addEventListener('change', () => {
    if (toggleLive.checked) calculate();
});

btnEncrypt.addEventListener('click', () => {
    activeMode = 'encrypt';
    btnEncrypt.classList.add('btn-primary');
    btnEncrypt.classList.remove('btn-secondary');
    btnDecrypt.classList.add('btn-secondary');
    btnDecrypt.classList.remove('btn-primary');
    calculate();
    
    // Add to history if text is computed
    const orig = textInput.value;
    const proc = textOutput.value;
    if (orig && orig !== "Type your plaintext or ciphertext here...") {
        appendHistoryItem('encrypt', orig, proc, parseInt(shiftInput.value) || 0);
        showToast('Encryption Successful', 'success');
    }
});

btnDecrypt.addEventListener('click', () => {
    activeMode = 'decrypt';
    btnDecrypt.classList.add('btn-primary');
    btnDecrypt.classList.remove('btn-secondary');
    btnEncrypt.classList.add('btn-secondary');
    btnEncrypt.classList.remove('btn-primary');
    calculate();

    const orig = textInput.value;
    const proc = textOutput.value;
    if (orig && orig !== "Type your plaintext or ciphertext here...") {
        appendHistoryItem('decrypt', orig, proc, parseInt(shiftInput.value) || 0);
        showToast('Decryption Successful', 'success');
    }
});

btnClear.addEventListener('click', () => {
    textInput.value = "";
    textOutput.value = "";
    updateCharCount();
    updateAnalytics(0, "", parseInt(shiftInput.value) || 0);
    showToast('Workspace Cleared', 'info');
});

btnCopy.addEventListener('click', () => {
    const text = textOutput.value;
    if (text && text !== "Result output will appear here...") {
        copyText(text);
    } else {
        showToast('No result output to copy!', 'info');
    }
});

// Brute Force Actions
btnBrute.addEventListener('click', () => {
    const text = textInput.value;
    if (!text || text === "Type your plaintext or ciphertext here...") {
        showToast("Please enter input text first!", "info");
        return;
    }

    const shiftNum = toggleNumbers.checked;
    const bruteResults = CaesarCipher.bruteForce(text, shiftNum);

    bruteContainer.innerHTML = "";
    for (let shift = 1; shift <= 25; shift++) {
        const decrypted = bruteResults[shift];

        const row = document.createElement('div');
        row.className = 'brute-row';

        const keyLabel = document.createElement('span');
        keyLabel.className = 'brute-key';
        keyLabel.innerText = `Shift ${String(shift).padStart(2, '0')}`;

        const previewText = document.createElement('span');
        previewText.className = 'brute-text';
        previewText.innerText = decrypted;
        previewText.title = decrypted;

        const copyBtn = document.createElement('button');
        copyBtn.className = 'btn-icon';
        copyBtn.innerText = '📋 Copy';
        copyBtn.addEventListener('click', () => copyText(decrypted));

        row.appendChild(keyLabel);
        row.appendChild(previewText);
        row.appendChild(copyBtn);
        bruteContainer.appendChild(row);
    }
    showToast('Brute Force Analysis Complete', 'success');
});

// Export triggers
btnExportTxt.addEventListener('click', exportTXT);
btnExportJson.addEventListener('click', exportJSON);
btnDownloadRaw.addEventListener('click', exportTXT);

btnClearHistory.addEventListener('click', () => {
    logsHistory = [];
    saveHistory();
    showToast('Logs History Cleared', 'info');
});

// Theme switcher
themeToggle.addEventListener('click', () => {
    const currentTheme = htmlEl.getAttribute('data-theme');
    const newTheme = (currentTheme === 'dark') ? 'light' : 'dark';
    htmlEl.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
});

// ⌨️ Hook Keyboard shortcuts:
// Ctrl + E = Encrypt
// Ctrl + D = Decrypt
// Ctrl + L = Clear Input
// Ctrl + Shift + C = Copy Result
window.addEventListener('keydown', (e) => {
    // Check if ctrl key is held
    if (e.ctrlKey && !e.altKey) {
        const key = e.key.toLowerCase();
        
        if (key === 'e') {
            e.preventDefault();
            btnEncrypt.click();
        } else if (key === 'd') {
            e.preventDefault();
            btnDecrypt.click();
        } else if (key === 'l') {
            e.preventDefault();
            btnClear.click();
        } else if (e.shiftKey && key === 'c') {
            e.preventDefault();
            btnCopy.click();
        }
    }
});

// Initialize on startup
window.addEventListener('DOMContentLoaded', () => {
    buildCipherWheel();
    syncShiftSlider();
    loadHistory();

    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        htmlEl.setAttribute('data-theme', savedTheme);
    }

    textInput.addEventListener('focus', function() {
        if (this.value === "Type your plaintext or ciphertext here...") {
            this.value = "";
        }
    });

    textInput.addEventListener('blur', function() {
        if (this.value.trim() === "") {
            this.value = "Type your plaintext or ciphertext here...";
        }
    });
});
