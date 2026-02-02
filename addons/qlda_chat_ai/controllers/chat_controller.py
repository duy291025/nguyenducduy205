from odoo import http
from odoo.http import request
from datetime import date
import requests
import re


class QLDAChatController(http.Controller):

    # ==================================================
    # ROUTE CHAT
    # ==================================================
    @http.route('/qlda/chat', type='json', auth='user')
    def chat(self, message=None):
        if not message:
            return {'reply': '❗ Nội dung trống'}

        try:
            reply = self.ai_agent(message)
        except Exception as e:
            reply = f'⚠️ Lỗi AI: {str(e)}'

        self._save_chat('user', message)
        self._save_chat('ai', reply)

        return {'reply': reply}

    # ==================================================
    # SAVE CHAT HISTORY
    # ==================================================
    def _save_chat(self, role, content):
        request.env['qlda.chat.message'].sudo().create({
            'user_id': request.env.user.id,
            'role': role,
            'content': content,
        })

    # ==================================================
    # AI AGENT – RULE FIRST
    # ==================================================
    def ai_agent(self, user_message):
        msg = user_message.lower()

        # ---------- NHÂN SỰ ----------
        if re.search(r'rảnh', msg):
            return self.tool_idle_staff()

        if re.search(r'nhiều việc nhất|bận nhất', msg):
            return self.tool_busy_staff()

        if re.search(r'bao nhiêu nhân sự|nhân sự|nhân viên', msg):
            return self.tool_staff_count()

        # ---------- PHÂN CÔNG ----------
        if re.search(r'phân công|giao việc', msg):
            return self.tool_suggest_assignment()

        # ---------- DỰ ÁN ----------
        if re.search(r'hoàn thành', msg):
            return self.tool_completed_projects()

        # ---------- CÔNG VIỆC ----------
        if re.search(r'công việc|tình trạng', msg):
            return self.tool_task_status()

        # ---------- CHÀO ----------
        if re.search(r'\b(chào|hello|hi)\b', msg):
            return "👋 Chào bạn! Tôi có thể hỗ trợ gì về dự án?"

        # ---------- FALLBACK AI (CÓ CONTEXT) ----------
        return self.ai_fallback_with_context(user_message)

    # ==================================================
    # AI FALLBACK WITH CONTEXT
    # ==================================================
    def ai_fallback_with_context(self, prompt):
        messages = request.env['qlda.chat.message'].sudo().search(
            [('user_id', '=', request.env.user.id)],
            order='id desc',
            limit=5
        )

        context = "\n".join(
            f"{m.role.upper()}: {m.content}" for m in reversed(messages)
        )

        full_prompt = f"""
Bạn là trợ lý quản lý dự án.

LỊCH SỬ HỘI THOẠI:
{context}

CÂU HỎI:
{prompt}
"""

        response = requests.post(
            "http://host.docker.internal:11434/api/generate",
            json={
                "model": "llama3:8b-instruct-q4_0",
                "prompt": full_prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        return response.json().get("response", "🤖 Tôi chưa hiểu rõ.")

    # ==================================================
    # TOOLS – NHÂN SỰ
    # ==================================================
    def tool_staff_count(self):
        staffs = request.env['nhan_vien'].search([])
        return f"👥 Hiện có {len(staffs)} nhân sự."

    def tool_idle_staff(self):
        staffs = request.env['nhan_vien'].search([])
        idle = []

        for s in staffs:
            tasks = request.env['du_an_cong_viec'].search([
                ('assigned_to', '=', s.id),
                ('status', '!=', 'done')
            ])
            if not tasks:
                idle.append(s.name)

        if not idle:
            return "⚠️ Không có nhân sự nào đang rảnh."

        return "🟢 Nhân sự đang rảnh:\n" + "\n".join(f"- {n}" for n in idle)

    def tool_busy_staff(self):
        staffs = request.env['nhan_vien'].search([])
        workload = {}

        for s in staffs:
            count = request.env['du_an_cong_viec'].search_count([
                ('assigned_to', '=', s.id),
                ('status', '!=', 'done')
            ])
            workload[s.name] = count

        busiest = max(workload, key=workload.get)
        return f"🔥 Nhân sự bận nhất: {busiest} ({workload[busiest]} công việc)"

    # ==================================================
    # TOOLS – PHÂN CÔNG
    # ==================================================
    def tool_suggest_assignment(self):
        staffs = request.env['nhan_vien'].search([])
        suggestion = []

        for s in staffs:
            tasks = request.env['du_an_cong_viec'].search([
                ('assigned_to', '=', s.id),
                ('status', '!=', 'done')
            ])
            suggestion.append((s.name, len(tasks)))

        suggestion.sort(key=lambda x: x[1])

        return (
            "🤖 Gợi ý phân công:\n"
            + "\n".join(f"- {n}: {c} công việc" for n, c in suggestion)
        )

    # ==================================================
    # TOOLS – DỰ ÁN & CÔNG VIỆC
    # ==================================================
    def tool_completed_projects(self):
        projects = request.env['quan_ly_du_an'].search([
            ('status', '=', 'completed')
        ])
        if not projects:
            return "❌ Chưa có dự án hoàn thành."

        return "✅ Dự án hoàn thành:\n" + "\n".join(
            f"- {p.name}" for p in projects
        )

    def tool_task_status(self):
        tasks = request.env['du_an_cong_viec'].search([])
        return (
            "📋 Tình trạng công việc:\n"
            f"- Chưa bắt đầu: {len(tasks.filtered(lambda t: t.status == 'to_do'))}\n"
            f"- Đang làm: {len(tasks.filtered(lambda t: t.status == 'in_progress'))}\n"
            f"- Hoàn thành: {len(tasks.filtered(lambda t: t.status == 'done'))}"
        )
