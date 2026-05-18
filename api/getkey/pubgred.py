from http.server import BaseHTTPRequestHandler
from urllib.parse import quote
import requests


TOKEN_USER = "b8b60726e4ebf47ffe41df8a8d96c869"

SOURCE_URL = "https://keyauth.click/get/duyanh"


def get_redirect_url():
    session = requests.Session()

    response = session.get(
        SOURCE_URL,
        allow_redirects=True,
        timeout=15,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    return response.url


def rut_gon_link(url_can_rut_gon, link_du_phong="", format_response="json"):
    api_url = "https://api.layma.net/api/admin/shortlink/quicklink"

    params = {
        "tokenUser": TOKEN_USER,
        "format": format_response,
        "url": url_can_rut_gon,
        "link_du_phong": link_du_phong
    }

    response = requests.get(
        api_url,
        params=params,
        timeout=15,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    if format_response == "json":
        data = response.json()

        if data.get("success") is True:
            return data.get("html")

        return None

    return response.text.strip()


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            duyanh_url = get_redirect_url()

            layma_link = rut_gon_link(
                url_can_rut_gon=duyanh_url,
                format_response="json"
            )

            if not layma_link:
                self.send_response(500)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write("Không thể rút gọn link".encode("utf-8"))
                return

            self.send_response(302)
            self.send_header("Location", layma_link)
            self.end_headers()

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()

            error_message = f"Lỗi server: {str(e)}"
            self.wfile.write(error_message.encode("utf-8"))