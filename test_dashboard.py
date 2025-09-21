#!/usr/bin/env python3

from app import app
from enhanced_roadmap_generator import enhanced_roadmap_generator

def test_dashboard():
    with app.test_client() as client:
        with app.test_request_context():
            # Create test roadmap data
            test_preferences = {
                'specialization': 'web_development',
                'skill_focus': 'Beginner',
                'target_company': 'Tech Company',
                'position': 'Developer',
                'learning_duration': 8
            }
            
            roadmap = enhanced_roadmap_generator.generate_enhanced_roadmap(test_preferences)
            
            # Test dashboard template rendering
            from flask import render_template
            try:
                html = render_template('DefaultDashboard_fixed.html',
                                     user_name='Test User',
                                     profile_completion=100,
                                     latest_test_result=None,
                                     user_roadmap=roadmap)
                print("✅ Dashboard template renders successfully!")
                print(f"✅ HTML length: {len(html)} characters")
                print(f"✅ Contains roadmap: {'roadmap' in html.lower()}")
                print(f"✅ Contains phases: {'phase' in html.lower()}")
                print(f"✅ Contains topics: {'topic' in html.lower()}")
                return True
            except Exception as e:
                print(f"❌ Dashboard template error: {e}")
                return False

if __name__ == '__main__':
    test_dashboard()
