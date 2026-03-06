# Admin Portal CSS & Design System Documentation

## Color Palette

### Primary Colors
```css
--primary: #dc2626                  /* Red - Main brand color *)
--primary-dark: #991b1b             /* Dark Red - Darker accent *)
--primary-light: #fecaca            /* Light Red - Subtle accents *)
```

### Status Colors
```css
--success: #10b981                  /* Green - Success/Approved *)
--warning: #f59e0b                  /* Amber - Warning/Attention *)
--info: #3b82f6                     /* Blue - Information *)
--danger: #ef4444                   /* Bright Red - Errors *)
```

### Neutral Colors
```css
--bg: #f9fafb                       /* Light background *)
--bg-secondary: #ffffff             /* White surfaces *)
--border: #e5e7eb                   /* Standard border *)
--border-light: #f3f4f6             /* Light border *)
--text-primary: #1f2937             /* Dark text *)
--text-secondary: #6b7280           /* Medium gray text *)
--text-light: #9ca3af               /* Light gray text *)
```

### Effects
```css
--shadow: 0 4px 12px rgba(0, 0, 0, 0.1)
--shadow-lg: 0 10px 28px rgba(0, 0, 0, 0.12)
--transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1)
```

---

## Typography System

### Font Stack
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
```

### Font Weights
- **400 (Regular)**: Body text
- **500 (Medium)**: Secondary information
- **600 (Semi-bold)**: Labels, strong text
- **700 (Bold)**: Headers, important text
- **800 (Extra-bold)**: Large values, emphasis

### Font Sizes
- **32px**: Profile header name
- **28px**: Page titles, large stats
- **22px**: Section headers
- **18px**: Card titles
- **16px**: Regular body text
- **15px**: UI controls
- **14px**: Secondary text
- **13px**: Labels, captions
- **12px**: Small text, badges

---

## Component System

### Header Component
```css
.header {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    padding: 16px 24px;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: var(--shadow-lg);
}

.header-content {
    display: flex;
    justify-content: space-between;
    gap: 24px;
    max-width: 1400px;
    margin: 0 auto;
}
```

**Includes:**
- Logo section with icon
- Admin name display
- Notification bell with badge
- Profile dropdown menu
- Enhanced logout button

### Tab Navigation
```css
.tabs {
    display: flex;
    gap: 8px;
    border-bottom: 2px solid var(--border);
    margin-bottom: 32px;
}

.tab-btn {
    padding: 14px 24px;
    font-weight: 600;
    color: var(--text-secondary);
    transition: var(--transition);
}

.tab-btn.active {
    color: var(--primary);
}

.tab-btn.active::after {
    content: '';
    position: absolute;
    bottom: -2px;
    height: 3px;
    background: linear-gradient(90deg, var(--primary) 0%, var(--primary-dark) 100%);
}
```

### Stat Card
```css
.stat-card {
    background: white;
    padding: 28px 24px;
    border-radius: 12px;
    border: 1px solid var(--border);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    transition: var(--transition);
}

.stat-card::before {
    content: '';
    position: absolute;
    top: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--primary) 0%, var(--primary-dark) 100%);
    border-radius: 2px;
}

.stat-card:hover {
    transform: translateY(-8px);
    box-shadow: var(--shadow-lg);
    border-color: var(--primary-light);
}

.stat-value {
    font-size: 36px;
    font-weight: 800;
    color: var(--primary);
    letter-spacing: -1px;
}

.stat-label {
    font-size: 14px;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
```

### Button Styles

#### Primary Button
```css
.btn-primary {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    color: white;
}

.btn-primary:hover {
    box-shadow: 0 8px 20px rgba(220, 38, 38, 0.3);
}
```

#### Success Button
```css
.btn-success {
    background: linear-gradient(135deg, var(--success) 0%, #059669 100%);
    color: white;
}

.btn-success:hover {
    box-shadow: 0 8px 20px rgba(16, 185, 129, 0.3);
}
```

#### Info Button
```css
.btn-info {
    background: linear-gradient(135deg, var(--info) 0%, #2563eb 100%);
    color: white;
}

.btn-info:hover {
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
}
```

#### Default Button
```css
.btn:not(.btn-primary):not(.btn-success):not(.btn-warning):not(.btn-info) {
    background: white;
    border: 1.5px solid var(--border);
    color: var(--text-primary);
}

.btn:not(.btn-primary):not(.btn-success):not(.btn-warning):not(.btn-info):hover {
    background: var(--border-light);
}
```

### Request Card
```css
.request-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    transition: var(--transition);
}

.request-card::before {
    content: '';
    position: absolute;
    left: 0;
    width: 4px;
    background: linear-gradient(180deg, var(--primary) 0%, var(--primary-dark) 100%);
}

.request-card:hover {
    border-color: var(--primary-light);
    box-shadow: 0 8px 20px rgba(220, 38, 38, 0.12);
    transform: translateY(-2px);
}
```

### Filter Panel
```css
.filters {
    display: flex;
    gap: 12px;
    margin-bottom: 28px;
    padding: 20px;
    background: white;
    border-radius: 12px;
    border: 1px solid var(--border);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}
```

### Modal Dialog
```css
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(4px);
    z-index: 1000;
    justify-content: center;
    align-items: center;
}

.modal-content {
    background: white;
    border-radius: 16px;
    padding: 36px;
    max-width: 600px;
    width: 90%;
    animation: slideUp 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
```

### Form Elements
```css
.form-input, .form-textarea {
    width: 100%;
    padding: 12px 16px;
    border: 1.5px solid var(--border);
    border-radius: 8px;
    font-size: 14px;
    background: var(--bg);
    transition: var(--transition);
}

.form-input:focus, .form-textarea:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 4px rgba(220, 38, 38, 0.1);
    background: white;
}
```

### Table Component
```css
.table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    border-radius: 12px;
    border: 1px solid var(--border);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.table th {
    background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
    padding: 18px 16px;
    text-align: left;
    font-weight: 700;
    border-bottom: 2px solid var(--border);
    color: var(--text-secondary);
}

.table tbody tr:hover {
    background: linear-gradient(90deg, var(--border-light) 0%, transparent 100%);
}
```

---

## Profile Section Components

### Profile Header
```css
.profile-header {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    padding: 48px 32px;
    border-radius: 16px;
    display: flex;
    gap: 32px;
    align-items: flex-end;
    box-shadow: var(--shadow-lg);
    margin-bottom: 32px;
}

.profile-avatar-large {
    width: 140px;
    height: 140px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 56px;
    font-weight: 700;
    border: 3px solid rgba(255, 255, 255, 0.3);
}
```

### Profile Card
```css
.profile-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 28px 24px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    transition: var(--transition);
}

