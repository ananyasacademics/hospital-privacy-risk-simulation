"""Main entry point for Hospital Privacy Risk Simulation."""

from src.simulation.generator import generate_access_events, save_events_csv


def main() -> None:
    output_path = "data/generated/report_run/sample_events.csv"

    events = generate_access_events(num_events=100, seed=42)

    save_events_csv(events, output_path)

    print(f"Saved {len(events)} events to {output_path}")


if __name__ == "__main__":
    main()