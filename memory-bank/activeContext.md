# Asteroids Roguelike Active Context

## Current Work Focus

The project is currently in the initial planning and design phase. The feature design document (project brief) has been created, outlining the key features and gameplay mechanics for the Asteroids Roguelike game.

The immediate focus is to prepare for implementation of the first milestone: **Improve Wave Flow & Progression**. This involves creating the core game structure and implementing the wave management systems that will serve as the foundation for the roguelike progression.

## Recent Changes

- Created comprehensive project brief detailing:

  - Core gameplay mechanics
  - Roguelike elements (perks, elite enemies)
  - Progression system
  - User experience goals
  - Technical considerations
  - Implementation milestones

- Established memory bank documentation structure to track project progress and maintain contextual understanding

## Next Steps

Following the milestone sequence outlined in the project brief:

1. Begin implementing the core game framework:

   - Set up basic pygame project structure
   - Create main game loop
   - Implement basic player ship and asteroid rendering

2. Develop wave management system:

   - Wave initialization and completion detection
   - Interlude screen between waves
   - Wave countdown timer
   - Progressive difficulty scaling

3. Once wave flow is working properly, move on to perk system implementation

## Active Decisions and Considerations

### Architecture Decisions

- Determining the best approach to structure the game's component systems
- Deciding on state management pattern for game flow transitions
- Planning how to implement a flexible perk system that can be easily extended

### Design Considerations

- How to visually communicate wave transitions clearly to the player
- Creating a clean, intuitive UI for the interlude screens
- Balancing wave difficulty progression for satisfying gameplay

### Technical Considerations

- Optimizing collision detection for potentially large numbers of entities
- Planning ahead for how perks will modify player stats and behaviors
- Designing an extensible system for elite enemy behaviors

### Current Questions

- What is the best way to structure the wave difficulty scaling to ensure balanced progression?
- How should active perks be triggered (key bindings, automatic effects, etc.)?
- What visual indicators should be used to distinguish elite enemies from regular asteroids?

## Implementation Approach

The current plan is to follow an iterative development approach:

1. First implement the basic gameplay loop with simple asteroids and player ship
2. Add wave management and interlude screens
3. Implement the perk selection UI and basic passive perks
4. Add elite enemies with unique behaviors
5. Refine balance and add polish features

This approach allows for testing core gameplay before adding the more complex roguelike elements.
