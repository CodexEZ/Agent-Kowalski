
import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleLLM(nn.Module):
    def __init__(self, vocab_size, d_model, nhead, num_layers, dim_feedforward, max_seq_len, dropout=0.1):
        super(SimpleLLM, self).__init__()
        self.d_model = d_model

        # 1. Token Embeddings
        self.embedding = nn.Embedding(vocab_size, d_model)

        # 2. Positional Embeddings (learned or sinusoidal)
        # For simplicity, let's use learned positional embeddings
        self.positional_embedding = nn.Embedding(max_seq_len, d_model)

        # 3. Transformer Encoder Layer
        # We'll use a standard TransformerEncoderLayer as a building block
        # For a true LLM (generative), you'd typically use a TransformerDecoderLayer
        # or a custom decoder block with masked self-attention.
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True # Input/output shape: (batch_size, seq_len, d_model)
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)

        # 4. Output Layer
        # Projects the transformer output back to the vocabulary size
        self.fc_out = nn.Linear(d_model, vocab_size)

        self.dropout = nn.Dropout(dropout)

    def forward(self, src):
        # src shape: (batch_size, seq_len)
        seq_len = src.size(1)
        batch_size = src.size(0)

        # Generate positional indices
        positions = torch.arange(0, seq_len, device=src.device).unsqueeze(0).expand(batch_size, -1)

        # Apply embeddings
        token_embeddings = self.embedding(src)
        pos_embeddings = self.positional_embedding(positions)

        # Combine token and positional embeddings
        x = self.dropout(token_embeddings + pos_embeddings)

        # Pass through transformer encoder
        # Transformer expects (seq_len, batch_size, d_model) if batch_first=False
        # But we set batch_first=True, so it expects (batch_size, seq_len, d_model)
        transformer_output = self.transformer_encoder(x)

        # Project to vocabulary size
        output = self.fc_out(transformer_output)

        return output

# --- Example Usage ---
if __name__ == "__main__':
    vocab_size = 10000  # Example vocabulary size
    d_model = 512       # Embedding dimension
    nhead = 8           # Number of attention heads
    num_layers = 6      # Number of transformer layers
    dim_feedforward = 2048 # Dimension of the feedforward network
    max_seq_len = 256   # Maximum sequence length

    # Instantiate the model
    llm_model = SimpleLLM(vocab_size, d_model, nhead, num_layers, dim_feedforward, max_seq_len)
    print("Model Architecture:")
    print(llm_model)

    # Create a dummy input
    batch_size = 4
    seq_len = 50
    dummy_input = torch.randint(0, vocab_size, (batch_size, seq_len)) # (batch_size, seq_len)

    print(f"
Dummy Input Shape: {dummy_input.shape}")

    # Pass through the model
    output = llm_model(dummy_input)

    print(f"Output Shape (logits for next token prediction): {output.shape}")
    # Expected output shape: (batch_size, seq_len, vocab_size)
    # The last dimension represents the logits for each token in the vocabulary
    # for each position in the sequence.

    # Example of getting the predicted next token for the last position in the sequence
    predicted_logits_for_last_token = output[:, -1, :]
    predicted_token_ids = torch.argmax(predicted_logits_for_last_token, dim=-1)
    print(f"Predicted Token IDs for last position in each batch: {predicted_token_ids}")
