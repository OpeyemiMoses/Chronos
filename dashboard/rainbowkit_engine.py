# Authentic RainbowKit Design System & Functional Engine
# Replicating the official RainbowKit 2-column wide modal, authentic ConnectButton,
# Chain Switcher Modal, Account Modal, deterministic gradient avatar, and real Web3 hooks.

RAINBOWKIT_CSS = """
/* ==========================================================================
   AUTHENTIC RAINBOWKIT DESIGN SYSTEM
   ========================================================================== */

/* 1. RainbowKit Connect Button & Header Widget */
.rk-connect-btn {
  background: #1A1B1F;
  color: #FFFFFF;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 14px;
  font-weight: 700;
  padding: 8px 16px;
  border-radius: 12px;
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1);
  user-select: none;
}

.rk-connect-btn:hover {
  background: #272A30;
  transform: translateY(-1px);
  box-shadow: 0px 6px 18px rgba(0, 0, 0, 0.16);
}

.rk-connect-btn:active {
  transform: scale(0.98);
}

.rk-rainbow-dot-icon {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: conic-gradient(#FF494A, #FF8700, #FFD600, #00D369, #0075FF, #7A00FF, #FF494A);
  display: inline-block;
  box-shadow: 0 0 6px rgba(0, 117, 255, 0.4);
}

/* Connected Dual-Pill Widget */
.rk-connected-widget {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  user-select: none;
}

.rk-chain-pill {
  background: #FFFFFF;
  color: #1A1B1F;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  padding: 6px 12px;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 13.5px;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
  transition: all 0.15s ease;
}

.rk-chain-pill:hover {
  background: #F4F4F6;
  border-color: rgba(0, 0, 0, 0.15);
}

.rk-account-pill {
  background: #FFFFFF;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 12px;
  padding: 3px 4px 3px 10px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
  transition: all 0.15s ease;
}

.rk-account-pill:hover {
  background: #F4F4F6;
  border-color: rgba(0, 0, 0, 0.15);
}

.rk-balance-label {
  font-family: var(--font-terminal);
  font-size: 12px;
  font-weight: 700;
  color: #4B5563;
}

.rk-account-badge {
  background: #1A1B1F;
  color: #FFFFFF;
  border-radius: 9px;
  padding: 4px 10px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-terminal);
  font-size: 12.5px;
  font-weight: 700;
}

.rk-avatar-sm {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  box-shadow: 0 0 3px rgba(0, 0, 0, 0.2);
}

/* 2. Modal Overlay Backdrop */
.rk-overlay {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  z-index: 99999;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.rk-overlay.open {
  display: flex;
}

/* 3. The 2-Column Wide RainbowKit Connect Modal */
.rk-modal-wide {
  width: 712px;
  max-width: 95vw;
  height: 485px;
  max-height: 90vh;
  background: #FFFFFF;
  border-radius: 24px;
  box-shadow: 0 20px 60px -10px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(0, 0, 0, 0.06);
  display: flex;
  overflow: hidden;
  position: relative;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
  animation: rkSpringPop 0.25s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes rkSpringPop {
  0% { opacity: 0; transform: scale(0.96) translateY(10px); }
  100% { opacity: 1; transform: scale(1) translateY(0); }
}

/* Left Column: Wallet Connectors List */
.rk-panel-left {
  width: 290px;
  border-right: 1px solid rgba(0, 0, 0, 0.08);
  padding: 1.25rem 1rem 1.25rem 1.25rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: #FFFFFF;
}

.rk-panel-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #1A1B1F;
  margin-bottom: 1rem;
  padding-left: 0.5rem;
}

.rk-connector-list {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.rk-connector-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.65rem 0.85rem;
  border-radius: 14px;
  border: none;
  background: transparent;
  cursor: pointer;
  width: 100%;
  text-align: left;
  transition: background-color 0.15s ease, transform 0.1s ease;
  user-select: none;
}

.rk-connector-row:hover {
  background: #F4F4F6;
}

.rk-connector-row.active {
  background: #F4F4F6;
}

.rk-row-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.rk-icon-box {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.rk-row-name {
  font-size: 0.94rem;
  font-weight: 600;
  color: #1A1B1F;
}

.rk-connector-row.active .rk-row-name {
  font-weight: 700;
}

.rk-badge {
  font-size: 0.68rem;
  font-weight: 700;
  font-family: var(--font-terminal);
  color: #767D8E;
  background: #EBECEF;
  padding: 0.2rem 0.45rem;
  border-radius: 6px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.rk-badge.detected {
  color: #00C853;
  background: rgba(0, 200, 83, 0.12);
}

.rk-panel-left-footer {
  padding-top: 1rem;
  border-top: 1px solid rgba(0, 0, 0, 0.06);
}

.rk-help-btn {
  background: none;
  border: none;
  font-size: 0.82rem;
  font-weight: 600;
  color: #767D8E;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  transition: color 0.15s ease;
}

.rk-help-btn:hover {
  color: #1A1B1F;
}

/* Right Column: Dynamic QR / Status Viewport */
.rk-panel-right {
  flex: 1;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  background: #FFFFFF;
}

.rk-close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  background: #F4F4F6;
  color: #767D8E;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  transition: all 0.15s ease;
}

.rk-close-btn:hover {
  background: #E2E3E8;
  color: #1A1B1F;
}

.rk-qr-card {
  background: #FFFFFF;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 20px;
  padding: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0.85rem 0;
  position: relative;
}

.rk-qr-logo-badge {
  position: absolute;
  width: 44px;
  height: 44px;
  background: #FFFFFF;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
}

.rk-action-pill-btn {
  background: #F4F4F6;
  color: #1A1B1F;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 20px;
  padding: 0.45rem 1rem;
  font-size: 0.82rem;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  transition: all 0.15s ease;
}

.rk-action-pill-btn:hover {
  background: #E5E7EB;
  border-color: rgba(0, 0, 0, 0.15);
}

.rk-btn-primary {
  background: #1A1B1F;
  color: #FFFFFF;
  border: none;
  border-radius: 12px;
  padding: 0.65rem 1.5rem;
  font-size: 0.88rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
}

.rk-btn-primary:hover {
  background: #272A30;
  transform: translateY(-1px);
}

/* 4. Chain Switcher Modal */
.rk-modal-dialog {
  width: 340px;
  max-width: 92vw;
  background: #FFFFFF;
  border-radius: 24px;
  box-shadow: 0 20px 60px -10px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(0, 0, 0, 0.06);
  padding: 1.5rem;
  position: relative;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  animation: rkSpringPop 0.25s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.rk-chain-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  border-radius: 14px;
  border: none;
  background: transparent;
  cursor: pointer;
  width: 100%;
  transition: background 0.15s ease;
}

.rk-chain-row:hover {
  background: #F4F4F6;
}

.rk-chain-row.selected {
  background: #F4F4F6;
  font-weight: 700;
}

/* 5. Account Modal */
.rk-account-dialog {
  width: 360px;
  max-width: 92vw;
  background: #FFFFFF;
  border-radius: 24px;
  box-shadow: 0 20px 60px -10px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(0, 0, 0, 0.06);
  padding: 1.75rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  position: relative;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  animation: rkSpringPop 0.25s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.rk-avatar-lg {
  width: 68px;
  height: 68px;
  border-radius: 50%;
  margin-bottom: 1rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.rk-btn-disconnect {
  width: 100%;
  background: rgba(255, 73, 74, 0.08);
  color: #FF494A;
  border: 1px solid rgba(255, 73, 74, 0.2);
  border-radius: 12px;
  padding: 0.65rem;
  font-size: 0.88rem;
  font-weight: 700;
  cursor: pointer;
  margin-top: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.15s ease;
}

.rk-btn-disconnect:hover {
  background: rgba(255, 73, 74, 0.16);
  border-color: rgba(255, 73, 74, 0.4);
}

@media (max-width: 720px) {
  .rk-modal-wide {
    flex-direction: column;
    height: auto;
    max-height: 92vh;
    overflow-y: auto;
    width: 360px;
  }
  .rk-panel-left {
    width: 100% !important;
    border-right: none !important;
    border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  }
}
"""

