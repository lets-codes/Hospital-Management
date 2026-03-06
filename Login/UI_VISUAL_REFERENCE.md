# Admin Portal UI - Quick Visual Reference

## 🎨 Color Quick Reference

### Primary Palette
```
┌─────────────────────────────────────────────────┐
│ Primary Red     │ ██ #dc2626                    │
│ Primary Dark    │ ██ #991b1b                    │
│ Primary Light   │ ██ #fecaca                    │
│ Success Green   │ ██ #10b981                    │
│ Warning Amber   │ ██ #f59e0b                    │
│ Info Blue       │ ██ #3b82f6                    │
│ Danger Red      │ ██ #ef4444                    │
└─────────────────────────────────────────────────┘
```

### Neutral Palette
```
┌─────────────────────────────────────────────────┐
│ Dark Text       │ ██ #1f2937 (Primary text)     │
│ Med Gray Text   │ ██ #6b7280 (Secondary text)   │
│ Light Gray Text │ ██ #9ca3af (Light text)       │
│ White           │ ██ #ffffff (Surfaces)         │
│ Light BG        │ ██ #f9fafb (Page background)  │
│ Light Gray BG   │ ██ #f3f4f6 (Card backgrounds) │
│ Border Color    │ ██ #e5e7eb (Borders)          │
│ Light Border    │ ██ #f3f4f6 (Subtle borders)   │
└─────────────────────────────────────────────────┘
```

---

## 📐 Size Reference

### Typography Sizes
```
Large Headers        │ 32px (Profile name)
Page Titles         │ 28px (Stat values, modals)
Section Headers     │ 22px (Page headers)
Card Titles         │ 18px (Card headers)
Body Text           │ 16px (Main text)
UI Controls         │ 15px (Buttons, tabs)
Regular Text        │ 14px (Labels, form text)
Small Labels        │ 13px (Captions)
Tiny Text           │ 12px (Badges, small text)
```

### Spacing Scale
```
Extra Small         │ 4px   (Minimal gaps)
Small               │ 8px   (Small padding)
Medium              │ 12px  (Default gaps)
Standard            │ 16px  (Form padding)
Large               │ 20px  (Card padding)
Extra Large         │ 24px  (Section padding)
XXL                 │ 28px  (Header padding)
Huge                │ 32px  (Container padding)
```

### Border Radius
```
Minimal             │ 6px   (Subtle)
Default             │ 8px   (Standard)
Large               │ 12px  (Cards)
Extra Large         │ 16px  (Profile header, modals)
Circular            │ 50%   (Avatars)
```

---

## 🎯 Component Reference

### Header Component
```
┌────────────────────────────────────────────────────────┐
│ ⚕️ Hospital Admin | Welcome Admin  │ 🔔 👤 Logout      │
└────────────────────────────────────────────────────────┘
```

### Tab Navigation
```
📋 Restock  │ 💊 Medicines  │ ⏰ Expiring  │ 👤 Profile
━━━━━━━━━━━
```

### Stat Card
```
┌─────────────────────┐
│ ▮▮ (Red bar top)    │
│                     │
│        42           │
│  PENDING REQUESTS   │
│                     │
└─────────────────────┘
```

### Button States
```
Active:      [████ Red Gradient ████]  → Hover: Elevated + Shadow
Hover:       [████ Darker Red ████]    → Ready to click
Focus:       [████ Red ████] 🎯        → Keyboard accessible
Disabled:    [░░░░ Gray ░░░░]          → Not clickable
```

### Request Card
```
┌─────────────────────────────────────┐
│▮ Aspirin - 100 Tablets              │  ← Red left border
│                                     │
│ Medicine: Aspirin                   │
│ Requested by: Pharmacist Name       │
│ Quantity: 100 tablets               │
│                                     │
│ [✓ Approve]  [✗ Reject]            │
└─────────────────────────────────────┘
```

### Modal Dialog
```
╔═════════════════════════════════════╗
║ Approve Restock Request             ║  ← Slide up animation
║                                     ║
║ Medicine:    [____________]         ║
║ Pharmacist:  [____________]         ║
║ Quantity:    [____________]         ║
║                                     ║
║        [Cancel]  [Approve ✓]       ║
╚═════════════════════════════════════╝
```

