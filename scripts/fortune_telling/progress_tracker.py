#!/usr/bin/env python3
"""
Progress tracking system for fortune-telling analysis
Provides real-time status updates during multi-stage analysis
"""

import sys
import time
from datetime import datetime
from typing import Optional


class ProgressTracker:
    """Track and display analysis progress with color-coded status"""

    def __init__(self):
        self.stages = []
        self.current_stage = None
        self.start_time = None

    def start(self):
        """Start progress tracking"""
        self.start_time = time.time()
        print("\n" + "=" * 80)
        print("🔮 綜合命理分析系統 - 進度追蹤")
        print("=" * 80)

    def add_stage(self, name: str, description: str, emoji: str = "📋"):
        """Register a new stage"""
        stage = {
            'name': name,
            'description': description,
            'emoji': emoji,
            'status': 'pending',
            'start_time': None,
            'end_time': None
        }
        self.stages.append(stage)

    def start_stage(self, name: str):
        """Mark stage as in progress"""
        for stage in self.stages:
            if stage['name'] == name:
                stage['status'] = 'in_progress'
                stage['start_time'] = time.time()
                self.current_stage = stage
                self._print_status()
                break

    def complete_stage(self, name: str):
        """Mark stage as completed"""
        for stage in self.stages:
            if stage['name'] == name:
                stage['status'] = 'completed'
                stage['end_time'] = time.time()
                elapsed = stage['end_time'] - stage['start_time']
                self._print_status(elapsed)
                break

    def fail_stage(self, name: str, error: str):
        """Mark stage as failed"""
        for stage in self.stages:
            if stage['name'] == name:
                stage['status'] = 'failed'
                stage['error'] = error
                self._print_status()
                break

    def _print_status(self, elapsed: Optional[float] = None):
        """Print current progress status"""
        if not self.current_stage:
            return

        status_emoji = {
            'pending': '⏳',
            'in_progress': '🔄',
            'completed': '✅',
            'failed': '❌'
        }

        stage = self.current_stage
        emoji = status_emoji.get(stage['status'], '📋')

        print(f"\n{stage['emoji']} {emoji} {stage['description']}", end='')

        if elapsed:
            print(f" ({elapsed:.1f}s)")
        elif stage['status'] == 'in_progress':
            print(" ...")
        elif stage['status'] == 'failed':
            print(f"\n   ❌ 錯誤: {stage.get('error', 'Unknown error')}")
        else:
            print()

    def show_summary(self):
        """Display final summary"""
        total_time = time.time() - self.start_time
        completed = sum(1 for s in self.stages if s['status'] == 'completed')
        failed = sum(1 for s in self.stages if s['status'] == 'failed')

        print("\n" + "=" * 80)
        print("📊 分析進度總結")
        print("=" * 80)

        for stage in self.stages:
            status_emoji = {
                'pending': '⏳',
                'in_progress': '🔄',
                'completed': '✅',
                'failed': '❌'
            }

            emoji = status_emoji.get(stage['status'], '📋')
            elapsed_text = ""

            if stage['start_time'] and stage['end_time']:
                elapsed = stage['end_time'] - stage['start_time']
                elapsed_text = f" ({elapsed:.1f}s)"

            print(f"{stage['emoji']} {emoji} {stage['description']}{elapsed_text}")

            if stage['status'] == 'failed':
                print(f"   ❌ {stage.get('error', 'Unknown error')}")

        print(f"\n⏱️  總計時間: {total_time:.1f}s ({total_time/60:.1f}min)")
        print(f"✅ 完成: {completed}/{len(self.stages)}")

        if failed > 0:
            print(f"❌ 失敗: {failed}/{len(self.stages)}")

        print("=" * 80)


class AgentProgressTracker:
    """Track individual agent progress during parallel execution"""

    def __init__(self):
        self.agents = {}
        self.start_time = time.time()

    def register_agent(self, agent_name: str, description: str, emoji: str):
        """Register an agent for tracking"""
        self.agents[agent_name] = {
            'name': agent_name,
            'description': description,
            'emoji': emoji,
            'status': 'waiting',
            'start_time': None,
            'end_time': None
        }

    def start_agent(self, agent_name: str):
        """Mark agent as started"""
        if agent_name in self.agents:
            self.agents[agent_name]['status'] = 'running'
            self.agents[agent_name]['start_time'] = time.time()
            self._print_agent_status()

    def complete_agent(self, agent_name: str):
        """Mark agent as completed"""
        if agent_name in self.agents:
            self.agents[agent_name]['status'] = 'completed'
            self.agents[agent_name]['end_time'] = time.time()
            self._print_agent_status()

    def fail_agent(self, agent_name: str, error: str):
        """Mark agent as failed"""
        if agent_name in self.agents:
            self.agents[agent_name]['status'] = 'failed'
            self.agents[agent_name]['error'] = error
            self._print_agent_status()

    def _print_agent_status(self):
        """Print current agent status"""
        print("\n   🤖 專家代理狀態:")

        for agent_name, agent in self.agents.items():
            status_emoji = {
                'waiting': '⏳',
                'running': '🔄',
                'completed': '✅',
                'failed': '❌'
            }

            emoji = status_emoji.get(agent['status'], '📋')
            elapsed_text = ""

            if agent['start_time']:
                if agent['end_time']:
                    elapsed = agent['end_time'] - agent['start_time']
                    elapsed_text = f" ({elapsed:.1f}s)"
                else:
                    elapsed = time.time() - agent['start_time']
                    elapsed_text = f" ({elapsed:.0f}s...)"

            print(f"      {agent['emoji']} {emoji} {agent['description']}{elapsed_text}")

            if agent['status'] == 'failed':
                print(f"         ❌ {agent.get('error', 'Unknown error')}")


# Global tracker instances
_global_tracker: Optional[ProgressTracker] = None
_global_agent_tracker: Optional[AgentProgressTracker] = None


def init_tracker():
    """Initialize global progress tracker"""
    global _global_tracker
    _global_tracker = ProgressTracker()
    _global_tracker.start()
    return _global_tracker


def init_agent_tracker():
    """Initialize global agent progress tracker"""
    global _global_agent_tracker
    _global_agent_tracker = AgentProgressTracker()
    return _global_agent_tracker


def get_tracker() -> Optional[ProgressTracker]:
    """Get global progress tracker"""
    return _global_tracker


def get_agent_tracker() -> Optional[AgentProgressTracker]:
    """Get global agent progress tracker"""
    return _global_agent_tracker
