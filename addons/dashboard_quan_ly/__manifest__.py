{
    'name': 'Dashboard Quản Lý Tổng Hợp',
    'version': '1.0',
    'category': 'Productivity',

    'depends': [
        'web',
        'nhan_su',
        'quan_ly_du_an',
        'quan_ly_cong_viec',
    ],

    'data': [
        'security/ir.model.access.csv',
        'data/dashboard_data.xml',
        'views/dashboard_views.xml',
        'views/menu.xml',
    ],

    'assets': {
        'web.assets_backend': [
            # ✅ Chart.js nội bộ Odoo 15
            'web/static/lib/Chart/Chart.js',

            # CSS
            'dashboard_quan_ly/static/src/css/dashboard.css',

            # JS dashboard (PHẢI SAU Chart.js)
            'dashboard_quan_ly/static/src/js/dashboard_chart.js',
        ],
    },

    'application': True,
    'installable': True,
}
