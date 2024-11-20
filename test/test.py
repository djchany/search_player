import requests

# Nexon API URL 템플릿
ACTION_IMAGE_URL = "https://fco.dn.nexoncdn.co.kr/live/externalAssets/common/playersAction/p{spid}.png"
PLAYER_IMAGE_URL = "https://fco.dn.nexoncdn.co.kr/live/externalAssets/common/players/p{spid}.png"

# 세 가지 URL 조건을 검사하는 함수
def test_image_urls(player_ids):
    results = []
    for player_id in player_ids:
        spid = player_id  # 기본 ID
        reduced_id = player_id[3:].lstrip("0")  # 앞 3자리 제거 및 선행 0 제거
        spid_with_suffix = f"{reduced_id}_24"  # ID에 '_24' 추가

        # 첫 번째 URL 시도
        action_url = ACTION_IMAGE_URL.format(spid=spid)
        action_status = check_url(action_url)

        # 두 번째 URL 시도
        player_url = PLAYER_IMAGE_URL.format(spid=reduced_id)
        player_status = check_url(player_url)

        # 세 번째 URL 시도
        player_url_with_suffix = ACTION_IMAGE_URL.format(spid=spid_with_suffix)
        suffix_status = check_url(player_url_with_suffix)

        results.append({
            "ID": player_id,
            "Action URL": {"url": action_url, "status": action_status},
            "Player URL": {"url": player_url, "status": player_status},
            "Player URL with _24": {"url": player_url_with_suffix, "status": suffix_status},
        })

    return results

# URL 상태를 확인하는 함수
def check_url(url):
    try:
        response = requests.get(url)
        return response.status_code == 200  # 성공 여부 반환
    except requests.RequestException:
        return False  # 요청 실패

# 테스트 실행
if __name__ == "__main__":
    # 테스트용 ID 리스트
    player_ids = ["214188350", "188350", "101000051"]

    # 결과 확인
    results = test_image_urls(player_ids)
    for result in results:
        print(f"\nID: {result['ID']}")
        print(f"Action URL: {result['Action URL']['url']} - {'Success' if result['Action URL']['status'] else 'Fail'}")
        print(f"Player URL: {result['Player URL']['url']} - {'Success' if result['Player URL']['status'] else 'Fail'}")
        print(f"Player URL with _24: {result['Player URL with _24']['url']} - {'Success' if result['Player URL with _24']['status'] else 'Fail'}")
