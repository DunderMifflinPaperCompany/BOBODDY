// BOBODDY Brainstorm Engine JavaScript

class BOBODDYApp {
    constructor() {
        this.currentAcronym = 'BOBODDY';
        this.currentMode = 'manual';
        this.init();
    }

    init() {
        this.bindEvents();
        this.createDefinitionGrid();
        this.setupInitialState();
    }

    bindEvents() {
        // Generate new acronym button
        document.getElementById('generate-btn').addEventListener('click', () => {
            this.generateNewAcronym();
        });

        // Mode selector
        document.getElementById('mode-select').addEventListener('change', (e) => {
            this.currentMode = e.target.value;
            this.onModeChange();
        });

        // Fill all definitions button
        document.getElementById('fill-definitions-btn').addEventListener('click', () => {
            this.fillAllDefinitions();
        });

        // Clear all definitions button
        document.getElementById('clear-definitions-btn').addEventListener('click', () => {
            this.clearAllDefinitions();
        });
    }

    async generateNewAcronym() {
        try {
            const response = await fetch('/generate_acronym');
            const data = await response.json();
            this.currentAcronym = data.acronym;
            
            // Update display with animation
            const acronymElement = document.getElementById('acronym-letters');
            acronymElement.style.opacity = '0';
            
            setTimeout(() => {
                acronymElement.textContent = this.currentAcronym;
                acronymElement.style.opacity = '1';
                this.createDefinitionGrid();
            }, 300);
            
        } catch (error) {
            console.error('Error generating acronym:', error);
        }
    }

    createDefinitionGrid() {
        const grid = document.getElementById('definitions-grid');
        grid.innerHTML = '';
        
        // Create grid based on acronym length
        const letters = this.currentAcronym.split('');
        letters.forEach((letter, index) => {
            const definitionItem = document.createElement('div');
            definitionItem.className = 'definition-item';
            
            const letterElement = document.createElement('div');
            letterElement.className = 'definition-letter';
            letterElement.textContent = letter;
            
            const inputElement = document.createElement('input');
            inputElement.type = 'text';
            inputElement.className = 'definition-input';
            inputElement.placeholder = `What does ${letter} stand for?`;
            inputElement.id = `definition-${index}`;
            
            // Add event listener for input changes
            inputElement.addEventListener('input', () => {
                this.onDefinitionChange(inputElement);
            });
            
            definitionItem.appendChild(letterElement);
            definitionItem.appendChild(inputElement);
            grid.appendChild(definitionItem);
        });
    }

    onDefinitionChange(inputElement) {
        // Add visual feedback when user types
        if (inputElement.value.trim()) {
            inputElement.classList.add('filled');
        } else {
            inputElement.classList.remove('filled');
        }
    }

    onModeChange() {
        const inputs = document.querySelectorAll('.definition-input');
        inputs.forEach(input => {
            // Remove all mode classes
            input.classList.remove('creed-mode', 'corporate-mode');
            
            // Add current mode class
            if (this.currentMode === 'creed') {
                input.classList.add('creed-mode');
                this.showCreedElements();
            } else if (this.currentMode === 'corporate') {
                input.classList.add('corporate-mode');
                this.hideCreedElements();
            } else {
                this.hideCreedElements();
            }
        });
    }

    showCreedElements() {
        document.getElementById('creed-gif').style.display = 'block';
        document.getElementById('creed-quote').style.display = 'block';
    }

    hideCreedElements() {
        document.getElementById('creed-gif').style.display = 'none';
        document.getElementById('creed-quote').style.display = 'none';
    }

    async fillAllDefinitions() {
        if (this.currentMode === 'manual') {
            this.showMessage('Please select Corporate Jargon or Creed Mode to auto-fill definitions!');
            return;
        }

        const inputs = document.querySelectorAll('.definition-input');
        const letters = this.currentAcronym.split('');
        
        // Add loading animation
        inputs.forEach(input => {
            input.disabled = true;
            input.placeholder = 'Loading...';
        });

        try {
            for (let i = 0; i < letters.length; i++) {
                const letter = letters[i];
                const input = inputs[i];
                
                const response = await fetch('/get_definition', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        letter: letter,
                        mode: this.currentMode
                    })
                });
                
                const data = await response.json();
                
                // Animate the text appearing
                setTimeout(() => {
                    input.value = data.definition;
                    input.disabled = false;
                    input.placeholder = `What does ${letter} stand for?`;
                    this.onDefinitionChange(input);
                }, i * 200); // Stagger the animations
            }
        } catch (error) {
            console.error('Error filling definitions:', error);
            inputs.forEach(input => {
                input.disabled = false;
                input.placeholder = 'Error loading definition';
            });
        }
    }

    clearAllDefinitions() {
        const inputs = document.querySelectorAll('.definition-input');
        inputs.forEach((input, index) => {
            setTimeout(() => {
                input.value = '';
                input.classList.remove('filled', 'creed-mode', 'corporate-mode');
                
                // Re-add mode class if needed
                if (this.currentMode === 'creed') {
                    input.classList.add('creed-mode');
                } else if (this.currentMode === 'corporate') {
                    input.classList.add('corporate-mode');
                }
            }, index * 100);
        });
    }

    showMessage(message) {
        // Create a temporary message element
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        messageElement.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: #007acc;
            color: white;
            padding: 20px;
            border-radius: 15px;
            z-index: 1000;
            font-weight: bold;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        `;
        
        document.body.appendChild(messageElement);
        
        setTimeout(() => {
            document.body.removeChild(messageElement);
        }, 3000);
    }

    setupInitialState() {
        // Set up the initial BOBODDY display
        this.createDefinitionGrid();
        
        // Add some fun initial definitions for BOBODDY
        const initialDefinitions = [
            'Business',
            'Optimization', 
            'By',
            'Organizational',
            'Development',
            'Dynamics',
            'Yes!'
        ];
        
        setTimeout(() => {
            const inputs = document.querySelectorAll('.definition-input');
            inputs.forEach((input, index) => {
                if (initialDefinitions[index]) {
                    input.value = initialDefinitions[index];
                    this.onDefinitionChange(input);
                }
            });
        }, 500);
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new BOBODDYApp();
});

// Add some fun easter eggs
document.addEventListener('keydown', (e) => {
    // Konami code easter egg
    if (e.code === 'KeyC' && e.ctrlKey && e.shiftKey) {
        document.getElementById('mode-select').value = 'creed';
        document.getElementById('mode-select').dispatchEvent(new Event('change'));
        
        // Show a fun message
        const app = new BOBODDYApp();
        app.showMessage('🎉 Creed Mode Activated! Welcome to the chaos! 🎉');
    }
});