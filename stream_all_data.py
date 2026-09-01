"""
Master Streaming Script
Launches all producers and display consumer for end-to-end data streaming demo
Usage: python stream_all_data.py [bootstrap_servers] [duration_seconds]
"""

import os
import sys
import subprocess
import logging
import time
import signal
from typing import List
from pathlib import Path

logger = logging.getLogger(__name__)


class StreamingManager:
    """Manages all streaming producers and consumers"""

    def __init__(self, bootstrap_servers: str = "localhost:9092", duration: int = None):
        self.bootstrap_servers = bootstrap_servers
        self.duration = duration
        self.processes: List[subprocess.Popen] = []
        self.project_root = Path(__file__).parent

    def start_open_meteo_producer(self):
        """Start Open-Meteo weather producer"""
        print(f"\n{'-'*70}")
        print("🌤️  STARTING OPEN-METEO WEATHER PRODUCER")
        print(f"{'-'*70}")

        cmd = [
            sys.executable,
            "-m",
            "energy_kafka.producers.openmeteo_producer",
            self.bootstrap_servers,
        ]
        if self.duration:
            cmd.append(str(self.duration))

        try:
            proc = subprocess.Popen(
                cmd,
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
            self.processes.append(proc)
            print(f"✅ Open-Meteo producer started (PID: {proc.pid})")
            return proc
        except Exception as e:
            print(f"❌ Failed to start Open-Meteo producer: {e}")
            return None

    def start_synthetic_producer(self):
        """Start Synthetic India energy producer"""
        print(f"\n{'-'*70}")
        print("📊 STARTING SYNTHETIC INDIA ENERGY PRODUCER")
        print(f"{'-'*70}")

        cmd = [
            sys.executable,
            "-m",
            "energy_kafka.producers.synthetic_india_producer",
            self.bootstrap_servers,
        ]
        if self.duration:
            cmd.append(str(self.duration))

        try:
            proc = subprocess.Popen(
                cmd,
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
            self.processes.append(proc)
            print(f"✅ Synthetic producer started (PID: {proc.pid})")
            return proc
        except Exception as e:
            print(f"❌ Failed to start Synthetic producer: {e}")
            return None

    def start_display_consumer(self):
        """Start real-time display consumer"""
        print(f"\n{'-'*70}")
        print("📺 STARTING REAL-TIME DATA DISPLAY")
        print(f"{'-'*70}")

        cmd = [
            sys.executable,
            "-m",
            "energy_kafka.consumers.display_consumer",
            "--bootstrap-servers",
            self.bootstrap_servers,
        ]

        try:
            proc = subprocess.Popen(
                cmd,
                cwd=str(self.project_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
            self.processes.append(proc)
            print(f"✅ Display consumer started (PID: {proc.pid})")
            return proc
        except Exception as e:
            print(f"❌ Failed to start display consumer: {e}")
            return None

    def print_banner(self):
        """Print welcome banner"""
        print("\n" + "=" * 100)
        print("╔" + "═" * 98 + "╗")
        print("║" + " " * 98 + "║")
        print("║" + "🚀 AI ENERGY CONTROL TOWER - STREAMING DATA PIPELINE 🚀".center(98) + "║")
        print("║" + " " * 98 + "║")
        print("║" + "Streaming all data sources through Kafka in real-time".center(98) + "║")
        print("║" + " " * 98 + "║")
        print("╚" + "═" * 98 + "╝")
        print("=" * 100 + "\n")

    def print_info(self):
        """Print connection info"""
        print(f"{'='*100}")
        print("📋 STREAMING CONFIGURATION")
        print(f"{'='*100}")
        print(f"Bootstrap Servers:    {self.bootstrap_servers}")
        print(f"Producers:            Open-Meteo Weather + Synthetic India Energy")
        print(f"Data Topics:          weather-data, grid-demand, generation-data, price-data, anomaly-alerts")
        print(f"Display Mode:         Real-time console with colored output")

        if self.duration:
            print(f"Duration:             {self.duration} seconds")
        else:
            print(f"Duration:             Continuous (until Ctrl+C)")

        print(f"{'='*100}\n")

    def start_all(self):
        """Start all producers and consumer"""
        self.print_banner()
        self.print_info()

        # Start producers with slight delays
        print("🚀 Launching all producers...\n")

        self.start_open_meteo_producer()
        time.sleep(2)  # Delay to ensure connection

        self.start_synthetic_producer()
        time.sleep(2)  # Delay to ensure connection

        # Start display (this will read from both producers)
        print("\nWaiting for producers to initialize...")
        time.sleep(3)

        self.start_display_consumer()

        print("\n" + "=" * 100)
        print("✅ ALL COMPONENTS STARTED SUCCESSFULLY!")
        print("=" * 100)
        print("\n📊 Streaming data from:")
        print("  ✓ Open-Meteo (Weather Data)")
        print("  ✓ Synthetic India (Energy Demand & Generation)")
        print("\n📡 Display is live on the console above")
        print("\n🛑 Press Ctrl+C to stop all services\n")

        return True

    def monitor_processes(self):
        """Monitor running processes"""
        while True:
            # Check if display consumer is still running
            if self.processes:
                display_proc = self.processes[-1]  # Last process is display consumer
                if display_proc.poll() is not None:
                    print("\n📺 Display consumer stopped")
                    break

            time.sleep(1)

    def cleanup(self):
        """Stop all processes"""
        print(f"\n\n{'='*100}")
        print("🛑 STOPPING ALL SERVICES...")
        print(f"{'='*100}\n")

        for i, proc in enumerate(self.processes, 1):
            if proc and proc.poll() is None:
                print(f"Stopping process {i} (PID: {proc.pid})...")
                try:
                    proc.terminate()
                    proc.wait(timeout=5)
                    print(f"  ✓ Process {i} stopped")
                except subprocess.TimeoutExpired:
                    proc.kill()
                    print(f"  ✓ Process {i} killed")
                except Exception as e:
                    print(f"  ❌ Error stopping process {i}: {e}")

        print(f"\n{'='*100}")
        print("✅ ALL SERVICES STOPPED")
        print(f"{'='*100}\n")


def main():
    """Main entry point"""
    # Parse arguments
    bootstrap_servers = sys.argv[1] if len(sys.argv) > 1 else "localhost:9092"
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else None

    # Create manager
    manager = StreamingManager(bootstrap_servers=bootstrap_servers, duration=duration)

    # Setup signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        manager.cleanup()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Start all components
        if manager.start_all():
            # Monitor until user interrupts
            manager.monitor_processes()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        manager.cleanup()
        sys.exit(1)

    finally:
        manager.cleanup()


if __name__ == "__main__":
    main()
