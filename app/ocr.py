"""
macOS Vision framework OCR — free, built-in, no API needed.
Captures a user-selected region, extracts text.
"""

import subprocess
import tempfile
import os


def capture_and_ocr() -> str:
    """Screenshot selected area, run OCR via macOS Vision, return text."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        img_path = f.name

    try:
        # Interactive screenshot selection (user drags to select area)
        result = subprocess.run(
            ["screencapture", "-i", "-s", img_path],
            capture_output=True,
        )
        if result.returncode != 0 or not os.path.exists(img_path):
            return ""

        # Use macOS Vision via swift one-liner for OCR
        swift_code = f"""
import Vision
import AppKit

let url = URL(fileURLWithPath: "{img_path}")
guard let image = NSImage(contentsOf: url),
      let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {{
    print("")
    exit(0)
}}

let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = true

let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
try? handler.perform([request])

let text = request.results?
    .compactMap {{ $0.topCandidates(1).first?.string }}
    .joined(separator: " ") ?? ""

print(text)
"""
        swift_file = img_path.replace(".png", ".swift")
        with open(swift_file, "w") as f:
            f.write(swift_code)

        ocr_result = subprocess.run(
            ["swift", swift_file],
            capture_output=True,
            text=True,
            timeout=15,
        )
        return ocr_result.stdout.strip()
    except Exception as e:
        return ""
    finally:
        for path in [img_path, img_path.replace(".png", ".swift")]:
            try:
                os.unlink(path)
            except Exception:
                pass
