import requests

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
            else:
                return None

        elif format_response == "text":
            return response.text.strip()

    except requests.exceptions.RequestException as e:
        print("Lỗi request:", e)
        return None

    except ValueError:
        print("API không trả về JSON hợp lệ")
        return None

url = "https://keyauth.click/get/duyanh"

session = requests.Session()

response = session.get(
    url,
    allow_redirects=True,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

duyanh_url = response.url

layma_link = rut_gon_link(duyanh_url)
