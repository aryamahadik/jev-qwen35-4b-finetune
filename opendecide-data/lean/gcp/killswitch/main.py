"""Budget kill switch for GCP project atmosphor (Cloud Run function, Pub/Sub trigger from a Cloud Billing budget).

Budget messages carry costAmount = spend in the budget period. The budget is created with credits EXCLUDED, so the
cost is the gross usage that eats the free-trial credit (with credits included it would read $0 until real money is
spent), and with a custom 90-day period covering the trial (a monthly budget would reset and never see the total).
  cost >= SOFT_USD  -> delete every Compute Engine instance and every remaining disk in the project (soft kill)
  cost >= HARD_USD  -> also unlink the billing account from the project (hard kill: all paid services stop)
A message with "dryRun": true (only sent by hand for testing) logs what would happen and changes nothing.
"""
import base64
import json
import os

import functions_framework
from googleapiclient import discovery

PROJECT = os.environ["PROJECT_ID"]
SOFT = float(os.environ.get("SOFT_USD", "250"))
HARD = float(os.environ.get("HARD_USD", "285"))


def _compute():
    return discovery.build("compute", "v1", cache_discovery=False)


def delete_all_vms(dry):
    c = _compute()
    acted = []
    agg = c.instances().aggregatedList(project=PROJECT).execute()
    for zone_key, scoped in agg.get("items", {}).items():
        for inst in scoped.get("instances", []):
            zone = zone_key.split("/")[-1]
            acted.append(f"instance {zone}/{inst['name']}")
            if not dry:
                c.instances().delete(project=PROJECT, zone=zone, instance=inst["name"]).execute()
    disks = c.disks().aggregatedList(project=PROJECT).execute()
    for zone_key, scoped in disks.get("items", {}).items():
        for d in scoped.get("disks", []):
            if d.get("users"):
                continue  # still attached; deleted with its instance (auto-delete) or on the next message
            zone = zone_key.split("/")[-1]
            acted.append(f"disk {zone}/{d['name']}")
            if not dry:
                c.disks().delete(project=PROJECT, zone=zone, disk=d["name"]).execute()
    return acted


def disable_billing(dry):
    b = discovery.build("cloudbilling", "v1", cache_discovery=False)
    name = f"projects/{PROJECT}"
    info = b.projects().getBillingInfo(name=name).execute()
    if not info.get("billingEnabled"):
        return "billing already disabled"
    if dry:
        return "would disable billing"
    b.projects().updateBillingInfo(name=name, body={"billingAccountName": ""}).execute()
    return "billing disabled"


@functions_framework.cloud_event
def killswitch(cloud_event):
    msg = json.loads(base64.b64decode(cloud_event.data["message"]["data"]).decode())
    cost = float(msg.get("costAmount", 0.0))
    dry = bool(msg.get("dryRun", False))
    out = {"cost": cost, "budget": msg.get("budgetAmount"), "soft": SOFT, "hard": HARD, "dry_run": dry, "actions": []}
    if cost >= SOFT:
        out["actions"] += delete_all_vms(dry)
    if cost >= HARD:
        out["actions"].append(disable_billing(dry))
    print(json.dumps(out))