print("RainbowKit engine CSS prepared successfully.")

# Official SVGs
SVG_RAINBOW = '''<svg width="28" height="28" viewBox="0 0 28 28" fill="none"><rect width="28" height="28" rx="8" fill="#0E76FD"/><path d="M5 21C5 12.1634 12.1634 5 21 5" stroke="#FF494A" stroke-width="2.5" stroke-linecap="round"/><path d="M7 21C7 13.268 13.268 7 21 7" stroke="#FF8700" stroke-width="2.5" stroke-linecap="round"/><path d="M9 21C9 14.3726 14.3726 9 21 9" stroke="#FFD600" stroke-width="2.5" stroke-linecap="round"/><path d="M11 21C11 15.4772 15.4772 11 21 11" stroke="#00D369" stroke-width="2.5" stroke-linecap="round"/><path d="M13 21C13 16.5817 16.5817 13 21 13" stroke="#0075FF" stroke-width="2.5" stroke-linecap="round"/><path d="M15 21C15 17.6863 17.6863 15 21 15" stroke="#7A00FF" stroke-width="2.5" stroke-linecap="round"/></svg>'''

SVG_METAMASK = '''<svg width="28" height="28" viewBox="0 0 318.6 318.6"><polygon fill="#E2761B" points="274.1 35.5 174.6 109.4 193 65.8 274.1 35.5"/><polygon fill="#E4761B" points="44.4 35.5 124.6 66.3 143.9 109.4 44.4 35.5"/><polygon fill="#E4761B" points="238.3 206.8 211.8 247.4 268.5 263 284.8 207.7 238.3 206.8"/><polygon fill="#E4761B" points="33.9 207.7 50.1 263 106.8 247.4 80.3 206.8 33.9 207.7"/><polygon fill="#D7C1B3" points="87.3 140.9 73.6 172.9 129.5 174.5 127.8 120.3 87.3 140.9"/><polygon fill="#D7C1B3" points="231.3 140.9 190.2 120.3 189.1 174.5 245 172.9 231.3 140.9"/><polygon fill="#233447" points="129.5 174.5 73.6 172.9 80.3 206.8 131.6 206.8 129.5 174.5"/><polygon fill="#233447" points="189.1 174.5 187 206.8 238.3 206.8 245 172.9 189.1 174.5"/><polygon fill="#CD6116" points="106.8 247.4 140.6 230.9 131.6 206.8 80.3 206.8 106.8 247.4"/><polygon fill="#CD6116" points="178 230.9 211.8 247.4 238.3 206.8 187 206.8 178 230.9"/><polygon fill="#E4751F" points="174.6 109.4 274.1 35.5 284.8 207.7 238.3 206.8 245 172.9 231.3 140.9 190.2 120.3 174.6 109.4"/><polygon fill="#E4751F" points="44.4 35.5 143.9 109.4 127.8 120.3 87.3 140.9 73.6 172.9 80.3 206.8 33.9 207.7 44.4 35.5"/><polygon fill="#F6851B" points="159.3 187.4 159.3 268.5 211.8 247.4 178 230.9 187 206.8 189.1 174.5 159.3 187.4"/><polygon fill="#C0AD9E" points="159.3 268.5 159.3 187.4 129.5 174.5 131.6 206.8 140.6 230.9 106.8 247.4 159.3 268.5"/></svg>'''

SVG_COINBASE = '''<svg width="28" height="28" viewBox="0 0 28 28" fill="none"><rect width="28" height="28" rx="8" fill="#0052FF"/><path d="M14 7C10.134 7 7 10.134 7 14C7 17.866 10.134 21 14 21C17.866 21 21 17.866 21 14C21 10.134 17.866 7 14 7Z" fill="white"/><rect x="12" y="12" width="4" height="4" rx="1" fill="#0052FF"/></svg>'''

