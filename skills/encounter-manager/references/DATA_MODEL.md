# Data Model

## encounter_request

Store the incoming structured request in `state/inputs/encounter_request.json`.

Recommended shape:

```json
{
  "encounter_id": "TP-001",
  "campaign_id": "CAMPAIGN-001",
  "scene_id": "SCENE-001",
  "encounter_type": "social",
  "tone": "tense, strange, low-magic",
  "objective": "Get past the ferryman guarding passage across the river.",
  "difficulty": "normal",
  "narrative_context": "The river crossing is the only obvious way forward.",
  "trigger": "The party reaches the dock at dusk.",
  "stakes": {
    "success": "The party crosses safely.",
    "failure": "The ferryman refuses and alerts nearby patrol.",
    "complication": "The ferryman reveals a hidden price or secret condition."
  },
  "environment": {
    "location_name": "Black River Dock",
    "description": "A narrow ferry platform rocks against the dock in cold mist.",
    "tags": ["water", "mist", "unstable", "only-route-forward"]
  },
  "players": [
    {
      "id": "CHAR-001",
      "name": "Nyra",
      "traits": ["sharp", "intuitive", "calm"],
      "conditions": [],
      "inventory_tags": [],
      "narrative_role": "observer"
    }
  ],
  "npcs": [],
  "monsters": [],
  "prior_state_refs": [],
  "campaign_import": {
    "summary": {
      "resolved": "Optional status-specific summary override for the markdown export."
    },
    "resolved_loops": {
      "resolved": ["LOOP-001 | Optional loop to mark resolved when this encounter lands."]
    },
    "new_loops": {
      "resolved": ["LOOP-002 | Optional loop to open from this scene | pressure: medium | next: follow the new lead"]
    },
    "world_changes": {
      "resolved": ["Optional world-state bullet for campaign import."]
    },
    "rewards": {
      "resolved": ["Optional campaign reward bullet."]
    },
    "consequences": {
      "resolved": ["Optional campaign consequence bullet."]
    },
    "suggested_follow_up": {
      "resolved": ["Optional follow-up bullet for the campaign manager."]
    }
  }
}
```

`campaign_import` is optional. When present, `resolve_encounter.py` uses it to populate the campaign-manager markdown export instead of falling back to generic placeholder bullets.

## scene_state

The local scene state lives in `state/encounters/scene_state.json`.

Keep:
- `round`
- `phase`
- `tension`
- `active_hazards`
- `active_opportunities`
- `environment_changes`
- `unresolved_threads`
- `spotlight_order`

## normalized_actions

The normalized player actions live in `state/encounters/normalized_actions.json`.

Each action should include:
- `player_id`
- `approach`
- `intent`
- `target_id`
- `uses_item_tag`
- `risk_level`
- `aiding_player_id`

## encounter_result

Write the final structured output to `state/outputs/encounter_result.json`.
