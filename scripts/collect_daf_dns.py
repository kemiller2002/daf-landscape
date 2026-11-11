#!/usr/bin/env python3
"""Passive, public DNS and certificate-transparency inventory. No scanning or authentication."""
import argparse, csv, datetime as dt, json, pathlib, time, urllib.parse, urllib.request
HOSTS = [
 ("npt.stellartechsol.com","NPT","documented historical Stellar-hosted NPT documents"),
 ("bofa.donorfirst.org","Bank of America","public BofA donor portal"),
 ("tda.donorfirstx.com","Ren DonorFirstX","public Ren-associated terms"),
 ("demo.stellartechsol.com","Stellar iPhi","public demonstration host"),
 ("nptdaf.org","NPT","historical NPT donor-access domain"),
 ("reninc.com","Ren","vendor domain"),
 ("donorfirst.org","DonorFirst","portal domain family"),
 ("donorfirstx.com","DonorFirstX","portal domain family"),
 ("stellartechsol.com","Stellar","legacy vendor domain"),
 ("nptrust.org","NPT","sponsor domain"),
 ("fidelitycharitable.org","Fidelity Charitable","sponsor domain"),
 ("dafgiving360.org","DAFgiving360","sponsor domain"),
 ("ncfgiving.com","NCF","sponsor domain"),
 ("aefonline.org","AEF","sponsor domain"),
 ("tifin.com","TIFIN","vendor domain"),
 ("givechariot.com","Chariot","vendor domain"),
 ("charityvest.org","Charityvest","sponsor domain"),
 ("foundationsource.com","Foundation Source","vendor domain"),
]
RESOLVERS = [("google","https://dns.google/resolve"),("cloudflare","https://cloudflare-dns.com/dns-query")]
TYPES = ("CNAME","A","AAAA","NS","HTTPS")
def fetch(url, headers=None, timeout=18):
    req=urllib.request.Request(url,headers={"User-Agent":"DAF-public-DNS-research/1.0",**(headers or {})})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return json.load(r)
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="research/observations/dns")
    p.add_argument("--ct",action="store_true",help="Query crt.sh for vendor domains; can be slow or rate limited")
    p.add_argument("--hosts-file",help="Optional CSV with hostname,organization,source_note")
    a=p.parse_args()
    hosts=HOSTS[:]
    if a.hosts_file:
        with open(a.hosts_file,newline="") as f:
            for row in csv.DictReader(f): hosts.append((row["hostname"].strip(),row.get("organization",""),row.get("source_note","")))
    out=pathlib.Path(a.out);out.mkdir(parents=True,exist_ok=True)
    timestamp=dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    records=[]; errors=[]
    for host,org,note in dict(((h.lower(),o,n),(h,o,n)) for h,o,n in hosts).values():
        for resolver,base in RESOLVERS:
            for typ in TYPES:
                url=base+"?"+urllib.parse.urlencode({"name":host,"type":typ})
                try:
                    data=fetch(url,{"accept":"application/dns-json"})
                    for ans in data.get("Answer",[]) or []:
                        records.append(dict(observed_at_utc=timestamp,hostname=host,organization=org,source_note=note,resolver=resolver,query_type=typ,rcode=data.get("Status"),answer_name=ans.get("name"),answer_type=ans.get("type"),answer_value=ans.get("data"),ttl=ans.get("TTL"),query_url=url,attribution="unverified"))
                    if not data.get("Answer"):
                        records.append(dict(observed_at_utc=timestamp,hostname=host,organization=org,source_note=note,resolver=resolver,query_type=typ,rcode=data.get("Status"),answer_name="",answer_type="",answer_value="",ttl="",query_url=url,attribution="no answer (not proof of no supplier)"))
                except Exception as e:errors.append(dict(hostname=host,resolver=resolver,query_type=typ,error=str(e)[:250]))
                time.sleep(.12)
    fields=["observed_at_utc","hostname","organization","source_note","resolver","query_type","rcode","answer_name","answer_type","answer_value","ttl","query_url","attribution"]
    with (out/f"dns-{timestamp}.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(records)
    ct=[]
    if a.ct:
        for domain in ("stellartechsol.com","donorfirst.org","donorfirstx.com","reninc.com"):
            url="https://crt.sh/?"+urllib.parse.urlencode({"q":"%."+domain,"output":"json"})
            try:
                data=fetch(url,timeout=35)
                for item in data:
                    for name in (item.get("name_value") or "").splitlines():
                        name=name.strip().lower().removeprefix("*.")
                        if name.endswith("."+domain) or name==domain:
                            ct.append(dict(domain=domain,hostname=name,not_before=item.get("not_before"),not_after=item.get("not_after"),issuer=item.get("issuer_name"),source="crt.sh",attribution="unverified"))
            except Exception as e:errors.append(dict(hostname=domain,resolver="crt.sh",query_type="CT",error=str(e)[:250]))
            time.sleep(1)
        with (out/f"ct-{timestamp}.csv").open("w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=["domain","hostname","not_before","not_after","issuer","source","attribution"]);w.writeheader();w.writerows(ct)
    (out/f"run-{timestamp}.json").write_text(json.dumps({"timestamp_utc":timestamp,"host_count":len(hosts),"dns_rows":len(records),"ct_rows":len(ct),"errors":errors},indent=2)+"\n")
    print(f"DNS rows: {len(records)}; CT rows: {len(ct)}; errors: {len(errors)}")
    if not records: raise SystemExit("No DNS responses; collection failed")
if __name__=="__main__":main()
