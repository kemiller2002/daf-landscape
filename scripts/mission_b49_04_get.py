"""Robots-checked fetcher (stdlib, functional). Usage: python3 -I get.py CACHE_DIR LOG_CSV URL [URL...]
Fetches only if robots.txt allows every listed agent; 404 robots = no restriction; other non-200 = blocked."""
import sys, os, csv, hashlib, ssl, urllib.request, urllib.robotparser, urllib.error, datetime
from urllib.parse import urlparse
from functools import lru_cache

UA = "research-script/1.0"
AGENTS = ("*", UA, "ClaudeBot", "anthropic-ai", "Claude-User", "Claude-Web", "Claude-SearchBot")
CTX = ssl.create_default_context(cafile=os.environ.get("SSL_CERT_FILE", "/root/.ccr/ca-bundle.crt"))

def http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=40, context=CTX) as r:
            return r.status, r.read(), r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        return e.code, b"", ""
    except Exception as e:
        return 0, str(e).encode(), ""

@lru_cache(maxsize=None)
def robots(host):
    st, body, _ = http_get(f"https://{host}/robots.txt")
    if st == 404:
        return ("no robots (404)", None)
    if st != 200:
        return (f"robots HTTP {st}", False)
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(body.decode("utf-8", "replace").splitlines())
    return ("robots 200", rp)

def verdict(url):
    host = urlparse(url).netloc
    note, rp = robots(host)
    if rp is None:
        return True, note
    if rp is False:
        return False, note
    denied = [a for a in AGENTS if not rp.can_fetch(a, url)]
    return (not denied), note + ("; disallowed for " + ",".join(denied) if denied else "; allowed all agents")

def fetch(cache, url):
    ok, note = verdict(url)
    path = os.path.join(cache, hashlib.sha1(url.encode()).hexdigest()[:16])
    if not ok:
        return dict(url=url, robots=note, status="blocked", bytes=0, path="")
    st, body, ct = http_get(url)
    ext = ".pdf" if (b"%PDF" == body[:4]) else ".html"
    if st == 200:
        with open(path + ext, "wb") as f:
            f.write(body)
    return dict(url=url, robots=note, status=str(st) + (" " + body.decode('utf-8','replace')[:80] if st == 0 else ""), bytes=len(body), path=(path + ext) if st == 200 else "")

def main(argv):
    cache, log, urls = argv[1], argv[2], argv[3:]
    rows = list(map(lambda u: {**fetch(cache, u), "fetched": datetime.date.today().isoformat()}, urls))
    new = not os.path.exists(log)
    with open(log, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["fetched", "url", "robots", "status", "bytes", "path"])
        if new: w.writeheader()
        w.writerows(rows)
    print("\n".join(f"{r['status']}\t{r['bytes']}\t{r['robots'][:70]}\t{r['url']}\t{r['path']}" for r in rows))

if __name__ == "__main__":
    main(sys.argv)
