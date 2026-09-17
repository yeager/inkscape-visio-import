# 0.1.1 — 2026-09-17

- Clean up all temporary input and SVG files after success or failure.
- Preserve binary .vsd parser dispatch for anonymous OLE streams.
- Report invalid page selections instead of silently choosing a different page.
- Report conversion errors through Inkscape AbortExtension.
- Align documented Python requirement with libvisio-ng and add adapter tests.

Validation: five adapter tests with an Inkscape UI stub. Full Inkscape UI integration was not exercised.

