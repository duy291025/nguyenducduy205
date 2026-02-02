{
    'name': 'QLDA Chat AI',
    'version': '1.0',
    'summary': 'Chat AI hỗ trợ dự án và công việc',
    'category': 'Productivity',
    'author': 'Bui Anh Duc',

    'depends': [
        'web',
        'quan_ly_du_an',
        'quan_ly_cong_viec',
    ],

    # ✅ PHẢI LOAD VIEW + MENU
    'data': [
        'security/ir.model.access.csv',
        'data/knowledge.xml',
        'views/chat_views.xml',
        'views/chat_menu.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'qlda_chat_ai/static/src/js/chat.js',
            'qlda_chat_ai/static/src/css/chat.css',
        ],
    },

    'installable': True,
    'application': False,
}
