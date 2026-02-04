def get_llm_solution(error_log):
    """OpenRouter (AI) fallback with verified Model ID and max_tokens"""
    try:
        # Use Llama 3.3 70B (Free version) - check for typos in the string!
        selected_model = "meta-llama/llama-3.3-70b-instruct:free"

        response = client.chat.completions.create(
            model=selected_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a Senior DevOps Engineer. Provide a concise, 2-line technical fix."
                },
                {"role": "user", "content": f"Fix this error: {error_log}"}
            ],
            max_tokens=500,  # Prevents 402 Error
            extra_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "AIOps Sentinel",
            }
        )
        return {
            "solution": response.choices[0].message.content,
            "source": f"openrouter_{selected_model.split('/')[1]}"
        }
    except Exception as e:
        # Detailed error reporting for debugging
        return {"solution": f"AI Error: {str(e)}", "source": "error"}