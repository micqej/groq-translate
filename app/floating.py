"""
Floating translation result — shown via AppleScript (reliable on all macOS).
Auto-copies translation to clipboard.
"""

import subprocess


def show_result(original: str, translated: str):
    """Show translation result and auto-copy to clipboard."""
    # Auto-copy
    subprocess.run(["pbcopy"], input=translated.encode(), capture_output=True)

    src = original[:120].replace('"', "'").replace("\\", "")
    tgt = translated[:300].replace('"', "'").replace("\\", "")

    script = f'''
tell application "System Events"
    display dialog "→ {tgt}" & return & return & "(" & "{src}" & ")" ¬
        with title "Prekladač" ¬
        buttons {{"Zavrieť"}} ¬
        default button "Zavrieť" ¬
        giving up after 10
end tell
'''
    subprocess.Popen(["osascript", "-e", script])


def show_status(message: str):
    """Show short status notification."""
    subprocess.run(
        ["osascript", "-e",
         f'display notification "{message}" with title "Prekladač" sound name "Tink"'],
        capture_output=True,
    )
