"""
Output Formatting Module

This module provides functions to format and display task information
in a user-friendly manner.
"""


def display_task(t):
    """
    Display full task details in formatted layout.
    
    Shows task ID, name, status, and multi-line description with
    visual separators for readability.
    
    Args:
        t: Task object with attributes: id, name, status, content
    """
    print("\n" + "=" * 60)
    print(f"  ID     : {t.id}")
    print(f"  Name   : {t.name}")
    print(f"  Status : [{t.status}]")
    print("-" * 60)
    print("  Description:")
    for line in t.content.split('\n'):
        print(f"    {line}")
    print("=" * 60 + "\n")
