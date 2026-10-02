import { NextRequest, NextResponse } from "next/server";
import { verifyKey } from "@/lib/gameIntegration";
import { VerifyKeyResponse } from "@/lib/gameIntegration/types";

/**
 * POST /api/printing-press/verify
 *
 * Verifies a game key provided by the contestant.
 *
 * Request Body:
 * {
 *   "key": "PP-TEST-12345"
 * }
 *
 * Responses:
 * - 200 OK: { "valid": true }
 * - 200 OK: { "valid": false, "message": "Invalid game key" }
 * - 400 Bad Request: { "valid": false, "message": "..." } (missing key, empty key, malformed JSON)
 * - 500 Internal Server Error: { "valid": false, "message": "Internal server error" }
 */
export async function POST(req: NextRequest): Promise<NextResponse<VerifyKeyResponse>> {
  let body: unknown;

  // 1. Parse JSON body and handle malformed JSON
  try {
    body = await req.json();
  } catch {
    return NextResponse.json(
      {
        valid: false,
        message: "Invalid JSON in request body",
      },
      { status: 400 }
    );
  }

  // 2. Validate request payload structure
  if (!body || typeof body !== "object") {
    return NextResponse.json(
      {
        valid: false,
        message: "Request body must be a JSON object",
      },
      { status: 400 }
    );
  }

  const { key } = body as { key?: unknown };

  // 3. Handle missing key
  if (typeof key !== "string") {
    return NextResponse.json(
      {
        valid: false,
        message: "Game key is required and must be a string",
      },
      { status: 400 }
    );
  }

  // 4. Handle empty key
  const trimmedKey = key.trim();
  if (trimmedKey.length === 0) {
    return NextResponse.json(
      {
        valid: false,
        message: "Game key cannot be empty",
      },
      { status: 400 }
    );
  }

  // 5. Verify the key through the isolated integration module
  try {
    const result = await verifyKey(trimmedKey);

    if (result.valid) {
      return NextResponse.json({ valid: true }, { status: 200 });
    }

    return NextResponse.json(
      {
        valid: false,
        message: result.message || "Invalid game key",
      },
      { status: 200 }
    );
  } catch (error) {
    // Avoid logging secrets; log standard internal error information
    console.error(
      "Game key verification failed unexpectedly:",
      error instanceof Error ? error.message : "Unknown error"
    );

    return NextResponse.json(
      {
        valid: false,
        message: "Internal server error during key verification",
      },
      { status: 500 }
    );
  }
}
