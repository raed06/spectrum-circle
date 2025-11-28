import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


class LocalFineTunedModel:
    """
    Wrapper for a local LoRA fine-tuned model (e.g., a small open-source model).
    
    It loads the base model and the LoRA adapter, merging them to enable inference,
    and exposes a Gemini-like generation interface.
    """

    def __init__(self, base_model_name: str, adapter_path: str):
        """
        Initializes the model by loading weights and tokenizer.

        Args:
            base_model_name (str): Hugging Face name of the pre-trained base model.
            adapter_path (str): Local path (or Hugging Face path) to the LoRA adapter weights.
        """

        # Device selection
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(adapter_path)
        self.tokenizer.pad_token = self.tokenizer.eos_token

        # Load base model
        base_model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch.float32
        ).to(self.device)

        # Load LoRA adapter
        self.model = PeftModel.from_pretrained(base_model, adapter_path)
        self.model.eval()
        self.model.to(self.device)


    # Gemini-compatible interface
    def generate_content(self, prompt: str, max_new_tokens=180):
        """
        Synchronous method mimicking the standard Gemini SDK interface.
        Used for non-async parts of the code.
        """
        return SimpleResponse(self._generate(prompt, max_new_tokens))

    async def generate_content_async(self, prompt: str, max_new_tokens=180):
        """
        Asynchronous method required by the AgentOrchestrator for smooth integration
        within an ASGI server (like FastAPI).
        
        Note: The actual generation is synchronous, so we run it directly. 
        For true non-blocking async, this would use a thread executor.
        """
        return SimpleResponse(self._generate(prompt, max_new_tokens))

    # Internal generation method
    def _generate(self, prompt, max_new_tokens):
        """
        Core logic for tokenizing the input and generating the response using
        the Hugging Face model interface.
        """
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )

        decoded = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return decoded


class SimpleResponse:
    """
    Helper class to mimic the response object returned by the
    google-generativeai SDK (e.g., response.text).
    This allows the LocalFineTunedModel to drop into the existing framework.
    """
    def __init__(self, text: str):
        self.text = text
