# Vercel AI SDK

Save each block below under the file name in its heading, in one folder, then run it as [the examples table](../README.md) says.

## `package.json`

```json
{
  "name": "terralab-vercel-ai-sdk-example",
  "private": true,
  "type": "module",
  "dependencies": {
    "@ai-sdk/mcp": "^2.0.83",
    "@ai-sdk/openai": "^4.0.101",
    "ai": "^7.0.150"
  }
}
```

## `agent.mjs`

```javascript
// A Vercel AI SDK agent with TerraLab tools.
//   npm install
//   OPENAI_API_KEY=sk-... node agent.mjs "Schools within 2 km of Kisumu centre as CSV"
// Without OPENAI_API_KEY it loads the tools and calls one directly (no model call).
import { createMCPClient } from "@ai-sdk/mcp";
import { generateText, stepCountIs } from "ai";
import { openai } from "@ai-sdk/openai";

// Your TerraLab API key, sent when TERRALAB_API_KEY is set.
const key = process.env.TERRALAB_API_KEY;
const terralab = await createMCPClient({
  transport: {
    type: "http",
    url: "https://mcp.terra-lab.ai/mcp",
    headers: key ? { Authorization: `Bearer ${key}` } : undefined,
  },
});
const tools = await terralab.tools();
console.log("TerraLab tools:", Object.keys(tools).join(", "));

if (!process.env.OPENAI_API_KEY) {
  const out = await tools.find_places.execute(
    { query: "Kisumu, Kenya", limit: 1 },
    { toolCallId: "demo", messages: [] },
  );
  console.log(out.content[0].text);
  console.log("Set OPENAI_API_KEY to run the agent.");
} else {
  const { text } = await generateText({
    model: openai("gpt-5.5"),
    tools,
    stopWhen: stepCountIs(6),
    prompt: process.argv.slice(2).join(" ") || "What is the elevation of the Eiffel Tower?",
  });
  console.log(text);
}
await terralab.close();
```
