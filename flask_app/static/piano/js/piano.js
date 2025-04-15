// Mapping piano keys to corresponding keyboard keys
const keyMapping = {
  whiteKey1: ['A'], // Maps the first white piano key to 'A'
  whiteKey2: ['S'], // Maps the second white piano key to 'S'
  whiteKey3: ['D'], // And so on for each white key
  whiteKey4: ['F'],
  whiteKey5: ['G'],
  whiteKey6: ['H'],
  whiteKey7: ['J'],
  whiteKey8: ['K'],
  whiteKey9: ['L'],
  whiteKey10: [';'], // Last white key maps to ';'
  blackKey1: ['W'], // Maps the first black piano key to 'W'
  blackKey2: ['E'], // Maps the second black key to 'E'
  blackKey3: ['T'],
  blackKey4: ['Y'],
  blackKey5: ['U'],
  blackKey6: ['O'],
  blackKey7: ['P']  // Last black key maps to 'P'
};

// Function to display all keyboard keys associated with piano keys
function displayAllKeyboardKeys() {
  const pianoKeys = Object.keys(keyMapping); // Get all piano keys

  pianoKeys.forEach(key => { // Iterate through each piano key
    const keyboardKeys = keyMapping[key]; // Get the corresponding keyboard key(s)
    const pianoKey = document.getElementById(key); // Get the piano key element by its ID

    const tool = document.createElement('div'); // Create a new div for the keyboard key display
    tool.className = 'keyboard'; // Add a class for styling
    tool.innerHTML = keyboardKeys.map(k => `<span>${k}</span>`).join(''); // Display each key as a span
    pianoKey.appendChild(tool); // Append the keyboard display to the piano key element
  });
}

// Function to remove all keyboard key displays
function removeAllKeyboardKeys() {
  const tools = document.querySelectorAll('.keyboard'); // Select all elements with class 'keyboard'
  tools.forEach(tool => tool.remove()); // Remove each tool
}

// Add event listeners to the piano for mouseover and mouseout
const piano = document.querySelector('.piano');
piano.addEventListener('mouseover', displayAllKeyboardKeys); // Show keys when mouse is over the piano
piano.addEventListener('mouseout', removeAllKeyboardKeys); // Remove keys when mouse leaves the piano

// Mapping keyboard keys to white piano keys
const whiteKeyMapping = {
  'A': 'whiteKey1', // 'A' key maps to the first white key
  'S': 'whiteKey2', // 'S' to second white key, and so on
  'D': 'whiteKey3',
  'F': 'whiteKey4',
  'G': 'whiteKey5',
  'H': 'whiteKey6',
  'J': 'whiteKey7',
  'K': 'whiteKey8',
  'L': 'whiteKey9',
  ';': 'whiteKey10'
};

// Event listener for when a key is pressed down
document.addEventListener('keydown', event => {
  const key = event.key.toUpperCase(); // Get the pressed key in uppercase
  const pianoKey = whiteKeyMapping[key]; // Find the corresponding piano key

  if (pianoKey) { // If the key is mapped to a piano key
    const whiteKey = document.getElementById(pianoKey); // Get the piano key element
    whiteKey.classList.add('pressed'); // Add 'pressed' class for styling
  }
});

// Event listener for when a key is released
document.addEventListener('keyup', event => {
  const key = event.key.toUpperCase(); // Get the released key in uppercase
  const pianoKey = whiteKeyMapping[key]; // Find the corresponding piano key

  if (pianoKey) { // If the key is mapped to a piano key
    const whiteKey = document.getElementById(pianoKey); // Get the piano key element
    whiteKey.classList.remove('pressed'); // Remove the 'pressed' class
  }
});

// Mapping keyboard keys to black piano keys
const blackKeyMapping = {
  'W': 'blackKey1', // 'W' key maps to the first black key
  'E': 'blackKey2', // 'E' maps to second black key, and so on
  'T': 'blackKey3',
  'Y': 'blackKey4',
  'U': 'blackKey5',
  'O': 'blackKey6',
  'P': 'blackKey7'
};

// Event listener for when a black piano key is pressed down
document.addEventListener('keydown', event => {
  const key = event.key.toUpperCase(); // Get the pressed key in uppercase
  const pianoKey = blackKeyMapping[key]; // Find the corresponding black piano key

  if (pianoKey) { // If the key is mapped to a piano key
    const blackKey = document.getElementById(pianoKey); // Get the piano key element
    blackKey.classList.add('pressed'); // Add 'pressed' class for styling
  }
});

// Event listener for when a black piano key is released
document.addEventListener('keyup', event => {
  const key = event.key.toUpperCase(); // Get the released key in uppercase
  const pianoKey = blackKeyMapping[key]; // Find the corresponding black piano key

  if (pianoKey) { // If the key is mapped to a piano key
    const blackKey = document.getElementById(pianoKey); // Get the piano key element
    blackKey.classList.remove('pressed'); // Remove the 'pressed' class
  }
});

