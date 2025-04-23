# Asteroids Roguelike Active Context

## Current Work Focus

The project has progressed from the initial planning phase into active implementation. The core game structure has been established and significant progress has been made on the first milestone: **Improve Wave Flow & Progression**.

The immediate focus is on completing the remaining features of the first milestone and polishing the currently implemented features, particularly the perk system and elite enemy behaviors.

## Recent Changes

- Implemented core game components:

  - Main game loop with state management system (playing, wave transition, perk selection, game over)
  - Entity system including Player, Asteroids, Shots
  - Wave management with difficulty scaling
  - UI system for game transitions and perk selection

- Completed key features of the first milestone:

  - Wave interlude screen with countdown timer
  - Wave composition scaling with increasing difficulty per wave
  - Transition between gameplay and perk selection

- Made significant progress on the perk system:

  - Implemented PerkManager class
  - Created UI for perk selection between waves
  - Added player method to apply perks

- Implemented elite enemy system:
  - Refactored elite asteroid design to use class inheritance
  - Created base EliteAsteroid class and specialized child classes:
    - ExploderAsteroid: Creates more fragments when destroyed
    - ShieldedAsteroid: Has directional shielding that reduces damage
    - SwarmLeaderAsteroid: Makes unpredictable movements
  - Implemented factory pattern to create the appropriate elite asteroid type
  - Enhanced elite mechanics to make them harder to kill and more threatening
  - Added attack angle-based damage calculation for shielded asteroids

## Next Steps

Following the progress already made:

1. Complete remaining first milestone features:

   - Add health regeneration system
   - Implement boss waves (every 5th wave)

2. Finalize perk system implementation:

   - Complete effects for all passive perks
   - Implement active perk mechanics
   - Balance perk impacts for meaningful choices

3. Polish elite enemy implementation:

   - Further enhance visual distinction for elite enemies
   - Fine-tune elite behaviors for better gameplay
   - Balance elite spawn rates across waves

4. Once above items are complete, focus on game polish:
   - Add more visual feedback for player actions
   - Improve UI elements for better readability
   - Add sound effects and potentially background music

## Active Decisions and Considerations

### Architecture Decisions

- The game uses a state-based architecture with distinct states for gameplay, wave transitions, perk selection, and game over
- Entity management is handled through pygame sprite groups for efficient updates and collision detection
- Wave management is implemented with scaling difficulty based on wave number
- Elite enemies now use class inheritance for cleaner, more maintainable code
- Factory pattern is used to instantiate the appropriate elite asteroid type

### Design Considerations

- Elite enemies have enhanced visual and behavioral distinctions:
  - Color-based identification for different types
  - Pulsing effects to highlight elite status
  - Type-specific visual elements (crosses, shields, orbital rings)
- Directional attack damage for shielded asteroids creates tactical gameplay
- Elite enemies are now significantly harder to kill with increased health and damage reduction

### Technical Considerations

- Collision detection now includes attack angle calculation for more tactical combat
- The new inheritance-based structure makes adding new elite types simpler
- Elite enemy behaviors are now encapsulated in their respective classes

### Current Questions

- What additional elite types might be interesting to implement?
- How can we further improve visual effects to communicate elite status?
- Should active perks provide counters to specific elite asteroid types?
- Should boss waves have unique visuals or behaviors beyond regular elites?

## Implementation Approach

The current development approach follows the planned iterative process:

1. Core gameplay loop is now functional with wave management
2. Perk system foundation is in place but needs completion
3. Elite enemies have been refactored with improved inheritance structure
4. Next focus will be on completing health regeneration and boss waves
5. Final polish will focus on visual feedback and balancing

This approach has allowed for testing the core mechanics while gradually layering in the roguelike elements.
