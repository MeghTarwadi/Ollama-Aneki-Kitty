
# Ollama-Aneki-Kitty

<p align="center">
  <img src="https://github.com/user-attachments/assets/af1d17b1-ee6f-4bb9-8000-ef2dc9b3e828" alt="Ollama-Aneki-Kitty Logo" width="600">
</p>
<p align="center">
  <b>A beautiful terminal UI for Ollama with emotion visualization and custom model management</b><br>
  <i>Transform your CLI into a visually appealing, feature-rich tool for interacting with Ollama models</i>
</p>
<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#customization">Customization</a> •
  <a href="#contributing">Contributing</a>
</p>
## Features

### 🔄 Enhanced Chat Management

* **History View:** Easily browse through past conversations and pick up where you left off
* **Continue Chats:** Seamlessly continue conversations without losing context
* **Automatic Saving:** Conversations are stored in JSON format for easy recall

### 😊 Emotion Generation Mode

* **Visual Emotions:** Analyzes the emotional tone of responses and displays corresponding high-resolution PNGs
* **Rich Expression Library:** Choose from 38 predefined emotion expressions:
  * afraid, anger, annoyed, blush, catty, coffee, confused, crying, curious, default, demon, disapproval, disgust, dizzy, embarrassed, evil, excited, happy, heart, joy, laughing, love, music, naughty, pain, peaceful, pleased, proud, sad, scared, shocked, shy, sleepy, smug, surprised, sweat, thinking, wink
* **Rich Terminal Display:** PNGs render beautifully using Kitty's `icat` functionality

### 🤖 Custom Model Building

* **Create Personal Models:** Build custom models based on existing ones
* **Personalized Behavior:** Define unique system prompts for your models
* **Memory Management:** Add personalized information to your model's memory
* **No Duplication:** Uses the base model efficiently without duplicating storage

### ⚙️ Fully Configurable

* **Rich Terminal UI:** Beautiful tables, colors, and borders that work perfectly in Kitty terminal
* **ASCII Art:** Custom banners and art with random or fixed display options
* **Appearance Settings:** Customize colors, borders, and layout to your preferences
* **Behavior Control:** Fine-tune how conversations are handled and saved

## Installation

### Quick Setup

```bash
# Clone the repository
git clone https://github.com/MeghTarwadi/ollama-aneki-kitty.git

# Navigate to the directory
cd ollama-aneki-kitty

# Run the setup script
chmod +x setup.sh
./setup.sh
```

### Post-Installation

After running the setup script:

1. Restart your terminal or run:
   ```bash
   source ~/.bashrc  # If using Bash
   source ~/.zshrc   # If using Zsh
   ```
2. You can now use the `aneki` command from anywhere in your terminal:
   ```bash
   aneki           # Start the main interface
   aneki run phi3  # Run a specific model (if it exists)
   aneki new       # Create a new model
   ```

### Requirements

* **Terminal:** Kitty terminal or any terminal that supports `icat` for PNG display
* **Python:** Python 3.6 or higher
* **Ollama:** Must be installed and configured on your system

## Usage

### Basic Commands

* `aneki` - Launch the main interface
* `aneki run [model_name]` - Run a specific model
* `aneki new` - Create a new custom model
* `aneki history` - View past model configurations
* `aneki help` - Display help information
* `aneki asciiart` - Merge ASCII arts for custom display

### Creating a Custom Model

1. Run `aneki new`
2. Enter base model name (e.g., `phi3.5`)
3. Choose a name for your custom model
4. Set behavior instructions for your model
5. Optionally add information to your model's memory

### Chat Management

* Inside a conversation, type your exit code (default: `die`) to quit
* Use `aneki run read` to view past conversations
* Use `aneki run cont` to continue a previous conversation

## Configuration

The configuration file is located at `saves/default/config.conf`. Here are some key settings:

```ini
# Appearance settings
alert = [red]                # Color for alerts
asciiart = [yellow]          # Color for ASCII art  
normal = [white]             # Default text color
highlight = [blue]           # Color for highlighted text
box_borders = DOUBLE         # Box style: DOUBLE, HEAVY, SIMPLE, ROUNDED, SQUARE
box_width = 0                # Terminal width (0 = auto)

# Behavior settings
auto_clear = 1               # Clear terminal automatically (1 = yes, 0 = no)
emotion_generation = 1       # Enable emotion visualization (1 = yes, 0 = no)
exit_code = die              # Command to exit conversation
memory_length = 10           # Number of messages to keep in memory

# Content settings
pngfolder = Aneki            # Emotion style ("Aneki", "Makima", "Makima white background")
custom_path = saves/custom   # Custom data storage location
```

## Customization

### Adding Custom Emotions

Place your PNG files in the `saves/custom/exp/` directory with the emotion name as filename (e.g., `happy.png`).

### Creating Custom ASCII Art

1. Edit the ASCII art files in `saves/default/ascii1.txt` or `saves/default/ascii2.txt`
2. Run `aneki asciiart` to merge the arts
3. Your custom art will appear in the banner

## Contributing

We welcome contributions to improve Ollama-Aneki-Kitty! Feel free to:

* Report issues
* Suggest new features
* Create pull requests
* Share your custom configurations and ASCII art

## License

This project is licensed under the [MIT License]().

---

**Experience the beauty of simplicity with Ollama-Aneki-Kitty. Elevate your CLI game today!**
