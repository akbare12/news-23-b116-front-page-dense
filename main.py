#!/usr/bin/env python3
"""news-23 b116 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys
import zlib

MIN_BYTES = 10_000
MAX_BYTES = 1_048_576
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def parse_png(data):
    """Validate the PNG structure; return (width, height) or raise ValueError."""
    if len(data) < 8 or data[:8] != PNG_SIG:
        raise ValueError("bad PNG signature")
    if len(data) < 8 + 25:
        raise ValueError("file too short for IHDR")
    # First chunk must be IHDR, 13 bytes, 1024x1024, bit depth 8, colour type 2/6.
    # Layout after the 8-byte signature: length(4) + type(4) + data(13) + crc(4).
    # So IHDR data sits at bytes 16..29 and its CRC at bytes 29..33.
    ln, ctype = struct.unpack(">I4s", data[8:16])
    if ctype != b"IHDR" or ln != 13:
        raise ValueError("first chunk is not a 13-byte IHDR")
    w, h, depth, ctype_id, comp, filt, inter = struct.unpack(">IIBBBBB", data[16:29])
    if (w, h) != (1024, 1024):
        raise ValueError("expected 1024x1024, got %dx%d" % (w, h))
    if depth != 8 or ctype_id not in (2, 6):
        raise ValueError("expected 8-bit RGB/RGBA, got depth %d colour %d" % (depth, ctype_id))
    if comp != 0 or filt != 0 or inter != 0:
        raise ValueError("compression/filter/interlace must all be 0")
    ihdr_crc = zlib.crc32(b"IHDR" + data[16:29]) & 0xFFFFFFFF
    stored_crc = struct.unpack(">I", data[29:33])[0]
    if ihdr_crc != stored_crc:
        raise ValueError("IHDR CRC mismatch")
    # Walk the remaining chunks: CRC each, require non-empty IDAT payload, IEND last.
    pos = 33
    idat_total = 0
    saw_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError("truncated chunk header")
        clen, cname = struct.unpack(">I4s", data[pos:pos + 8])
        if pos + 12 + clen > len(data):
            raise ValueError("truncated chunk %r" % cname)
        crc = zlib.crc32(cname + data[pos + 8:pos + 8 + clen]) & 0xFFFFFFFF
        if crc != struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])[0]:
            raise ValueError("CRC mismatch in chunk %r" % cname)
        if cname == b"IDAT":
            if clen == 0:
                raise ValueError("empty IDAT chunk")
            idat_total += clen
        if cname == b"IEND":
            if clen != 0:
                raise ValueError("IEND must be 0 bytes")
            if pos + 12 + clen != len(data):
                raise ValueError("trailing data after IEND")
            saw_iend = True
            break
        pos += 12 + clen
    if not saw_iend:
        raise ValueError("missing IEND chunk")
    if idat_total < 1000:
        raise ValueError("IDAT payload too small (%d bytes)" % idat_total)
    return w, h


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    # Refuse to write inside the repo (the grader runs from a read-only copy).
    here_abs = os.path.abspath(here)
    if out_dir_abs == here_abs or out_dir_abs.startswith(here_abs + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must be outside the repo: %s" % out_dir)
    if os.path.isfile(out_dir_abs):
        return fail("MAKEFUN_OUTPUT_DIR is a file, not a directory: %s" % out_dir)
    if not os.path.isfile(src):
        return fail("entry.png not found next to main.py: %s" % src)
    with open(src, "rb") as fh:
        data = fh.read()
    if len(data) < MIN_BYTES:
        return fail("entry.png too small: %d bytes" % len(data))
    if len(data) > MAX_BYTES:
        return fail("entry.png too large: %d bytes" % len(data))
    try:
        w, h = parse_png(data)
    except ValueError as exc:
        return fail(str(exc))
    dst = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(dst) == os.path.abspath(src):
        return fail("output would overwrite the source image")
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(dst, "wb") as fh:
        fh.write(data)
    with open(dst, "rb") as fh:
        written = fh.read()
    if written != data:
        return fail("output differs from source after write")
    print("wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (dst, w, h, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
