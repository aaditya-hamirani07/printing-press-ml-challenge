/**
 * Request payload for verifying a game key.
 */
export interface VerifyKeyRequest {
  key: string;
}

/**
 * Response returned to the client/caller for game key verification.
 */
export interface VerifyKeyResponse {
  valid: boolean;
  message?: string;
}

/**
 * Internal result returned from the verification integration layer.
 */
export interface VerifyKeyResult {
  valid: boolean;
  message?: string;
  source?: "mock" | "remote";
}
