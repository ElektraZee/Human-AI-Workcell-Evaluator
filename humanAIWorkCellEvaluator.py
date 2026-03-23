# dependencies
import numpy as np
import pandas as pd


# class initialization and parameters
class WorkCellSimulation:
    def __init__(
        self,
        p_machine=0.85,
        p_human=0.95,
        t_machine=1.0,
        t_override=0.5,
        uncertainty_threshold=0.15,
        noise_threshold=0.05,
        n_parts=200,
    ):
        """Initialize the work cell simulator."""
        self.p_machine = p_machine
        self.p_human = p_human
        self.t_machine = t_machine
        self.t_override = t_override
        self.uncertainty_threshold = uncertainty_threshold
        self.noise_threshold = noise_threshold
        self.n_parts = n_parts

    def noisy(self, base: float) -> float:
        """Apply uniform noise to a base probability and clip to [0,1]."""
        delta = np.random.uniform(-self.noise_threshold, self.noise_threshold)
        return float(np.clip(base + delta, 0.0, 1.0))

    # Mode A: Machine Only
    def simulate_machine_only(self) -> pd.DataFrame:
        """Simulate n_parts where only the machine acts."""
        logs = []
        for _ in range(self.n_parts):
            p = self.noisy(self.p_machine)
            correct = np.random.rand() < p
            cycle_time = self.t_machine
            logs.append([correct, cycle_time, 0])

        return pd.DataFrame(logs, columns=["correct", "cycle_time", "human_intervention"])
    
    # Mode B: Human In The Loop
    def simulate_human_in_loop(self) -> pd.DataFrame:
        """Simulate n_parts with possible human intervention based on uncertainty."""
        logs = []
        for _ in range(self.n_parts):
            p_machine = self.noisy(self.p_machine)

            # Machine confidence → distance from uncertainty midpoint (0.5), scaled 0..1
            confidence = abs(p_machine - 0.5) * 2

            # Decision logic: if confidence is low, human intervenes
            if confidence < self.uncertainty_threshold:
                correct = np.random.rand() < self.p_human
                cycle_time = self.t_machine + self.t_override
                intervention = 1
            else:
                correct = np.random.rand() < p_machine
                cycle_time = self.t_machine
                intervention = 0

            logs.append([correct, cycle_time, intervention])

        return pd.DataFrame(logs, columns=["correct", "cycle_time", "human_intervention"])


if __name__ == "__main__":
    # quick smoke test
    sim = WorkCellSimulation(n_parts=10)
    df1 = sim.simulate_machine_only()
    df2 = sim.simulate_human_in_loop()
    print("Machine-only sample:\n", df1.head())
    print("Human-in-loop sample:\n", df2.head())
