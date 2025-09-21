import json
import random
from datetime import datetime, timedelta
from roadmap_references import get_roadmap_reference, get_roadmap_url

class EnhancedRoadmapGenerator:
    """Enhanced AI-based personalized roadmap generator with advanced features"""
    
    def __init__(self):
        self.roadmap_templates = self._load_roadmap_templates()
        self.skill_levels = {
            'Beginner': {'weeks': 8, 'difficulty': 1, 'topics': 5},
            'Intermediate': {'weeks': 12, 'difficulty': 2, 'topics': 8},
            'Advanced': {'weeks': 16, 'difficulty': 3, 'topics': 12},
            'Expert': {'weeks': 20, 'difficulty': 4, 'topics': 15}
        }
        
    def _load_roadmap_templates(self):
        """Load enhanced roadmap templates for different specializations"""
        return {
            'Machine Learning': {
                'foundations': [
                    'Mathematics for ML (Linear Algebra, Statistics)',
                    'Python Programming Fundamentals',
                    'Data Analysis with Pandas & NumPy',
                    'Data Visualization with Matplotlib/Seaborn'
                ],
                'core_ml': [
                    'Supervised Learning Algorithms',
                    'Unsupervised Learning Techniques',
                    'Model Evaluation & Validation',
                    'Feature Engineering'
                ],
                'advanced': [
                    'Deep Learning with TensorFlow/PyTorch',
                    'Neural Networks & CNNs',
                    'Natural Language Processing',
                    'Computer Vision'
                ],
                'projects': [
                    'Predictive Analytics Project',
                    'Image Classification Model',
                    'NLP Sentiment Analysis',
                    'Recommendation System'
                ]
            },
            'Data Science': {
                'foundations': [
                    'Statistics & Probability',
                    'Python/R Programming',
                    'SQL Database Management',
                    'Data Wrangling & Cleaning'
                ],
                'core_ds': [
                    'Exploratory Data Analysis',
                    'Statistical Modeling',
                    'Data Visualization',
                    'Business Intelligence'
                ],
                'advanced': [
                    'Machine Learning for Data Science',
                    'Big Data Technologies (Spark, Hadoop)',
                    'Cloud Platforms (AWS, GCP)',
                    'Data Pipeline Development'
                ],
                'projects': [
                    'End-to-End Data Analysis',
                    'Predictive Modeling Project',
                    'Dashboard Creation',
                    'Data Pipeline Automation'
                ]
            },
            'CyberSecurity': {
                'foundations': [
                    'Network Security Fundamentals',
                    'Operating System Security',
                    'Cryptography Basics',
                    'Security Policies & Procedures'
                ],
                'core_sec': [
                    'Penetration Testing',
                    'Vulnerability Assessment',
                    'Incident Response',
                    'Security Monitoring'
                ],
                'advanced': [
                    'Advanced Persistent Threats',
                    'Digital Forensics',
                    'Security Architecture',
                    'Compliance & Risk Management'
                ],
                'projects': [
                    'Security Audit Project',
                    'Penetration Testing Lab',
                    'Incident Response Simulation',
                    'Security Tool Development'
                ]
            },
            'Web Development': {
                'foundations': [
                    'HTML5 & CSS3',
                    'JavaScript Fundamentals',
                    'Responsive Design',
                    'Version Control (Git)'
                ],
                'core_web': [
                    'Frontend Frameworks (React/Vue)',
                    'Backend Development (Node.js/Python)',
                    'Database Design & Management',
                    'API Development'
                ],
                'advanced': [
                    'Full-Stack Development',
                    'Cloud Deployment (AWS/Vercel)',
                    'Performance Optimization',
                    'Security Best Practices'
                ],
                'projects': [
                    'Portfolio Website',
                    'E-commerce Application',
                    'Social Media Platform',
                    'Real-time Chat Application'
                ]
            },
            'Cloud Computing': {
                'foundations': [
                    'Cloud Computing Concepts',
                    'Linux System Administration',
                    'Networking Fundamentals',
                    'Virtualization Technologies'
                ],
                'core_cloud': [
                    'AWS/Azure/GCP Services',
                    'Containerization (Docker)',
                    'Infrastructure as Code',
                    'Cloud Security'
                ],
                'advanced': [
                    'Kubernetes Orchestration',
                    'Serverless Architecture',
                    'DevOps & CI/CD',
                    'Cloud Cost Optimization'
                ],
                'projects': [
                    'Multi-tier Application Deployment',
                    'Containerized Microservices',
                    'Automated Infrastructure',
                    'Cloud Migration Project'
                ]
            },
            'Mobile Development': {
                'foundations': [
                    'Mobile App Development Concepts',
                    'Platform-Specific Languages (Swift/Kotlin)',
                    'Cross-Platform Frameworks (React Native/Flutter)',
                    'Mobile UI/UX Design Principles'
                ],
                'core_mobile': [
                    'Native iOS Development (Swift)',
                    'Native Android Development (Kotlin)',
                    'Cross-Platform Development',
                    'Mobile App Architecture'
                ],
                'advanced': [
                    'Advanced Mobile Features (Push Notifications, GPS)',
                    'Mobile App Testing & Debugging',
                    'App Store Optimization',
                    'Mobile Security & Performance'
                ],
                'projects': [
                    'Personal Portfolio App',
                    'E-commerce Mobile App',
                    'Social Media App',
                    'Real-time Chat Application'
                ]
            }
        }
    
    def generate_enhanced_roadmap(self, user_preferences):
        """Generate enhanced personalized roadmap based on user preferences"""
        # Map questionnaire values to roadmap template keys
        specialization_mapping = {
            'web_development': 'Web Development',
            'mobile_development': 'Mobile Development',
            'machine_learning': 'Machine Learning',
            'data_science': 'Data Science',
            'cloud_computing': 'Cloud Computing',
            'cybersecurity': 'CyberSecurity'
        }
        
        raw_specialization = user_preferences.get('specialization', 'web_development')
        specialization = specialization_mapping.get(raw_specialization, 'Web Development')
        
        # Map skill focus values
        skill_focus_mapping = {
            'soft_skills': 'Beginner',
            'hard_skills': 'Intermediate'
        }
        
        raw_skill_focus = user_preferences.get('skill_focus', 'soft_skills')
        skill_focus = skill_focus_mapping.get(raw_skill_focus, 'Beginner')
        
        target_company = user_preferences.get('target_company', 'Tech Company')
        position = user_preferences.get('position', 'Developer')
        
        # Get custom duration if provided
        custom_duration = user_preferences.get('learning_duration')
        if custom_duration:
            total_weeks = int(custom_duration)
        else:
            # Use default based on skill level
            skill_config = self.skill_levels.get(skill_focus, self.skill_levels['Beginner'])
            total_weeks = skill_config['weeks']
        
        # Get roadmap template for specialization
        template = self.roadmap_templates.get(specialization, self.roadmap_templates['Web Development'])
        skill_config = self.skill_levels.get(skill_focus, self.skill_levels['Beginner'])
        
        start_date = datetime.now()
        
        # Generate roadmap phases
        roadmap_phases = self._generate_enhanced_phases(template, skill_config, total_weeks, user_preferences)
        
        # Get roadmap.sh reference
        roadmap_reference = get_roadmap_reference(specialization)
        
        # Create enhanced personalized roadmap
        roadmap = {
            'user_info': {
                'specialization': specialization,
                'skill_level': skill_focus,
                'target_company': target_company,
                'target_position': position,
                'estimated_completion': (start_date + timedelta(weeks=total_weeks)).strftime('%B %Y'),
                'learning_goals': user_preferences.get('learning_goals', ''),
                'focus_area': user_preferences.get('focus_area', '')
            },
            'timeline': {
                'total_weeks': total_weeks,
                'start_date': start_date.strftime('%B %d, %Y'),
                'end_date': (start_date + timedelta(weeks=total_weeks)).strftime('%B %d, %Y')
            },
            'phases': roadmap_phases,
            'progress': {
                'current_phase': 0,
                'completed_topics': 0,
                'total_topics': sum(len(phase['topics']) for phase in roadmap_phases),
                'completion_percentage': 0
            },
            'reference': {
                'source': 'roadmap.sh',
                'url': get_roadmap_url(specialization),
                'description': roadmap_reference['description'],
                'key_areas': roadmap_reference['key_areas']
            },
            'enhanced_features': {
                'adaptive_learning': True,
                'progress_tracking': True,
                'milestone_rewards': True,
                'peer_learning': True,
                'mentor_support': True
            }
        }
        
        return roadmap
    
    def _generate_enhanced_phases(self, template, skill_config, total_weeks, user_preferences):
        """Generate enhanced learning phases based on template and skill level"""
        phases = []
        weeks_per_phase = total_weeks // 4  # 4 main phases
        
        # Determine the correct core skills key based on specialization
        core_key = 'core_ml' if 'core_ml' in template else 'core_web' if 'core_web' in template else 'core_mobile' if 'core_mobile' in template else 'core_cloud' if 'core_cloud' in template else 'core_ds' if 'core_ds' in template else 'core_sec' if 'core_sec' in template else 'core_web'
        
        phase_configs = [
            {'name': 'Foundation', 'topics': template['foundations'], 'weeks': weeks_per_phase},
            {'name': 'Core Skills', 'topics': template[core_key], 'weeks': weeks_per_phase},
            {'name': 'Advanced Topics', 'topics': template['advanced'], 'weeks': weeks_per_phase},
            {'name': 'Projects & Portfolio', 'topics': template['projects'], 'weeks': weeks_per_phase}
        ]
        
        current_week = 1
        for i, config in enumerate(phase_configs):
            # Adjust topics based on skill level
            topics = config['topics'][:skill_config['topics']//4 + 1]
            
            phase = {
                'id': i + 1,
                'name': config['name'],
                'weeks': config['weeks'],
                'start_week': current_week,
                'end_week': current_week + config['weeks'] - 1,
                'topics': [],
                'status': 'locked' if i > 0 else 'current',
                'difficulty': min(skill_config['difficulty'], i + 1),
                'learning_objectives': self._generate_learning_objectives(config['name'], user_preferences),
                'assessment_criteria': self._generate_assessment_criteria(config['name'])
            }
            
            # Generate topics with enhanced details
            for j, topic in enumerate(topics):
                topic_detail = {
                    'id': f"{i+1}.{j+1}",
                    'title': topic,
                    'estimated_hours': random.randint(8, 20),
                    'resources': self._generate_enhanced_resources(topic, user_preferences),
                    'milestones': self._generate_enhanced_milestones(topic, user_preferences),
                    'status': 'pending',
                    'priority': 'high' if j < 2 else 'medium',
                    'prerequisites': self._generate_prerequisites(topic, i),
                    'learning_path': self._generate_learning_path(topic),
                    'practical_exercises': self._generate_practical_exercises(topic)
                }
                phase['topics'].append(topic_detail)
            
            phases.append(phase)
            current_week += config['weeks']
        
        return phases
    
    def _generate_enhanced_resources(self, topic, user_preferences):
        """Generate enhanced learning resources for a topic"""
        resource_types = [
            {'type': 'Course', 'name': f'{topic} - Complete Course', 'platform': 'Coursera/edX', 'difficulty': 'Beginner'},
            {'type': 'Book', 'name': f'Learning {topic}', 'platform': 'O\'Reilly/Packt', 'difficulty': 'Intermediate'},
            {'type': 'Tutorial', 'name': f'{topic} Tutorial Series', 'platform': 'YouTube/FreeCodeCamp', 'difficulty': 'Beginner'},
            {'type': 'Practice', 'name': f'{topic} Hands-on Labs', 'platform': 'GitHub/Lab Environment', 'difficulty': 'Advanced'},
            {'type': 'Documentation', 'name': f'{topic} Official Docs', 'platform': 'Official Documentation', 'difficulty': 'All'},
            {'type': 'Community', 'name': f'{topic} Community Forum', 'platform': 'Stack Overflow/Reddit', 'difficulty': 'All'}
        ]
        
        return random.sample(resource_types, 4)
    
    def _generate_enhanced_milestones(self, topic, user_preferences):
        """Generate enhanced learning milestones for a topic"""
        milestones = [
            f'Complete {topic} fundamentals',
            f'Build a small project using {topic}',
            f'Create a portfolio piece showcasing {topic}',
            f'Get certified in {topic} (optional)',
            f'Contribute to open-source {topic} project',
            f'Teach {topic} to others'
        ]
        
        return random.sample(milestones, 3)
    
    def _generate_learning_objectives(self, phase_name, user_preferences):
        """Generate learning objectives for each phase"""
        objectives = {
            'Foundation': [
                'Master fundamental concepts and terminology',
                'Set up development environment',
                'Complete basic hands-on exercises',
                'Understand core principles'
            ],
            'Core Skills': [
                'Apply concepts in real-world scenarios',
                'Build intermediate-level projects',
                'Understand best practices and patterns',
                'Develop problem-solving skills'
            ],
            'Advanced Topics': [
                'Master advanced techniques and tools',
                'Build complex, production-ready projects',
                'Understand performance optimization',
                'Learn industry-specific knowledge'
            ],
            'Projects & Portfolio': [
                'Create impressive portfolio projects',
                'Demonstrate full-stack capabilities',
                'Showcase problem-solving skills',
                'Prepare for job interviews'
            ]
        }
        
        return objectives.get(phase_name, [])
    
    def _generate_assessment_criteria(self, phase_name):
        """Generate assessment criteria for each phase"""
        criteria = {
            'Foundation': ['Quiz completion', 'Basic project', 'Code review'],
            'Core Skills': ['Project submission', 'Code quality', 'Documentation'],
            'Advanced Topics': ['Complex project', 'Performance analysis', 'Code optimization'],
            'Projects & Portfolio': ['Portfolio review', 'Live demonstration', 'Peer feedback']
        }
        
        return criteria.get(phase_name, [])
    
    def _generate_prerequisites(self, topic, phase_index):
        """Generate prerequisites for a topic"""
        if phase_index == 0:
            return ['Basic computer skills', 'Internet access']
        elif phase_index == 1:
            return ['Foundation phase completion', 'Basic programming knowledge']
        else:
            return ['Previous phase completion', 'Intermediate programming skills']
    
    def _generate_learning_path(self, topic):
        """Generate a structured learning path for a topic"""
        return [
            'Theory and concepts',
            'Hands-on practice',
            'Project implementation',
            'Review and optimization'
        ]
    
    def _generate_practical_exercises(self, topic):
        """Generate practical exercises for a topic"""
        exercises = [
            f'Build a simple {topic} application',
            f'Debug and fix {topic} code issues',
            f'Optimize {topic} performance',
            f'Create {topic} documentation'
        ]
        
        return random.sample(exercises, 2)
    
    def update_progress(self, roadmap, completed_topics):
        """Update roadmap progress with enhanced tracking"""
        total_topics = roadmap['progress']['total_topics']
        completed_count = len(completed_topics)
        
        roadmap['progress']['completed_topics'] = completed_count
        roadmap['progress']['completion_percentage'] = int((completed_count / total_topics) * 100)
        
        # Update current phase based on progress
        for i, phase in enumerate(roadmap['phases']):
            phase_completed = all(topic['id'] in completed_topics for topic in phase['topics'])
            if phase_completed:
                phase['status'] = 'completed'
                roadmap['progress']['current_phase'] = i + 1
            elif i == roadmap['progress']['current_phase']:
                phase['status'] = 'current'
            else:
                phase['status'] = 'locked'
        
        return roadmap

# Global instance
enhanced_roadmap_generator = EnhancedRoadmapGenerator()
