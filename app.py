import random
import string
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Corporate jargon words for different categories
CORPORATE_JARGON = {
    'business_words': [
        'Business', 'Brand', 'Breakthrough', 'Benchmark', 'Bandwidth', 'Blockchain',
        'Bootstrap', 'Brainstorm', 'Blueprint', 'Buyout', 'Ballpark', 'Bottom-line'
    ],
    'optimization_words': [
        'Optimization', 'Opportunity', 'Operations', 'Objectives', 'Outcomes', 'Oversight',
        'Outsourcing', 'Orchestration', 'Organic', 'Onboarding', 'Offerings', 'Offline'
    ],
    'general_words': [
        'Synergy', 'Leverage', 'Paradigm', 'Innovation', 'Strategy', 'Solution',
        'Framework', 'Platform', 'Ecosystem', 'Methodology', 'Architecture', 'Scalability',
        'Monetization', 'Disruption', 'Transformation', 'Optimization', 'Engagement',
        'Alignment', 'Integration', 'Implementation', 'Deliverables', 'Stakeholders'
    ]
}

# Creed-style surreal definitions
CREED_DEFINITIONS = [
    'Bears. Beets. Battlestar Galactica.',
    'The Taliban is the worst. Great heroin though.',
    'I want to be wined, dined, and sixty-nined.',
    'Nobody steals from Creed Bratton and gets away with it.',
    'If I can\'t scuba, then what\'s this all been about?',
    'Cool beans, man. I live by the quarry. We should hang out by the quarry and throw things down there.',
    'Two eyes, two ears, a chin, a mouth, ten fingers, two nipples.',
    'I already won the lottery. I was born in the US of A, baby.',
    'I\'ve been involved in a number of cults both as a leader and a follower.',
    'The only difference between me and a homeless man is this job.',
    'Later skater.',
    'If that\'s flashing then lock me up.',
    'Jinx, buy me some Coke.',
    'www.creedthoughts.gov.www\\creedthoughts',
    'Strike, scream, and run.',
    'That wasn\'t a tapeworm.',
    'Northern lights cannabis indica.',
    'Bob Vance, Vance Refrigeration.'
]

def generate_random_acronym(length=None):
    """Generate a random acronym"""
    if length is None:
        length = random.choice([5, 6, 7, 8])  # Variable length like BOBODDY (7 letters)
    
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def get_corporate_definition(letter):
    """Generate a corporate jargon definition for a letter"""
    # Try to find words that start with the letter
    all_words = []
    for category in CORPORATE_JARGON.values():
        all_words.extend(category)
    
    # Filter words that start with the letter
    matching_words = [word for word in all_words if word.upper().startswith(letter.upper())]
    
    if matching_words:
        return random.choice(matching_words)
    else:
        # Fallback to any corporate word
        return random.choice(CORPORATE_JARGON['general_words'])

def get_creed_definition(letter):
    """Generate a Creed-style surreal definition"""
    return random.choice(CREED_DEFINITIONS)

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/generate_acronym')
def generate_acronym():
    """Generate a new random acronym"""
    acronym = generate_random_acronym()
    return jsonify({'acronym': acronym})

@app.route('/get_definition', methods=['POST'])
def get_definition():
    """Get definition for a letter based on mode"""
    data = request.json
    letter = data.get('letter', '').upper()
    mode = data.get('mode', 'manual')
    
    if mode == 'corporate':
        definition = get_corporate_definition(letter)
    elif mode == 'creed':
        definition = get_creed_definition(letter)
    else:
        definition = ''  # Manual mode - user types their own
    
    return jsonify({'definition': definition})

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)