import time

def parse_header_int(headers, key):
    value = headers.get(key)
    return int(value) if value else 0

def handle_rate_limiting(response):
    headers = response.headers
    requests_remaining = parse_header_int(headers, 'x-ratelimit-remaining')
    retry_after_millis = 1000 * parse_header_int(headers, 'retry-after')

    if requests_remaining > 0:
        tier = parse_header_int(headers, 'x-front-tier')
        print(f"Tier {tier} resource burst limit reached")
    else:
        global_limit = parse_header_int(headers, 'x-ratelimit-limit')
        print(f"Global rate limit of {global_limit} reached")

    time.sleep(retry_after_millis / 1000)