![Ollama-Aneki-Kitty](https://github.com/user-attachments/assets/af1d17b1-ee6f-4bb9-8000-ef2dc9b3e828)


**Ollama-Aneki-Kitty is a sleek terminal user interface (TUI) designed specifically for Kitty Terminal, enhancing the experience of using the Ollama-Aneki with high-resolution PNGs instead of pixelated images of emotion. With its intuitive and visually appealing design, it transforms the CLI into a more user-friendly and feature-rich tool.**


# Features

#### 1. **Enhanced Chat Management**
   - **History View**: Easily access your ***past conversations*** and pick up right where you left off. Conversation history is stored in JSON format.
   - **Continue Chats**: Seamlessly continue conversations without losing context.

https://github.com/user-attachments/assets/b1120195-777a-45ba-9373-2b0a213c64cb

#### 2. **Emotion Generation Mode**
   - Analyzes the emotions of the conversation and provides a corresponding high-resolution PNG from 38 predefined emotion files, such as:
     - afraid, anger, joy, surprised, sadness... and many more.
   - PNGs are displayed in high resolution using `icat`, visually reflecting the emotional tone of the chat.

https://github.com/user-attachments/assets/c8d601f8-c597-4230-9e2a-448984e1aeb6

#### 3. **Custom Model Building**
   - Allows users to create ***custom models*** based on existing ones with ***personalized behavior***.

https://github.com/user-attachments/assets/0a8e6b33-1c2e-4381-978e-2bdf9dec4e4d

#### 4. **Configurable Settings**
   - ***Highly customizable*** configuration options to tailor the interface and features to your preferences:
     ```ini
     alert = [red]                                   // Alerts color
     asciiart = [yellow]                             // ASCII art color
     asciiart_index = -1                             // Use -1 for random ASCII art or specify an index for fixed ASCII art
     ascii2_path = saves/default/ascii2.txt          // Path to single-string ASCII art
     asciis1_path = saves/default/ascii1.txt         // Path to ASCII art list; separated by three line breaks
     ask_for_Topic = 1                               // Set to 1 to ask for a topic name; 0 saves history based on date and time
     auto_clear = 1                                  // Set to 0 to disable auto-clear; use an integer to enable clearing the console
     box_borders = DOUBLE                            // Box style: DOUBLE, HEAVY, SIMPLE, ROUNDED, or SQUARE
     box_width = 0                                   // Set to 0 for maximum terminal width or specify an integer for a fixed width
     custom_path = saves/custom                      // Use an absolute path if custom saves are stored in a different location
     emotion_generation = 1                          // Set to 0 to disable emotion generation in tables; 1 enables it
     exit_code = die                                 // Exit code to quit conversation; not case-sensitive
     highlight = [blue]                              // Highlighted areas color
     max_respose_size = 500                          // Maximum response size in alphabets to be fed for emotion regeneration
     memory_length = 10                              // Conversation memory length; higher value may slow down performance
     normal = [white]                                // Default color for majority of content
     pngfolder = Aneki                               // PNG emotion groups: "Aneki," "Makima," or "Makima white background"
     reprint_everytime = 0                           // Reprints the entire conversation after prompt generation if terminal size changes
     user_conversation = >>                          // String displayed when the user replies
     width = 40                                      // Width for pixel art emotions; resize PNG accordingly
     ```

---

# Why Use Ollama-Aneki-Kitty?

- **High-Resolution Visuals**: Experience visually stunning PNGs rendered beautifully with Kitty's `icat`.
- **Improved Productivity**: Save time by efficiently managing conversations.
- **Better Experience**: The TUI adds a touch of elegance and simplicity to your interactions.
- **Exclusive Features**: Access functionalities like history, emotion generation, and custom model creation not available in the standard Ollama CLI by default.

# Contributions
We welcome contributions to improve Ollama-Aneki-Kitty. Feel free to:
- Submit issues
- Suggest new features
- Create pull requests

---

## License
This project is licensed under the [MIT License](LICENSE).

---

**Experience the beauty of simplicity with Ollama-Aneki-Kitty. Elevate your CLI game today!**

