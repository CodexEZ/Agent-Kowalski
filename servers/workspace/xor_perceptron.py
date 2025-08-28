
import torch
import torch.nn as nn
import torch.optim as optim
import time

# --- Logging setup ---
def log_message(message):
    print(f"[LOG] {message}")

# --- 1. Define the Two-Layer Perceptron Model ---
class TwoLayerPerceptron(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(TwoLayerPerceptron, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU() # Activation function for the hidden layer
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

# --- 2. XOR Data ---
# Input data for XOR: (0,0), (0,1), (1,0), (1,1)
xor_inputs = torch.tensor([
    [0.0, 0.0],
    [0.0, 1.0],
    [1.0, 0.0],
    [1.0, 1.0]
], dtype=torch.float32)

# Corresponding XOR labels: 0, 1, 1, 0
xor_labels = torch.tensor([
    [0.0],
    [1.0],
    [1.0],
    [0.0]
], dtype=torch.float32)

# --- 3. Model Parameters and Device Setup ---
input_size = 2
hidden_size = 4 # A small hidden layer is enough for XOR
output_size = 1
learning_rate = 0.1
epochs = 1000

# Check for CUDA availability
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
log_message(f"Using device: {device}")

model = TwoLayerPerceptron(input_size, hidden_size, output_size).to(device)
log_message(f"Model initialized: {model}")

# Move data to the selected device
xor_inputs = xor_inputs.to(device)
xor_labels = xor_labels.to(device)

# --- 4. Loss Function and Optimizer ---
# BCEWithLogitsLoss combines sigmoid and BCELoss for numerical stability
criterion = nn.BCEWithLogitsLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)
log_message(f"Loss function: {criterion}")
log_message(f"Optimizer: {optimizer}")

# --- 5. Training Loop ---
log_message("Starting training...")
start_time = time.time()

for epoch in range(epochs):
    # Forward pass
    outputs = model(xor_inputs)
    loss = criterion(outputs, xor_labels)

    # Backward and optimize
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 100 == 0:
        log_message(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")

end_time = time.time()
training_duration = end_time - start_time
log_message("Training finished.")

# --- 6. Benchmarking and Evaluation ---
log_message("--- Benchmarking and Evaluation ---")

# Calculate accuracy
with torch.no_grad():
    model.eval() # Set model to evaluation mode
    predicted_logits = model(xor_inputs)
    predicted_probs = torch.sigmoid(predicted_logits)
    predicted_classes = (predicted_probs > 0.5).float()
    
    correct = (predicted_classes == xor_labels).sum().item()
    total = xor_labels.size(0)
    accuracy = correct / total
    
    log_message(f"Predicted outputs (logits):\\n{predicted_logits.cpu().numpy()}")
    log_message(f"Predicted probabilities:\\n{predicted_probs.cpu().numpy()}")
    log_message(f"Predicted classes:\\n{predicted_classes.cpu().numpy()}")
    log_message(f"Actual labels:\\n{xor_labels.cpu().numpy()}")
    
    log_message(f"Accuracy: {accuracy * 100:.2f}%")

log_message(f"Total training time: {training_duration:.4f} seconds")

# --- Print a summary for the user ---
# This part would print the HTML summary shown in the previous turn if executed successfully.
# For now, it\'s commented out as the script execution failed.
# print(f"""
# <div style=\"
#     background-color:#1e293b;
#     color:#f1f5f9;
#     font-family:\'Roboto\', sans-serif;
#     padding:20px;
#     border-radius:8px;
#     box-shadow:1px 2px 10px rgba(0,0,0,0.6);
#     max-width:600px;
#     margin:20px auto;
# \">
#     <h2>XOR Perceptron Training Results</h2>
#     <h3>Configuration:</h3>
#     <ul>
#         <li><strong>Model:</strong> 2-Layer Perceptron</li>
#         <li><strong>Input Size:</strong> {input_size}</li>
#         <li><strong>Hidden Size:</strong> {hidden_size}</li>
#         <li><strong>Output Size:</strong> {output_size}</li>
#         <li><strong>Learning Rate:</strong> {learning_rate}</li>
#         <li><strong>Epochs:</strong> {epochs}</li>
#         <li><strong>Device Used:</strong> {device}</li>
#     </ul>
#     <h3>Training Summary:</h3>
#     <p>Training completed in <strong>{training_duration:.4f} seconds</strong>.</p>
#     <h3>Final Evaluation:</h3>
#     <p><strong>Accuracy on XOR data:</strong> <span style=\"color:#4CAF50; font-weight:bold;\">{accuracy * 100:.2f}%</span></p>
#     <p><strong>Predicted Classes:</strong></p>
#     <pre style=\"
#         background-color: #2d3748;
#         color: #e2e8f0;
#         padding: 10px;
#         border-radius: 5px;
#         overflow-x: auto;
#         font-family: \'Fira Code\', \'Monaco\', \'Consolas\', monospace;\
#     \">{predicted_classes.cpu().numpy()}</pre>
#     <p><strong>Actual Labels:</strong></p>
#     <pre style=\"
#         background-color: #2d3748;
#         color: #e2e8f0;
#         padding: 10px;
#         border-radius: 5px;
#         overflow-x: auto;
#         font-family: \'Fira Code\', \'Monaco\', \'Consolas\', monospace;\
#     \">{xor_labels.cpu().numpy()}</pre>
# </div>
# """)
