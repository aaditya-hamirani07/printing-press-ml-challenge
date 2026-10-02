/**
 * Configuration for the external Main Game / Leaderboard integration.
 *
 * NOTE:
 * - These environment variables are strictly server-side (no NEXT_PUBLIC_ prefix).
 * - They are optional during development so mock verification can run without configuration.
 */
export interface GameIntegrationConfig {
  mainSystemApiUrl?: string;
  mainSystemApiKey?: string;
  isMockEnabled: boolean;
}

export function getGameIntegrationConfig(): GameIntegrationConfig {
  const mainSystemApiUrl = process.env.MAIN_SYSTEM_API_URL?.trim();
  const mainSystemApiKey = process.env.MAIN_SYSTEM_API_KEY?.trim();

  return {
    mainSystemApiUrl: mainSystemApiUrl || undefined,
    mainSystemApiKey: mainSystemApiKey || undefined,
    // When no API URL is configured, fallback to mock verification
    isMockEnabled: !mainSystemApiUrl,
  };
}
