from flask import Flask, redirect
import requests

app = Flask(__name__)

# --- Hàm tiện ích rút gọn link ---
def rut_gon_link(url_can_rut_gon, link_du_phong="", format_response="json"):
    api_url = "https://api.layma.net/api/admin/shortlink/quicklink"
    params = {
        "tokenUser": "b8b60726e4ebf47ffe41df8a8d96c869",
        "format": format_response,
        "url": url_can_rut_gon,
        "link_du_phong": link_du_phong
    }

    try:
        response = requests.get(api_url, params=params, timeout=15)
        response.raise_for_status()

        if format_response == "json":
            data = response.json()
            if data.get("success") is True:
                return data.get("html")
            return None
    except Exception as e:
        print("Lỗi request layma:", e)
        return None

# --- Hàm xử lý logic chung ---
def process_and_redirect(target_url):
    session = requests.Session()
    try:
        # Lấy URL đích thực sự
        response = session.get(
            target_url,
            allow_redirects=True,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        final_url = response.url
        
        # Rút gọn và chuyển hướng
        layma_link = rut_gon_link(final_url)
        
        if layma_link:
            return redirect(layma_link, code=302)
        else:
            return {"error": "Không thể tạo link rút gọn từ layma API"}, 500
            
    except Exception as e:
        return {"error": f"Lỗi máy chủ: {str(e)}"}, 500

# ==========================================
# CÁC ENDPOINT API CỦA HỆ THỐNG
# ==========================================

@app.route('/api/pubgred')
def get_key_pubg():
    # Gọi logic dùng chung với URL của PUBG
    url_goc = "https://keyauth.click/get/duyanh"
    return process_and_redirect(url_goc)

@app.route('/api/lqm')
def get_key_lqm():
    # Gọi logic dùng chung với URL của Liên Quân Mobile (thay bằng link thực tế của bạn)
    url_goc = "https://keyauth.click/get/link_lqm_cua_ban" 
    return process_and_redirect(url_goc)

# Bạn có thể tiếp tục thêm các @app.route('/api/...') khác tương tự tại đây.