### Profile Card
```
┌─────────────────────┐
│  Total Requests     │
│        24           │
│ Processed this     │
│ month              │
└─────────────────────┘
```

### Profile Header
```
╔═════════════════════════════════════════╗
║  [140x140]                              ║
║   Avatar   Admin Name                   ║
║            admin@hospital.com           ║
║            [Administrator Badge]       ║
╚═════════════════════════════════════════╝
```

---

## 🎬 Animation Quick Guide

### Slide Up (Modals)
```
Frame 1:  ↑↑↑ (Below, transparent)
Frame 2:  → (Moving up)
Frame 3:  ↓↓↓ (In place, opaque)
Duration: 350ms
Easing:   cubic-bezier(0.4, 0, 0.2, 1)
```

### Fade In (Alerts)
```
Frame 1:  ░░░ (Invisible)
Frame 2:  ▒▒▒ (Fading in)
Frame 3:  ██ (Visible)
Duration: 300ms
Easing:   ease-in
```

### Hover Lift (Cards)
```
Rest:     Original position
Hover:    translateY(-8px)
Effect:   Enhanced shadow
Duration: 300ms
```

### Tab Underline
```
Default:  Gray text, no underline
Active:   Red text, gradient underline
          (Red → Dark Red)
Duration: Instant
```

---

## 📱 Responsive Breakpoints

### Mobile (Max 768px)
```
Header:   Stacks vertically
Buttons:  Full-width on small screens
Grid:     1 column layout
Spacing:  Reduced padding
Font:     Slightly smaller
```

### Tablet (768px - 1024px)
```
Header:   Mostly horizontal
Buttons:  Side-by-side when possible
Grid:     2 column layout
Spacing:  Standard padding
Font:     Standard size
```

### Desktop (1024px+)
```
Header:   Full horizontal layout
Buttons:  All controls visible
Grid:     Auto-fit (usually 3-4 columns)
Spacing:  Full padding
Font:     Standard size
Container: Max-width 1400px
```

---

## ✨ Shadow & Depth Reference

### Elevation Levels

**Level 0 (No Shadow)**
```css
User Input, Disabled Elements
```

**Level 1 (Subtle Shadow)**
```css
0 1px 3px rgba(0, 0, 0, 0.05)
│ Tables, Cards at rest
└─ Barely noticeable, background elements
```

**Level 2 (Standard Shadow)**
```css
0 4px 12px rgba(0, 0, 0, 0.1)
│ Cards on hover, Buttons
└─ Normal interactive elements
```

**Level 3 (Large Shadow)**
```css
0 10px 28px rgba(0, 0, 0, 0.12)
│ Modals, Dropdowns
└─ Floating elements, high priority
```

---

## 🎨 Design Tokens Reference

### Corners (border-radius)
```
Sharp:       0px
Subtle:      4px
Default:     6-8px
Rounded:     12px
Extra Round: 16px
Circle:      50%
```

### Transitions (duration & easing)
```
Quick:       0.2s (hover, state change)
Standard:    0.3s (normal interactions)
Smooth:      0.35s (modal entry)
Slow:        0.5s (complex animations)

Easing:      cubic-bezier(0.4, 0, 0.2, 1)
             (Smooth, professional feel)
```

### Z-Index Stack
```
Background Layer:        0
Dropdowns/Tooltips:     50
Sticky Header:         100
Modals:              1000
```

---

## 🎯 Interactive Elements

### Button Variations

**Primary (Red)**
```
Rest:    Linear gradient (Red → Dark Red)
Hover:   Lift + Shadow
Active:  Darker appearance
Focus:   Outline visible
```

**Success (Green)**
```
Rest:    Linear gradient (Green → Dark Green)
Hover:   Lift + Green shadow
Active:  Pressed appearance
Focus:   Accessible outline
```

**Info (Blue)**
```
Rest:    Linear gradient (Blue → Dark Blue)
Hover:   Lift + Blue shadow
Active:  More saturated
Focus:   Clear focus ring
```

