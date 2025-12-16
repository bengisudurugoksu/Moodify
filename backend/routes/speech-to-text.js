import dotenv from "dotenv";
dotenv.config();

import express from "express";
import multer from "multer";
import fs from "fs";
import path from "path";
import OpenAI from "openai";
import { File } from "node:buffer";

// Polyfill for older Node versions
if (!globalThis.File) {
  globalThis.File = File;
}

const router = express.Router();

/* -------------------- OpenAI Client -------------------- */
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

/* -------------------- Multer Configuration -------------------- */
const storage = multer.diskStorage({
  destination: "uploads/",
  filename: (req, file, cb) => {
    // Extract extension from original filename or use .m4a as default
    const ext = path.extname(file.originalname) || '.m4a';
    const uniqueName = `recording-${Date.now()}${ext}`;
    cb(null, uniqueName);
  }
});

const upload = multer({
  storage: storage,
  limits: { fileSize: 25 * 1024 * 1024 }, // 25MB limit
  fileFilter: (req, file, cb) => {
    const allowedMimes = [
      "audio/m4a",
      "audio/mp4",
      "audio/mpeg",
      "audio/mpga",
      "audio/mp3",
      "audio/wav",
      "audio/webm",
      "audio/x-m4a",
      "audio/aac",
      "audio/3gpp",
      "audio/3gpp2",
    ];
    // Accept if mimetype matches OR if filename has audio extension
    const hasAudioExtension = /\.(m4a|mp4|mp3|wav|webm|aac|3gp)$/i.test(file.originalname);
    
    if (allowedMimes.includes(file.mimetype) || hasAudioExtension) {
      cb(null, true);
    } else {
      console.log('❌ Rejected file:', file.originalname, 'mimetype:', file.mimetype);
      cb(new Error("Invalid file type. Only audio files are allowed."));
    }
  },
});

/* -------------------- Route -------------------- */
router.post("/", upload.single("audio"), async (req, res) => {
  let filePath = null;

  try {
    if (!req.file) {
      return res.status(400).json({ error: "No audio file uploaded" });
    }

    filePath = req.file.path;

    // Use OpenAI Whisper to transcribe audio
    const transcription = await openai.audio.transcriptions.create({
      file: fs.createReadStream(filePath),
      model: "whisper-1",
      language: "en", // Optional: specify language for better accuracy
    });

    const transcribedText = transcription.text;

    if (!transcribedText || transcribedText.trim() === "") {
      return res.status(400).json({ error: "Could not transcribe audio" });
    }

    // Clean up the uploaded file
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }

    // Return the transcribed text
    return res.json({
      text: transcribedText,
    });

  } catch (err) {
    console.error("SPEECH-TO-TEXT ERROR:", err);

    // Clean up file on error
    if (filePath && fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }

    res.status(500).json({
      error: "Failed to process audio",
      details: err.message,
    });
  }
});

export default router;
