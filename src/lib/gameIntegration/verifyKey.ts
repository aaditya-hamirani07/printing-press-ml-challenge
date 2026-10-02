import { getGameIntegrationConfig } from "./config";
import { VerifyKeyResult } from "./types";

/**
 * Valid test key for local development and testing.
 */
export const MOCK_VALID_TEST_KEY = "PP-TEST-12345";

/**
 * Verifies a game key using the local mock verification logic.
 * Used when the external Main System API is not yet configured.
 */
async function verifyKeyMock(key: string): Promise<VerifyKeyResult> {
  const normalizedKey = key.trim();

  if (normalizedKey === MOCK_VALID_TEST_KEY) {
    return {
      valid: true,
      source: "mock",
    };
  }

  return {
    valid: false,
    message: "Invalid game key",
    source: "mock",
  };
}

/**
 * Verifies a game key with the external Main Game / Leaderboard system.
 *
 * Flow:
 * 1. If real external API is configured, call the remote Main System verification endpoint.
 * 2. If not configured (development/mock mode), use the mock verifier with MOCK_VALID_TEST_KEY.
 *
 * @param key The game key string submitted by the user.
 * @returns Promise<VerifyKeyResult> indicating whether the key is valid.
 */
export async function verifyKey(key: string): Promise<VerifyKeyResult> {
  if (typeof key !== "string" || !key.trim()) {
    return {
      valid: false,
      message: "Game key must be a non-empty string",
    };
  }

  const config = getGameIntegrationConfig();

  // If real API is not yet configured, delegate to the isolated mock verifier
  if (config.isMockEnabled || !config.mainSystemApiUrl) {
    return verifyKeyMock(key);
  }

  // =========================================================================
  // TODO: Real Main System API Integration
  // =========================================================================
  // The following specifications are required to complete real API verification:
  // 1. Main System API URL: (Configured via MAIN_SYSTEM_API_URL env var)
  // 2. HTTP Method: (e.g., POST / GET)
  // 3. Request Format: (e.g., JSON body { key: string } or URL query / path param)
  // 4. Authentication Method: (e.g., Bearer token, Header 'x-api-key', Basic auth via MAIN_SYSTEM_API_KEY)
  // 5. Response Format: (e.g., { valid: boolean, teamId?: string, error?: string })
  // 6. Participant/Team Identifier: (if required in payload or returned in response)
  //
  // Example future implementation skeleton:
  //
  // const response = await fetch(`${config.mainSystemApiUrl}/verify`, {
  //   method: "POST",
  //   headers: {
  //     "Content-Type": "application/json",
  //     ...(config.mainSystemApiKey ? { Authorization: `Bearer ${config.mainSystemApiKey}` } : {}),
  //   },
  //   body: JSON.stringify({ key: key.trim() }),
  // });
  //
  // if (!response.ok) {
  //   return { valid: false, message: "Verification service failed or key rejected" };
  // }
  // const data = await response.json();
  // return { valid: Boolean(data.valid), message: data.message, source: "remote" };
  // =========================================================================

  return verifyKeyMock(key);
}