**Default (Gray)**
```
Rest:    White with border
Hover:   Light gray background
Active:  Border darkens
Focus:   Blue outline
```

### Form Elements

**Text Input**
```
Rest:       Border: 1.5px solid #e5e7eb
Focus:      Border: 1.5px solid #dc2626
            Box-shadow: 0 0 0 4px rgba(220, 38, 38, 0.1)
Filled:     Background changes on focus
Error:      Border color: #ef4444
Success:    Border color: #10b981
```

### Icons

**Icon Size Scale**
```
Small Actions:   16px
Buttons/Labels:  22px
Headers:         28px
Large Display:   32-56px
```

---

## 📊 Layout Grid System

### Container
```
Max Width:   1400px
Side Margin: Auto centered
Padding:     24px (desktop), 16px (mobile)
```

### Column System

**Responsive Grid**
```
Min Column Width: 220px-280px (depending on component)
Gap:             24px (desktop), 12px (mobile)
Auto Fit:        Automatically wraps on small screens
```

### Common Grid Configurations

**3 Column (Stat Cards)**
```
┌─────┐ ┌─────┐ ┌─────┐
│ Stat│ │ Stat│ │ Stat│  → Desktop
└─────┘ └─────┘ └─────┘

┌─────┐ ┌─────┐
│ Stat│ │ Stat│  → Tablet
└─────┘ └─────┘

┌─────┐
│ Stat│  → Mobile
└─────┘
```

---

## 🎬 Micro-Interactions

### Button Click
```
1. Hover:   Scale effect + shadow
2. Press:   Slight darken
3. Release: Return to hover state
4. After:   Return to rest state
```

### Tab Switch
```
1. Click target tab
2. Underline animates to new position
3. Content fades in (very quick)
4. Scroll to top (optional)
```

### Notification Bell
```
1. New notification arrives
2. Badge appears with number
3. Badge pulses (optional)
4. Slight bounce animation
```

### Profile Dropdown
```
1. Click profile avatar
2. Dropdown slides down (optional)
3. Items appear with stagger (optional)
4. Click away to close
```

---

## ♿ Accessibility Indicators

### Focus States
```
✓ Keyboard navigation visible
✓ High contrast outlines
✓ 2px+ outline width
✓ Color AND shape change (not just color)
✓ Focus trap in modals
```

### Color Usage
```
✓ Not relying on color alone
✓ Icons + labels
✓ Text + colors
✓ Badges + indicators
✓ WCAG AA compliant contrast (4.5:1)
```

### Touch Targets
```
✓ Minimum 40x40px
✓ Adequate spacing between targets
✓ Hover areas = touch areas
✓ Mobile-friendly sizing
```

---

## 📋 Checklist for New Components

When adding new components, ensure:

- [ ] Uses CSS variables for colors
- [ ] Responsive at mobile/tablet/desktop
- [ ] Proper hover/focus states
- [ ] Consistent spacing (multiples of 4px)
- [ ] Appropriate shadows for elevation
- [ ] Smooth transitions (0.3s default)
- [ ] Accessible font sizes (min 14px for body)
- [ ] High contrast text (4.5:1 minimum)
- [ ] Touch-friendly click targets (40x40px+)
- [ ] Works without JavaScript (progressive enhancement)
- [ ] Consistent with design system
- [ ] Performance optimized (transform over position)

---

## 🚀 Implementation Tips

### Best Practices
```
✓ Use CSS Variables for everything themeable
✓ Use Flexbox/Grid for layouts
✓ Use transform/opacity for animations
✓ Style :hover, :focus, :active states
✓ Test on real devices, not just browsers
✓ Use display: none instead of height: 0
✓ Optimize for touch (larger hit areas)
✓ Provide focus indicators for keyboard users
```

### Common Mistakes to Avoid
```
✗ Using pixels for responsive units
✗ Animations that flicker on mobile
✗ Missing focus states
✗ Low contrast text
✗ Tiny touch targets
✗ Heavy shadows impacting performance
✗ Colors as only indicator
✗ No fallbacks for unsupported features
```

---

**Version**: 2.0
**Last Updated**: 2024
**Status**: Active Reference
**For**: Admin Portal v2.0+