SVG_WALLETCONNECT = '''<svg width="28" height="28" viewBox="0 0 28 28" fill="none"><rect width="28" height="28" rx="8" fill="#3B99FC"/><path d="M8.2 11.2C11.4 8.2 16.6 8.2 19.8 11.2L20.4 11.7C20.6 11.9 20.6 12.2 20.4 12.4L18.7 13.9C18.6 14 18.4 14 18.3 13.9L17.4 13.1C15.5 11.3 12.5 11.3 10.6 13.1L9.7 13.9C9.6 14 9.4 14 9.3 13.9L7.6 12.4C7.4 12.2 7.4 11.9 7.6 11.7L8.2 11.2ZM22.8 14.1L24.3 15.6C24.5 15.8 24.5 16.1 24.3 16.3L17.8 22.3C17.6 22.5 17.3 22.5 17.1 22.3L14 19.4C13.9 19.3 13.8 19.3 13.7 19.4L10.9 22.3C10.7 22.5 10.4 22.5 10.2 22.3L3.7 16.3C3.5 16.1 3.5 15.8 3.7 15.6L5.2 14.1C5.4 13.9 5.7 13.9 5.9 14.1L8.7 16.8C8.8 16.9 8.9 16.9 9 16.8L13.7 12.4C13.9 12.2 14.1 12.2 14.3 12.4L19 16.8C19.1 16.9 19.2 16.9 19.3 16.8L22.1 14.1C22.3 13.9 22.6 13.9 22.8 14.1Z" fill="white"/></svg>'''

SVG_INJECTED = '''<svg width="28" height="28" viewBox="0 0 28 28" fill="none"><rect width="28" height="28" rx="8" fill="#1A1B1F"/><circle cx="14" cy="14" r="8" stroke="#FFFFFF" stroke-width="1.8"/><circle cx="14" cy="14" r="3" fill="#00C853"/></svg>'''

# Chains SVGs
SVG_CHAIN_ETH = '''<svg width="18" height="18" viewBox="0 0 256 417"><path fill="#343434" d="M127.961 0l-2.795 9.5v275.668l2.795 2.79 127.962-75.638z"/><path fill="#8C8C8C" d="M127.962 0L0 212.32l127.962 75.639V0z"/><path fill="#3C3C3B" d="M127.961 312.187l-1.575 1.92v98.199l1.575 4.601 128.038-180.32z"/><path fill="#8C8C8C" d="M127.962 416.905v-104.72L0 236.585z"/><path fill="#141414" d="M127.961 287.958l127.96-75.637-127.96-58.162z"/><path fill="#393939" d="M0 212.32l127.96 75.638v-133.8z"/></svg>'''
SVG_CHAIN_ARB = '''<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#28A0F0" d="M12 2L2 7l10 5 10-5-10-5zm0 8.5L5.5 7.25 12 4l6.5 3.25L12 10.5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>'''
SVG_CHAIN_OP = '''<svg width="18" height="18" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#FF0420"/><path fill="#FFF" d="M8.5 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8zm7 0h-3v8h3a4 4 0 0 0 0-8z"/></svg>'''
SVG_CHAIN_POLYGON = '''<svg width="18" height="18" viewBox="0 0 24 24"><path fill="#8247E5" d="M16.5 12l3.5-2v4l-3.5 2zM12 9.5l3.5-2v4l-3.5 2zM7.5 12l3.5-2v4l-3.5 2zM12 14.5l3.5-2v4l-3.5 2z"/></svg>'''
SVG_CHAIN_BASE = '''<svg width="18" height="18" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#0052FF"/><path fill="#FFF" d="M12 6a6 6 0 1 0 0 12 6 6 0 0 0 0-12z"/></svg>'''

# Generate Authentic QR Code Matrix SVG
def generate_qr_svg(badge_type="rainbow"):
    # Precise deterministic pattern simulating WalletConnect / Rainbow QR
    matrix_dots = ""
    # Corners
    matrix_dots += '<rect x="10" y="10" width="36" height="36" rx="6" fill="#1A1B1F"/>'
    matrix_dots += '<rect x="18" y="18" width="20" height="20" rx="3" fill="#FFFFFF"/>'
    matrix_dots += '<rect x="22" y="22" width="12" height="12" rx="2" fill="#1A1B1F"/>'

    matrix_dots += '<rect x="154" y="10" width="36" height="36" rx="6" fill="#1A1B1F"/>'
    matrix_dots += '<rect x="162" y="18" width="20" height="20" rx="3" fill="#FFFFFF"/>'
    matrix_dots += '<rect x="166" y="22" width="12" height="12" rx="2" fill="#1A1B1F"/>'

    matrix_dots += '<rect x="10" y="154" width="36" height="36" rx="6" fill="#1A1B1F"/>'
    matrix_dots += '<rect x="18" y="162" width="20" height="20" rx="3" fill="#FFFFFF"/>'
    matrix_dots += '<rect x="22" y="166" width="12" height="12" rx="2" fill="#1A1B1F"/>'

    # Matrix pattern dots
    import random
    rng = random.Random(42 if badge_type == "rainbow" else 99)
    for row in range(4, 25):
        for col in range(4, 25):
            # Skip corners and center
            if (row < 8 and (col < 8 or col > 20)) or (row > 20 and col < 8):
                continue
            if 10 <= row <= 18 and 10 <= col <= 18:
                continue
            if rng.random() > 0.48:
                x = col * 8 + 4
                y = row * 8 + 4
                matrix_dots += f'<rect x="{x}" y="{y}" width="6" height="6" rx="1.5" fill="#1A1B1F"/>'

    center_badge = ""
    if badge_type == "rainbow":
        center_badge = f'''
        <g transform="translate(84, 84)">
          <rect width="32" height="32" rx="8" fill="#FFFFFF" filter="drop-shadow(0 2px 6px rgba(0,0,0,0.15))"/>
          <g transform="translate(2, 2) scale(1)">
            {SVG_RAINBOW}
          </g>
        </g>
        '''
    else:
        center_badge = f'''
        <g transform="translate(84, 84)">
          <rect width="32" height="32" rx="8" fill="#FFFFFF" filter="drop-shadow(0 2px 6px rgba(0,0,0,0.15))"/>
          <g transform="translate(2, 2) scale(1)">
            {SVG_WALLETCONNECT}
          </g>
        </g>
        '''

    return f'''
    <svg width="200" height="200" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="200" height="200" fill="#FFFFFF" rx="12"/>
      {matrix_dots}
      {center_badge}
    </svg>
    '''

