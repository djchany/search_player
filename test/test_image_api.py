import requests

# 테스트할 API URL
ACTION_IMAGE_URL = "https://fco.dn.nexoncdn.co.kr/live/externalAssets/common/playersAction/p{spid}.png"
PLAYER_IMAGE_URL = "https://fco.dn.nexoncdn.co.kr/live/externalAssets/common/players/p{spid}.png"

# 테스트할 선수 ID 목록
test_ids = [
    "101000123",  # 정상적으로 존재할 가능성이 높은 ID
    "201000456",  # 대체 URL 시도 가능
    "999999999",  # 없는 ID 테스트
]

# 이미지 URL 요청 테스트
for player_id in test_ids:
    spid = f"{player_id}"  # 'p' 접두사 추가
    print(f"Testing ID: {player_id}")

    try:
        # 첫 번째 URL 시도
        action_url = ACTION_IMAGE_URL.format(spid=spid)
        response = requests.get(action_url)
        if response.status_code == 200:
            print(f"Success! Image found at: {action_url}")
            continue  # 성공 시 다음 ID로 이동
        else:
            print(f"Failed at ACTION_IMAGE_URL: {action_url}")

        # 두 번째 URL 시도
        reduced_id = player_id[3:].lstrip("0")  # ID 축소 (앞 3자리 제거 및 선행 0 제거)
        spid = f"{reduced_id}"
        player_url = PLAYER_IMAGE_URL.format(spid=spid)
        response = requests.get(player_url)
        if response.status_code == 200:
            print(f"Success! Image found at: {player_url}")
        else:
            print(f"Failed at PLAYER_IMAGE_URL: {player_url}")

    except requests.RequestException as e:
        print(f"Error testing ID {player_id}: {e}")

    print("-" * 50)
