# cardboard-architecture
A mockup of the possible architecture for Project Cardboard.

Corresponds to the uml here https://app.diagrams.net/#G1FgDDXJkHqSUfd3N0scSGIVnR5D1kXhla

- Fully decoupled view and controller communicating via api, with shared models
- Available action calculation on a readonly model
- Sending Effects from the user interface (non deterministic actions)
- Converting those Effects into Events in the controller (determinstic accounts of what actually happened)
- Allowing listeners to trigger off of that event, and respond with their own effects (when you draw a card, gain one life)
- Returning game_state, event pairs to the view to animate
