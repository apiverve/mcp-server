#!/usr/bin/env node
// APIVerve local MCP server. The MCP protocol layer runs here; every tool call is a
// plain HTTPS request to api.apiverve.com with the caller's x-api-key. The tool catalog
// is baked into manifest.json at build time, so the server starts and lists tools
// without a key — the key is only read when a tool is actually invoked.
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const here = dirname(fileURLToPath(import.meta.url));
const manifest = JSON.parse(readFileSync(join(here, "manifest.json"), "utf8"));

// Map a manifest param type (from OpenAPI) to a JSON Schema type MCP clients accept.
const JSON_TYPES = new Set(["string", "number", "integer", "boolean", "array", "object"]);

function toInputSchema(params) {
  const properties = {};
  const required = [];
  for (const p of params) {
    const prop = { type: JSON_TYPES.has(p.type) ? p.type : "string" };
    if (p.description) prop.description = p.description;
    if (p.example !== undefined) prop.examples = [p.example];
    properties[p.name] = prop;
    if (p.required) required.push(p.name);
  }
  const schema = { type: "object", properties };
  if (required.length) schema.required = required;
  return schema;
}

const tools = Object.entries(manifest.apis).map(([id, api]) => ({
  name: id,
  description: api.title && api.title !== api.description
    ? `${api.title}: ${api.description}`
    : api.description || api.title || id,
  inputSchema: toInputSchema(api.params || []),
}));

async function callApi(id, args) {
  const api = manifest.apis[id];
  if (!api) throw new Error(`Unknown API "${id}". See https://apiverve.com/marketplace for the catalog.`);

  const apiKey = process.env.APIVERVE_API_KEY;
  if (!apiKey) {
    throw new Error(
      "APIVERVE_API_KEY is not set. Get a free API key at https://dashboard.apiverve.com and set it in the server's environment."
    );
  }

  const url = new URL(manifest.apiBase + api.path);
  const init = { method: api.method, headers: { "x-api-key": apiKey, accept: "application/json" } };

  if (api.method === "GET") {
    for (const p of api.params || []) {
      if (args[p.name] !== undefined) url.searchParams.set(p.name, String(args[p.name]));
    }
  } else {
    init.headers["content-type"] = "application/json";
    const body = {};
    for (const p of api.params || []) {
      if (args[p.name] !== undefined) body[p.name] = args[p.name];
    }
    init.body = JSON.stringify(body);
  }

  const res = await fetch(url, init);
  const text = await res.text();

  // APIVerve status semantics: 401 is the only bad-key verdict; 403 usually means the
  // account is out of credits; 429 is the burst rate limit.
  if (res.status === 401) throw new Error("APIVerve rejected the API key (401). Check APIVERVE_API_KEY.");
  if (res.status === 403)
    throw new Error(
      "Request refused (403) — this usually means the account is out of credits, not a bad key. Check your plan at https://dashboard.apiverve.com."
    );
  if (res.status === 404) throw new Error(`Unknown API "${id}" (404). See https://apiverve.com/marketplace for the catalog.`);
  if (res.status === 429) throw new Error("Rate limited (429). Wait a moment and retry.");

  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch {
    throw new Error(`APIVerve returned a non-JSON response (HTTP ${res.status}).`);
  }
  if (parsed.status && parsed.status !== "ok") {
    throw new Error(parsed.error || `APIVerve returned status "${parsed.status}" (HTTP ${res.status}).`);
  }
  return parsed.data !== undefined ? parsed.data : parsed;
}

const server = new Server(
  { name: "apiverve", version: manifest.version },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools }));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  try {
    const data = await callApi(name, args || {});
    return { content: [{ type: "text", text: JSON.stringify(data, null, 2) }] };
  } catch (e) {
    return { content: [{ type: "text", text: e.message }], isError: true };
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
console.error(`APIVerve MCP server ready — ${tools.length} tools (stdio).`);
