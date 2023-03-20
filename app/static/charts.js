const ctx = document.getElementById('myChart');

new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ["A", "B", "C", "D"],
        datasets: [
            {
                data: [300, 50, 100, 80],
                borderWidth: 0,
                backgroundColor: ["#723ac3", "#864DD9", "#9762e6", "#a678eb"],
                hoverBackgroundColor: ["#723ac3", "#864DD9", "#9762e6", "#a678eb"],
            },
        ],
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});