QR_RAINBOW_SVG = generate_qr_svg("rainbow")
QR_WALLETCONNECT_SVG = generate_qr_svg("walletconnect")

RAINBOWKIT_HTML_MARKUP = f"""
<!-- ==========================================================================
     AUTHENTIC RAINBOWKIT MODALS & WIDGETS
     ========================================================================== -->

<!-- 1. The 2-Column Wide RainbowKit Connect Modal -->
<div class="rk-overlay" id="rainbowConnectModalOverlay" onclick="handleRainbowBackdrop(event, 'rainbowConnectModalOverlay')">
  <div class="rk-modal-wide" id="rainbowConnectModalWindow">
    
    <!-- LEFT PANEL: CONNECTORS LIST -->
    <div class="rk-panel-left">
      <div>
        <div class="rk-panel-title">Connect a Wallet</div>
        <div class="rk-connector-list">
          <!-- Rainbow -->
          <button type="button" class="rk-connector-row active" id="rk-row-Rainbow" onclick="switchRainbowProvider('Rainbow')">
            <div class="rk-row-left">
              <div class="rk-icon-box">{SVG_RAINBOW}</div>
              <span class="rk-row-name">Rainbow</span>
            </div>
            <span class="rk-badge">QR CODE</span>
          </button>

          <!-- MetaMask -->
          <button type="button" class="rk-connector-row" id="rk-row-MetaMask" onclick="switchRainbowProvider('MetaMask')">
            <div class="rk-row-left">
              <div class="rk-icon-box">{SVG_METAMASK}</div>
              <span class="rk-row-name">MetaMask</span>
            </div>
            <span class="rk-badge" id="rk-badge-metamask">POPULAR</span>
          </button>

          <!-- Coinbase Wallet -->
          <button type="button" class="rk-connector-row" id="rk-row-Coinbase" onclick="switchRainbowProvider('Coinbase')">
            <div class="rk-row-left">
              <div class="rk-icon-box">{SVG_COINBASE}</div>
              <span class="rk-row-name">Coinbase Wallet</span>
            </div>
            <span class="rk-badge">APP</span>
          </button>

          <!-- WalletConnect -->
          <button type="button" class="rk-connector-row" id="rk-row-WalletConnect" onclick="switchRainbowProvider('WalletConnect')">
            <div class="rk-row-left">
              <div class="rk-icon-box">{SVG_WALLETCONNECT}</div>
              <span class="rk-row-name">WalletConnect</span>
            </div>
            <span class="rk-badge">QR CODE</span>
          </button>

          <!-- Browser Injected -->
          <button type="button" class="rk-connector-row" id="rk-row-Injected" onclick="switchRainbowProvider('Injected')">
            <div class="rk-row-left">
              <div class="rk-icon-box">{SVG_INJECTED}</div>
              <span class="rk-row-name">Browser Wallet</span>
            </div>
            <span class="rk-badge" id="rk-badge-injected">EVM</span>
          </button>
        </div>
      </div>

      <div class="rk-panel-left-footer">
        <button type="button" class="rk-help-btn" onclick="showRainbowHelp()">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          What is a Wallet?
        </button>
      </div>
    </div>

    <!-- RIGHT PANEL: INTERACTIVE VIEWPORT (QR CODE / CONNECTOR ACTION) -->
    <div class="rk-panel-right">
      <button type="button" class="rk-close-btn" onclick="closeRainbowModal()" title="Close">✕</button>
      <div id="rkRightContent" style="display: flex; flex-direction: column; align-items: center; text-align: center; width: 100%;">
        <!-- Rendered dynamically by renderRainbowRightPane() -->
      </div>
    </div>

  </div>
</div>

<!-- 2. Authentic RainbowKit Chain Switcher Modal -->
<div class="rk-overlay" id="rainbowChainModalOverlay" onclick="handleRainbowBackdrop(event, 'rainbowChainModalOverlay')">
  <div class="rk-modal-dialog">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem;">
      <h3 style="font-size: 1.1rem; font-weight: 700; color: #1A1B1F;">Switch Networks</h3>
      <button type="button" class="rk-close-btn" style="position: static;" onclick="closeRainbowChainModal()">✕</button>
    </div>
    
    <div style="display: flex; flex-direction: column; gap: 0.4rem;" id="rkChainsListContainer">
      <!-- Chains rendered dynamically -->
    </div>
  </div>
</div>

<!-- 3. Authentic RainbowKit Account Modal -->
<div class="rk-overlay" id="rainbowAccountModalOverlay" onclick="handleRainbowBackdrop(event, 'rainbowAccountModalOverlay')">
  <div class="rk-account-dialog">
    <button type="button" class="rk-close-btn" onclick="closeRainbowAccountModal()">✕</button>
    
    <div class="rk-avatar-lg" id="rkAccountModalAvatar"></div>
    <div style="font-size: 1.15rem; font-weight: 700; color: #1A1B1F;" id="rkAccountModalAddress">0x00...00</div>
    
    <div style="display: flex; gap: 0.5rem; margin: 0.65rem 0 1.25rem;">
      <button type="button" class="rk-action-pill-btn" onclick="copyConnectedAddress()">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
        <span id="rkCopyBtnLabel">Copy Address</span>
      </button>
      <a href="https://etherscan.io" target="_blank" class="rk-action-pill-btn" id="rkEtherscanLink" style="text-decoration: none;">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
        Explorer
      </a>
    </div>

    <div style="background: #F4F4F6; border-radius: 16px; width: 100%; padding: 0.85rem 1rem; margin-bottom: 0.5rem; text-align: left;">
      <div style="font-size: 0.72rem; font-weight: 700; color: #767D8E; font-family: var(--font-terminal);">ACTIVE NETWORK</div>
      <div style="font-size: 0.92rem; font-weight: 700; color: #1A1B1F; margin-top: 0.15rem;" id="rkAccountModalChainName">Ethereum Mainnet</div>
      <div style="font-size: 0.72rem; font-weight: 700; color: #767D8E; font-family: var(--font-terminal); margin-top: 0.65rem;">PAPER BALANCE SANDBOX</div>
      <div style="font-size: 1.25rem; font-weight: 700; color: var(--color-green); font-family: var(--font-number);" id="rkAccountModalBalance">$50,000.00 USDT</div>
    </div>

    <button type="button" class="rk-btn-disconnect" onclick="disconnectRainbowKit()">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
      Disconnect
    </button>
  </div>
</div>
"""

