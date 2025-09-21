"""
Roadmap.sh reference data integration
This module provides reference data inspired by roadmap.sh for different career paths
"""

ROADMAP_REFERENCES = {
    'Machine Learning': {
        'source': 'https://roadmap.sh/ai-data-scientist',
        'description': 'AI & Data Scientist Roadmap',
        'key_areas': [
            'Mathematics & Statistics',
            'Programming (Python/R)',
            'Data Analysis & Visualization',
            'Machine Learning Algorithms',
            'Deep Learning',
            'MLOps & Deployment'
        ]
    },
    'Data Science': {
        'source': 'https://roadmap.sh/data-scientist',
        'description': 'Data Scientist Roadmap',
        'key_areas': [
            'Statistics & Mathematics',
            'Programming Languages',
            'Data Wrangling',
            'Data Visualization',
            'Machine Learning',
            'Big Data Technologies'
        ]
    },
    'CyberSecurity': {
        'source': 'https://roadmap.sh/cyber-security',
        'description': 'Cyber Security Roadmap',
        'key_areas': [
            'Network Security',
            'Operating System Security',
            'Cryptography',
            'Penetration Testing',
            'Incident Response',
            'Security Architecture'
        ]
    },
    'Web Development': {
        'source': 'https://roadmap.sh/frontend',
        'description': 'Frontend Developer Roadmap',
        'key_areas': [
            'HTML & CSS',
            'JavaScript',
            'Frontend Frameworks',
            'Build Tools',
            'Testing',
            'Performance Optimization'
        ]
    },
    'Cloud Computing': {
        'source': 'https://roadmap.sh/aws',
        'description': 'AWS Cloud Practitioner Roadmap',
        'key_areas': [
            'Cloud Fundamentals',
            'AWS Core Services',
            'Security & Compliance',
            'Networking',
            'Storage & Databases',
            'DevOps & Automation'
        ]
    },
    'Mobile Development': {
        'source': 'https://roadmap.sh/android',
        'description': 'Android Developer Roadmap',
        'key_areas': [
            'Mobile App Fundamentals',
            'Platform-Specific Development',
            'Cross-Platform Frameworks',
            'UI/UX Design',
            'App Testing & Debugging',
            'App Store Optimization'
        ]
    }
}

def get_roadmap_reference(specialization):
    """Get roadmap.sh reference for a specialization"""
    return ROADMAP_REFERENCES.get(specialization, ROADMAP_REFERENCES['Web Development'])

def get_roadmap_url(specialization):
    """Get the roadmap.sh URL for a specialization"""
    reference = get_roadmap_reference(specialization)
    return reference['source']

def get_key_areas(specialization):
    """Get key learning areas from roadmap.sh for a specialization"""
    reference = get_roadmap_reference(specialization)
    return reference['key_areas']
