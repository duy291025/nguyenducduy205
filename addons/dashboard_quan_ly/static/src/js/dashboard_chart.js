odoo.define('dashboard_quan_ly.dashboard_chart', function (require) {
    'use strict';

    const KanbanRenderer = require('web.KanbanRenderer');

    KanbanRenderer.include({
        // Sử dụng on_attach_callback để đảm bảo Canvas đã hiển thị trên màn hình
        on_attach_callback: function () {
            this._super.apply(this, arguments);
            this._renderDashboardChart();
        },

        _renderDashboardChart: function () {
            const self = this;
            // Tìm container chứa biểu đồ
            const el = this.$el.find('.o_dashboard_chart')[0];
            
            if (!el) {
                return;
            }

            if (typeof Chart === 'undefined') {
                console.error('❌ Chart.js chưa được load. Kiểm tra lại manifest!');
                return;
            }

            const ctx = el.querySelector('#dashboard_bar_chart');
            if (!ctx) {
                return;
            }

            // Hủy biểu đồ cũ nếu đã tồn tại (tránh lỗi lồng biểu đồ khi reload)
            if (this.myChart) {
                this.myChart.destroy();
            }

            // Lấy dữ liệu từ dataset (đảm bảo XML dùng t-att-data-...)
            const nhanSu = parseInt(el.dataset.nhanSu || 0);
            const duAn = parseInt(el.dataset.duAn || 0);
            const congViec = parseInt(el.dataset.congViec || 0);
            const hoanThanh = parseInt(el.dataset.hoanThanh || 0);

            // Khởi tạo biểu đồ và lưu vào biến của Renderer
            this.myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Nhân sự', 'Dự án', 'Công việc', 'Hoàn thành'],
                    datasets: [{
                        label: 'Số lượng thực tế',
                        data: [nhanSu, duAn, congViec, hoanThanh],
                        backgroundColor: [
                            '#06b6d4', // Cyan
                            '#6366f1', // Indigo
                            '#f59e0b', // Amber
                            '#22c55e'  // Green
                        ],
                        borderWidth: 1,
                        borderRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1 // Chỉ hiện số nguyên
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            display: true,
                            position: 'top'
                        }
                    }
                }
            });

            console.log('✅ Dashboard chart rendered successfully');
        }
    });
});