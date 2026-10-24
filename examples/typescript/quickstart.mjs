// List the TerraLab tools and run one with the official MCP TypeScript SDK.
//   npm install
//   TERRALAB_API_KEY=tlk_... node quickstart.mjs
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const client = new Client({ name: "terralab-quickstart", version: "1.0.0" });
// Your TerraLab API key, sent when TERRALAB_API_KEY is set.
const key = process.env.TERRALAB_API_KEY;
const requestInit = key ? { headers: { Authorization: `Bearer ${key}` } } : undefined;
await client.connect(
  new StreamableHTTPClientTransport(new URL("https://mcp.terra-lab.ai/mcp"), { requestInit }),
);

const { tools } = await client.listTools();
console.log("Tools:", tools.map((t) => t.name).join(", "));

const result = await client.callTool({
  name: "get_elevation",
  arguments: { mode: "point", points: ["Mont Blanc summit", "Lake Annecy"] },
});
console.log(result.content[0].text);
await client.close();