// Sound mapping from key codes to sound files
const sound = {
  65: "http://carolinegabriel.com/demo/js-keyboard/sounds/040.wav", // Key 'A' sound
  87: "http://carolinegabriel.com/demo/js-keyboard/sounds/041.wav", // Key 'W' sound
  83: "http://carolinegabriel.com/demo/js-keyboard/sounds/042.wav", // And so on for all mapped keys
  69: "http://carolinegabriel.com/demo/js-keyboard/sounds/043.wav",
  68: "http://carolinegabriel.com/demo/js-keyboard/sounds/044.wav",
  70: "http://carolinegabriel.com/demo/js-keyboard/sounds/045.wav",
  84: "http://carolinegabriel.com/demo/js-keyboard/sounds/046.wav",
  71: "http://carolinegabriel.com/demo/js-keyboard/sounds/047.wav",
  89: "http://carolinegabriel.com/demo/js-keyboard/sounds/048.wav",
  72: "http://carolinegabriel.com/demo/js-keyboard/sounds/049.wav",
  85: "http://carolinegabriel.com/demo/js-keyboard/sounds/050.wav",
  74: "http://carolinegabriel.com/demo/js-keyboard/sounds/051.wav",
  75: "http://carolinegabriel.com/demo/js-keyboard/sounds/052.wav",
  79: "http://carolinegabriel.com/demo/js-keyboard/sounds/053.wav",
  76: "http://carolinegabriel.com/demo/js-keyboard/sounds/054.wav",
  80: "http://carolinegabriel.com/demo/js-keyboard/sounds/055.wav",
  186: "http://carolinegabriel.com/demo/js-keyboard/sounds/056.wav" // ';' key sound
};

let typedKeys = ''; // String to keep track of typed keys for secret sequence

// Function to fade in the image with smooth opacity transition
const fadeInImage = (image) => {
  let opacity = 0;

  const intervalId = setInterval(() => {
    opacity += 0.05; // Increase opacity in increments of 0.05

    if (opacity >= 1) { // Once fully opaque, stop the transition
      opacity = 1;
      clearInterval(intervalId);

      addTextAboveImage(); // Add text once the image fades in
    }

    image.style.opacity = opacity; // Apply the opacity value to the image
  }, 100); // Repeat every 100ms for smooth fade
};

// Function to add text above the image when it fades in
const addTextAboveImage = () => {
  // Select the text element with the class 'awokenText'
  const awokenTextElement = document.querySelector('.awokenText');
  // Make both text elements visible
  if (awokenTextElement) {
    awokenTextElement.style.display = 'block'; // Set display to block to show it
  }
};

// Function to check for a secret key sequence
const checkSequence = () => {
  if (typedKeys.includes('weseeyou')) { // If the sequence 'weseeyou' is typed
    const piano = document.querySelector('.piano');
    piano.style.transition = 'opacity 0.0s'; // Set transition duration to 1.5 seconds
    piano.style.opacity = '0'; // Gradually fade the piano out

    const image = document.createElement('img'); // Create an image element
    image.src = '/static/piano/images/texture.jpeg'; // Set the image source
    image.alt = 'The Great Old One'; // Alt text for the image
    image.style.width = '100%'; // Full width
    image.style.height = '60%'; // 60% of viewport height
    image.style.objectFit = 'cover'; // Cover the entire space
    image.style.opacity = '0'; // Start with invisible image
    image.style.borderRadius = '15px'; // Add rounded corners with 15px radius

    const greySquare = document.querySelector('.greySquare'); // Find the element to append the image to
    greySquare.appendChild(image); // Add the image to the element

    const creepyAudio = new Audio('https://orangefreesounds.com/wp-content/uploads/2020/09/Creepy-piano-sound-effect.mp3?_=1'); // Creepy sound
    creepyAudio.play(); // Play the sound

    fadeInImage(image); // Fade the image in

    document.removeEventListener('keydown', keydownListener); // Stop listening to further keydown events
  }
};

// Listener for key presses to handle sounds and the secret sequence
const keydownListener = (event) => {
  const keyCode = event.keyCode; // Get the key code of the pressed key
  const soundUrl = sound[keyCode]; // Get the sound associated with the key

  if (soundUrl) { // If there is a sound for the key
    const audio = new Audio(soundUrl); // Create an audio object
    audio.play(); // Play the sound
  }

  typedKeys += String.fromCharCode(event.keyCode).toLowerCase(); // Add the pressed key to the typedKeys string
  checkSequence(); // Check if the secret sequence has been typed
};

// Attach the keydown listener to the document
document.addEventListener('keydown', keydownListener);