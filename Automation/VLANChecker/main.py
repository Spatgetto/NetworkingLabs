from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get


def normalize_vlans(vlans):
    """Keep the VLAN attributes we want to compare."""
    return {
        str(vlan_id): {
            "name": details.get("name"),
            "status": details.get("status"),
        }
        for vlan_id, details in vlans.items()
    }


nr = InitNornir(config_file="config.yml")

# Retrieve VLAN information from every switch.
results = nr.run(
    task=napalm_get,
    getters=["get_vlans"],
)

# Display the raw Nornir task results for troubleshooting.
print_result(results)

# Collect successful results and report failures.
switch_vlans = {}

for hostname, multi_result in results.items():
    if multi_result.failed:
        print(f"\nERROR: Could not retrieve VLANs from {hostname}")
        continue

    vlan_data = multi_result[0].result["get_vlans"]
    switch_vlans[hostname] = normalize_vlans(vlan_data)

if len(switch_vlans) < 2:
    print("\nNeed at least two successfully queried switches to compare.")
    raise SystemExit(1)

# Use the first successful switch as the reference.
reference_name = next(iter(switch_vlans))
reference = switch_vlans[reference_name]

print(f"\nReference switch: {reference_name}")
print(f"Reference VLANs: {reference}")

all_identical = True

for hostname, vlans in switch_vlans.items():
    if hostname == reference_name:
        continue

    if vlans == reference:
        print(f"\nPASS: {hostname} matches {reference_name}")
        continue

    all_identical = False
    print(f"\nFAIL: {hostname} differs from {reference_name}")

    reference_ids = set(reference)
    current_ids = set(vlans)

    missing = reference_ids - current_ids
    extra = current_ids - reference_ids

    if missing:
        print(f"  Missing VLANs: {sorted(missing, key=int)}")

    if extra:
        print(f"  Extra VLANs: {sorted(extra, key=int)}")

    # Identify differences in name or status for shared VLAN IDs.
    for vlan_id in sorted(reference_ids & current_ids, key=int):
        if reference[vlan_id] != vlans[vlan_id]:
            print(f"  VLAN {vlan_id}:")
            print(f"    Reference: {reference[vlan_id]}")
            print(f"    Actual:    {vlans[vlan_id]}")

if all_identical:
    print("\nSUCCESS: All successfully queried switches have identical VLANs.")
else:
    print("\nVLAN differences detected.")
