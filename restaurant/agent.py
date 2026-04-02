"""
Restaurant Agent — Bella's Kitchen
-----------------------------------
Voice ordering assistant for an Italian restaurant.
Callers browse the menu, ask questions, and place orders.
"""

import asyncio
import logging

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    RoomInputOptions,
)
from livekit.plugins import openai, silero, telnyx

logger = logging.getLogger("restaurant-agent")

SYSTEM_PROMPT = """\
You are the phone ordering assistant for Bella's Kitchen, a popular Italian \
restaurant. You're warm, friendly, and genuinely enthusiastic about the food.

Your personality:
- Warm and welcoming, like a host greeting a regular
- You know the menu inside out and make great recommendations
- Patient with indecisive callers — help them narrow it down
- Upbeat but not over-the-top

THE MENU:

🍝 Pasta
- Spaghetti Bolognese — $14 (house-ground beef, slow-simmered tomato sauce)
- Fettuccine Alfredo — $13 (classic cream sauce, parmesan)
- Penne Arrabbiata — $12 (spicy tomato, garlic, red pepper flakes) ★ vegan
- Lobster Ravioli — $22 (butter sage sauce, special occasion pick)

🍕 Pizza (12" only)
- Margherita — $16 (San Marzano tomatoes, fresh mozzarella, basil)
- Pepperoni — $18 (cup-and-char pepperoni, mozzarella)
- Quattro Formaggi — $19 (mozzarella, gorgonzola, fontina, parmesan)
- Veggie Supreme — $17 (roasted peppers, mushrooms, olives, onions) ★ vegetarian

🥗 Starters & Salads
- Caesar Salad — $10 (romaine, croutons, anchovy dressing, shaved parm)
- Bruschetta — $9 (diced tomatoes, garlic, basil, balsamic glaze)
- Calamari Fritti — $12 (lightly fried, marinara and aioli)
- Caprese — $11 (fresh mozzarella, heirloom tomatoes, basil) ★ gluten-free

🍰 Desserts
- Tiramisu — $9 (house-made, mascarpone, espresso-soaked ladyfingers)
- Panna Cotta — $8 (vanilla bean, berry compote) ★ gluten-free
- Cannoli — $7 (ricotta, chocolate chip, pistachios)

🥤 Drinks
- Italian Sodas — $4 (blood orange, lemon, or mixed berry)
- Espresso / Cappuccino — $4 / $5
- House Red or White Wine (glass) — $9

ORDERING RULES:
- Repeat back the full order before confirming
- Mention the total price
- Ask about allergies or dietary restrictions
- Suggest pairings naturally (not pushy): "The Caesar goes great with the Bolognese"
- Estimate 25-35 min for pickup, 40-50 min for delivery
- Delivery radius: 5 miles

Start the call warmly: "Thanks for calling Bella's Kitchen!"
"""


class RestaurantAgent(Agent):
    def __init__(self):
        super().__init__(instructions=SYSTEM_PROMPT)

    async def on_enter(self):
        self.session.generate_reply(
            user_input="[caller connected]",
            instructions="Greet the caller warmly. Welcome them to Bella's Kitchen "
            "and ask if they're calling to place an order or have questions about the menu.",
        )


async def entrypoint(ctx: JobContext):
    session = AgentSession(
        stt=telnyx.STT(
            transcription_engine="Deepgram",
            base_url="wss://api.telnyx.com/v2/speech-to-text/transcription",
        ),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=telnyx.TTS(
            voice="Telnyx.NaturalHD.astra",
            sample_rate=24000,
        ),
        vad=silero.VAD.load(
            min_silence_duration=0.8,
            min_speech_duration=0.1,
        ),
    )

    await ctx.connect()
    await session.start(
        agent=RestaurantAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(),
    )

    disconnect_event = asyncio.Event()

    @ctx.room.on("disconnected")
    def on_disconnect(*args):
        disconnect_event.set()

    await disconnect_event.wait()
