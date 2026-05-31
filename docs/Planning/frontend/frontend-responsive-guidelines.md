# Frontend Responsive Guidelines (MVP)

## Objective
Ensure core workflows are usable and performant across desktop, tablet, and mobile.

## Breakpoints
- Mobile: up to 767px
- Tablet: 768px to 1023px
- Desktop: 1024px and above

## Navigation Behavior
- Desktop: persistent sidebar + top actions
- Tablet: collapsible sidebar/drawer
- Mobile: top bar + slide-out navigation

## Layout Adaptation Rules
- Multi-column forms collapse to single column on mobile.
- Wide data tables switch to stacked card/list pattern on mobile.
- Primary actions remain visible without excessive scrolling.

## Workorder Form Responsiveness
- Group related fields into collapsible sections on small screens.
- Keep required fields first and minimize context switching.
- Sticky save actions on mobile where practical.

## Dashboard/Report Responsiveness
- Priority columns visible first on tablet/mobile.
- Secondary details available via expansion drawer/row details.

## Performance Constraints
- Minimize initial payload for list views.
- Use paginated loading for large data sets.
- Avoid blocking render with non-critical UI assets.

## Accessibility Considerations
- Touch target size suitable for mobile interaction.
- Sufficient contrast and focus indicators.
- Avoid hover-only interaction patterns.

## Acceptance Criteria
- All MVP pages are usable on representative mobile/tablet/desktop sizes.
- No horizontal scrolling required for primary form completion on mobile.
- Key actions are discoverable and reachable on all supported breakpoints.