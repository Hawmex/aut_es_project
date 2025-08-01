import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.rulebase import *
from core.inference_engine import *


rulebase = Rulebase(
    "example/fashion.txt",
    # Season-based color preferences
    Rule(
        Evaluation("season", "==", "spring"),
        Assignment("color_preference", "light & warm colors"),
    ),
    Rule(
        Evaluation("season", "==", "summer"),
        Assignment("color_preference", "light & cold colors"),
    ),
    Rule(
        Evaluation("season", "==", "autumn"),
        Assignment("color_preference", "dark & warm colors"),
    ),
    Rule(
        Evaluation("season", "==", "winter"),
        Assignment("color_preference", "dark & cold colors"),
    ),
    # Color preferences to clothing choices
    Rule(
        Evaluation("color_preference", "==", "light & warm colors"),
        Assignment("clothing_colors", "peach|coral|light yellow|mint|lavender"),
    ),
    Rule(
        Evaluation("color_preference", "==", "light & cold colors"),
        Assignment(
            "clothing_colors", "sky blue|aqua|lavender|cool gray|icy white"
        ),
    ),
    Rule(
        Evaluation("color_preference", "==", "dark & warm colors"),
        Assignment(
            "clothing_colors",
            "mustard|olive|burnt orange|burgundy|chocolate brown",
        ),
    ),
    Rule(
        Evaluation("color_preference", "==", "dark & cold colors"),
        Assignment(
            "clothing_colors", "navy|charcoal|emerald|deep red|black|icy white"
        ),
    ),
    # Precipitation-based footwear choices
    Rule(
        Evaluation("precipitation_probability", "<", 50),
        Assignment("precipitation_risk", "low"),
    ),
    Rule(
        Evaluation("precipitation_probability", ">=", 50),
        Assignment("precipitation_risk", "high"),
    ),
    # Temperature-based weather conditions
    Rule(
        Evaluation("temperature", "<", 8),
        Assignment("weather_condition", "cold"),
    ),
    Rule(
        LogicalAnd(
            Evaluation("temperature", ">=", 8),
            Evaluation("temperature", "<", 16),
        ),
        Assignment("weather_condition", "cool"),
    ),
    Rule(
        LogicalAnd(
            Evaluation("temperature", ">=", 16),
            Evaluation("temperature", "<", 24),
        ),
        Assignment("weather_condition", "moderate"),
    ),
    Rule(
        Evaluation("temperature", ">=", 24),
        Assignment("weather_condition", "hot"),
    ),
    # Precipitation risk to footwear
    Rule(
        Evaluation("precipitation_risk", "==", "high"),
        Assignment("footwear", "black boots"),
    ),
    Rule(
        Evaluation("precipitation_risk", "==", "low"),
        Assignment("footwear", "sneakers"),
    ),
    # Weather condition to clothing
    Rule(
        Evaluation("weather_condition", "==", "cold"),
        Assignment("clothing", "pullover|hoodie|long sleeve shirt & jacket"),
    ),
    Rule(
        Evaluation("weather_condition", "==", "cool"),
        Assignment("clothing", "pullover|hoodie|long sleeve shirt"),
    ),
    Rule(
        Evaluation("weather_condition", "==", "moderate"),
        Assignment("clothing", "long sleeve|sweat shirt"),
    ),
    Rule(
        Evaluation("weather_condition", "==", "hot"),
        Assignment("clothing", "t-shirt"),
    ),
)

engine = InferenceEngine(rulebase)

engine.infer("backward")

print("\nOutput:")

for key, value in engine.output.items():
    print(f"  {key}: {f'"{value}"' if isinstance(value, str) else value}")
