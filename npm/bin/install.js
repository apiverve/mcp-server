#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

const SERVER_CONFIG = {
  type: 'sse',
  url: 'https://api.apiverve.com/v1/mcp'
};

function getClaudeConfigPath() {
  const platform = os.platform();

  if (platform === 'darwin') {
    // macOS
    return path.join(os.homedir(), 'Library', 'Application Support', 'Claude', 'claude_desktop_config.json');
  } else if (platform === 'win32') {
    // Windows
    return path.join(process.env.APPDATA, 'Claude', 'claude_desktop_config.json');
  } else {
    // Linux
    return path.join(os.homedir(), '.config', 'Claude', 'claude_desktop_config.json');
  }
}

function getVSCodeConfigPath() {
  const platform = os.platform();

  if (platform === 'darwin') {
    return path.join(os.homedir(), 'Library', 'Application Support', 'Code', 'User', 'settings.json');
  } else if (platform === 'win32') {
    return path.join(process.env.APPDATA, 'Code', 'User', 'settings.json');
  } else {
    return path.join(os.homedir(), '.config', 'Code', 'User', 'settings.json');
  }
}

function getCursorConfigPath() {
  const platform = os.platform();

  if (platform === 'darwin') {
    return path.join(os.homedir(), 'Library', 'Application Support', 'Cursor', 'User', 'settings.json');
  } else if (platform === 'win32') {
    return path.join(process.env.APPDATA, 'Cursor', 'User', 'settings.json');
  } else {
    return path.join(os.homedir(), '.config', 'Cursor', 'User', 'settings.json');
  }
}

function ensureDirectoryExists(filePath) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function installToClaudeDesktop() {
  const configPath = getClaudeConfigPath();

  console.log('📍 Claude Desktop config path:', configPath);

  ensureDirectoryExists(configPath);

  let config = {};

  // Read existing config
  if (fs.existsSync(configPath)) {
    try {
      const content = fs.readFileSync(configPath, 'utf8');
      config = JSON.parse(content);
    } catch (err) {
      console.warn('⚠️  Could not parse existing config, creating new one');
    }
  }

  // Ensure mcpServers section exists
  if (!config.mcpServers) {
    config.mcpServers = {};
  }

  // Add APIVerve server
  config.mcpServers.apiverve = SERVER_CONFIG;

  // Write config
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8');

  console.log('✅ APIVerve MCP server added to Claude Desktop config');
  return true;
}

function installToVSCode() {
  const configPath = getVSCodeConfigPath();

  console.log('📍 VS Code config path:', configPath);

  ensureDirectoryExists(configPath);

  let config = {};

  // Read existing config
  if (fs.existsSync(configPath)) {
    try {
      const content = fs.readFileSync(configPath, 'utf8');
      config = JSON.parse(content);
    } catch (err) {
      console.warn('⚠️  Could not parse existing config, creating new one');
    }
  }

  // Ensure mcp section exists (VS Code / Cline extension)
  if (!config.mcp) {
    config.mcp = { servers: {} };
  }
  if (!config.mcp.servers) {
    config.mcp.servers = {};
  }

  // Add APIVerve server
  config.mcp.servers.APIVerve = {
    type: 'sse',
    url: SERVER_CONFIG.url,
    headers: {}
  };

  // Write config
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8');

  console.log('✅ APIVerve MCP server added to VS Code config');
  return true;
}

function installToCursor() {
  const configPath = getCursorConfigPath();

  console.log('📍 Cursor config path:', configPath);

  ensureDirectoryExists(configPath);

  let config = {};

  // Read existing config
  if (fs.existsSync(configPath)) {
    try {
      const content = fs.readFileSync(configPath, 'utf8');
      config = JSON.parse(content);
    } catch (err) {
      console.warn('⚠️  Could not parse existing config, creating new one');
    }
  }

  // Ensure mcpServers section exists
  if (!config.mcpServers) {
    config.mcpServers = {};
  }

  // Add APIVerve server
  config.mcpServers.apiverve = SERVER_CONFIG;

  // Write config
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8');

  console.log('✅ APIVerve MCP server added to Cursor config');
  return true;
}

function main() {
  console.log('\n🔌 APIVerve MCP Server Installer\n');

  const args = process.argv.slice(2);
  const target = args[0] || 'all';

  try {
    if (target === 'claude' || target === 'all') {
      installToClaudeDesktop();
    }

    if (target === 'vscode' || target === 'all') {
      installToVSCode();
    }

    if (target === 'cursor' || target === 'all') {
      installToCursor();
    }

    console.log('\n✨ Installation complete!');
    console.log('\n📖 Next steps:');
    console.log('   1. Restart your MCP client (Claude Desktop, VS Code, or Cursor)');
    console.log('   2. Sign up at https://apiverve.com');
    console.log('   3. Authorize when prompted');
    console.log('   4. Start using 249+ APIs!\n');
  } catch (error) {
    console.error('\n❌ Installation failed:', error.message);
    console.error('\n💡 Manual installation:');
    console.error('   Add this to your MCP client config:\n');
    console.error('   {');
    console.error('     "mcpServers": {');
    console.error('       "apiverve": {');
    console.error('         "type": "sse",');
    console.error('         "url": "https://api.apiverve.com/v1/mcp"');
    console.error('       }');
    console.error('     }');
    console.error('   }\n');
    process.exit(1);
  }
}

main();
