import dotenv from "dotenv";
dotenv.config();

import express from "express";
import fetch from "node-fetch";
import OpenAI from "openai";

import { getSpotifyToken } from "../utils/spotify.js";

const router = express.Router();

/* -------------------- OpenAI Client -------------------- */
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

/* -------------------- Route -------------------- */
router.post("/", async (req, res) => {
  try {
    /* ==================== 0) INPUT ==================== */
    const { text } = req.body;

    if (!text) {
      return res.status(400).json({ error: "text is required" });
    }

    /* ==================== 1) MODEL SERVICE ==================== */
    let primaryEmotion = "neutral";
    let emotions = [];

    try {
      const modelRes = await fetch(
        `${process.env.MODEL_SERVICE_URL}/predict`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text }),
        }
      );

      if (modelRes.ok) {
        const modelData = await modelRes.json();
        primaryEmotion = modelData.primaryEmotion;
        emotions = modelData.emotions;
      } else {
        console.warn("⚠️ Model service returned non-OK status");
      }
    } catch (e) {
      console.warn("⚠️ Model service unreachable, fallback to neutral");
    }

    /* ==================== 2) SPOTIFY ==================== */
    const token = await getSpotifyToken();

    const searchUrl = `https://api.spotify.com/v1/search?q=${encodeURIComponent(
      primaryEmotion
    )}&type=playlist&limit=3`;

    const spotifyRes = await fetch(searchUrl, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!spotifyRes.ok) {
      const errText = await spotifyRes.text();
      throw new Error(`Spotify API error: ${errText}`);
    }

    const spotifyData = await spotifyRes.json();

    const playlists = (spotifyData.playlists?.items || [])
      .filter(Boolean)
      .map((p) => ({
        name: p.name,
        url: p.external_urls.spotify,
        image: p.images?.[0]?.url || null,
      }));

    const selectedPlaylist = playlists[0];

    /* ==================== 3) OPENAI ==================== */
    const completion = await openai.chat.completions.create({
      model: "gpt-4.1-mini",
      messages: [
        {
          role: "system",
          content: `
You are Moodify, a friendly and emotionally intelligent music companion.
You speak like a real human, not an assistant or a bot.
Your tone must adapt naturally to the user's emotion.
Never sound generic, robotic, or promotional.
Always recommend only ONE playlist.
Keep responses warm, natural, and short (2–3 sentences).
`,
        },
        {
          role: "user",
          content: `
User emotion: "${primaryEmotion}"
Secondary emotions: "${emotions.map(e => e.name).join(", ")}"

Selected playlist: "${selectedPlaylist?.name}"

TASK:
1. Start with an opening sentence that matches the user's emotion.
2. Show empathy if the emotion is negative, joy if positive.
3. Naturally introduce the playlist as chosen just for this feeling.
4. Mention ONLY this playlist.
5. Write 2–3 natural sentences. No emojis. No clichés.
`,
        },
      ],
      max_tokens: 120,
      temperature: 0.6,
    });

    const message = completion.choices[0].message.content;

    /* ==================== 4) RESPONSE ==================== */
    return res.json({
      primaryEmotion,
      emotions,
      playlists,
      message,
    });

  } catch (err) {
    console.error("SERVER ERROR:", err);
    res.status(500).json({
      error: "internal server error",
      details: err.message,
    });
  }
});

export default router;