.profile-card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-4px);
    border-color: var(--primary-light);
}

.profile-card-value {
    font-size: 28px;
    font-weight: 800;
    color: var(--primary);
    letter-spacing: -1px;
}
```

### Profile Section
```css
.profile-section {
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 32px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    margin-bottom: 24px;
}

.profile-section h2 {
    font-size: 18px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 10px;
    padding-bottom: 16px;
    border-bottom: 2px solid var(--border);
}

.profile-section h2::before {
    content: '';
    width: 4px;
    height: 24px;
    background: linear-gradient(180deg, var(--primary) 0%, var(--primary-dark) 100%);
    border-radius: 2px;
}
```

---

## Responsive Design

### Mobile-First Approach
```css
@media (max-width: 768px) {
    /* Header adjustments */
    .header-content {
        flex-direction: column;
    }

    /* Profile adjustments */
    .profile-header {
        flex-direction: column;
        text-align: center;
        padding: 32px 24px;
    }

    .profile-grid {
        grid-template-columns: 1fr;
    }

    /* Stats adjustments */
    .stat-value {
        font-size: 28px;
    }

    /* Button adjustments */
    .action-buttons {
        flex-direction: column;
    }

    .action-buttons .btn {
        width: 100%;
    }

    /* Table adjustments */
    .table th, .table td {
        padding: 12px 8px;
        font-size: 12px;
    }

    /* Filter adjustments */
    .filters {
        flex-direction: column;
        padding: 16px;
    }

    .filters input {
        width: 100% !important;
    }
}
```

---

## Animation System

### Slide Up Animation (Modals)
```css
@keyframes slideUp {
    from {
        transform: translateY(30px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}
```

### Fade In Animation (Alerts)
```css
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
```

### Transitions
```css
--transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

/* Applied to: hover effects, state changes, animations */
```

---

## Layout System

### Container
```css
.container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 32px 24px;
}
```

### Grid Layouts

**Stat Grid**
```css
.stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 24px;
}
```

**Profile Grid**
```css
.profile-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
}
```

**Info Grid**
```css
.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 24px;
}
```

---

## Elevation System (Z-Index)

```css
0       /* Default layer *)
50      /* Notification dropdown *)
100     /* Header (sticky) *)
1000    /* Modal overlay *)
```

---

## Accessibility Considerations

✅ **Semantic HTML**: Proper heading hierarchy, labels on forms
✅ **Color Contrast**: WCAG AA compliant text contrast ratios
✅ **Focus States**: Clear visual indicators for keyboard navigation
✅ **Touch Targets**: Buttons and links are 40px+ tall/wide
✅ **Alt Text**: Icons have meaningful labels
✅ **Skip Links**: Quick navigation options (when needed)
✅ **Form Labels**: All inputs properly labeled
✅ **Error Messages**: Clear and actionable

---

## Performance Optimizations

- **CSS Variables**: Single point of change for theming
- **Efficient Selectors**: Specific, short selectors
- **Hardware Acceleration**: Transform/opacity for animations
- **Reduced Motion**: Support for `prefers-reduced-motion`
- **Mobile-First**: Load only necessary styles
- **Minimal Repaints**: Smooth 60fps animations
- **Optimized Files**: Well-organized, maintainable CSS

---

## Browser Support

- ✅ Chrome/Edge 88+
- ✅ Firefox 85+
- ✅ Safari 14+
- ✅ Mobile browsers (iOS Safari, Chrome Android)

**Fallbacks available for**:
- CSS Grid (Flexbox alternative)
- Gradients (solid color backup)
- Transforms (opacity fallback)
- Backdrop filters (none fallback)

---

## Customization Guide

### Changing Primary Color
```css
:root {
    --primary: #YOUR_COLOR;
    --primary-dark: #DARKER_SHADE;
    --primary-light: #LIGHTER_SHADE;
}
```

### Adjusting Spacing
```css
/* Increase all padding/gaps by modifying base values */
.stat-card { padding: 28px 24px; }  /* Change these */
.filter { gap: 12px; }              /* and these */
```

### Modifying Shadows
```css
--shadow: 0 2px 8px rgba(0, 0, 0, 0.1);    /* Lighter */
--shadow-lg: 0 20px 40px rgba(0, 0, 0, 0.15); /* Heavier */
```

---

**Last Updated**: 2024
**Status**: Complete & Production Ready
**Version**: 2.0 (Enhanced UI)
