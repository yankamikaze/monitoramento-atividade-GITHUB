document.addEventListener('DOMContentLoaded', () => {
    const generateBtn = document.getElementById('generate-btn');
    const usernameInput = document.getElementById('username');
    const yearInput = document.getElementById('year');
    const heatmapContainer = document.getElementById('heatmap');
    const statsDiv = document.getElementById('stats');
    const errorDiv = document.getElementById('error-message');
    const tooltip = document.getElementById('tooltip');

    generateBtn.addEventListener('click', fetchAndRender);

    async function fetchAndRender() {
        const username = usernameInput.value.trim();
        const year = yearInput.value.trim();

        if (!username || !year) {
            errorDiv.textContent = 'Please enter both username and year.';
            return;
        }

        errorDiv.textContent = '';
        statsDiv.textContent = 'Loading...';
        heatmapContainer.innerHTML = '';

        try {
            const response = await fetch(`/api/prs/${username}?year=${year}`);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to fetch data');
            }

            let statsHtml = `<strong>${data.total_prs} atividades em ${year}</strong>`;
            statsDiv.innerHTML = statsHtml;
            renderHeatmap(year, data.prs_by_date);

        } catch (error) {
            errorDiv.textContent = error.message;
            statsDiv.textContent = '';
        }
    }

    function renderHeatmap(year, prsByDate) {
        // Calculate days to show
        const startDate = new Date(`${year}-01-01T12:00:00Z`);
        const endDate = new Date(`${year}-12-31T12:00:00Z`);
        
        let startDay = startDate.getUTCDay(); // 0 is Sunday
        
        // Adjust start date to the beginning of the week (Sunday)
        const current = new Date(startDate);
        current.setUTCDate(current.getUTCDate() - startDay);
        
        const weeks = [];
        let currentWeek = [];
        
        while (current <= endDate || current.getUTCDay() !== 0) {
            const dateStr = current.toISOString().split('T')[0];
            const isCurrentYear = current.getUTCFullYear() == year;
            
            let prs = [];
            let count = 0;
            if (isCurrentYear && prsByDate[dateStr]) {
                prs = prsByDate[dateStr];
                count = prs.length;
            }

            currentWeek.push({
                date: dateStr,
                count: count,
                prs: prs,
                inYear: isCurrentYear
            });

            if (current.getUTCDay() === 6) {
                weeks.push(currentWeek);
                currentWeek = [];
            }
            
            current.setUTCDate(current.getUTCDate() + 1);
        }

        weeks.forEach(week => {
            const weekDiv = document.createElement('div');
            weekDiv.className = 'week';
            
            week.forEach(day => {
                const cell = document.createElement('div');
                cell.className = 'cell';
                
                if (day.inYear) {
                    let level = 0;
                    if (day.count > 0 && day.count <= 2) level = 1;
                    else if (day.count > 2 && day.count <= 5) level = 2;
                    else if (day.count > 5 && day.count <= 8) level = 3;
                    else if (day.count > 8) level = 4;
                    
                    cell.classList.add(`level-${level}`);
                    
                    cell.addEventListener('mouseover', (e) => {
                        showTooltip(e, day);
                    });
                    
                    cell.addEventListener('mouseout', hideTooltip);
                }
                
                weekDiv.appendChild(cell);
            });
            
            heatmapContainer.appendChild(weekDiv);
        });
    }

    function showTooltip(event, day) {
        // Convert date to Brazilian format DD/MM/YYYY
        const [y, m, d] = day.date.split('-');
        const brDate = `${d}/${m}/${y}`;
        
        const plural = day.count === 1 ? 'atividade' : 'atividades';
        let html = `<strong>${day.count} ${plural}</strong> em ${brDate}`;
        
        tooltip.innerHTML = html;
        tooltip.style.opacity = 1;
        
        const rect = event.target.getBoundingClientRect();
        
        // Center horizontally above the cell
        let left = rect.left + window.scrollX + (rect.width / 2) - (tooltip.offsetWidth / 2);
        let top = rect.top + window.scrollY - tooltip.offsetHeight - 10;
        
        tooltip.style.left = `${left}px`;
        tooltip.style.top = `${top}px`;
    }

    function hideTooltip() {
        tooltip.style.opacity = 0;
    }

    function escapeHtml(unsafe) {
        return unsafe
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }

    // Auto-load if username is present
    if (usernameInput.value.trim() !== '') {
        fetchAndRender();
    }
});
