const line = require("@line/bot-sdk");
const https = require("https");

const config = {
  channelAccessToken: "YOUR_CHANNEL_ACCESS_TOKEN",
  channelSecret: "YOUR_CHANNEL_SECRET",
  endpoint: "YOUR_CF_ENDPOINT"  // Replace with your Cloudflare endpoint
};\n \n// Create a new LINE client
const client = new line.Client(config);

addEventListener("fetch", event => {
  event.respondWith(handleRequest(event.request));
});

// Handle incoming HTTP requests
async function handleRequest(request) {
  // Receive the webhook event from LINE
  const body = await request.body();
  const signature = request.headers.get("X-Line-Signature");
  const events = client.parse(body, signature);

  // Handle each event
  for (const event of events) {
    if (event.type === "message" && event.message.type === "text") {
      // Echo the same message back to the user
      await client.replyMessage(event.replyToken, {
        type: "text",
        text: event.message.text
      });
    }
  }

  return new Response("OK");
}
