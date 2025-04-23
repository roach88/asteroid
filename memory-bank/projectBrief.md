# 🚀 Asteroids Roguelike Feature Design Doc

🎯 tl;dr

Enhance the classic arcade-style “Asteroids” gameplay with roguelike progression: upgrades between waves, elite enemies, and refined pacing through smarter wave flow and transitions.

⸻

🧩 Goals

Business Goals
• Create a replayable, engaging solo dev game project that feels polished and fun.
• Showcase mechanics that blend retro gameplay with modern roguelike depth.
• Potentially publish or showcase on portfolio/GitHub.

User Goals
• Feel a growing sense of power and challenge with each wave.
• Make meaningful choices through upgrades.
• Experience surprise and variety through randomized elements.

Non-Goals
• Multiplayer support.
• Full game persistence/saves.
• Complex in-game economy (yet).

⸻

💡 Feature Sections

## Upgrade & Perk System

Overview: After each wave, the player picks one of 3 randomly drawn perks. Perks grant passive or active bonuses and can synergize for powerful builds.

Examples:
• Passive: +15% movement speed, +1 HP, bullets pierce through 1 enemy.
• Active: EMP Blast (stuns asteroids in radius), Shield Recharge, Teleport.

Design Considerations:
• Show perks on a clean UI between waves.
• Limit choices to 1 of 3 for quick decision-making.
• Store selected perks per session (no carryover on death).

⸻

## Elite Enemies

Overview: Introduce tougher asteroid variants that appear starting at later waves (e.g. wave 5+). Elites have unique properties and yield bonus credits.

Types:
• Exploder: On death, spawns multiple small fast-moving shards.
• Shielded: Takes reduced damage unless shot from behind.
• Swarm Leader: Causes nearby asteroids to move in coordinated patterns.

Design Considerations:
• Distinct visuals or outlines for elite enemies.
• Unique behavior patterns (random movement overrides).
• Rarity scales with wave level.

⸻

## Gameplay Flow & Progression Enhancements

Current State:
• Linear wave progression.
• All waves have roughly similar timing/composition ramp.
• Instant jump to next wave once all enemies die.

Proposed Enhancements:
• Wave Interlude Screen: Pause + display stats, allow perk choice, and build tension before next wave.
• Wave Timer/Countdown: Add delay (e.g. 3 seconds) before wave begins to let player prepare.
• Wave Composition Scaling: Use functions (not just multipliers) to gradually increase wave complexity—more enemy types, formations, etc.
• Health Regen Option: Heal +1 HP after wave if HP < max, or tie healing to a perk.
• Boss Waves (later): Every 5th wave could feature a miniboss-style asteroid.

⸻

🎮 User Stories
• “As a player, I want to choose perks after each wave so I can shape my build.”
• “As a player, I want some breathing room between waves so the pacing feels right.”
• “As a player, I want new enemy types to shake up the gameplay as I progress.”

⸻

🧠 Narrative

You’re a lone pilot in a cursed sector of space, where waves of increasingly bizarre and dangerous asteroids warp in through dimensional rifts. With every wave cleared, you tap into alien tech—temporary perks that enhance your survival. But you don’t just get stronger—your enemies do too. By wave 10, it’s a bullet ballet of chaos and reflexes. How far can you go before the void consumes you?

⸻

📈 Success Metrics
• Session duration (target 5–10 mins average).
• Perk selection rate (ensure they’re all being chosen).
• Average wave reached before death.
• Elite enemy engagement and credit yields.

⸻

🧰 Technical Considerations
• Add Perk class and perk manager.
• Use simple pygame menu/overlay system for interlude screens.
• Track player state, perks, and wave number.
• Extend Asteroid class to handle elite variants.

⸻

🛠 Milestones & Sequencing

1. Improve Wave Flow & Progression – XX weeks
2. Add Upgrade & Perk System – XX weeks
3. Design + Implement Elite Enemies – XX weeks

⸻
