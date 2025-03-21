from odoo import models, fields, api

class ThongKeSuDungPhong(models.Model):
    _name = 'thong_ke_su_dung_phong'
    _description = 'Thống kê tần suất sử dụng phòng họp'
    _auto = False  # Không tạo bảng trong DB vì dữ liệu lấy từ bảng khác

    room_id = fields.Many2one('phong_hop', string="Phòng họp", readonly=True)
    usage_count = fields.Integer(string="Số lần sử dụng", readonly=True)

    def init(self):
        """Tạo view SQL để thống kê số lần sử dụng phòng họp"""
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW thong_ke_su_dung_phong AS (
                SELECT
                    row_number() OVER () AS id,
                    room_id,
                    COUNT(*) AS usage_count
                FROM lich_su_muon_phong
                GROUP BY room_id
            )
        """)
