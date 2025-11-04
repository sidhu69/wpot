# features/check_link.py
import requests, socket, ssl, re, time
from urllib.parse import urlparse

# Optional: install python-whois (pip install python-whois) or use subprocess whois
try:
    import whois
except Exception:
    whois = None

PHISHTANK_CHECK = False  # set True if you add PhishTank integration / API

def _get_hostname(url):
    try:
        parsed = urlparse(url if url.startswith(('http://','https://')) else 'http://' + url)
        return parsed.hostname, parsed.scheme, parsed.geturl()
    except Exception:
        return None, None, None

def _http_check(url, timeout=8):
    try:
        r = requests.get(url, allow_redirects=True, timeout=timeout, headers={"User-Agent":"ProAI/1.0"})
        return {"ok": True, "status": r.status_code, "final_url": r.url, "redirects": len(r.history)}
    except requests.exceptions.RequestException as e:
        return {"ok": False, "error": str(e)}

def _ssl_check(hostname):
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=6) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                # basic checks
                subject = dict(x[0] for x in cert.get('subject', []))
                issued_to = subject.get('commonName', '')
                not_after = cert.get('notAfter')
                return {"valid": True, "issued_to": issued_to, "expires": not_after}
    except Exception as e:
        return {"valid": False, "error": str(e)}

def _whois_age_days(domain):
    try:
        if whois:
            info = whois.whois(domain)
            # prefer creation_date; handle lists
            cd = info.creation_date
            if isinstance(cd, list):
                cd = cd[0]
            if cd:
                delta = (time.time() - cd.timestamp())/86400.0
                return int(delta)
        else:
            # fallback: return None if whois not installed
            return None
    except Exception:
        return None

def _simple_heuristics(url, hostname, final_url, redirects, html_text=None):
    score = 0
    reasons = []

    # suspicious TLDs or very long hostnames
    if re.search(r'\.(tk|ml|cf|gq|ga)$', hostname or ''):
        score += 2; reasons.append("uses risky free TLD")
    if hostname and len(hostname) > 60:
        score += 1; reasons.append("very long hostname")

    # a lot of redirects
    if redirects >= 3:
        score += 1; reasons.append(f"{redirects} redirects")

    # mismatch between hostname and final URL
    if final_url and hostname and hostname not in final_url:
        score += 1; reasons.append("final URL differs from hostname")

    # check for common phishing keywords in url or title
    if re.search(r'login|signin|secure|account|verify|confirm|bank|update|password', url, re.I):
        score += 1; reasons.append("phishy keywords in URL")

    # simple content checks (if HTML provided)
    if html_text:
        # many forms or password fields
        if html_text.count("<form") > 2 or "type=\"password\"" in html_text:
            score += 2; reasons.append("contains multiple forms / password fields")
        # tiny content with redirects meta
        if len(html_text) < 200 and "redirect" in html_text.lower():
            score += 1; reasons.append("tiny page with redirect")

    return score, reasons

def check_link_safety(url):
    hostname, scheme, normalized = _get_hostname(url)
    if not hostname:
        return "❌ Invalid URL format."

    # 1) HTTP reachability
    http = _http_check(normalized)
    if not http["ok"]:
        return f"🚫 Unable to reach URL: {http.get('error')}"

    # 2) SSL check (if https)
    ssl_info = {"valid": None}
    if scheme == "https":
        ssl_info = _ssl_check(hostname)

    # 3) whois age
    age_days = _whois_age_days(hostname)

    # 4) fetch small HTML for heuristics (already fetched by _http_check; reuse)
    try:
        html = requests.get(http["final_url"], timeout=6, headers={"User-Agent":"ProAI/1.0"}).text[:4000]
    except Exception:
        html = None

    score, reasons = _simple_heuristics(url, hostname, http.get("final_url"), http.get("redirects",0), html)

    # 5) optional community checks (PhishTank/URLScan/VT) - not included here
    # If score high, mark suspicious
    verdict = "✅ Likely safe"
    if score >= 3:
        verdict = "🚫 Likely malicious / phishing"
    elif score == 2:
        verdict = "⚠️ Suspicious — caution advised"

    # Combine details summary
    parts = [
        f"{verdict}: {url}",
        f"HTTP status: {http.get('status')}, redirects: {http.get('redirects')}",
    ]
    if ssl_info:
        if ssl_info.get("valid"):
            parts.append(f"SSL: valid, issued to {ssl_info.get('issued_to')}, expires {ssl_info.get('expires')}")
        else:
            parts.append(f"SSL: invalid or missing ({ssl_info.get('error')})")
    if age_days is not None:
        parts.append(f"Domain age: {age_days} days")
    if reasons:
        parts.append("Flags: " + "; ".join(reasons))

    return "\n".join(parts)
