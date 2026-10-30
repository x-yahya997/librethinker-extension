# LibreThinker

LibreThinker is a LibreOffice Writer extension that brings AI-assisted text 
editing directly into your sidebar. It integrates an LLM to help you rewrite, improve, 
and edit text without leaving your document.

You can use a free online LLM (no signup required), OpenRouter, self-hosted Ollama, LM Studio, or bring your own API key (ChatGPT/OpenAI, Mistral, Groq, etc).

![Screenshot](./screenshot.png)

## Quickstart

Download the latest extension file (.oxt) from the [releases page](https://github.com/mihailthebuilder/librethinker-extension/releases/) or [build from source](#building-from-source). Open LibreOffice Writer, go to *Tools > Extension Manager > Add*, and select the downloaded `.oxt` file to install.

Open the sidebar in LibreOffice; you should see the lightbulb icon for the extension. Click the icon to open the extension panel, then you're ready to start using the free model!

## OpenRouter & OpenAI-Compatible Endpoints

You can connect directly to **OpenRouter**, **LM Studio**, **llama.cpp**, **vLLM**, or any OpenAI-compatible provider:

1. **Model ID**: Enter the model identifier as expected by the provider (e.g. `nvidia/nemotron-3-ultra-550b-a55b:free` or `google/gemma-2-9b-it`). **No `sh/` prefix is required** when a custom `Model URL` is set.
2. **Model URL**: Set the provider's chat completions endpoint:
   - **OpenRouter**: `https://openrouter.ai/api/v1/chat/completions`
   - **LM Studio**: `http://127.0.0.1:1234/v1/chat/completions`
   - **Local / Remote OpenAI-compatible server**: `http://<host>:<port>/v1/chat/completions`
3. **Model API key**: You can provide the raw API key or reference an environment variable (see below).
4. Click **Save settings**.

## Environment Variable Resolution for API Keys

You don't need to hardcode sensitive API keys into LibreOffice:
- In the **Model API key** field, you can type the environment variable name:
  - Plain: `OPENROUTER_API_KEY`
  - Linux/macOS style: `$OPENROUTER_API_KEY`
  - Windows style: `%OPENROUTER_API_KEY%`
- If you use an OpenRouter URL and leave the API key blank, the extension will automatically look up `OPENROUTER_API_KEY` from your environment (including the Windows User Registry).

## Customizable System Prompt

The BYOK/Ollama Settings section includes a **System prompt** text area:
- Customize assistant behavior, output constraints (e.g. *"Return only the rewritten text without markdown fences"*), tone, or persona.
- Changes are persisted locally across LibreOffice sessions when you click **Save settings**.

## Ollama

For local Ollama instances:
- **Default endpoint**: Leave `Model URL` blank and prefix the model ID with `sh/` (e.g. `sh/gemma2:2b`). Requests will go to `http://localhost:11434/api/chat`.
- **Custom endpoint**: Alternatively, specify `Model URL` (e.g. `http://localhost:11434/api/chat` or a remote URL) and use the plain model name (e.g. `gemma2:2b`) without any prefix.

## Bring Your Own Key (LibreThinker Cloud Backend)

You can also use the cloud proxy path via [LiteLLM's model directory](https://models.litellm.ai/):
1. Copy the model name from LiteLLM (e.g. `gpt-4o` or `mistral/mistral-medium`).
2. Leave `Model URL` blank.
3. Set your vendor's API key in **Model API key**.

## Building from Source

To package the `.oxt` extension yourself:

```powershell
# On Windows PowerShell
.\build.ps1
```

This generates `dist/LibreThinker.oxt`, which can be added directly via LibreOffice *Tools > Extension Manager > Add...*.

## Buy me a coffee

You can leave a tip at https://ko-fi.com/mihailmarian to support the original author's work.

## License

See [license.txt](./extension/registration/license.txt) for license.

## More info

Check out the project's site [librethinker.com](https://librethinker.com)
