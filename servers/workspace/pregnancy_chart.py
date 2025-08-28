
html_content = """
<div style="
    font-family: 'Roboto', sans-serif;
    color: #e5e7eb;
    background-color: transparent;
    padding: 20px;
    border-radius: 8px;
">
    <h2 style="font-size: 1.5em; margin-bottom: 20px; color: #f1f5f9; text-align: center;">
        Average Pregnancies per Age
    </h2>
    <canvas id="pregnancyChart" width="800" height="400" style="background-color: #2d3748; border-radius: 8px;"></canvas>

    <script>
        const canvas = document.getElementById('pregnancyChart');
        const ctx = canvas.getContext('2d');

        const data = [
            {"Age": 21, "Average Pregnancies": 1.19},
            {"Age": 22, "Average Pregnancies": 1.82},
            {"Age": 23, "Average Pregnancies": 2.05},
            {"Age": 24, "Average Pregnancies": 2.23},
            {"Age": 25, "Average Pregnancies": 2.59},
            {"Age": 26, "Average Pregnancies": 3.03},
            {"Age": 27, "Average Pregnancies": 3.17},
            {"Age": 28, "Average Pregnancies": 3.67},
            {"Age": 29, "Average Pregnancies": 4.50},
            {"Age": 30, "Average Pregnancies": 4.33},
            {"Age": 31, "Average Pregnancies": 4.40},
            {"Age": 32, "Average Pregnancies": 4.73},
            {"Age": 33, "Average Pregnancies": 4.44},
            {"Age": 34, "Average Pregnancies": 5.40},
            {"Age": 35, "Average Pregnancies": 5.00},
            {"Age": 36, "Average Pregnancies": 5.00},
            {"Age": 37, "Average Pregnancies": 5.67},
            {"Age": 38, "Average Pregnancies": 6.50},
            {"Age": 39, "Average Pregnancies": 7.20},
            {"Age": 40, "Average Pregnancies": 7.00},
            {"Age": 41, "Average Pregnancies": 7.10},
            {"Age": 42, "Average Pregnancies": 7.10},
            {"Age": 43, "Average Pregnancies": 7.88},
            {"Age": 44, "Average Pregnancies": 7.60},
            {"Age": 45, "Average Pregnancies": 7.25},
            {"Age": 46, "Average Pregnancies": 7.67},
            {"Age": 47, "Average Pregnancies": 7.60},
            {"Age": 48, "Average Pregnancies": 9.00},
            {"Age": 49, "Average Pregnancies": 7.00},
            {"Age": 50, "Average Pregnancies": 8.60},
            {"Age": 51, "Average Pregnancies": 8.80},
            {"Age": 52, "Average Pregnancies": 6.40},
            {"Age": 53, "Average Pregnancies": 6.75},
            {"Age": 54, "Average Pregnancies": 7.80},
            {"Age": 55, "Average Pregnancies": 6.25},
            {"Age": 56, "Average Pregnancies": 10.00},
            {"Age": 57, "Average Pregnancies": 8.00},
            {"Age": 58, "Average Pregnancies": 7.60},
            {"Age": 59, "Average Pregnancies": 3.50},
            {"Age": 60, "Average Pregnancies": 6.00},
            {"Age": 61, "Average Pregnancies": 5.50},
            {"Age": 62, "Average Pregnancies": 5.00},
            {"Age": 63, "Average Pregnancies": 6.00},
            {"Age": 64, "Average Pregnancies": 8.00},
            {"Age": 65, "Average Pregnancies": 3.33},
            {"Age": 66, "Average Pregnancies": 6.00},
            {"Age": 67, "Average Pregnancies": 6.00},
            {"Age": 68, "Average Pregnancies": 8.00},
            {"Age": 69, "Average Pregnancies": 5.00},
            {"Age": 70, "Average Pregnancies": 4.00},
            {"Age": 72, "Average Pregnancies": 2.00},
            {"Age": 81, "Average Pregnancies": 9.00}
        ];

        const chartWidth = canvas.width;
        const chartHeight = canvas.height;
        const padding = 50;
        const barWidth = 15;
        const maxPregnancies = 10; // Max value on Y-axis based on data
        const scaleY = (chartHeight - 2 * padding) / maxPregnancies;

        // Clear canvas
        ctx.clearRect(0, 0, chartWidth, chartHeight);

        // Draw Y-axis
        ctx.strokeStyle = '#94a3b8';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(padding, padding);
        ctx.lineTo(padding, chartHeight - padding);
        ctx.stroke();

        // Draw X-axis
        ctx.beginPath();
        ctx.moveTo(padding, chartHeight - padding);
        ctx.lineTo(chartWidth - padding, chartHeight - padding);
        ctx.stroke();

        // Draw Y-axis labels
        ctx.fillStyle = '#f1f5f9';
        ctx.font = '12px Roboto';
        ctx.textAlign = 'right';
        for (let i = 0; i <= maxPregnancies; i += 2) { // Labels for every 2 pregnancies
            const y = chartHeight - padding - (i * scaleY);
            ctx.fillText(i, padding - 10, y + 4);
            ctx.beginPath();
            ctx.moveTo(padding, y);
            ctx.lineTo(padding + 5, y);
            ctx.stroke();
        }
        ctx.fillText('Pregnancies', padding - 30, chartHeight / 2); // Y-axis title

        // Draw X-axis title
        ctx.textAlign = 'center';
        ctx.fillText('Age', chartWidth / 2, chartHeight - padding + 30);

        // Draw bars
        ctx.fillStyle = '#0284c7'; // Bar color
        let currentX = padding + 20; // Starting X for the first bar

        data.forEach(item => {
            const barHeight = item["Average Pregnancies"] * scaleY;
            const x = currentX;
            const y = chartHeight - padding - barHeight;

            ctx.fillRect(x, y, barWidth, barHeight);

            // Draw Age label below X-axis
            ctx.fillStyle = '#cbd5e1';
            ctx.font = '10px Roboto';
            ctx.textAlign = 'center';
            ctx.fillText(item.Age, x + barWidth / 2, chartHeight - padding + 15);

            // Draw value label above bar
            ctx.fillStyle = '#f8fafc';
            ctx.font = '10px Roboto';
            ctx.textAlign = 'center';
            ctx.fillText(item["Average Pregnancies"].toFixed(2), x + barWidth / 2, y - 5);

            currentX += barWidth + 5; // Move to the next bar position
        });
    </script>
</div>
"""
print(html_content)
