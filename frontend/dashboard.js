document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-scan-btn');
    const exportBtn = document.getElementById('export-pdf-btn');
    const logContainer = document.getElementById('scan-logs');
    const resultsSection = document.getElementById('results-section');
    const tableBody = document.getElementById('vuln-table-body');

    // Stats
    const riskScoreDisplay = document.getElementById('risk-score-display');
    const vulnCountDisplay = document.getElementById('vuln-count');
    const passedCountDisplay = document.getElementById('passed-count');

    // State
    let currentScanIndex = -1;

    // Chart
    const ctx = document.getElementById('riskChart').getContext('2d');
    let riskChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Critical', 'High', 'Medium', 'Low', 'Safe'],
            datasets: [{
                data: [0, 0, 0, 0, 100],
                backgroundColor: ['#ef4444', '#f97316', '#f59e0b', '#3b82f6', '#10b981'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'right', labels: { color: '#94a3b8' } }
            }
        }
    });

    function addLog(message) {
        const p = document.createElement('p');
        p.className = 'log-entry';
        p.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
        logContainer.prepend(p);
    }

    startBtn.addEventListener('click', async () => {
        startBtn.disabled = true;
        exportBtn.disabled = true;
        startBtn.textContent = "Scanning...";
        addLog("Initiating vulnerability scan on Mock LLM...");

        try {
            const response = await fetch('http://localhost:8000/api/v1/scan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target_type: 'mock' })
            });

            const data = await response.json();

            // In a real app, we'd get the ID from the response. 
            // Here we assume it's the latest one added to history.
            // We'll fetch history to get the index/ID.
            const historyResponse = await fetch('http://localhost:8000/api/v1/history');
            const history = await historyResponse.json();
            currentScanIndex = history.length - 1;

            addLog("Scan complete. Processing results...");
            displayResults(data);
            exportBtn.disabled = false;

        } catch (error) {
            addLog(`Error: ${error.message}`);
            console.error(error);
        } finally {
            startBtn.disabled = false;
            startBtn.textContent = "🚀 Start New Scan";
        }
    });

    exportBtn.addEventListener('click', async () => {
        if (currentScanIndex === -1) return;

        addLog("Generating PDF report...");
        try {
            const response = await fetch(`http://localhost:8000/api/v1/export/pdf/${currentScanIndex}`);
            if (!response.ok) throw new Error("Failed to generate PDF");

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `scan_report_${new Date().toISOString().slice(0, 10)}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            addLog("PDF report downloaded successfully.");
        } catch (error) {
            addLog(`Error downloading PDF: ${error.message}`);
        }
    });

    function displayResults(data) {
        // Update Stats
        riskScoreDisplay.textContent = Math.round(data.risk_score);
        vulnCountDisplay.textContent = data.failed_tests;
        passedCountDisplay.textContent = data.passed_tests;

        // Show Results Section
        resultsSection.style.display = 'block';
        tableBody.innerHTML = '';

        // Populate Table
        data.vulnerabilities.forEach(vuln => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><span class="severity-badge severity-${vuln.severity.toUpperCase()}">${vuln.severity}</span></td>
                <td>${vuln.module}</td>
                <td>${vuln.name}</td>
                <td style="font-family: monospace; font-size: 0.85rem; color: #cbd5e1;">${vuln.evidence}</td>
            `;
            tableBody.appendChild(row);
        });

        // Update Chart
        const counts = { Critical: 0, High: 0, Medium: 0, Low: 0 };
        data.vulnerabilities.forEach(v => {
            if (counts[v.severity] !== undefined) counts[v.severity]++;
        });

        riskChart.data.datasets[0].data = [
            counts.Critical,
            counts.High,
            counts.Medium,
            counts.Low,
            data.passed_tests
        ];
        riskChart.update();

        addLog(`Found ${data.failed_tests} vulnerabilities. Risk Score: ${data.risk_score}`);
    }
});
