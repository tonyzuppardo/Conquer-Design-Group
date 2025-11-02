# PRD: Sparkle Button Click Effect

## Introduction/Overview

Add a delightful sparkle particle animation to the "Generate Folder Structure" button that triggers when clicked. This feature enhances user engagement by providing satisfying visual feedback during the folder generation process, making the app feel more polished and modern while maintaining the existing lime green (#BFFF00) brand aesthetic.

**Problem it solves:** The current button interaction feels static. Adding a sparkle effect creates a more engaging, premium user experience that makes the action feel more rewarding and confirms user interaction.

**Goal:** Create a visually appealing particle burst animation that activates when the user clicks the submit button, reinforcing the modern, playful design language of the app.

## Goals

1. Add a particle burst sparkle effect to the main submit button
2. Use lime green (#BFFF00) and white sparkles to match the app's color scheme
3. Trigger animation every time the button is clicked (when enabled)
4. Ensure animation is smooth and performs well on mobile devices
5. Maintain accessibility and not interfere with form submission

## User Stories

**User Story 1:**
As a user, when I click the "Generate Folder Structure" button, I want to see a satisfying sparkle animation so that I get immediate visual feedback that my action was registered and the app feels more engaging.

**User Story 2:**
As a mobile user, I want the sparkle animation to run smoothly without lag so that the app feels responsive and professional on my device.

**User Story 3:**
As a user, I want the sparkle effect to match the app's lime green theme so that it feels like a cohesive part of the design.

## Functional Requirements

### FR-1: Sparkle Animation Trigger
The system must trigger a particle burst animation when the user clicks the "Generate Folder Structure" button (submitBtn).

### FR-2: Particle Design
The sparkles must be:
- Small circular particles (2-4px diameter)
- Mix of lime green (#BFFF00) and white (#FFFFFF) colors
- Randomly sized within the specified range

### FR-3: Particle Behavior
Particles must:
- Burst outward from the click point in random directions (360-degree spread)
- Travel 50-100px from the origin point
- Fade out as they travel (opacity: 1 → 0)
- Complete animation within 0.6 seconds
- Self-remove from DOM after animation completes

### FR-4: Particle Count
Each click must generate 12-15 particles for a visible but not overwhelming effect.

### FR-5: Animation Performance
The animation must:
- Use CSS transforms and opacity for smooth performance
- Not block or delay form submission
- Work on mobile devices without lag

### FR-6: Disabled State Handling
The sparkle effect must NOT trigger when the button is in disabled state.

### FR-7: Multiple Click Support
The animation must support multiple rapid clicks without breaking or accumulating particles (proper cleanup).

## Non-Goals (Out of Scope)

- Sound effects when clicking
- Sparkle effects on other buttons or elements
- Customizable sparkle colors or intensity by users
- Sparkle animation on hover (only on click)
- Persistent sparkle effects or continuous animations
- Backend integration (purely client-side CSS/JavaScript feature)

## Design Considerations

### Visual Design
- Particles should feel lightweight and energetic
- Animation timing should feel snappy (0.6s total)
- Sparkles should complement, not distract from, the button's primary function
- Maintain the modern, playful aesthetic established by the lime green theme

### Color Palette
- Primary sparkle color: #BFFF00 (lime green) - 60% of particles
- Secondary sparkle color: #FFFFFF (white) - 40% of particles
- Particles fade from opacity 1 to 0

### Animation Curve
- Use `ease-out` timing for natural deceleration
- Particles should slow down as they reach their destination

## Technical Considerations

### Implementation Approach
- Pure JavaScript + CSS solution (no external libraries needed)
- Create particles as absolute positioned div elements
- Use CSS transitions for smooth animation
- Use `requestAnimationFrame` or CSS animations for best performance
- Clean up particle elements after animation completes

### Browser Compatibility
- Must work on modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile Safari and Chrome on Android
- Gracefully degrade on older browsers (no sparkles, but button still works)

### Performance
- Use CSS `transform` and `opacity` for GPU acceleration
- Limit particle count to 15 per click to avoid performance issues
- Remove DOM elements after animation to prevent memory leaks

### Code Location
All code should be added to `/templates/index.html`:
- CSS animations in the `<style>` section
- JavaScript sparkle function in the `<script>` section

## Success Metrics

1. **User Engagement:** Animation triggers successfully on 100% of button clicks (when enabled)
2. **Performance:** Animation completes smoothly at 60fps on mobile devices
3. **No Bugs:** Form submission works correctly with sparkle effect active
4. **Visual Polish:** Sparkles enhance the perceived quality of the app
5. **Clean Code:** No memory leaks or DOM buildup after multiple clicks

## Open Questions

None - all requirements are well-defined for implementation.

---

## Implementation Notes for Developer

**Key implementation steps:**
1. Add CSS keyframe animation for particle movement and fade
2. Create JavaScript function `createSparkles(event)` that:
   - Gets click coordinates relative to button
   - Generates 12-15 particle divs
   - Positions them at click point
   - Applies random direction, distance, and color
   - Removes particles after 600ms
3. Attach click event listener to submitBtn
4. Ensure particles are positioned absolutely relative to button or form container

**Suggested particle generation logic:**
- Use `Math.random()` for angles (0-360 degrees)
- Use `Math.random()` for distance (50-100px)
- Randomly assign lime green or white color (60/40 split)
- Set particle size: 2-4px randomly

**CSS considerations:**
- `position: absolute` for particles
- `pointer-events: none` so particles don't interfere with clicks
- `z-index` to layer above button but not block other UI
