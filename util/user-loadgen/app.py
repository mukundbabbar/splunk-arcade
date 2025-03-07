import re
import time
import httpx
from faker import Faker
from concurrent.futures import ThreadPoolExecutor, as_completed

fake = Faker()

USER_COUNT = 10
URL = "https://splunk-arcade.local/register"

def backoff_retry_request(client, url, data, max_retries=5, backoff_factor=2):
    for attempt in range(max_retries):
        try:
            response = client.post(url, data=data)
            return response
        except Exception:
            if attempt == max_retries - 1:
                raise
            time.sleep(backoff_factor**attempt)

def create_account(client, i):
    response = client.get(URL)
    match = re.search(r'name="csrf_token" type="hidden" value="([^"]+)"', response.text)
    csrf_token = match.group(1) if match else None

    if csrf_token is None:
        raise Exception("couldn't find csrf token...")
    
    password = fake.password()

    payload = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "username": fake.user_name(),
        "email": fake.email(),
        "password": password,
        "password2": password,
        "accept_tos": "y",
        "csrf_token": csrf_token,
    }

    response = backoff_retry_request(client, URL, payload)

    if "You should be redirected automatically to the target URL" in response.text:
        return f"created account for {payload['username']}"
    else:
        return f"failed creating account for {payload['username']}"

def main():
    with httpx.Client(verify=False) as client:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(create_account, client, i) for i in range(USER_COUNT)]
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    print(result)
                except Exception as e:
                    print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()