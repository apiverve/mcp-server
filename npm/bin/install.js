#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

const SERVER_URL = 'https://api.apiverve.com/v1/mcp';
const TARGETS = ['claude', 'vscode', 'cursor', 'all'];

// Auth is negotiated, not configured: with no headers the server answers 401 with a
// WWW-Authenticate challenge and the client runs OAuth. --api-key skips that for
// headless setups by sending the key directly instead.
function parseArgs(argv) {
  const args = { target: 'all', apiKey: null };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--api-key') {
      args.apiKey = argv[++i] || null;
    } else if (argv[i].startsWith('--api-key=')) {
      args.apiKey = argv[i].slice('--api-key='.length);
    } else if (!argv[i].startsWith('-')) {
      args.target = argv[i];
    }
  }
  return args;
}

function userConfigDir(appName) {
  const platform = os.platform();
  if (platform === 'darwin') return path.join(os.homedir(), 'Library', 'Application Support', appName);
  if (platform === 'win32') return path.join(process.env.APPDATA, appName);
  return path.join(os.homedir(), '.config', appName);
}

// VS Code moved MCP config out of settings.json into its own mcp.json.
function getVSCodeConfigPath() {
  return path.join(userConfigDir('Code'), 'User', 'mcp.json');
}

// Cursor reads ~/.cursor/mcp.json, not the app support dir.
function getCursorConfigPath() {
  return path.join(os.homedir(), '.cursor', 'mcp.json');
}

function readJson(filePath) {
  if (!fs.existsSync(filePath)) return {};
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (err) {
    throw new Error(`${filePath} exists but is not valid JSON. Fix or remove it, then re-run.`);
  }
}

function writeJson(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf8');
}

function authHeaders(apiKey) {
  return apiKey ? { headers: { 'x-api-key': apiKey } } : {};
}

// Remote servers cannot be added through claude_desktop_config.json — that file is
// stdio-only. Custom Connectors is the supported path and it is UI-driven, so the most
// honest thing the installer can do is say so rather than write config Claude ignores.
function installToClaudeDesktop() {
  console.log('○ Claude Desktop — manual step required');
  console.log('  Claude Desktop only accepts remote MCP servers through Custom Connectors,');
  console.log('  which cannot be configured from a file. Add it in the app:');
  console.log('');
  console.log('    Settings → Connectors → Add custom connector');
  console.log(`    URL: ${SERVER_URL}`);
  console.log('');
  console.log('  Claude will prompt you to sign in on first use.');
  console.log('');
  return true;
}

function installToVSCode(apiKey) {
  const configPath = getVSCodeConfigPath();
  const config = readJson(configPath);

  if (!config.servers) config.servers = {};
  config.servers.apiverve = { type: 'http', url: SERVER_URL, ...authHeaders(apiKey) };

  writeJson(configPath, config);
  console.log(`✅ VS Code configured — ${configPath}`);
  return true;
}

function installToCursor(apiKey) {
  const configPath = getCursorConfigPath();
  const config = readJson(configPath);

  // Cursor infers the transport from the presence of url; type is for stdio servers only.
  if (!config.mcpServers) config.mcpServers = {};
  config.mcpServers.apiverve = { url: SERVER_URL, ...authHeaders(apiKey) };

  writeJson(configPath, config);
  console.log(`✅ Cursor configured — ${configPath}`);
  return true;
}

function printManualConfig() {
  console.error('\n💡 Configure manually instead:');
  console.error('');
  console.error('  VS Code — mcp.json');
  console.error(`    { "servers": { "apiverve": { "type": "http", "url": "${SERVER_URL}" } } }`);
  console.error('');
  console.error('  Cursor — ~/.cursor/mcp.json');
  console.error(`    { "mcpServers": { "apiverve": { "url": "${SERVER_URL}" } } }`);
  console.error('');
  console.error('  Claude Desktop — Settings → Connectors → Add custom connector');
  console.error(`    ${SERVER_URL}`);
  console.error('');
}

function main() {
  console.log('\n🔌 APIVerve MCP Server Installer\n');

  const { target, apiKey } = parseArgs(process.argv.slice(2));

  // An unrecognised target used to match no branch and exit 0 having done nothing.
  if (!TARGETS.includes(target)) {
    console.error(`Unknown target "${target}".`);
    console.error(`Usage: apiverve-mcp [${TARGETS.join('|')}] [--api-key KEY]\n`);
    process.exit(1);
  }

  if (apiKey) {
    console.log('Using API key auth — the key will be written into the config file.\n');
  } else {
    console.log('Using OAuth — no key is stored; your client will prompt you to sign in.\n');
  }

  try {
    if (target === 'claude' || target === 'all') installToClaudeDesktop();
    if (target === 'vscode' || target === 'all') installToVSCode(apiKey);
    if (target === 'cursor' || target === 'all') installToCursor(apiKey);

    console.log('\n✨ Done. Restart your MCP client to pick up the change.');
    console.log('   Manage access and API keys at https://apiverve.com\n');
  } catch (error) {
    console.error('\n❌ Installation failed:', error.message);
    printManualConfig();
    process.exit(1);
  }
}

main();
