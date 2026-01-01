"""
Style prompt templates for room design.
"""
from typing import Dict, Any

# Base prompts for different styles
STYLE_PROMPTS = {
    "modern": {
        "base": "A modern {room_type} with clean lines, minimalist furniture, neutral colors, contemporary design, sleek surfaces, open space, natural light, geometric patterns",
        "colors": "white, gray, black, beige accents",
        "furniture": "sleek sofas, minimalist tables, modern lighting fixtures",
        "materials": "glass, metal, polished wood, concrete",
    },
    "minimalist": {
        "base": "A minimalist {room_type} with sparse furniture, neutral palette, clean surfaces, uncluttered space, simple decor, natural materials, soft lighting",
        "colors": "white, cream, light gray, natural wood tones",
        "furniture": "essential pieces only, low-profile furniture, hidden storage",
        "materials": "wood, linen, cotton, natural fibers",
    },
    "rustic": {
        "base": "A rustic {room_type} with wooden beams, vintage furniture, warm colors, cozy atmosphere, natural textures, country style, traditional elements",
        "colors": "brown, beige, warm earth tones, cream",
        "furniture": "vintage pieces, reclaimed wood furniture, cozy seating",
        "materials": "wood, stone, brick, natural fabrics",
    },
    "scandinavian": {
        "base": "A Scandinavian {room_type} with light colors, natural wood, cozy textiles, hygge atmosphere, simple design, plants, soft lighting",
        "colors": "white, light gray, pastel colors, natural wood",
        "furniture": "functional furniture, light wood pieces, cozy textiles",
        "materials": "light wood, wool, linen, natural materials",
    },
    "industrial": {
        "base": "An industrial {room_type} with exposed brick, metal fixtures, raw materials, urban loft style, high ceilings, vintage elements",
        "colors": "gray, black, brown, metallic accents",
        "furniture": "metal furniture, reclaimed wood, vintage industrial pieces",
        "materials": "brick, concrete, metal, raw wood",
    },
    "bohemian": {
        "base": "A bohemian {room_type} with eclectic decor, vibrant colors, patterns, plants, layered textiles, artistic elements, relaxed atmosphere",
        "colors": "warm earth tones, jewel tones, vibrant accents",
        "furniture": "vintage pieces, floor cushions, eclectic mix",
        "materials": "textiles, plants, natural materials, art pieces",
    },
    "traditional": {
        "base": "A traditional {room_type} with classic furniture, rich colors, elegant decor, formal arrangement, timeless design, sophisticated style",
        "colors": "deep reds, navy, gold accents, rich browns",
        "furniture": "classic pieces, ornate details, formal seating",
        "materials": "wood, velvet, silk, traditional fabrics",
    },
    "contemporary": {
        "base": "A contemporary {room_type} with current trends, mixed styles, comfortable furniture, balanced design, updated classic elements",
        "colors": "neutral base with accent colors, balanced palette",
        "furniture": "comfortable modern pieces, mixed styles",
        "materials": "mixed materials, updated classics",
    },
}

# Room type mappings
ROOM_TYPES = {
    "living_room": "living room",
    "bedroom": "bedroom",
    "kitchen": "kitchen",
    "bathroom": "bathroom",
    "dining_room": "dining room",
    "office": "home office",
    "study": "study room",
    "nursery": "nursery",
}


def get_style_prompt(style: str, parameters: Dict[str, Any] = None) -> str:
    """
    Generate prompt from style and parameters.
    
    Args:
        style: Design style (e.g., 'modern', 'minimalist')
        parameters: Additional parameters including room_type, colors, etc.
    
    Returns:
        Generated prompt string
    """
    parameters = parameters or {}
    style_lower = style.lower()
    
    # Get style template
    if style_lower not in STYLE_PROMPTS:
        logger.warning(f"Unknown style '{style}', using 'modern' as default")
        style_lower = "modern"
    
    style_template = STYLE_PROMPTS[style_lower]
    
    # Get room type
    room_type = parameters.get("room_type", "living room")
    if room_type in ROOM_TYPES:
        room_type = ROOM_TYPES[room_type]
    
    # Build prompt
    prompt = style_template["base"].format(room_type=room_type)
    
    # Add optional elements
    if parameters.get("include_colors", True):
        prompt += f", {style_template['colors']}"
    
    if parameters.get("include_furniture", True):
        prompt += f", {style_template['furniture']}"
    
    if parameters.get("include_materials", True):
        prompt += f", {style_template['materials']}"
    
    # Add custom additions
    if parameters.get("additional_elements"):
        prompt += f", {parameters['additional_elements']}"
    
    # Add quality modifiers
    quality_modifiers = [
        "high quality",
        "detailed",
        "professional photography",
        "interior design",
        "architectural rendering",
    ]
    prompt += ", " + ", ".join(quality_modifiers)
    
    return prompt


# Import logger
import logging
logger = logging.getLogger(__name__)


