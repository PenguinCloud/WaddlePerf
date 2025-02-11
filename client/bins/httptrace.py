#!/usr/bin/env python3
import subprocess
import json
import sys
import getopt
import statistics

def measure_http_load_time(url):
    try:
        result = subprocess.run(
            ['curl', '-w', '@-', '-o', '/dev/null', '-s', url],
            input='''{
                "url_effective": "%{url_effective}",
                "http_code": %{http_code},
                "time_namelookup": %{time_namelookup},
                "time_connect": %{time_connect},
                "time_appconnect": %{time_appconnect},
                "time_pretransfer": %{time_pretransfer},
                "time_redirect": %{time_redirect},
                "time_starttransfer": %{time_starttransfer},
                "time_total": %{time_total}
            }''',
            text=True,
            capture_output=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        return None

def main(argv):
    url = ''
    tries = 1

    try:
        opts, args = getopt.getopt(argv, "hu:t:", ["url=", "tries="])
    except getopt.GetoptError:
        print("Usage: python httptrace.py -u <URL> -t <TRIES>", file=sys.stderr)
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("Usage: python httptrace.py -u <URL> -t <TRIES>")
            sys.exit()
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("-t", "--tries"):
            tries = int(arg)

    if not url:
        print("URL is required. Usage: python httptrace.py -u <URL> -t <TRIES>", file=sys.stderr)
        sys.exit(2)

    results = []
    for _ in range(tries):
        load_time_data = measure_http_load_time(url)
        if load_time_data:
            results.append(load_time_data)

    if results:
        summary = {
            "min_time": min(result['time_total'] for result in results),
            "mean_time": statistics.mean(result['time_total'] for result in results),
            "max_time": max(result['time_total'] for result in results),
            "all_times": [result['time_total'] for result in results],
            "details": results
        }
        print(json.dumps(summary, indent=4))

if __name__ == "__main__":
    main(sys.argv[1:])
