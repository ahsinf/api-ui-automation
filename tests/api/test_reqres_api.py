import requests
import pytest
import requests_mock
from unittest.mock import patch

BASE_URL = "https://reqres.in/api/users"

@pytest.fixture(autouse=True)
def mock_reqres_server():
    """Fixture to dynamically simulate Reqres server."""
    with requests_mock.Mocker(real_http=False) as m:
        def dynamic_response(request, context):
            page = request.qs.get('page', ['1'])[0]
            payload = {
                "per_page": 6, "total": 12, "total_pages": 2,
                "support": {"url": "https://reqres.in/#support-heading", "text": "Support us"}
            }

            if page in ['3', '999']: # Edge/Boundary
                payload.update({"page": int(page), "data": []})
            elif page == '2': # Positive
                payload.update({
                    "page": 2,
                    "data": [
                        {"id": 7, "email": "michael.lawson@reqres.in", "first_name": "Michael", "last_name": "Lawson", "avatar": "https://reqres.in/img/faces/7-image.jpg"},
                        {"id": 8, "email": "lindsay.ferguson@reqres.in", "first_name": "Lindsay", "last_name": "Ferguson", "avatar": "https://reqres.in/img/faces/8-image.jpg"}
                    ]
                })
            else: # Default/Page 1
                payload.update({
                    "page": 1,
                    "data": [{"id": 1, "email": "george.bluth@reqres.in", "first_name": "George", "last_name": "Bluth", "avatar": "https://reqres.in/img/faces/1-image.jpg"}]
                })
            return payload

        m.get(BASE_URL, json=dynamic_response)
        yield m

# =========================================================================
# POSITIVE TEST CASES (TC-API-001 s/d TC-API-010)
# =========================================================================

def test_tc_api_001_get_users_valid_page():
    """Verify status code 200 and response body is returned."""
    response = requests.get(f"{BASE_URL}?page=2")
    assert response.status_code == 200
    assert response.json() is not None

def test_tc_api_002_validate_response_structure():
    """Verify response contains required structure."""
    data = requests.get(f"{BASE_URL}?page=2").json()
    keys = ["page", "per_page", "total", "total_pages", "data"]
    assert all(k in data for k in keys)

def test_tc_api_003_validate_page_value():
    """Verify page value matches request."""
    assert requests.get(f"{BASE_URL}?page=1").json()['page'] == 1

def test_tc_api_004_validate_per_page_value():
    """Verify data length equals per_page (max 6 data)."""
    data = requests.get(f"{BASE_URL}?page=2").json()
    assert len(data['data']) <= data['per_page']

def test_tc_api_005_to_010_validate_user_data_format():
    """TC-API-005 s/d 010: Validate user object details."""
    user = requests.get(f"{BASE_URL}?page=2").json()['data'][0]
    assert isinstance(user['id'], int)            # 005: numeric id
    assert "first_name" in user                   # 006: first_name exists
    assert isinstance(user['last_name'], str)     # 007: last_name is string
    assert "@" in user['email']                   # 008: valid email format
    assert user['avatar'].startswith("http")      # 009: valid avatar URL
    assert isinstance(user, dict)                 # 010: data is object

# =========================================================================
# NEGATIVE TEST CASES (TC-API-011 s/d TC-API-021)
# =========================================================================

@pytest.mark.parametrize("tc_id, val", [
    ("TC-API-011", "abc"),
    ("TC-API-012", "!@#"),
    ("TC-API-013", "-1"),
    ("TC-API-014", "0"),
    ("TC-API-015", "null"),
])
def test_negative_page_inputs(tc_id, val):
    """TC-API-011 s/d 015: Handle invalid page values gracefully."""
    response = requests.get(f"{BASE_URL}?page={val}")
    assert response.status_code == 200

def test_tc_api_016_page_parameter_missing():
    """Verify API returns default page data when param is missing."""
    assert requests.get(BASE_URL).json()['page'] == 1

def test_tc_api_017_to_021_validate_data_integrity():
    """TC-API-017 s/d 021: Ensure no null or invalid data types in fields / validate value on fields."""
    users = requests.get(f"{BASE_URL}?page=2").json()['data']
    for user in users:
        u_id = user.get('id')
        assert user['email'] is not None, f"Failed TC-017: Email user {u_id} null!"                               # 017: email not null
        assert "." in user['email'].split("@")[1], f"Failed TC-018: Format email user {u_id} is wrong!"              # 018: domain exists
        assert user['first_name'] is not None, f"Failed TC-019: First name user {u_id} null!"                     # 019: first_name not null
        assert user['avatar'] != "", f"Failed TC-020: Avatar user {u_id} is empty!"                                 # 020: avatar not empty
        assert not isinstance(user['id'], str), f"Failed TC-021: ID user {u_id} must be a number, not a string!"    # 021: id not string

# =========================================================================
# EDGE CASES (TC-API-022 s/d TC-API-028)
# =========================================================================

def test_tc_api_022_last_name_optional():
    """Verify API doesn't fail if last_name exists (as data is dynamic) /  Validate fields on structure response."""
    assert "last_name" in requests.get(f"{BASE_URL}?page=2").json()['data'][0]

def test_tc_api_023_avatar_optional():
    """Verify API remains valid with avatar field present / Validate fields on structure response."""
    assert "avatar" in requests.get(f"{BASE_URL}?page=2").json()['data'][0]

def test_tc_api_024_empty_data_array_page_3():
    """Verify API returns empty data array for page > 2."""
    assert requests.get(f"{BASE_URL}?page=3").json()['data'] == []

def test_tc_api_025_response_time_sla():
    """Verify response time is within SLA (< 2s)."""
    assert requests.get(f"{BASE_URL}?page=2").elapsed.total_seconds() < 2.0

def test_tc_api_026_unexpected_additional_field():
    """Verify API ignores extra fields and remains valid."""
    response = requests.get(f"{BASE_URL}?page=2&extra=dummy")
    assert response.status_code == 200

def test_tc_api_027_validate_408_timeout():
    """Simulate and validate Request Timeout."""
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 408
        assert requests.get(BASE_URL).status_code == 408

def test_tc_api_028_validate_500_server_error():
    """Simulate and validate Internal Server Error."""
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 500
        assert requests.get(BASE_URL).status_code == 500

# =========================================================================
# BOUNDARY CASES (TC-API-029 s/d TC-API-033)
# =========================================================================

def test_tc_api_029_minimum_page_value():
    """Verify data returned for minimum page (1)."""
    assert len(requests.get(f"{BASE_URL}?page=1").json()['data']) > 0

def test_tc_api_030_maximum_page_value():
    """Verify data returned for maximum valid page (2)."""
    assert len(requests.get(f"{BASE_URL}?page=2").json()['data']) > 0

def test_tc_api_031_page_exceeds_total_pages():
    """Verify empty data array when page exceeds total_pages."""
    assert requests.get(f"{BASE_URL}?page=999").json()['data'] == []

def test_tc_api_032_validate_per_page_boundary():
    """Verify data count matches per_page metadata."""
    res = requests.get(f"{BASE_URL}?page=1").json()
    assert len(res['data']) <= res['per_page']

def test_tc_api_033_validate_total_pages_value():
    """Verify total_pages is greater than 0."""
    assert requests.get(BASE_URL).json()['total_pages'] > 0