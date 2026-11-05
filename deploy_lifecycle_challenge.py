# deploy_lifecycle_challenge.py

from collections import defaultdict

# state -> set of states it is allowed to move to
ALLOWED_TRANSITIONS = {
    "queued":      {"approved", "cancelled"},
    "approved":    {"deploying", "cancelled"},
    "deploying":   {"succeeded", "failed"},
    "failed":      {"rolled_back", "deploying"},
    "succeeded":   set(),
    "rolled_back": set(),
    "cancelled":   set(),
}

# (deploy_id, sequence_number, event). Events for a deployment happen in
# sequence_number order, but the list is NOT sorted.
events = [
    ("deploy-4", 3, "deploying"),
    ("deploy-1", 2, "approved"),
    ("deploy-6", 1, "queued"),
    ("deploy-3", 4, "failed"),
    ("deploy-8", 1, "queued"),
    ("deploy-2", 2, "deploying"),
    ("deploy-5", 1, "approved"),
    ("deploy-7", 1, "queued"),
    ("deploy-1", 1, "queued"),
    ("deploy-3", 2, "approved"),
    ("deploy-8", 4, "failed"),
    ("deploy-4", 1, "queued"),
    ("deploy-6", 3, "approved"),
    ("deploy-2", 1, "queued"),
    ("deploy-3", 6, "succeeded"),
    ("deploy-7", 3, "deploying"),
    ("deploy-8", 2, "approved"),
    ("deploy-1", 4, "succeeded"),
    ("deploy-4", 5, "rolled_back"),
    ("deploy-5", 2, "deploying"),
    ("deploy-3", 1, "queued"),
    ("deploy-6", 2, "cancelled"),
    ("deploy-8", 6, "deploying"),
    ("deploy-1", 3, "deploying"),
    ("deploy-4", 2, "approved"),
    ("deploy-2", 3, "succeeded"),
    ("deploy-3", 5, "deploying"),
    ("deploy-7", 2, "approved"),
    ("deploy-8", 3, "deploying"),
    ("deploy-4", 4, "succeeded"),
    ("deploy-3", 3, "deploying"),
    ("deploy-8", 5, "rolled_back"),
]

def find_invalid_deployments(events, allowed_transitions):
    """
    Every deployment must start with a "queued" event, and each later
    event must be a legal transition from the previous event's state.
    Return a dict mapping each INVALID deployment_id to the sequence
    number of its FIRST illegal event. Valid deployments (including ones
    still in progress) should not appear in the result.
    """
    # TODO: implement
    # pass

    # Step 1: Group the events by deployment.
    # Example: {"deploy-1": [(2, "approved"), (1, "queued"), ...], ...}
    events_by_deploy = defaultdict(list)
    for deploy_id, sequence_number, state in events:
        events_by_deploy[deploy_id].append((sequence_number, state))

    # Step 2: Check each deployment's events in order.
    first_illegal_event_by_deploy = {}
    for deploy_id, deploy_events in events_by_deploy.items():
        # Sort by sequence number so the events are in the order they happened.
        deploy_events.sort()
        previous_state = None
        for sequence_number, state in deploy_events:
            # First event must be "queued".
            if previous_state is None:
                is_legal_transition = state == "queued"
            # Later events must be allowed from the previous state.
            else:
                is_legal_transition = state in allowed_transitions.get(previous_state, set())
            # Illegal? Save its sequence number and stop checking this deployment.
            if not is_legal_transition:
                first_illegal_event_by_deploy[deploy_id] = sequence_number
                break  # only the FIRST illegal event counts
            previous_state = state

    # Step 3: Return only the invalid deployments.
    return first_illegal_event_by_deploy


if __name__ == "__main__":
    # Step 4: Find the invalid deployments.
    invalid_deployments = find_invalid_deployments(events, ALLOWED_TRANSITIONS)

    # Step 5: Print each one with its first illegal sequence number.
    print("\nInvalid deployments:")
    for deploy_id_key, sequence_number_value in sorted(invalid_deployments.items()):
        print(f"\033[33m{deploy_id_key}\033[0m > First illegal event at sequence: \033[1;31m{sequence_number_value}\033[0m")
