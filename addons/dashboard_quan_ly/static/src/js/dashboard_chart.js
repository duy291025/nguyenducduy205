odoo.define('dashboard_quan_ly.dashboard_chart', function (require) {
    'use strict';

    const KanbanRenderer = require('web.KanbanRenderer');

    KanbanRenderer.include({

        mounted() {
            this._super(...arguments);
            this._renderDashboardChart();
        },

        _renderDashboardChart() {
            const el = this.el.querySelector('.o_dashboard_chart');
            if (!el) {
                return;
            }

            if (typeof Chart === 'undefined') {
                console.error('❌ Chart.js chưa được load');
                return;
            }

            const ctx = el.querySelector('#dashboard_bar_chart');
            if (!ctx) {
                return;
            }

            const nhanSu = parseInt(el.dataset.nhanSu || 0);
            const duAn = parseInt(el.dataset.duAn || 0);
            const congViec = parseInt(el.dataset.congViec || 0);
            const hoanThanh = parseInt(el.dataset.hoanThanh || 0);

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Nhân sự', 'Dự án', 'Công việc', 'Hoàn thành'],
                    datasets: [{
                        label: 'Thống kê',
                        data: [nhanSu, duAn, congViec, hoanThanh],
                        backgroundColor: [
                            '#06b6d4',
                            '#6366f1',
                            '#f59e0b',
                            '#22c55e'
                        ],
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                }
            });

            console.log('✅ Dashboard chart rendered');
        }
    });
});
