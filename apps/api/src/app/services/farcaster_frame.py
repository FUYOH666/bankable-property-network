"""Farcaster Frame endpoint helpers for AttestRWA.

A Frame is an interactive HTML page tagged with Open-Graph + `fc:frame:*`
meta tags. Farcaster clients (Warpcast, Supercast, Yup) render the frame
inline in a feed, show the dynamic image, and route button clicks to the
`fc:frame:post_url`.

This module:

- Renders the HTML wrapper for a Frame.
- Renders an SVG status image inline (no external image host needed).
- Exposes one canonical Frame: `Verify Settlement Status` keyed by a
  `dealId` or attestation `uid`.
"""

from __future__ import annotations

from html import escape

FRAME_VERSION = "vNext"
DEFAULT_IMAGE_WIDTH = 1200
DEFAULT_IMAGE_HEIGHT = 630


def frame_html(
    *,
    image_url: str,
    post_url: str,
    title: str = "AttestRWA — Verify Settlement",
    button_1: str = "Verify Settlement",
    button_2: str | None = "Open on BaseScan",
    button_2_link: str | None = None,
    description: str = (
        "On-chain compliance bridge for RWA stablecoin settlements. "
        "Tap to verify a deal's attestation status."
    ),
) -> str:
    """Build the full HTML page with `fc:frame:*` meta tags."""
    meta_lines = [
        '<meta property="fc:frame" content="vNext" />',
        f'<meta property="fc:frame:image" content="{escape(image_url, quote=True)}" />',
        '<meta property="fc:frame:image:aspect_ratio" content="1.91:1" />',
        f'<meta property="fc:frame:post_url" content="{escape(post_url, quote=True)}" />',
        f'<meta property="fc:frame:button:1" content="{escape(button_1, quote=True)}" />',
        '<meta property="fc:frame:button:1:action" content="post" />',
    ]
    if button_2 and button_2_link:
        meta_lines.append(f'<meta property="fc:frame:button:2" content="{escape(button_2, quote=True)}" />')
        meta_lines.append('<meta property="fc:frame:button:2:action" content="link" />')
        meta_lines.append(f'<meta property="fc:frame:button:2:target" content="{escape(button_2_link, quote=True)}" />')

    og_lines = [
        f'<meta property="og:title" content="{escape(title, quote=True)}" />',
        f'<meta property="og:description" content="{escape(description, quote=True)}" />',
        f'<meta property="og:image" content="{escape(image_url, quote=True)}" />',
    ]

    return (
        "<!doctype html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "  <meta charset=\"utf-8\" />\n"
        f"  <title>{escape(title)}</title>\n"
        f"  {''.join(og_lines)}\n"
        f"  {''.join(meta_lines)}\n"
        "</head>\n"
        "<body>\n"
        f"  <h1>{escape(title)}</h1>\n"
        f"  <p>{escape(description)}</p>\n"
        "</body>\n"
        "</html>\n"
    )


def status_svg(
    *,
    decision: str | None,
    deal_id: str | None,
    amount_base_units: int | None = None,
    payee: str | None = None,
) -> str:
    """Render an inline SVG showing the current attestation status."""
    if decision == "approve":
        accent = "#1abc9c"
        symbol = "VERIFIED"
        body_text = "Bank-grade settlement attested on Base Sepolia."
    elif decision == "reject":
        accent = "#e74c3c"
        symbol = "REJECTED"
        body_text = "Payee unverified or capital tainted. Escrow refunds buyer."
    else:
        accent = "#3498db"
        symbol = "PENDING"
        body_text = "Tap Verify Settlement to look up the attestation."

    short_deal = (deal_id or "—")
    if len(short_deal) > 22:
        short_deal = short_deal[:10] + "…" + short_deal[-8:]

    short_payee = (payee or "—")
    if len(short_payee) > 22:
        short_payee = short_payee[:10] + "…" + short_payee[-8:]

    amount_str = (
        f"{amount_base_units / 1_000_000:.2f} USDC"
        if amount_base_units is not None
        else "—"
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {DEFAULT_IMAGE_WIDTH} {DEFAULT_IMAGE_HEIGHT}" width="{DEFAULT_IMAGE_WIDTH}" height="{DEFAULT_IMAGE_HEIGHT}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0b1220"/>
      <stop offset="100%" stop-color="#1a2540"/>
    </linearGradient>
  </defs>
  <rect width="{DEFAULT_IMAGE_WIDTH}" height="{DEFAULT_IMAGE_HEIGHT}" fill="url(#bg)"/>
  <rect x="40" y="40" width="{DEFAULT_IMAGE_WIDTH - 80}" height="{DEFAULT_IMAGE_HEIGHT - 80}" fill="none" stroke="{accent}" stroke-width="3" rx="24"/>
  <text x="80" y="130" font-family="Helvetica, Arial, sans-serif" font-size="42" fill="#ffffff" font-weight="700">AttestRWA</text>
  <text x="80" y="180" font-family="Helvetica, Arial, sans-serif" font-size="22" fill="#9aa3b2">Settlement Attestation Layer for RWA</text>
  <text x="80" y="320" font-family="Helvetica, Arial, sans-serif" font-size="120" fill="{accent}" font-weight="800">{symbol}</text>
  <text x="80" y="380" font-family="Helvetica, Arial, sans-serif" font-size="28" fill="#ffffff">{escape(body_text)}</text>
  <text x="80" y="470" font-family="Helvetica, Arial, sans-serif" font-size="22" fill="#9aa3b2">Deal id  {escape(short_deal)}</text>
  <text x="80" y="510" font-family="Helvetica, Arial, sans-serif" font-size="22" fill="#9aa3b2">Payee    {escape(short_payee)}</text>
  <text x="80" y="550" font-family="Helvetica, Arial, sans-serif" font-size="22" fill="#9aa3b2">Amount   {escape(amount_str)}</text>
  <text x="80" y="600" font-family="Helvetica, Arial, sans-serif" font-size="18" fill="#5b6373">EAS schema 0x1f64ec96…  ·  Base Sepolia (dev fork)  ·  v1.0.0</text>
</svg>
"""