print("RainbowKit HTML Markup prepared successfully.")

# Complete JavaScript Engine for RainbowKit
RAINBOWKIT_JS = '''
    // =========================================================================
    // AUTHENTIC RAINBOWKIT CLIENT ENGINE & STATE MANAGER
    // =========================================================================

    const RAINBOWKIT_CHAINS = [
      { id: 1, name: "Ethereum", icon: "eth", color: "#627EEA", explorer: "https://etherscan.io" },
      { id: 42161, name: "Arbitrum One", icon: "arb", color: "#28A0F0", explorer: "https://arbiscan.io" },
      { id: 10, name: "Optimism", icon: "op", color: "#FF0420", explorer: "https://optimistic.etherscan.io" },
      { id: 137, name: "Polygon", icon: "polygon", color: "#8247E5", explorer: "https://polygonscan.com" },
      { id: 8453, name: "Base", icon: "base", color: "#0052FF", explorer: "https://basescan.org" },
    ];

    let rkActiveProvider = "Rainbow";
    let rkActiveChain = RAINBOWKIT_CHAINS[0];

    // Deterministic RainbowKit Avatar Gradient
    function getRainbowAvatarGradient(address) {
      if (!address) return "linear-gradient(135deg, #FF494A, #FF8700, #00D369, #0075FF)";
      let hash = 0;
      for (let i = 0; i < address.length; i++) {
        hash = address.charCodeAt(i) + ((hash << 5) - hash);
      }
      const hue1 = Math.abs(hash) % 360;
      const hue2 = (hue1 + 60) % 360;
      const hue3 = (hue1 + 180) % 360;
      return `linear-gradient(135deg, hsl(${hue1}, 90%, 65%), hsl(${hue2}, 95%, 55%), hsl(${hue3}, 90%, 70%))`;
    }

    // Format address truncated (0x12...34)
    function rkFormatAddress(addr) {
      if (!addr) return "";
      if (addr.length <= 10) return addr;
      return addr.slice(0, 6) + "..." + addr.slice(-4);
    }

    // Open & Close Connect Modal
    function openRainbowModal() {
      closeRainbowChainModal();
      closeRainbowAccountModal();
      const overlay = document.getElementById("rainbowConnectModalOverlay");
      if (!overlay) return;
      overlay.classList.add("open");
      detectInstalledProviders();
      switchRainbowProvider(rkActiveProvider);
    }

    function closeRainbowModal() {
      const overlay = document.getElementById("rainbowConnectModalOverlay");
      if (overlay) overlay.classList.remove("open");
    }

    // Open & Close Chain Modal
    function openRainbowChainModal() {
      closeRainbowModal();
      closeRainbowAccountModal();
      const overlay = document.getElementById("rainbowChainModalOverlay");
      if (!overlay) return;
      renderRainbowChainsList();
      overlay.classList.add("open");
    }

    function closeRainbowChainModal() {
      const overlay = document.getElementById("rainbowChainModalOverlay");
      if (overlay) overlay.classList.remove("open");
    }

    // Open & Close Account Modal
    function openRainbowAccountModal() {
      closeRainbowModal();
      closeRainbowChainModal();
      const overlay = document.getElementById("rainbowAccountModalOverlay");
      if (!overlay) return;
      renderRainbowAccountView();
      overlay.classList.add("open");
    }

    function closeRainbowAccountModal() {
      const overlay = document.getElementById("rainbowAccountModalOverlay");
      if (overlay) overlay.classList.remove("open");
    }

    function handleRainbowBackdrop(e, overlayId) {
      if (e.target.id === overlayId) {
        if (overlayId === "rainbowConnectModalOverlay") closeRainbowModal();
        if (overlayId === "rainbowChainModalOverlay") closeRainbowChainModal();
        if (overlayId === "rainbowAccountModalOverlay") closeRainbowAccountModal();
      }
    }

    // Detect browser extensions
    function detectInstalledProviders() {
      const hasMetaMask = !!(typeof window !== "undefined" && (window.ethereum?.isMetaMask || window.ethereum));
      const mmBadge = document.getElementById("rk-badge-metamask");
      if (mmBadge && hasMetaMask) {
        mmBadge.textContent = "INSTALLED";
        mmBadge.className = "rk-badge detected";
      }
      const hasInjected = !!(typeof window !== "undefined" && window.ethereum);
      const injBadge = document.getElementById("rk-badge-injected");
      if (injBadge && hasInjected) {
        injBadge.textContent = "DETECTED";
        injBadge.className = "rk-badge detected";
      }
    }

    // Switch provider tab inside Connect Modal
    function switchRainbowProvider(provider) {
      rkActiveProvider = provider;
      document.querySelectorAll(".rk-connector-row").forEach(r => r.classList.remove("active"));
      const activeRow = document.getElementById(`rk-row-${provider}`);
      if (activeRow) activeRow.classList.add("active");
      renderRainbowRightPane(provider);
    }

    // Render Right Panel of Connect Modal
    function renderRainbowRightPane(provider) {
      const container = document.getElementById("rkRightContent");
      if (!container) return;

      const hasMetaMask = !!(typeof window !== "undefined" && (window.ethereum?.isMetaMask || window.ethereum));
      const hasInjected = !!(typeof window !== "undefined" && window.ethereum);

      if (provider === "Rainbow") {
        container.innerHTML = `
          <div style="margin-top: 0.5rem;">
            <div style="width: 48px; height: 48px; margin: 0 auto 0.75rem;">
              __SVG_RAINBOW__
            </div>
            <div style="font-size: 1.15rem; font-weight: 700; color: #1A1B1F;">Scan with Rainbow</div>
            <div style="font-size: 0.82rem; color: #767D8E; margin-top: 0.25rem; max-width: 260px;">
              Open the Rainbow app on your phone and tap the scanner icon to connect instantly.
            </div>

            <div class="rk-qr-card">
              __QR_RAINBOW_SVG__
            </div>

            <div style="display: flex; gap: 0.5rem; justify-content: center; align-items: center; margin-top: 0.25rem;">
              <button type="button" class="rk-action-pill-btn" onclick="copyRainbowPairingUri(this)">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
                <span>Copy Link</span>
              </button>
              <button type="button" class="rk-action-pill-btn" onclick="connectRainbowDirect('0x71C8364437a9238f63173673cc2949604856f899')">
                <span>Connect Rainbow Demo</span>
              </button>
            </div>
            <div style="margin-top: 0.75rem;">
              <a href="https://rainbow.me" target="_blank" style="font-size: 0.78rem; font-weight: 600; color: #0E76FD; text-decoration: none;">Don't have Rainbow? Get the app &rarr;</a>
            </div>
          </div>
        `;
      } else if (provider === "WalletConnect") {
        container.innerHTML = `
          <div style="margin-top: 0.5rem;">
            <div style="width: 48px; height: 48px; margin: 0 auto 0.75rem;">
              __SVG_WALLETCONNECT__
            </div>
            <div style="font-size: 1.15rem; font-weight: 700; color: #1A1B1F;">Scan with your phone</div>
            <div style="font-size: 0.82rem; color: #767D8E; margin-top: 0.25rem; max-width: 260px;">
              Scan this QR code with any WalletConnect supported wallet to connect.
            </div>

            <div class="rk-qr-card">
              __QR_WALLETCONNECT_SVG__
            </div>

            <div style="display: flex; gap: 0.5rem; justify-content: center; align-items: center; margin-top: 0.25rem;">
              <button type="button" class="rk-action-pill-btn" onclick="copyRainbowPairingUri(this)">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
                <span>Copy Link</span>
              </button>
              <button type="button" class="rk-action-pill-btn" onclick="connectRainbowDirect('0x10B68C1C824a7337372b15D2F6AfB2e6b2169B60')">
                <span>Connect WC Demo</span>
              </button>
            </div>
          </div>
        `;
      } else if (provider === "MetaMask") {
        container.innerHTML = `
          <div style="margin-top: 1.5rem; max-width: 320px;">
            <div style="width: 64px; height: 64px; margin: 0 auto 1rem;">
              __SVG_METAMASK__
            </div>
            <div style="font-size: 1.25rem; font-weight: 700; color: #1A1B1F;">MetaMask</div>
            <div style="font-size: 0.86rem; color: #767D8E; margin: 0.5rem 0 1.5rem; line-height: 1.45;">
              ${hasMetaMask 
                ? 'Click below to connect your MetaMask browser extension directly via EIP-1193.' 
                : 'MetaMask extension not detected in this browser. Install it from the official Chrome store or connect via demo session.'}
            </div>

            <div style="display: flex; flex-direction: column; gap: 0.6rem; width: 100%;">
              ${hasMetaMask ? `
                <button type="button" class="rk-btn-primary" onclick="requestInjectedAccounts('MetaMask')">
                  Open MetaMask Extension
                </button>
              ` : `
                <a href="https://metamask.io/download/" target="_blank" class="rk-btn-primary" style="text-decoration: none; text-align: center;">
                  Install MetaMask &rarr;
                </a>
              `}
              <button type="button" class="rk-action-pill-btn" style="justify-content: center; padding: 0.6rem;" onclick="connectRainbowDirect('0x29D7d6365fDE07798569979228FB43D75a618342')">
                Connect Demo MetaMask Account
              </button>
            </div>
          </div>
        `;
      } else if (provider === "Coinbase") {
        container.innerHTML = `
          <div style="margin-top: 1.5rem; max-width: 320px;">
            <div style="width: 64px; height: 64px; margin: 0 auto 1rem;">
              __SVG_COINBASE__
            </div>
            <div style="font-size: 1.25rem; font-weight: 700; color: #1A1B1F;">Coinbase Wallet</div>
            <div style="font-size: 0.86rem; color: #767D8E; margin: 0.5rem 0 1.5rem; line-height: 1.45;">
              Connect using Coinbase Wallet extension or scan with the Coinbase mobile app.
            </div>

            <div style="display: flex; flex-direction: column; gap: 0.6rem; width: 100%;">
              <button type="button" class="rk-btn-primary" onclick="requestInjectedAccounts('Coinbase')">
                Connect Coinbase Wallet
              </button>
              <button type="button" class="rk-action-pill-btn" style="justify-content: center; padding: 0.6rem;" onclick="connectRainbowDirect('0x4B0897b0513fdC7C541B6d9D7E929C4e5364D2dB')">
                Connect Demo Coinbase Account
              </button>
            </div>
          </div>
        `;
      } else if (provider === "Injected") {
        container.innerHTML = `
          <div style="margin-top: 1.5rem; max-width: 320px;">
            <div style="width: 64px; height: 64px; margin: 0 auto 1rem;">
              __SVG_INJECTED__
            </div>
            <div style="font-size: 1.25rem; font-weight: 700; color: #1A1B1F;">Browser Wallet</div>
            <div style="font-size: 0.86rem; color: #767D8E; margin: 0.5rem 0 1.5rem; line-height: 1.45;">
              ${hasInjected 
                ? 'EIP-1193 compatible provider detected in window.ethereum. Click below to request accounts.' 
                : 'No injected Web3 provider found in current window.'}
            </div>

            <div style="display: flex; flex-direction: column; gap: 0.6rem; width: 100%;">
              ${hasInjected ? `
                <button type="button" class="rk-btn-primary" onclick="requestInjectedAccounts('Injected')">
                  Connect Browser Provider
                </button>
              ` : ''}
              <button type="button" class="rk-action-pill-btn" style="justify-content: center; padding: 0.6rem;" onclick="connectRainbowDirect('0x8ba1f109551bD432803012645Ac136ddd64DBA72')">
                Connect Injected Sandbox Account
              </button>
            </div>
          </div>
        `;
      }
    }

    // Show "What is a Wallet?" Educational View
    function showRainbowHelp() {
      const container = document.getElementById("rkRightContent");
      if (!container) return;
      container.innerHTML = `
        <div style="text-align: left; width: 100%; max-width: 360px;">
          <button type="button" class="rk-action-pill-btn" style="margin-bottom: 1rem;" onclick="switchRainbowProvider(rkActiveProvider)">
            &larr; Back to Wallets
          </button>
          <div style="font-size: 1.25rem; font-weight: 700; color: #1A1B1F; margin-bottom: 0.5rem;">What is a Wallet?</div>
          <div style="font-size: 0.85rem; color: #767D8E; margin-bottom: 1.25rem; line-height: 1.45;">
            Wallets allow you to store digital assets, sign cryptographic orders, and log into Web3 applications without passwords.
          </div>

          <div style="display: flex; flex-direction: column; gap: 0.85rem; margin-bottom: 1.25rem;">
            <div style="display: flex; gap: 0.75rem; align-items: flex-start;">
              <div style="background: #F4F4F6; width: 34px; height: 34px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0;">🛡️</div>
              <div>
                <div style="font-size: 0.88rem; font-weight: 700; color: #1A1B1F;">Digital Assets & Collateral</div>
                <div style="font-size: 0.8rem; color: #767D8E; line-height: 1.4;">Hold tokens, manage USDT collateral, and trade tokenized equities on 24/7 markets.</div>
              </div>
            </div>

            <div style="display: flex; gap: 0.75rem; align-items: flex-start;">
              <div style="background: #F4F4F6; width: 34px; height: 34px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.1rem; flex-shrink: 0;">🔑</div>
              <div>
                <div style="font-size: 0.88rem; font-weight: 700; color: #1A1B1F;">One Account for Web3</div>
                <div style="font-size: 0.8rem; color: #767D8E; line-height: 1.4;">No usernames or passwords needed. Your address is your sovereign identity across the blockchain.</div>
              </div>
            </div>
          </div>

          <a href="https://rainbow.me" target="_blank" class="rk-btn-primary" style="display: block; text-align: center; text-decoration: none;">
            Get Rainbow Wallet &rarr;
          </a>
        </div>
      `;
    }

    // Copy Pairing URI
    function copyRainbowPairingUri(btn) {
      const uri = "wc:c7a91bf97e2da0252197eb2f8c5b96919e1f40d39e761df894cf6740b2b8e3e4@2?relay-protocol=irn&symKey=92f4da896582570b503028dc7f6b2149b4334ee0b9df237ca5e46820ff569bdf";
      if (navigator.clipboard) {
        navigator.clipboard.writeText(uri).catch(() => {});
      }
      const span = btn.querySelector("span");
      if (span) {
        const orig = span.textContent;
        span.textContent = "✓ Copied!";
        btn.style.background = "#E0F2FE";
        btn.style.color = "#0369A1";
        setTimeout(() => {
          span.textContent = orig;
          btn.style.background = "#F4F4F6";
          btn.style.color = "#1A1B1F";
        }, 1500);
      }
    }

    // Real EIP-1193 Web3 Request
    function requestInjectedAccounts(providerName) {
      if (typeof window !== "undefined" && window.ethereum) {
        window.ethereum.request({ method: "eth_requestAccounts" })
          .then(accs => {
            if (accs && accs.length > 0) {
              connectRainbowDirect(accs[0]);
            }
          })
          .catch(err => {
            console.warn("User rejected or error in eth_requestAccounts:", err);
            alert("Connection request was rejected or cancelled in wallet.");
          });
      } else {
        alert(`${providerName} extension not found in browser. Connecting deterministic demo session.`);
        connectRainbowDirect("0x29D7d6365fDE07798569979228FB43D75a618342");
      }
    }

    // Connect wallet direct into ChronosWalletStore
    function connectRainbowDirect(address) {
      ChronosWalletStore.connect(address);
      closeRainbowModal();
      renderRainbowHeader();
      showRecalibrationToast(
        "Wallet Connected via RainbowKit",
        `Connected address: ${rkFormatAddress(address)}. Loaded isolated paper trading balance and settings.`
      );
    }

    // Disconnect RainbowKit
    function disconnectRainbowKit() {
      closeRainbowAccountModal();
      ChronosWalletStore.disconnect();
      renderRainbowHeader();
      showRecalibrationToast("Wallet Disconnected", "Restored isolated paper trading sandbox.");
    }

    // Copy Connected Address in Account Modal
    function copyConnectedAddress() {
      const addr = ChronosWalletStore.currentAddress;
      if (addr && navigator.clipboard) {
        navigator.clipboard.writeText(addr).catch(() => {});
      }
      const lbl = document.getElementById("rkCopyBtnLabel");
      if (lbl) {
        lbl.textContent = "✓ Copied!";
        setTimeout(() => { lbl.textContent = "Copy Address"; }, 1500);
      }
    }

    // Switch Chains
    function switchRainbowChain(chainId) {
      const c = RAINBOWKIT_CHAINS.find(x => x.id === chainId) || RAINBOWKIT_CHAINS[0];
      rkActiveChain = c;
      closeRainbowChainModal();
      renderRainbowHeader();
      showRecalibrationToast("Network Switched", `Active network switched to ${c.name}.`);
    }

    // Render Chains list in Chain Switcher Modal
    function renderRainbowChainsList() {
      const container = document.getElementById("rkChainsListContainer");
      if (!container) return;
      container.innerHTML = RAINBOWKIT_CHAINS.map(c => {
        const isSel = c.id === rkActiveChain.id;
        const iconSvg = getChainIconSvg(c.icon);
        return `
          <button type="button" class="rk-chain-row ${isSel ? 'selected' : ''}" onclick="switchRainbowChain(${c.id})">
            <div style="display: flex; align-items: center; gap: 0.75rem;">
              <div style="width: 24px; height: 24px; display: flex; align-items: center; justify-content: center;">
                ${iconSvg}
              </div>
              <span style="font-size: 0.94rem; font-weight: ${isSel ? '700' : '500'}; color: #1A1B1F;">${c.name}</span>
            </div>
            ${isSel ? '<span style="color: #00C853; font-weight: 700;">✓</span>' : ''}
          </button>
        `;
      }).join("");
    }

    function getChainIconSvg(iconKey) {
      if (iconKey === "eth") return `__SVG_CHAIN_ETH__`;
      if (iconKey === "arb") return `__SVG_CHAIN_ARB__`;
      if (iconKey === "op") return `__SVG_CHAIN_OP__`;
      if (iconKey === "polygon") return `__SVG_CHAIN_POLYGON__`;
      return `__SVG_CHAIN_BASE__`;
    }

    // Render Account View inside Account Modal
    function renderRainbowAccountView() {
      const addr = ChronosWalletStore.currentAddress;
      const d = ChronosWalletStore.getCurrentData();
      const bal = d ? d.paperBalance : 50000.0;
      
      const avatarEl = document.getElementById("rkAccountModalAvatar");
      if (avatarEl) avatarEl.style.background = getRainbowAvatarGradient(addr);

      const addrEl = document.getElementById("rkAccountModalAddress");
      if (addrEl) addrEl.textContent = rkFormatAddress(addr);

      const chainEl = document.getElementById("rkAccountModalChainName");
      if (chainEl) chainEl.textContent = `${rkActiveChain.name} (Chain ID: ${rkActiveChain.id})`;

      const balEl = document.getElementById("rkAccountModalBalance");
      if (balEl) balEl.textContent = `$${bal.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })} USDT`;

      const expLink = document.getElementById("rkEtherscanLink");
      if (expLink && addr) {
        expLink.href = `${rkActiveChain.explorer}/address/${addr}`;
      }
    }

    // Master Header Widget Renderer (Replaces both disconnected button and connected pills)
    function renderRainbowHeader() {
      const container = document.getElementById("rainbowkitHeaderContainer");
      if (!container) return;

      const addr = ChronosWalletStore.currentAddress;
      if (!addr) {
        // Disconnected: Render iconic RainbowKit Connect Button
        container.innerHTML = `
          <button type="button" class="rk-connect-btn" onclick="openRainbowModal()" id="btnRainbowConnect">
            <span class="rk-rainbow-dot-icon"></span>
            <span>Connect Wallet</span>
          </button>
        `;
      } else {
        // Connected: Render authentic 2-pill layout (Chain + Account with avatar & balance)
        const d = ChronosWalletStore.getCurrentData();
        const bal = d ? d.paperBalance : 50000.0;
        const balFmt = `$${Math.round(bal).toLocaleString("en-US")}`;
        const avatarGrad = getRainbowAvatarGradient(addr);
        const iconSvg = getChainIconSvg(rkActiveChain.icon);

        container.innerHTML = `
          <div class="rk-connected-widget">
            <button type="button" class="rk-chain-pill" onclick="openRainbowChainModal()" title="Switch Networks">
              <span style="display: flex; align-items: center; justify-content: center; width: 16px; height: 16px;">
                ${iconSvg}
              </span>
              <span>${rkActiveChain.name}</span>
              <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            <button type="button" class="rk-account-pill" onclick="openRainbowAccountModal()" title="Account & Paper Balance">
              <span class="rk-balance-label">${balFmt}</span>
              <div class="rk-account-badge">
                <div class="rk-avatar-sm" style="background: ${avatarGrad};"></div>
                <span>${rkFormatAddress(addr)}</span>
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
              </div>
            </button>
          </div>
        `;
      }
    }

    // Expose RainbowKit API on window
    window.openRainbowModal = openRainbowModal;
    window.closeRainbowModal = closeRainbowModal;
    window.openRainbowChainModal = openRainbowChainModal;
    window.closeRainbowChainModal = closeRainbowChainModal;
    window.openRainbowAccountModal = openRainbowAccountModal;
    window.closeRainbowAccountModal = closeRainbowAccountModal;
    window.switchRainbowProvider = switchRainbowProvider;
    window.switchRainbowChain = switchRainbowChain;
    window.renderRainbowHeader = renderRainbowHeader;
    window.connectRainbowDirect = connectRainbowDirect;
    window.disconnectRainbowKit = disconnectRainbowKit;
    window.copyRainbowPairingUri = copyRainbowPairingUri;
    window.copyConnectedAddress = copyConnectedAddress;
    window.showRainbowHelp = showRainbowHelp;
'''

def get_rainbowkit_js():
    js = RAINBOWKIT_JS
    js = js.replace("__SVG_RAINBOW__", SVG_RAINBOW)
    js = js.replace("__SVG_METAMASK__", SVG_METAMASK)
    js = js.replace("__SVG_COINBASE__", SVG_COINBASE)
    js = js.replace("__SVG_WALLETCONNECT__", SVG_WALLETCONNECT)
    js = js.replace("__SVG_INJECTED__", SVG_INJECTED)
    js = js.replace("__QR_RAINBOW_SVG__", QR_RAINBOW_SVG)
    js = js.replace("__QR_WALLETCONNECT_SVG__", QR_WALLETCONNECT_SVG)
    js = js.replace("__SVG_CHAIN_ETH__", SVG_CHAIN_ETH)
    js = js.replace("__SVG_CHAIN_ARB__", SVG_CHAIN_ARB)
    js = js.replace("__SVG_CHAIN_OP__", SVG_CHAIN_OP)
    js = js.replace("__SVG_CHAIN_POLYGON__", SVG_CHAIN_POLYGON)
    js = js.replace("__SVG_CHAIN_BASE__", SVG_CHAIN_BASE)
    return js

print("Full RainbowKit engine generated successfully.")
