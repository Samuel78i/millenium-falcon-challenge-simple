import json


class C3PO:
    """Calculate odds of reaching Endor successfully."""

    def __init__(self, millenniumFalconJsonFilePath):
        """Load the millennium falcon data."""
        # Read the JSON file
        with open(millenniumFalconJsonFilePath, 'r') as f:
            data = json.load(f)

        self.autonomy = data['autonomy']
        self.routes = data['routes']

        # Build a graph from routes
        # graph[planet] = list of (neighbor, travel_time) tuples
        self.graph = {}
        for route in self.routes:
            origin = route['origin']
            dest = route['destination']
            time = route.get('travel_time') or route.get('travelTime')

            # Add route in both directions
            if origin not in self.graph:
                self.graph[origin] = []
            if dest not in self.graph:
                self.graph[dest] = []

            self.graph[origin].append((dest, time))
            self.graph[dest].append((origin, time))

    def giveMeTheOdds(self, empireJsonFilePath):
        """Calculate probability of success."""
        # Read empire data
        with open(empireJsonFilePath, 'r') as f:
            empire_data = json.load(f)

        countdown = empire_data['countdown']
        bounty_hunters = empire_data['bounty_hunters']

        # Create a set of (planet, day) where bounty hunters are present
        hunters_set = set()
        for hunter in bounty_hunters:
            hunters_set.add((hunter['planet'], hunter['day']))

        # Use BFS to find path with minimum encounters
        # State: (planet, day, fuel, encounters)
        from collections import deque

        start_state = ('Tatooine', 0, self.autonomy, 0)
        queue = deque([start_state])

        # Track visited states: (planet, day, fuel) -> min encounters
        visited = {('Tatooine', 0, self.autonomy): 0}

        min_encounters = None  # Track minimum encounters to reach Endor

        while queue:
            planet, day, fuel, encounters = queue.popleft()

            # Skip if we exceeded countdown
            if day > countdown:
                continue

            # Check if we reached destination
            if planet == 'Endor':
                if min_encounters is None or encounters < min_encounters:
                    min_encounters = encounters
                continue

            # Skip if we already found a better solution
            if min_encounters is not None and encounters >= min_encounters:
                continue

            # Try traveling to neighbors
            if planet in self.graph:
                for neighbor, travel_time in self.graph[planet]:
                    # Can we travel with current fuel?
                    if travel_time <= fuel:
                        new_day = day + travel_time
                        new_fuel = fuel - travel_time
                        new_encounters = encounters

                        # Check if bounty hunters are there
                        if (neighbor, new_day) in hunters_set:
                            new_encounters += 1

                        # Should we visit this state?
                        state_key = (neighbor, new_day, new_fuel)
                        if state_key not in visited or visited[state_key] > new_encounters:
                            visited[state_key] = new_encounters
                            queue.append((neighbor, new_day, new_fuel, new_encounters))

            # Try refueling (if not at max fuel)
            if fuel < self.autonomy:
                new_day = day + 1
                new_encounters = encounters

                # Check if bounty hunters are here while refueling
                if (planet, new_day) in hunters_set:
                    new_encounters += 1

                state_key = (planet, new_day, self.autonomy)
                if state_key not in visited or visited[state_key] > new_encounters:
                    visited[state_key] = new_encounters
                    queue.append((planet, new_day, self.autonomy, new_encounters))

            # Try waiting (if at max fuel)
            if fuel == self.autonomy:
                new_day = day + 1
                new_encounters = encounters

                # Check if bounty hunters are here while waiting
                if (planet, new_day) in hunters_set:
                    new_encounters += 1

                state_key = (planet, new_day, self.autonomy)
                if state_key not in visited or visited[state_key] > new_encounters:
                    visited[state_key] = new_encounters
                    queue.append((planet, new_day, self.autonomy, new_encounters))

        # Calculate probability
        if min_encounters is None:
            return 0.0  # No path found

        # Formula: probability = 0.9^k where k is number of encounters
        probability = 0.9 ** min_encounters
        return probability


# Simple test function
def test_examples():
    """Test all 4 examples."""
    examples = [
        ("Example 1", "examples/example1/millennium-falcon.json", "examples/example1/empire.json", 0.0),
        ("Example 2", "examples/example2/millennium-falcon.json", "examples/example2/empire.json", 0.81),
        ("Example 3", "examples/example3/millennium-falcon.json", "examples/example3/empire.json", 0.9),
        ("Example 4", "examples/example4/millennium-falcon.json", "examples/example4/empire.json", 1.0),
    ]

    print("Testing examples...")
    for name, falcon_file, empire_file, expected in examples:
        c3po = C3PO(falcon_file)
        result = c3po.giveMeTheOdds(empire_file)
        status = "PASS" if abs(result - expected) < 0.001 else "FAIL"
        print(f"{name}: {result:.2f} (expected {expected:.2f}) - {status}")


if __name__ == "__main__":
    test_examples()