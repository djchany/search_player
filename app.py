from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Nexon API URL
PLAYER_DATA_URL = "https://open.api.nexon.com/static/fconline/meta/spid.json"
ACTION_IMAGE_URL = "https://fco.dn.nexoncdn.co.kr/live/externalAssets/common/playersAction/p{spid}.png"
PLAYER_IMAGE_URL = "https://fco.dn.nexoncdn.co.kr/live/externalAssets/common/players/p{spid}.png"

# 선수 데이터를 검색하는 함수
def search_players(search_term):
    try:
        response = requests.get(PLAYER_DATA_URL)
        response.raise_for_status()
        data = response.json()

        # 검색어를 포함하는 선수 필터링
        players = [
            {"id": item["id"], "name": item["name"]}
            for item in data if search_term.lower() in item["name"].lower()
        ]
        return players
    except requests.RequestException:
        return {"error": "Nexon API 요청에 실패했습니다. 나중에 다시 시도해주세요."}

# ID에 해당하는 이미지를 가져오는 함수
def fetch_player_images(player_ids):
    image_urls = []
    unique_images = set()  # 중복 방지를 위한 집합

    for player_id in player_ids:
        spid = player_id  # 기본 ID
        reduced_id = player_id[3:].lstrip("0")  # 앞 3자리 제거 및 선행 0 제거
        spid_with_suffix = f"{reduced_id}_24"  # ID에 '_24' 추가

        # 첫 번째 URL 시도
        action_url = ACTION_IMAGE_URL.format(spid=spid)
        if check_url(action_url, unique_images, image_urls):
            continue  # 성공하면 다음 ID로 이동

        # 두 번째 URL 시도
        player_url = PLAYER_IMAGE_URL.format(spid=reduced_id)
        if check_url(player_url, unique_images, image_urls):
            continue  # 성공하면 다음 ID로 이동

        # 세 번째 URL 시도
        player_url_with_suffix = ACTION_IMAGE_URL.format(spid=spid_with_suffix)
        check_url(player_url_with_suffix, unique_images, image_urls)

    return image_urls

# URL 상태를 확인하고 중복 방지 및 URL 추가 처리
def check_url(url, unique_images, image_urls):
    try:
        response = requests.get(url)
        if response.status_code == 200 and url not in unique_images:
            image_urls.append(url)
            unique_images.add(url)
            return True  # URL이 성공적으로 확인됨
    except requests.RequestException:
        pass  # 요청 실패 시 무시
    return False

# 기본 페이지
@app.route("/")
def home():
    return render_template("search_autocomplete.html")

# 자동 완성 엔드포인트
@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    search_term = request.args.get("term", "")
    if not search_term:
        return jsonify([])

    players = search_players(search_term)
    if "error" in players:
        return jsonify([])  # API 실패 시 빈 결과 반환
    return jsonify(list({player["name"] for player in players}))  # 중복 제거 후 반환

# 검색 결과 페이지
@app.route("/results", methods=["POST"])
def results():
    search_term = request.form.get("search-term")
    if not search_term:
        return render_template("results.html", error="검색어를 입력해주세요.", players=[], images=[])

    players = search_players(search_term)
    if "error" in players:
        return render_template("results.html", error=players["error"], players=[], images=[])

    player_ids = [str(player["id"]) for player in players]
    images = fetch_player_images(player_ids)

    return render_template("results.html", players=players, search_term=search_term, images=images)

if __name__ == "__main__":
    app.run(debug=True)
