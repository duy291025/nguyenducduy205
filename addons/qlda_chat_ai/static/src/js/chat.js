odoo.define('qlda_chat_ai.chat', function (require) {
    "use strict";

    const domReady = require('web.dom_ready');
    const rpc = require('web.rpc');

    domReady(function () {

        // Tránh load nhiều lần
        if (document.querySelector('.qlda-chat-icon')) return;

        /* ========== ICON CHAT ========== */
        const icon = document.createElement('div');
        icon.className = 'qlda-chat-icon';
        icon.innerHTML = `<img src="/qlda_chat_ai/static/src/img/favicon.png"/>`;
        document.body.appendChild(icon);

        /* ========== SIDEBAR CHAT ========== */
        const popup = document.createElement('div');
        popup.className = 'qlda-chat-popup';

        popup.innerHTML = `
            <div class="qlda-chat-header">
                <span>🤖 AI Support</span>
                <span id="qlda-chat-close" style="cursor:pointer;">❮</span>
            </div>

            <div class="qlda-chat-body" id="qlda-chat-body"></div>

            <div class="qlda-chat-footer">
                <input id="qlda-chat-input" placeholder="Nhập câu hỏi..." />
                <button id="qlda-chat-send">Gửi</button>
            </div>
        `;
        document.body.appendChild(popup);

        /* ========== OPEN / CLOSE ========== */
        icon.onclick = () => {
            popup.classList.add('open');
            popup.querySelector('#qlda-chat-input').focus();
        };

        popup.querySelector('#qlda-chat-close').onclick = () => {
            popup.classList.remove('open');
        };

        /* ========== SEND MESSAGE ========== */
        const sendMessage = async () => {
            const input = popup.querySelector('#qlda-chat-input');
            const body = popup.querySelector('#qlda-chat-body');
            const msg = input.value.trim();
            if (!msg) return;

            body.innerHTML += `<div class="msg user">${msg}</div>`;
            input.value = '';
            body.scrollTop = body.scrollHeight;

            // Loading
            const loading = document.createElement('div');
            loading.className = 'msg ai';
            loading.innerText = '🤖 Đang suy nghĩ...';
            body.appendChild(loading);
            body.scrollTop = body.scrollHeight;

            try {
                const res = await rpc.query({
                    route: '/qlda/chat',
                    params: { message: msg },
                });

                loading.remove();
                body.innerHTML += `<div class="msg ai">${res.reply}</div>`;
            } catch (e) {
                loading.remove();
                body.innerHTML += `<div class="msg ai error">⚠️ Lỗi kết nối AI</div>`;
            }

            body.scrollTop = body.scrollHeight;
        };

        popup.querySelector('#qlda-chat-send').onclick = sendMessage;

        popup.querySelector('#qlda-chat-input').addEventListener('keydown', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    });
});
