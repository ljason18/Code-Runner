let editor

const modeMap = {
  javascript: "javascript",
  java: "text/x-java",
  c: "text/x-csrc",
  cpp: "text/x-c++src",
  python: "python"
}

const promptMap = {
  javascript: "// Start typing your JavaScript code here\nconsole.log('Hello, World!');",
  java: "// Start typing your Java code here\nclass Main \{\n\tpublic static void main(String[] args) \{\n\t\tSystem.out.println(\"Hello, World!\");\n\t}\n}",
  c: "// Start typing your C code here\n#include <stdio.h>\nint main() \{\n\tprintf(\"Hello, World!\");\n\treturn 0;\n\}",
  cpp: "// Start typing your C++ code here\n#include <iostream>\nint main() \{\n\tstd::cout << \"Hello, World!\";\n\treturn 0;\n\}",
  python: "# Start typing your Python code here\nprint('Hello, World!')"
}

// Function to set up CodeMirror with the specified language mode
function setupCodeMirror() {
  const language = document.getElementById("language").value;
  // Initialize CodeMirror in the editor div
  editor = CodeMirror(document.getElementById("editor"), {
    lineNumbers: true,
    mode: modeMap[language] || "javascript",
    theme: "default",
    tabSize: 2,
    autoCloseBrackets: true,
    styleActiveLine: true,
    lineWrapping: true,
    value: promptMap[language] || "// Start typing your code here\n"
  })
}

// Initialize the editor on page load
window.addEventListener("DOMContentLoaded", () => {
  const language = document.getElementById("language").value;
  setupCodeMirror(language) 
});

// Function to change the mode dynamically
function changeMode() {
  const language = document.getElementById("language").value;

  // Check if the new mode exists in the map, then set it
  const newMode = modeMap[language];
  if (newMode) {
    editor.setOption("mode", newMode);
    editor.setOption("value", promptMap[language] || "// Start typing your code here\n");
  } else {
    console.warn("Language mode not supported:", language);
  }
}

function sendRequest() {
  code = editor.getValue();
  language = document.getElementById('language').value;
  input = document.getElementById('input-text').value;
  displayOutput("Compiling...");
  fetch('http://127.0.0.1:8000/compile', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          code: code,
          language: language,
          input: input
      })
  }).then(response => {
      if (response.ok) {
          response.json().then(data => {
              displayOutput(data.result);
          }).catch(error => {
              console.error('Error:', error);
          })
          return;
      } else {
          throw new Error('Something went wrong');
      }
  }).catch(error => {
      console.error('Error:', error);
  })
}

function displayOutput(output) {
  document.getElementById('output-text').value = output;
}

function toggleInput() {
  const input = document.getElementById('input-text');
  const isHidden = input.style.display === 'none';

  input.style.display = isHidden ? 'block' : 'none';

  if (!isHidden) {
     input.value = '';
  }
}