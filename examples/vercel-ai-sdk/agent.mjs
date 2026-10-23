// A Vercel AI SDK agent with TerraLab tools.
//   npm install
//   OPENAI_API_KEY=sk-... node agent.mjs "Schools within 2 km of Kisumu centre as CSV"
// Without OPENAI_API_KEY it loads the tools and calls one directly (no model call).
import { createMCPClient } from "@ai-sdk/mcp";
import { generateText, stepCountIs } from "ai";
import { openai } from "@ai-sdk/openai";

const terralab = await createMCPClient({
  transport: { type: "http", url: "https://mcp.terra-lab.ai/mcp" },
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
