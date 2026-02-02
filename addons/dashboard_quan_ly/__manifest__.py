{
    'name': 'Dashboard Quản Lý Tổng Hợp',
    'version': '1.0',
    'summary': 'Dashboard tổng hợp nhân sự, dự án, công việc',
    'category': 'Productivity',
    'author': 'Your Name',

    'depends': [
        'nhan_su',
        'quan_ly_du_an',
        'quan_ly_cong_viec',
    ],

    'data': [
        'security/ir.model.access.csv',

        # 🔥 PHẢI LOAD RECORD TRƯỚC
        'data/dashboard_data.xml',

        # 🔥 SAU ĐÓ MỚI LOAD VIEW
        'views/dashboard_views.xml',
        'views/menu.xml',
    ],

    'application': True,
}
