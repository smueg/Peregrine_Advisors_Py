# blast_radius_challenge.py

from collections import defaultdict, deque

# Each entry is (caller, callee): "caller depends on callee".
dependencies = [
    ("checkout", "payments"),
    ("reports", "warehouse"),
    ("web", "checkout"),
    ("search", "index"),
    ("payments", "auth"),
    ("warehouse", "etl"),
    ("web", "auth"),
    ("admin", "auth"),
    ("index", "storage"),
    ("etl", "reports"),
    ("mobile-api", "checkout"),
    ("payments", "ledger"),
    ("cdn", "web"),
    ("ledger", "storage"),
    ("admin", "reports"),
]

def find_affected_services(dependencies, failed_service):
    """
    If `failed_service` goes down, every service that depends on it,
    directly or transitively, is affected. Return a sorted list of all
    affected services. Do not include `failed_service` itself.
    """
    # TODO: implement
    # pass

    # Step 1: For each service, list who calls it (flip the arrows).
    # Example: {"auth": ["payments", "web", "admin"], ...}
    callers_by_service = defaultdict(list)
    for caller_service, callee_service in dependencies:
        callers_by_service[callee_service].append(caller_service)

    # Step 2: Start from the failed service and work outward.
    affected_services = set()
    services_to_visit = deque([failed_service])
    while services_to_visit:
        # Take the next service off the to-do list.
        current_service = services_to_visit.popleft()
        # Every caller of it is affected.
        for caller_service in callers_by_service[current_service]:
            # Not seen yet? Mark it affected and check its callers later.
            if caller_service not in affected_services:
                affected_services.add(caller_service)
                services_to_visit.append(caller_service)

    # Step 3: Remove the failed service itself (a loop can add it back).
    affected_services.discard(failed_service)

    # Step 4: Return the affected services in A-Z order.
    return sorted(affected_services)


if __name__ == "__main__":
    # Step 5: Print the affected services for each test failure.
    # ", ".join() turns the list into plain text without [ ] and quotes.
    for svc in ["auth", "etl", "storage", "cdn"]:
        affected_services = find_affected_services(dependencies, svc)
        print(f"\nService Name: \033[33m{svc}\033[0m")
        print(f"Affected Services: \033[1;31m{', '.join(affected_services) or 'None'}\033[0m")
