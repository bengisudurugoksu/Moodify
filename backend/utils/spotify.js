import fetch from "node-fetch";

let cachedToken = null;
let tokenExpiresAt = 0;

export async function getSpotifyToken() {
  const now = Date.now();

  // cache
  if (cachedToken && now < tokenExpiresAt) {
    return cachedToken;
  }

  const authString = `${process.env.SPOTIFY_CLIENT_ID}:${process.env.SPOTIFY_CLIENT_SECRET}`;
  const base64Auth = Buffer.from(authString).toString("base64");

  const res = await fetch("https://accounts.spotify.com/api/token", {
    method: "POST",
    headers: {
      Authorization: `Basic ${base64Auth}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: "grant_type=client_credentials",
  });

  const data = await res.json();

  cachedToken = data.access_token;
  tokenExpiresAt = now + data.expires_in * 1000;

  return cachedToken;
}
