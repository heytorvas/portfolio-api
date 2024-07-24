def user_default_payload() -> dict:
    return {
        "name": "Test 1",
        "email": "test@test.com",
        "phone": "123",
        "password": "abc",
    }


def education_default_payload(user: str = None) -> dict:
    payload = {
        "degree": {"en": "Degree English", "pt": "Degree Portuguese"},
        "school": {"en": "School English", "pt": "School Portuguese"},
        "course": {"en": "Course English", "pt": "Course Portuguese"},
        "date_from": "2024-01",
        "date_to": "2024-02",
    }
    if user:
        payload["user"] = user
    return payload


def experience_default_payload(user: str = None) -> dict:
    payload = {
        "company": "Company",
        "date_from": "2024-01",
        "date_to": "2024-02",
        "stack": ["Python"],
        "details": [
            {
                "role": {"en": "Role English", "pt": "Role Portuguese"},
                "project": {"en": "Project English", "pt": "Project Portuguese"},
                "description": [
                    {"en": "Description English", "pt": "Description Portuguese"}
                ],
            }
        ],
    }
    if user:
        payload["user"] = user
    return payload

def about_default_payload(user: str = None) -> dict:
    payload = {
        'address': {
            'city': 'City',
            'state': 'State',
            'country': 'Country',
        },
        'social_network': {
            'website': 'https://website',
            'github': 'https://github',
            'linkedin': 'https://linkedin'
        },
        'summary': {
            'en': 'Summary English',
            'pt': 'Summary Portuguese'
        }
    }
    if user:
        payload['user'] = user
    return payload
